<template>
    <div class="form-card">
        <v-card width="400" height="280" title="Login" subtitle="If you are new go to register" class="pa-2">
            <form @submit.prevent="submitForm">
                <v-text-field v-model="username" :counter="10" label="username" required></v-text-field>


                <v-text-field v-model="password" :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                    :rules="[rules.required, rules.min]" :type="show1 ? 'text' : 'password'" :counter="10"
                    hint="At least 8 characters" @click:append="show1 = !show1" label="password" required>
                </v-text-field>


                <v-btn class="me-4" type="Login">
                    Login
                </v-btn>

                <v-btn to="/register">
                    go to register
                </v-btn>
            </form>
        </v-card>
        <v-card width="400" v-if="errors.length" class="pa-2 mt-2" color="#555500">
            <ul>
                <li v-for="error in errors" :key="error">&#x2022; {{ error }}</li>
            </ul>
        </v-card>
    </div>
</template>

<script>
import axios from 'axios';

    export default {
        name: 'RegisterView',
        data() {
            return {
                username: 'Bendtsen',
                password: 'kagemand123',
                errors: [],

                show1: false,
                rules: {
                    required: value => !!value || 'Required.',
                    min: v => v.length >= 8 || 'Min 8 characters',
                }
            }

        },
        methods: {
                async submitForm() {
                    this.axios.defaults.headers.common["Authorization"] = ""
                    localStorage.removeItem("token");

                    this.errors = [];

                    const formData = {
                        username: this.username,
                        password: this.password
                    }

                    this.axios.post("/api/v1/token/login", formData)
                        .then(response => {
                            const token = response.data.auth_token;

                            this.$store.commit("setToken", token);

                            axios.defaults.headers.common["Authorization"] = `Token ${token}`;

                            localStorage.setItem("token", token);

                            const toPath = this.$route.query.to || "/about";

                            this.$router.push(toPath);
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
                }
        },
        mounted() {
            document.title = 'Login | Harmony'
        },
    }
</script>

<style lang="scss">
    .form-card {
        margin-left: calc(50% - 320px);
        margin-top: calc(50vh - 250px);
    }
</style>