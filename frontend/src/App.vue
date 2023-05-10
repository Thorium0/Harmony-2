<template>
    <div id="wrapper">
        <table v-if="showSidebar" class="sidebar">
            <tr>
                <td colspan="2">
                    <v-card>
                        <v-dialog v-model="accountDialog" width="auto">
                            <template v-slot:activator="{ props }">
                                <v-btn density="compact" icon="mdi-cog" color="grey" v-bind="props"></v-btn>
                            </template>

                            <v-card>
                                <v-card-actions>
                                    <v-btn color="primary" @click="accountDialog = false">Close</v-btn>
                                    <v-btn color="secondary" @click="logout">Logout</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>

                        {{ username }}
                        <!--<span class="text-muted">#1234</span>-->
                    </v-card>
                </td>
            </tr>
            <tr>
                <td class="sidebar-groups">

                    <!--FOREACH BULLSHIT-->






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
                                <v-btn text="<" height="80px" width="80px" class="ma-1 large-text rounded-circle" v-if="isMobile()" @click="showSidebar = !showSidebar"></v-btn>
                        </template>

                        <v-card width="400" height="220" title="Send Friend Request"
                            subtitle="Enter friend's username to send a friend request" class="pa-2">
                            <v-form @submit.prevent="sendFriendRequest">
                                <v-text-field v-model="request_username" :counter="10" label="Note: Case-sensitive" required>
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






                    <!--END FOREACH BULLSHIT-->


                </td>

                <td class="sidebar-friends">



                    <v-card v-if="friend_requests.length" v-for="friend_request in friend_requests"
                        v-bind:key="friend_request.id" class="mb-2 pr-2" :style="'border: 1px solid yellow;'">
                        <v-row align="center" class="mt-1 mb-1">
                            <v-col class="shrink">
                                <v-img src="//placehold.it/80x80" max-width="80" class="ml-3 rounded-circle"></v-img>
                            </v-col>
                            <v-col>
                                <v-card-text class="pa-0">Request: {{ friend_request.username }}</v-card-text>
                                <v-btn class="mr-1" density="compact" icon="mdi-check" color="green" @click="acceptFriendRequest(friend_request.id)"></v-btn>
                                <v-btn density="compact" icon="mdi-close" color="red" @click="rejectFriendRequest(friend_request.id)"></v-btn>
                            </v-col>
                        </v-row>
                    </v-card>


                    <v-card class="mb-2 pr-2">
                        <v-row align="center" class="mt-1 mb-1">
                            <v-col class="shrink">
                                <v-img src="//placehold.it/80x80" max-width="80" class="ml-3 rounded-circle"></v-img>
                            </v-col>
                            <v-col>
                                <v-card-text class="pa-0">kagemand</v-card-text>
                            </v-col>
                        </v-row>
                    </v-card>


                </td>
            </tr>

        </table>




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
                username: localStorage.username
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
                this.errors = []
                const formData = {
                    username: this.request_username
                }
                this.axios.post("/api/v1/request/create/", formData).then(response => {
                    this.addDialog = false
                    this.request_username = ''
                }).catch(error => {
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
            }
        }
    }
</script>



<style lang="scss">
    html,
    body {
        margin: 0;
        height: 100%;
    }

    .text-muted {
        color: #6c757d;
    }

    .large-text {
        font-size: 60px !important;
    }

    .sidebar {
        background-color: #3b3b3b;
        width: 250px;
        height: 100%;
        z-index: 1;
        position: fixed;
    }

    .sidebar-groups {
        background-color: #252525;
        width: 80px;
        height: 100%;
    }

    .section {
        margin-left: 250px;
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


    .section {
        padding-top: 80px;
    }
</style>