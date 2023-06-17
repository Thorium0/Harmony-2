<template>
    <div id="wrapper">
        <v-layout>
            <v-navigation-drawer :touchless="true" permanent width="300" v-model="showSidebar" class="sidebar">
                <div class="myaccount-container">
                    <v-card class="rounded-0 myaccount-card">
                        <v-dialog v-model="accountDialog" width="auto">
                            <template v-slot:activator="{ props }">
                                <v-btn density="compact" icon="mdi-cog" color="grey" v-bind="props"></v-btn>
                            </template>

                            <v-card class="pa-2">
                                <template v-slot:title>
                                    <v-card-title>
                                        Account Settings
                                    </v-card-title>
                                </template>
                                <v-form @submit.prevent="updateProfile">

                                    <v-text-field v-model="update_username" :counter="10" label="Change username">
                                    </v-text-field>


                                    <v-file-input accept="image/*" v-model="update_profile_picture"
                                        label="Upload profile picture"></v-file-input>


                                    <v-card-actions>
                                        <v-btn color="green" type="submit">Update</v-btn>
                                        <v-btn color="secondary" @click="passwordDialog = true">Change Password</v-btn>
                                        <v-btn color="primary" @click="accountDialog = false">Close</v-btn>
                                        <v-btn color="red" @click="logout">Logout</v-btn>

                                    </v-card-actions>

                                </v-form>
                            </v-card>
                            <v-card width="400" v-if="userErrors.length" class="pa-2 mt-2" color="#555500">
                                <ul>
                                    <li v-for="error in userErrors" :key="error">&#x2022; {{ error }}</li>
                                </ul>
                            </v-card>
                        </v-dialog>

                        {{ username }}
                        <!--<span class="text-muted">#1234</span>-->
                    </v-card>
                    <v-dialog v-model="passwordDialog" width="auto">
                        <v-form @submit.prevent="updatePassword">

                            <v-card class="pa-2">
                                <template v-slot:title>
                                    <v-card-title>
                                        Change Password
                                    </v-card-title>
                                </template>

                                <v-text-field v-model="changePassword"
                                    :append-icon="showChangePassword1 ? 'mdi-eye' : 'mdi-eye-off'"
                                    :rules="[changePasswordRules.required, changePasswordRules.min]"
                                    :type="showChangePassword1 ? 'text' : 'password'" :counter="20"
                                    hint="At least 8 characters" @click:append="showChangePassword1 = !showChangePassword1"
                                    label="password" required>
                                </v-text-field>


                                <v-text-field v-model="changePassword2"
                                    :append-icon="showChangePassword2 ? 'mdi-eye' : 'mdi-eye-off'"
                                    :rules="[changePasswordRules.required, changePasswordRules.min, changePasswordRules.matchingPasswords]"
                                    :type="showChangePassword2 ? 'text' : 'password'" :counter="20" label="repeat password"
                                    hint="At least 8 characters" class="input-group--focused"
                                    @click:append="showChangePassword2 = !showChangePassword2" required>
                                </v-text-field>


                                <v-card-actions>
                                    <v-btn color="green" type="submit">Update</v-btn>
                                    <v-btn color="primary" @click="passwordDialog = false">Close</v-btn>

                                </v-card-actions>
                            </v-card>
                        </v-form>
                    </v-dialog>
                </div>

                <div class="d-flex ustify-space-around channel-flex-box">
                    <div class="sidebar-groups">








                        <v-btn v-if="group_channels.length" v-for="channel in group_channels" :text="channel.name[0]"
                            @click="setChannelId(channel.id, '$'+channel.name)" :to="'/chat/'+ channel.id" height="80px"
                            width="80px" max-width="80" class="ma-1 large-text rounded-circle">
                        </v-btn>




                        <v-dialog v-model="addGroupDialog" width="auto">
                            <template v-slot:activator="{ props }">

                                <v-btn text="+" height="80px" width="80px" max-width="80"
                                    class="ma-1 large-text rounded-circle" v-bind="props"></v-btn>

                            </template>

                            <v-card width="400" title="Create/Join group"
                                subtitle="Enter group name and password to create or join group" class="pa-2">
                                <v-form @submit.prevent="">
                                    <v-text-field v-model="request_group_name" :counter="10" label="Group name"
                                        required>
                                    </v-text-field>

                                    <v-text-field v-model="request_group_password"
                                        :append-icon="groupPassShow ? 'mdi-eye' : 'mdi-eye-off'"
                                        :rules="[groupRules.required, groupRules.min]"
                                        :type="groupPassShow ? 'text' : 'password'" :counter="20"
                                        hint="At least 8 characters" @click:append="groupPassShow = !groupPassShow"
                                        label="password" required>
                                    </v-text-field>




                                    <v-card-actions>
                                        <v-btn color="primary" type="submit" @click="commitGroup('join')">Join</v-btn>
                                        <v-btn color="secondary" type="submit" @click="commitGroup('create')">Create
                                        </v-btn>
                                        <v-btn color="red" @click="addGroupDialog = false">Close</v-btn>
                                    </v-card-actions>
                                </v-form>
                            </v-card>
                            <v-card width="400" v-if="groupErrors.length" class="pa-2 mt-2" color="#555500">
                                <ul>
                                    <li v-for="error in groupErrors" :key="error">&#x2022; {{ error }}</li>
                                </ul>
                            </v-card>
                        </v-dialog>









                    </div>

                    <div class="sidebar-friends pa-4">



                        <v-card width="160px" v-if="friend_requests.length" v-for="friend_request in friend_requests"
                            v-bind:key="friend_request.id" class="mb-2 pr-2" :style="'border: 1px solid yellow;'">
                            <v-row align="center" class="mt-1 mb-1">
                                <v-col class="shrink pr-0">
                                    <v-img v-bind:src="imageBaseUrl + friend_request.image" height="50px" width="50px"
                                        class="ml-3 rounded-circle"></v-img>
                                </v-col>
                                <v-col>
                                    <v-card-text class="pa-0 friend-request-text">Friend request:</v-card-text>
                                    <v-card-text class="pa-0">{{ friend_request.username }}</v-card-text>
                                    <div class="d-flex ustify-space-around">
                                        <v-btn class="mr-1" density="compact" icon="mdi-check" color="green"
                                            @click="acceptFriendRequest(friend_request.id)"></v-btn>
                                        <v-btn density="compact" icon="mdi-close" color="red"
                                            @click="rejectFriendRequest(friend_request.id)"></v-btn>
                                    </div>
                                </v-col>
                            </v-row>
                        </v-card>


                        <v-btn height="80px" width="160px" class="mb-2" v-if="friend_channels.length"
                            v-for="channel in friend_channels" :to="'/chat/'+ channel.id"
                            @click="setChannelId(channel.id, channel.friend.username)">
                            <v-card height="80px" width="160px">
                                <v-row align="center" class="mt-1 mb-1">
                                    <v-col class="shrink">
                                        <v-img height="50px" width="50px"
                                            v-bind:src="imageBaseUrl + channel.friend.image"
                                            class="ml-3 rounded-circle"></v-img>
                                    </v-col>
                                    <v-col>
                                        <v-card-text class="pa-0 ma-0 font-weight-regular">{{ channel.friend.username }}
                                        </v-card-text>
                                    </v-col>
                                </v-row>
                            </v-card>
                        </v-btn>

                        <v-dialog v-model="addDialog" width="auto">
                            <template v-slot:activator="{ props }">

                                <v-btn icon="mdi-plus" height="40px" width="150px" class="ma-1 rounded-pill"
                                    v-bind="props"></v-btn>

                            </template>

                            <v-card width="400" height="220" title="Send Friend Request"
                                subtitle="Enter friend's username to send a friend request" class="pa-2">
                                <v-form @submit.prevent="sendFriendRequest">
                                    <v-text-field v-model="request_username" :counter="10" label="Note: Case-sensitive"
                                        required>
                                    </v-text-field>




                                    <v-card-actions>
                                        <v-btn color="primary" type="submit">Send</v-btn>
                                        <v-btn color="secondary" @click="addDialog = false">Close</v-btn>
                                    </v-card-actions>
                                </v-form>
                            </v-card>
                            <v-card width="400" v-if="requestErrors.length" class="pa-2 mt-2" color="#555500">
                                <ul>
                                    <li v-for="error in requestErrors" :key="error">&#x2022; {{ error }}</li>
                                </ul>
                            </v-card>
                        </v-dialog>



                    </div>

                </div>

            </v-navigation-drawer>
        </v-layout>



        <div class="is-loading-bar has-text-centered" v-bind:class="{ 'is-loading': $store.state.isLoading }">
            <v-progress-circular indeterminate color="blue"></v-progress-circular>
        </div>

        <v-dialog v-model="callNoti" persistent width="auto">
            <v-card>
                <v-card-title>
                    <span class="headline">Incoming Call from {{ callName }}</span>
                </v-card-title>
                <v-card-text>
                    <v-btn color="green" @click="acceptCall">Accept</v-btn>
                    <v-btn color="red" @click="rejectCall">Reject</v-btn>
                </v-card-text>
            </v-card>
        </v-dialog>



        <section class="section">
            <router-view />
        </section>

    </div>
</template>

<script>
    import {
        CometChat
    } from '@cometchat-pro/chat';

    export default {

        data() {
            return {
                accountDialog: false,
                passwordDialog: false,
                addDialog: false,
                addGroupDialog: false,
                showSidebar: false,
                friend_requests: [],
                request_username: '',
                requestErrors: [],
                userErrors: [],
                groupErrors: [],
                username: localStorage.username,
                update_username: "",
                update_profile_picture: null,
                imageBaseUrl: process.env.VUE_APP_AXIOS_URL,
                friend_channels: [],
                group_channels: [],
                selectedChannelId: null,
                incomingCall: false,
                callNoti: false,
                callName: '',
                session_id: '',
                sidebar_icon: '<',
                request_group_name: '',
                request_group_password: '',
                changePassword: '',
                changePassword2: '',

                showChangePassword1: false,
                showChangePassword2: false,
                changePasswordRules: {
                    required: value => !!value || 'Required.',
                    min: v => v.length >= 8 || 'Min 8 characters',
                    matchingPasswords: v => v === this.changePassword || "Passwords do not match"

                },


                groupPassShow: false,
                groupRules: {
                    required: value => !!value || 'Required.',
                    min: v => v.length >= 8 || 'Min 8 characters',
                }
            }
        },
        beforeCreate() {

            //this.$store.commit('initializeStore')
/*
            const token = this.$store.state.token

            if (token) {
                this.axios.defaults.headers.common['Authorization'] = `Token ${token}`
            } else {
                this.axios.defaults.headers.common['Authorization'] = null
            }
*/



        },
        watch: {
            $route(to, from) {
                if (to.name != 'login' && to.name != 'register') {
                    this.init()
                }
                if (to.name != 'call') {
                    this.loginCometChat()
                    this.listenCometChat()
                }

            }
        },
        mounted() {
            this.init()



        },
        created() {
            this.initCometChat()
            if (localStorage.CometChatIsLoggedIn != "true" && this.$store.state.isAuthenticated) {
                this.loginCometChat()
            }
            this.listenCometChat()

        },
        beforeUpdate() {
            
            this.username = localStorage.username

            var showSidebar = this.$store.state.showSidebar
            const route = this.$router.currentRoute.value.name;
            if (showSidebar && !(route == 'login' || route == 'register')) {
                this.showSidebar = true
                document.getElementsByClassName("section")[0].style.marginLeft = "300px";
            } else {
                this.showSidebar = false
                document.getElementsByClassName("section")[0].style.marginLeft = "0";
            }

        },
        updated() {

        },
        computed: {

        },
        components: {

        },
        methods: {

            acceptCall() {
                this.callNoti = false
                this.$router.push("/call/" + this.session_id)
            },
            rejectCall() {

                var sessionID = this.session_id;
                var globalContext = this;
                var status = CometChat.CALL_STATUS.REJECTED;
                CometChat.rejectCall(sessionID, status).then(
                    call => {
                        console.log("Call rejected successfully", call);
                        globalContext.incomingCall = false;
                        this.callNoti = false
                    },
                    error => {
                        console.log("Call rejection failed with error:", error);
                    }
                );
            },
            initCometChat() {
                var appID = process.env.VUE_APP_COMETCHAT_APP_ID;

                CometChat.init(appID).then(
                    () => {
                        console.log("[CometChat] Initialization completed successfully");
                    },
                    error => {
                        console.log("[CometChat] Initialization failed with error:", error);
                    }
                )
            },

            loginCometChat() {

                if (!this.$store.state.isAuthenticated) {
                    return
                }

                let apiKey = process.env.VUE_APP_COMETCHAT_API_KEY;

                this.$store.commit('setIsLoading', true)
                var uid = localStorage.user_id;

                CometChat.login(uid, apiKey).then(
                    success => {
                        this.$store.commit('setIsLoading', false)
                        console.log("[CometChat] Login Successful:", {
                            username: uid
                        });
                        localStorage.CometChatIsLoggedIn = true
                    },
                    error => {
                        this.$store.commit('setIsLoading', false)
                        console.log("[CometChat] Login failed with exception:", {
                            error
                        });
                    }
                )
            },

            listenCometChat() {
                if (!this.$store.state.isAuthenticated) {
                    return
                }
                let globalContext = this;
                var listnerID = this.lowercaseify(this.username);
                CometChat.addCallListener(
                    listnerID,
                    new CometChat.CallListener({
                        onIncomingCallReceived(call) {
                            console.log("Incoming call:", call);
                            if (globalContext.username == call.sender.name) {
                                return
                            }
                            globalContext.incomingCall = true;
                            globalContext.callNoti = true;
                            globalContext.callName = call.sender.name
                            globalContext.session_id = call.sessionId;
                        },
                        onIncomingCallCancelled(call) {
                            console.log("Incoming call calcelled:", call);
                        }
                    })
                );
            },
            lowercaseify(string) {
                if (string != null) {
                    for (var i = 0; i < string.length; i++) {
                        if (string[i] == string[i].toUpperCase()) {
                            string = string.replace(string[i], "_" + string[i].toLowerCase());
                        }
                    }
                    return string
                }
            },

            init() {
                if (!this.$store.state.isAuthenticated) {
                    return
                }
                clearInterval(this.interval)
                this.updateFriendRequests()
                this.getFriendChannels()
                this.getGroupChannels()
                this.interval = setInterval(() => {
                    var route = this.$router.currentRoute.value.name;
                    if (route == 'login' || route == 'register') {
                        clearInterval(this.interval)
                        return
                    }
                    this.updateFriendRequests()
                    this.getFriendChannels()
                    this.getGroupChannels()



                }, 2000);


            },



            logout() {
                this.axios.defaults.headers.common["Authorization"] = ""

                localStorage.removeItem("token");
                localStorage.removeItem("username");
                localStorage.removeItem("user_id");

                this.$store.commit("removeToken");

                this.accountDialog = false;

                CometChat.logout().then(
                    success => {
                        localStorage.CometChatIsLoggedIn = false
                        console.log("Logout completed successfully");
                        console.log(success);
                        this.$router.push("/login");
                    },
                    error => {
                        //Logout failed with exception
                        console.log("Logout failed with exception:", {
                            error
                        });
                    });


            },
            sendFriendRequest() {

                if (!this.$store.state.isAuthenticated) {
                    return
                }
                const formData = {
                    username: this.request_username
                }
                this.axios.post("/api/v1/request/create/", formData).then(response => {
                    this.requestErrors = []
                    this.addDialog = false
                    this.request_username = ''
                }).catch(error => {
                    this.requestErrors = []
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.requestErrors.push(
                                `${property}: ${error.response.data[property]}`);
                        }

                        console.log(JSON.stringify(error.response.data));
                    } else {
                        this.requestErrors.push("Something went wrong. Please try again.");

                        console.log(JSON.stringify(error));
                    }
                })
            },
            commitGroup(action) {
                if (!this.$store.state.isAuthenticated) {
                    return
                }

                const formData = {
                    name: this.request_group_name,
                    password: this.request_group_password,
                    action: action
                }

                this.axios.post("/api/v1/channel/group/", formData).then(response => {
                    this.groupErrors = []
                    this.addGroupDialog = false
                    this.request_group_name = ''
                    this.request_group_password = ''
                }).catch(error => {
                    this.groupErrors = []
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.groupErrors.push(
                                `${property}: ${error.response.data[property]}`);
                        }

                        console.log(JSON.stringify(error.response.data));
                    } else {
                        this.groupErrors.push("Something went wrong. Please try again.");

                        console.log(JSON.stringify(error));
                    }
                })
            },
            async updateFriendRequests() {
                this.axios.get("/api/v1/request/latest/")
                    .then(response => {
                        this.friend_requests = response.data
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            },
            isMobile() {
                return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator
                    .userAgent)
            },
            async acceptFriendRequest(requestId) {

                if (!this.$store.state.isAuthenticated) {
                    return
                }

                const formData = {
                    id: requestId,
                    status: "A"
                }

                this.axios.post("/api/v1/request/set/", formData).then(response => {
                    this.updateFriendRequests()
                    this.getFriendChannels()
                })
            },
            async rejectFriendRequest(requestId) {


                if (!this.$store.state.isAuthenticated) {
                    return
                }

                const formData = {
                    id: requestId,
                    status: "R"
                }

                this.axios.post("/api/v1/request/set/", formData).then(response => {
                    this.updateFriendRequests()
                })
            },
            updateCometChatUser(username) {
                let authKey = process.env.VUE_APP_COMETCHAT_AUTH_KEY;
                var user = new CometChat.User(localStorage.user_id);
                user.setName(username);
                CometChat.updateUser(user, authKey).then(
                    user => {
                        console.log("[CometChat] User updated", user);
                    }, error => {
                        console.log("[CometChat] Error updating user", error);
                    }
                )
            },
            async updateProfile() {

                if (!this.$store.state.isAuthenticated) {
                    return
                }

                var formData = new FormData()

                if (this.update_username.length > 1) {
                    formData.append("username", this.update_username)
                }
                if (this.update_profile_picture != null) {
                    formData.append("image", this.update_profile_picture[0])
                }



                const headers = {
                    'Content-Type': 'multipart/form-data'
                }

                this.axios.put("/api/v1/profile/", formData, {
                    headers: headers
                }).then(response => {
                    this.userErrors = []
                    this.update_profile_picture = null
                    this.accountDialog = false
                    //this.updateCometChatUser(this.update_username);
                    localStorage.username = this.update_username
                    this.update_username = ""

                }).catch(error => {
                    this.userErrors = []
                    this.update_profile_picture = null
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.userErrors.push(
                                `${property}: ${error.response.data[property]}`);
                        }

                        console.log(JSON.stringify(error.response.data));
                    } else {
                        this.userErrors.push(
                            "error: Make sure you have filled out the fields correctly."
                        );

                        console.log(JSON.stringify(error));
                    }
                })
            },
            async getFriendChannels() {
                this.axios.get("/api/v1/channel/").then(response => {
                    this.friend_channels = response.data
                })
            },
            async getGroupChannels() {
                this.axios.get("/api/v1/channel/group/").then(response => {
                    this.group_channels = response.data
                })
            },
            setChannelId(channel_id, channel_name = null) {
                this.$store.commit("setSelectedChannelId", channel_id)
                localStorage.selectedChannelId = channel_id
                if (channel_name != null) {
                    this.$store.commit("setSelectedChannelName", channel_name)
                    localStorage.selectedChannelName = channel_name
                }
            },
            updatePassword() {
                if (!this.$store.state.isAuthenticated || this.changePassword != this.changePassword2) {
                    return
                }

                const formData = {
                    password: this.changePassword,
                }

                const headers = {
                    'Content-Type': 'multipart/form-data'
                }

                this.axios.put("/api/v1/profile/", formData, {
                    headers: headers
                }).then(response => {
                    this.passwordDialog = false;
                    this.changePassword = "";
                    this.showChangePassword1 = false;
                    this.showChangePassword2 = false;
                    this.changePassword2 = "";
                }).catch(error => {
                    console.log(JSON.stringify(error))
                })

            }

        }
    }
</script>



<style lang="scss">
    html,
    body {
        margin: 0;
        height: 100%;
        overflow: hidden !important;
        background-color: #212121;
    }

    .large-text {
        font-size: 60px !important;
    }

    .v-navigation-drawer__content {
        overflow: hidden !important;
    }

    .friend-request-text {
        position: absolute;
        top: 0;
        right: 5px
    }

    .sidebar {
        height: 100%;
        width: auto;
        min-width: auto;
        overflow: hidden;
    }


    .sidebar-groups {
        background-color: #424242;
        width: fit-content;
        min-width: 90px;
        max-width: 90px;
        height: 100%;
        overflow-y: auto;
        overflow-x: hidden;
    }


    .sidebar-friends {
        background-color: #616161;
        height: 100%;
        width: auto;
        min-width: auto;
        overflow-y: auto;
        overflow-x: hidden;
    }


    .section {
        margin-left: 300px;
        height: 100vh !important;
    }

    .myaccount-container {
        width: 100%;
    }

    .myaccount-card {}

    .channel-flex-box {
        height: 100%;
    }

    .is-loading-bar {
        height: 0;
        overflow: hidden;

        -webkit-transition: all 0.3s;
        transition: all 0.3s;
        z-index: 10000;
        position: fixed;
        left: 50%;
        top: 8px;

        &.is-loading {
            height: 80px;
        }
    }

    .lds-loading-bar {
        position: fixed;
        animation: lds-loading-bar-2 0.1s normal forwards ease-in-out;
        width: 100vw;
        height: 4px;
        background-color: #2ac811;
        z-index: 1000;

        &.is-loading {
            animation: lds-loading-bar 0.2s normal forwards ease-in-out;
        }
    }
</style>