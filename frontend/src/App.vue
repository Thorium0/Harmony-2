<template>
    <div id="wrapper">
        <table v-if="showSidebar" class="sidebar">
            <tr>
                <td colspan="2">
                    ---Profile Placeholder--- <span class="text-muted">#1234</span>

                    <v-dialog v-model="accountDialog" width="auto">
                        <template v-slot:activator="{ props }">

                            <v-btn color="primary" v-bind="props">
                                <v-icon icon="mdi-account"></v-icon>
                            </v-btn>
                        </template>

                        <v-card>
                            <v-card-actions>
                                <v-btn color="primary"  @click="accountDialog = false">Close</v-btn>
                                <v-btn color="secondary"  @click="logout">Logout</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
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

                    <v-btn text="+" height="80px" width="80px" class="ma-1 large-text rounded-circle"></v-btn>





                    <!--END FOREACH BULLSHIT-->


                </td>

                <td class="sidebar-friends">

                    <!--FOREACH BULLSHIT-->

                    <v-card class="mb-2" tile="">
                        <v-row align="center" class="mt-1 mb-1">
                            <v-col class="shrink">
                                <v-img src="//placehold.it/80x80" max-width="80" class="ml-3 rounded-circle"></v-img>
                            </v-col>
                            <v-col>
                                <v-card-text class="pa-0">username</v-card-text>
                            </v-col>
                        </v-row>
                    </v-card>



                    <!--END FOREACH BULLSHIT-->

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
                showSidebar: true,
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


        },
        beforeUpdate() {
            if (this.$router.currentRoute.value.name == 'login' || this.$router.currentRoute.value.name == 'register') {
                this.showSidebar = false
            } else {
                this.showSidebar = true
}
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