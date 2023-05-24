<template>
    <div id="wrapper">
        <div v-if="showSidebar" class="sidebar">
            <div class="myaccount-container">
                <v-card>
                    <v-dialog v-model="accountDialog" width="auto">
                        <template v-slot:activator="{ props }">
                            <v-btn density="compact" icon="mdi-cog" color="grey" v-bind="props"></v-btn>
                        </template>

                        <v-card class="pa-2">
                            <template v-slot:title>
                                <v-card-text>
                                    Account Settings
                                </v-card-text>
                            </template>
                            <v-form @submit.prevent="updateProfile">

                                <v-text-field v-model="update_username" :counter="10" label="Change username">
                                </v-text-field>


                                <v-file-input accept="image/*" v-model="update_profile_picture"
                                    label="Upload profile picture"></v-file-input>


                                <v-card-actions>
                                    <v-btn color="green" type="submit">Update</v-btn>
                                    <v-btn color="primary" @click="accountDialog = false">Close</v-btn>
                                    <v-btn color="secondary" @click="logout">Logout</v-btn>
                                </v-card-actions>
                            </v-form>
                        </v-card>
                        <v-card width="400" v-if="errors.length" class="pa-2 mt-2" color="#555500">
                            <ul>
                                <li v-for="error in errors" :key="error">&#x2022; {{ error }}</li>
                            </ul>
                        </v-card>
                    </v-dialog>

                    {{ username }}
                    <!--<span class="text-muted">#1234</span>-->
                </v-card>
            </div>

            <div class="d-flex ustify-space-around channel-flex-box">
                <div class="sidebar-groups">








                    <v-btn height="80px" width="80px" max-width="80" class="ma-1 rounded-circle">
                        <img src="//placehold.it/80x80" class="rounded-circle">
                    </v-btn>
                    <v-btn height="80px" width="80px" max-width="80" class="ma-1 rounded-circle">
                        <img src="//placehold.it/80x80" class="rounded-circle">
                    </v-btn>
                    <v-btn height="80px" width="80px" max-width="80" class="ma-1 rounded-circle">
                        <img src="//placehold.it/80x80" class="rounded-circle">
                    </v-btn>
                    <v-btn height="80px" width="80px" max-width="80" class="ma-1 rounded-circle">
                        <img src="//placehold.it/80x80" class="rounded-circle">
                    </v-btn>



                    <v-dialog v-model="addDialog" width="auto">
                        <template v-slot:activator="{ props }">

                            <v-btn text="+" height="80px" width="80px" class="ma-1 large-text rounded-circle"
                                v-bind="props"></v-btn>
                            <v-btn text="<" height="80px" width="80px" class="ma-1 large-text rounded-circle"
                                v-if="isMobile()" @click="showSidebar = !showSidebar"></v-btn>
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
                        <v-card width="400" v-if="errors.length" class="pa-2 mt-2" color="#555500">
                            <ul>
                                <li v-for="error in errors" :key="error">&#x2022; {{ error }}</li>
                            </ul>
                        </v-card>
                    </v-dialog>









                </div>

                <div class="sidebar-friends pa-4">



                    <v-card width="145px" v-if="friend_requests.length" v-for="friend_request in friend_requests"
                        v-bind:key="friend_request.id" class="mb-2 pr-2" :style="'border: 1px solid yellow;'">
                        <v-row align="center" class="mt-1 mb-1">
                            <v-col class="shrink pr-0">
                                <v-img v-bind:src="imageBaseUrl + friend_request.image" height="50px" width="50px"
                                    class="ml-3 rounded-circle"></v-img>
                            </v-col>
                            <v-col>
                                <v-card-text class="pa-0">Request: {{ friend_request.username }}</v-card-text>
                                <div class="d-flex ustify-space-around">
                                    <v-btn class="mr-1" density="compact" icon="mdi-check" color="green"
                                        @click="acceptFriendRequest(friend_request.id)"></v-btn>
                                    <v-btn density="compact" icon="mdi-close" color="red"
                                        @click="rejectFriendRequest(friend_request.id)"></v-btn>
                                </div>
                            </v-col>
                        </v-row>
                    </v-card>


                    <v-btn height="80px" width="145px" class="mb-2" v-if="friend_channels.length"
                        v-for="channel in friend_channels" :to="'/chat/'+ channel.id" @click="setChannelId(channel.id)">
                        <v-card height="80px" width="145px">
                            <v-row align="center" class="mt-1 mb-1">
                                <v-col class="shrink">
                                    <v-img height="50px" width="50px" v-bind:src="imageBaseUrl + channel.friend.image"
                                        class="ml-3 rounded-circle"></v-img>
                                </v-col>
                                <v-col>
                                    <v-card-text class="pa-0 font-weight-regular">{{ channel.friend.username }}
                                    </v-card-text>
                                </v-col>
                            </v-row>
                        </v-card>
                    </v-btn>



                </div>

            </div>
        </div>




        <div class="lds-loading-bar" v-bind:class="{ 'is-loading': $store.state.isLoading }"></div>



        <section class="section">
            <router-view />
        </section>

    </div>
</template>

<script>

    export default {

        data() {
            return {
                accountDialog: false,
                addDialog: false,
                showSidebar: true,
                friend_requests: [],
                request_username: '',
                errors: [],
                username: localStorage.username,
                update_username: "",
                update_profile_picture: null,
                imageBaseUrl: "http://localhost:8000",
                friend_channels: [],
                selectedChannelId: null,
            }
        },
        beforeCreate() {
            this.$store.commit('initializeStore')

            const token = this.$store.state.token

            if (token) {
                this.axios.defaults.headers.common['Authorization'] = `Token ${token}`
            } else {
                this.axios.defaults.headers.common['Authorization'] = null
            }




        },
        mounted() {
            var route = this.$router.currentRoute.value.name;
            this.updateFriendRequests()
            this.interval = setInterval(() => {
                route = this.$router.currentRoute.value.name;
                if (route == 'login' || route == 'register') {
                    return
                }
                this.updateFriendRequests()
                this.getFriendChannels()

            }, 2000);



        },
        beforeUpdate() {
            const route = this.$router.currentRoute.value.name;
            if (route == 'login' || route == 'register') {
                this.showSidebar = false
            } else {
                this.showSidebar = true
            }
            this.username = localStorage.username
        },
        updated() {

        },
        computed: {

        },
        methods: {

            logout() {
                this.axios.defaults.headers.common["Authorization"] = ""

                localStorage.removeItem("token");
                localStorage.removeItem("username");
                localStorage.removeItem("userid");

                this.$store.commit("removeToken");

                this.accountDialog = false;

                this.$router.push("/login");

            },
            async sendFriendRequest() {
                const formData = {
                    username: this.request_username
                }
                this.axios.post("/api/v1/request/create/", formData).then(response => {
                    this.errors = []
                    this.addDialog = false
                    this.request_username = ''
                }).catch(error => {
                    this.errors = []
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`);
                        }

                        console.log(JSON.stringify(error.response.data));
                    } else {
                        this.errors.push("Something went wrong. Please try again.");

                        console.log(JSON.stringify(error));
                    }
                })
            },
            updateFriendRequests() {
                this.axios.get("/api/v1/request/latest/")
                    .then(response => {
                        this.friend_requests = response.data
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            },
            isMobile() {
                return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
            },
            acceptFriendRequest(requestId) {
                const formData = {
                    id: requestId,
                    status: "A"
                }

                this.axios.post("/api/v1/request/set/", formData).then(response => {
                    this.updateFriendRequests()
                    this.getFriendChannels()
                })
            },
            rejectFriendRequest(requestId) {
                const formData = {
                    id: requestId,
                    status: "R"
                }

                this.axios.post("/api/v1/request/set/", formData).then(response => {
                    this.updateFriendRequests()
                })
            },
            updateProfile() {

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
                    this.errors = []

                    if (response.data.user) {
                        localStorage.username = response.data.user.username
                    }
                    this.update_username = ""
                    this.update_profile_picture = null
                    this.accountDialog = false
                }).catch(error => {
                    this.errors = []
                    this.update_profile_picture = null
                    this.accountDialog = false
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`);
                        }

                        console.log(JSON.stringify(error.response.data));
                    } else {
                        this.errors.push("error: Make sure you have filled out the fields correctly.");

                        console.log(JSON.stringify(error));
                    }
                })
            },
            getFriendChannels() {
                this.axios.get("/api/v1/channel/").then(response => {
                    this.friend_channels = response.data
                })
            },
            setChannelId(channel_id) {
                this.$store.commit("setSelectedChannelId", channel_id)
            },
           
        }
    }
</script>



<style lang="scss">
    html,
    body {
        margin: 0;
        height: 100%;
        overflow: hidden;
    }

    .text-muted {
        color: #757575;
    }

    .large-text {
        font-size: 60px !important;
    }

    .sidebar {
        background-color: #424242;
        width: 300px;
        height: 100%;
        position: absolute;
        overflow: hidden;
    }


    .sidebar-groups {
        background-color: #616161;
        width: 110px;
        height: 100%;
        overflow-y: scroll;
    }


    .sidebar-friends {
        width: 200px;
        height: 100%;
        overflow-y: scroll;
    }

    .section {
        margin-left: 300px;
    }

    .myaccount-container {
        width: 100%;
    }

    .channel-flex-box {
        height: 100%;
    }

    .lds-loading-bar {
        position: fixed;
        animation: lds-loading-bar-2 0.1s normal forwards ease-in-out;
        width: 100vw;
        height: 4px;
        background-color: #2ac811;

        &.is-loading {
            animation: lds-loading-bar 0.2s normal forwards ease-in-out;
        }
    }

    @keyframes lds-loading-bar {
        from {
            transform: translateX(-100%);
            opacity: 0;
        }

        20% {
            opacity: 1;
        }

        to {
            transform: translateX(-25%);
        }
    }

    @keyframes lds-loading-bar-2 {
        from {
            transform: translateX(-25%);
        }


        80% {
            opacity: 1;
        }

        to {
            transform: translateX(0);
            opacity: 0;
        }
    }
</style>