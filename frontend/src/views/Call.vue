<template>
    <v-card v-if="waiting">
     <v-card-title>Waiting for response...</v-card-title>
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
                        this.listen();
                    }
                }, 1000);
                
            }


        },
        updated() {
        },
        methods: {
            lowercaseify(string) {
                for (var i = 0; i < string.length; i++) {
                    if (string[i] == string[i].toUpperCase()) {
                        string = string.replace(string[i], "_"+string[i].toLowerCase());
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
                                    globalContext.$router.go(-1);
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
                            CometChat.startCall(
                                call.sessionId,
                                document.getElementById("callScreen"),
                                new CometChat.OngoingCallListener({
                                    onUserJoined: user => {
                                        /* Notification received here if another user joins the call. */
                                        console.log("User joined call:", user);
                                        globalContext.waiting = false;
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
                                        globalContext.$router.go(-2);
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
                            globalContext.$router.go(-2);
                            
                        },
                    })

                );
            },
        }
    };
</script>

<style scoped>
    #callScreen {
        height: 80vh;
    }
</style>