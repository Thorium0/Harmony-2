<template>
    <div id="wrapper">
        <nav class="navbar is-dark">
            <div class="navbar-brand">
                <router-link to="/" class="navbar-item"><strong>Home</strong></router-link>

                <a class="navbar-burger" @click="burgerMenuActive = !burgerMenuActive" aria-label="menu"
                    aria-expanded="false" data-target="navbar-menu">
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                </a>
            </div>
            <div class="navbar-menu" id="navbar-menu" v-bind:class="{ 'is-active': burgerMenuActive }">
                <div class="navbar-start">
                    <router-link to="/about" class="navbar-item">About</router-link>
                </div>

                <div class="navbar-end">

                    <div class="navbar-item">
                        <div class="buttons">

                            <router-link to="/cart" class="button is-success">
                                <span class="icon"><i class="fas fa-shopping-cart"></i></span>
                                <span>Cart ({{ cartTotalLength }})</span>
                            </router-link>

                            <router-link to="/login" class="button is-primary">Login</router-link>
                            <router-link to="/register" class="button is-light">Register</router-link>

                        </div>
                    </div>
                </div>
            </div>
        </nav>


        <div class="lds-loading-bar" v-bind:class="{ 'is-loading': $store.state.isLoading }"></div>



        <section class="section">
            <router-view />
        </section>

        <footer class="footer">
            <p class="has-text-centered">Copyright (c) 2023</p>
        </footer>
    </div>
</template>

<script>
export default {
    data() {
        return {
            burgerMenuActive: false,
            cart: {
                items: []
            }
        }
    },
    beforeCreate() {
        this.$store.commit('initializeStore')
    },
    mounted() {
        this.cart = this.$store.state.cart
        console.log(this.$store.state.isLoading)
    },
    computed: {
        cartTotalLength() {
            let totalLength = 0

            for (let i = 0; i < this.cart.items.length; i++) {
                totalLength += this.cart.items[i].quantity
            }

            return totalLength
        }
    }
}
</script>



<style lang="scss">
@import '../node_modules/bulma';


.lds-loading-bar {
    position: fixed;
    animation: lds-loading-bar-2 0.1s normal forwards ease-in-out;
    width: 100vw;
    height: 6px;
    margin-top: 50px;
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

.navbar {
    position: fixed;
    left: 0;
    top: 0;
    width: calc(100vw - 10px);
    z-index: 100;
    height: 50px;
    ;
}

.footer {
    height: 100px;
}</style>

