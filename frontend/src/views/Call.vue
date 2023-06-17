<template>
    <v-card v-if="waiting">
        <v-card-title>Calling {{ receiver_id }}...</v-card-title>
    </v-card>

    <div id="callScreen"></div>

</template>

<script>
    import {
        CometChat
    } from "@cometchat-pro/chat";
    export default {
        name: "CallView",
        data() {
            return {
                username: localStorage.username,
                uid: "",
                receiver_id: localStorage.selectedChannelName,
                error: false,
                waiting: false,
            };
        },
        created() {
            this.getLoggedInUser();
            if (this.$route.params.session_id != 'null') {
                if (localStorage.ongoingCall == 'true') {
                    this.endCall();
                } else {
                    localStorage.session_id = this.$route.params.session_id;
                    this.joinCall();

                }
            } else {
                if (localStorage.ongoingCall) {
                    this.endCall();
                }
                setTimeout(() => {
                    if (this.$route.path.split("/")[1] == "call") {
                        this.startVideoChat();
                        
                    }
                }, 1000);

            }


        },
        updated() {},
        methods: {
            lowercaseify(string) {
                for (var i = 0; i < string.length; i++) {
                    if (string[i] == string[i].toUpperCase()) {
                        string = string.replace(string[i], "_" + string[i].toLowerCase());
                    }
                }
                return string
            },

            endCall() {

                CometChat.endCall(localStorage.session_id).then(
                    call => {
                        console.log("[CometChat] Call ended successfully:", call);
                        localStorage.session_id = null
                        localStorage.ongoingCall = false;
                    },
                    error => {
                        console.log("[CometChat] Call ending failed with exception:", error);
                    }
                )

            },
            joinCall() {
                let globalContext = this;
                var sessionID = localStorage.session_id;
                CometChat.acceptCall(sessionID).then(
                    call => {
                        console.log("Call accepted successfully:", call);
                        console.log("call accepted now....");
                        // start the call using the startCall() method
                        localStorage.ongoingCall = true;
                        CometChat.startCall(
                            call.sessionId,
                            document.getElementById("callScreen"),
                            new CometChat.OngoingCallListener({
                                onUserJoined: user => {
                                    /* Notification received here if another user joins the call. */
                                    console.log("User joined call:", user);
                                    /* this method can be use to display message or perform any actions if someone joining the call */
                                },
                                onUserLeft: user => {
                                    /* Notification received here if another user left the call. */
                                    console.log("User left call:", user);
                                    /* this method can be use to display message or perform any actions if someone leaving the call */
                                },
                                onCallEnded: call => {
                                    /* Notification received here if current ongoing call is ended. */
                                    console.log("Call ended:", call);
                                    localStorage.ongoingCall = false;
                                    localStorage.session_id = null;
                                    CometChat.removeCallListener(call.sessionId);
                                    /* hiding/closing the call screen can be done here. */
                                    window.location.replace(window.origin+"/chat/"+localStorage.selectedChannelId);
                                }
                            })
                        );
                    },
                    error => {
                        console.log("Call acceptance failed with error", error);
                        // handle exception
                    }
                );
            },
            getLoggedInUser() {
                CometChat.getLoggedinUser().then(
                    user => {
                        this.username = user.name;
                        this.uid = user.uid;
                    },
                    error => {
                        this.$router.push({
                            name: "homepage"
                        });
                    }
                );
            },
            startVideoChat() {
                if (!this.receiver_id) this.error = true;
                this.$store.commit("setIsLoading", true);
                var globalContext = this;
                if (this.receiver_id[0] == "$") {
                    this.waiting = false;
                    console.log(this.waiting)
                    var sessionID = this.lowercaseify(this.receiver_id.substring(1));

                    let audioOnly = false;
                    let defaultLayout = true;
                    localStorage.session_id = sessionID;
                    localStorage.ongoingCall = true
                    history.pushState({}, null, sessionID);

                    let callSettings = new CometChat.CallSettingsBuilder()
                        .enableDefaultLayout(defaultLayout)
                        .setSessionID(sessionID)
                        .setIsAudioOnlyCall(audioOnly)
                        .build();

                    this.$store.commit("setIsLoading", false);


                    CometChat.startCall(
                        callSettings,
                        document.getElementById("callScreen"),
                        new CometChat.OngoingCallListener({
                            onUserListUpdated: userList => {
                                console.log("user list:", userList);
                            },
                            onCallEnded: call => {
                                console.log("Call ended:", call);
                                localStorage.ongoingCall = false;
                                localStorage.session_id = null;
                                console.log("eyo")
                                window.location.replace(window.origin+"/chat/"+localStorage.selectedChannelId);
                            },
                            onError: error => {
                                console.log("Error :", error);
                            },
                            onMediaDeviceListUpdated: deviceList => {
                                console.log("Device List:", deviceList);
                            },
                            onUserMuted: (userMuted, userMutedBy) => {
                                // This event will work in JS SDK v3.0.2-beta1 & later.
                                console.log("Listener => onUserMuted:", userMuted, userMutedBy);
                            },
                            onScreenShareStarted: () => {
                                // This event will work in JS SDK v3.0.3 & later.
                                console.log("Screen sharing started.");
                            },
                            onScreenShareStopped: () => {
                                // This event will work in JS SDK v3.0.3 & later.
                                console.log("Screen sharing stopped.");
                            },
                            onCallSwitchedToVideo: (sessionId, callSwitchInitiatedBy,
                                callSwitchAcceptedBy) => {
                                    // This event will work in JS SDK v3.0.8 & later.
                                    console.log("call switched to video:", {
                                        sessionId,
                                        callSwitchInitiatedBy,
                                        callSwitchAcceptedBy
                                    });
                                }
                        })
                    );


                } else {

                    var receiverID = this.lowercaseify(this.receiver_id);
                    var callType = CometChat.CALL_TYPE.VIDEO;
                    var receiverType = CometChat.RECEIVER_TYPE.USER;
                    var call = new CometChat.Call(receiverID, callType, receiverType);

                    CometChat.initiateCall(call).then(
                        outGoingCall => {
                            this.$store.commit("setIsLoading", false);
                            localStorage.session_id = outGoingCall.sessionId;
                            history.pushState({}, null, outGoingCall.sessionId);
                            console.log("Call initiated successfully:", outGoingCall);
                            // perform action on success. Like show your calling screen.
                        },
                        error => {
                            console.log("Call initialization failed with exception:", error);
                        }
                    );

                    this.listen();
                }

            },
            listen() {
                let globalContext = this;
                var listnerID = this.username;
                this.waiting = true;
                CometChat.addCallListener(
                    listnerID,
                    new CometChat.CallListener({
                        onOutgoingCallAccepted(call) {
                            console.log("Outgoing call accepted:", call);
                            localStorage.ongoingCall = true;
                            globalContext.waiting = false;
                            globalContext.$store.commit("setIsLoading", false);
                            CometChat.startCall(
                                call.sessionId,
                                document.getElementById("callScreen"),
                                new CometChat.OngoingCallListener({
                                    onUserJoined: user => {

                                        /* Notification received here if another user joins the call. */
                                        console.log("User joined call:", user);
                                        /* this method can be use to display message or perform any actions if someone joining the call */
                                    },
                                    onUserLeft: user => {
                                        /* Notification received here if another user left the call. */
                                        console.log("User left call:", user);
                                        /* this method can be use to display message or perform any actions if someone leaving the call */
                                    },
                                    onCallEnded: call => {
                                        localStorage.ongoingCall = false;
                                        localStorage.session_id = null;

                                        /* Notification received here if current ongoing call is ended. */
                                        console.log("Call ended:", call);
                                        /* hiding/closing the call screen can be done here. */
                                        CometChat.removeCallListener(call.sessionId);
                                        window.location.replace(window.origin+"/chat/"+localStorage.selectedChannelId);
                                    }

                                })
                            );
                            // Outgoing Call Accepted
                        },
                        onOutgoingCallRejected(call) {
                            console.log("Outgoing call rejected:", call);
                            localStorage.ongoingCall = false;
                            localStorage.session_id = null;
                            // Outgoing Call Rejected
                            window.location.replace(window.origin+"/chat/"+localStorage.selectedChannelId);

                        },
                    })

                );
            },
        }
    };
</script>

<style scoped>
    #callScreen {
        height: 100%;
    }

    @media only screen and (max-width: 600px) {
        #callScreen {
        height: 94%;
    }
}
</style>