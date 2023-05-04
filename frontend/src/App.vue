<template>
    <div id="wrapper">
        <table v-if="showSidebar" class="sidebar">
            <tr>
                <td colspan="2">
                    ---Profile Placeholder--- <span class="text-muted">#1234</span>
                </td>
            </tr>
            <tr>
                <td class="sidebar-groups">

                    <!--FOREACH BULLSHIT-->



              
                        
                           
                    <v-btn height="80px" width="80px"  max-width="80" class="ma-1 rounded-circle">
                        <img src="//placehold.it/80x80" class="rounded-circle">
                    </v-btn>
                    <v-btn height="80px" width="80px"  max-width="80" class="ma-1 rounded-circle">
                        <img src="//placehold.it/80x80" class="rounded-circle">
                    </v-btn>
                    <v-btn height="80px" width="80px"  max-width="80" class="ma-1 rounded-circle">
                        <img src="//placehold.it/80x80" class="rounded-circle">
                    </v-btn>
                    <v-btn height="80px" width="80px"  max-width="80" class="ma-1 rounded-circle">
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
        
        },
        beforeCreate() {
        
        },
        mounted() {
            //console.log(this.$store.state.isLoading)
            
            
        },
        beforeUpdate() {
            //console.log(!this.$store.state.isOnLoginPage)
            this.showSidebar = !this.$store.state.isOnLoginPage
            
        },
        computed: {
            
        },
        methods: {
          
           
          
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
        height: 6px;
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