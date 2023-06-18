<template>
    <div class="form-card align-center justify-center d-flex ml-1 mr-1">
        <v-card width="400" height="360" title="Register" subtitle="If you already have an account go to login"
            class="pa-2">
            <form @submit.prevent="submitForm">
                <v-text-field v-model="username" :counter="25" label="username" required></v-text-field>


                <v-text-field v-model="password" :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                    :rules="[rules.required, rules.min]" :type="show1 ? 'text' : 'password'" :counter="20"
                    hint="At least 8 characters" @click:append="show1 = !show1" label="password" required>
                </v-text-field>


                <v-text-field v-model="password2" :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                    :rules="[rules.required, rules.min, rules.matchingPasswords]" :type="show2 ? 'text' : 'password'" :counter="20"
                    label="repeat password" hint="At least 8 characters" class="input-group--focused"
                    @click:append="show2 = !show2" required>
                </v-text-field>


                <v-btn class="me-4" type="Sign up">
                    signUp
                </v-btn>

                <v-btn to="/login">
                    back to login
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
    import { CometChat } from '@cometchat-pro/chat';
    export default {
        name: 'RegisterView',
        data() {
            return {
                username: '',
                password: '',
                password2: '',
                errors: [],

                show1: false,
                show2: false,
                rules: {
                    required: value => !!value || 'Required.',
                    min: v => v.length >= 8 || 'Min 8 characters',
                    matchingPasswords: v => v === this.password || "Passwords do not match"

                }
            }

        },
        methods: {
            async submitForm() {
                const isAlpha = str => /^[a-zA-Z]*$/.test(str);

                if (!isAlpha(this.username)) {
                    this.errors.push({"Error" : "Username can only contain letters in the alphabet"});
                    return;
                }

                const formData = {
                    username: this.username,
                    password: this.password
                }
                    

                this.axios.post("/api/v1/users/", formData)
                    .then(response => {
                        this.errors = [];
                        this.CreateCometChatUser(response.data.id)
                        this.$router.push("/login");
                    }).catch(error => {
                        this.errors = [];
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
            CreateCometChatUser(_user_id) {
                let user_id = _user_id.toString();
                
                let authKey = process.env.VUE_APP_COMETCHAT_AUTH_KEY;
                
                var uid = user_id;
                var name = this.username;

                var user = new CometChat.User(uid);
                user.setName(name);

                CometChat.createUser(user, authKey).then(
                    user => {
                        console.log("[CometChat] User created", user);
                    }, error => {
                        console.log("[CometChat] Failed to create user", error);
                    }
                )
            },
            lowercaseify(string) {
                for (var i = 0; i < string.length; i++) {
                    if (string[i] == string[i].toUpperCase()) {
                        string = string.replace(string[i], "_" + string[i].toLowerCase());
                    }
                }
                return string
            },

        },
        mounted() {
            document.title = 'Register | Harmony'
        },
    }
</script>

<style lang="scss">
    .form-card {
        margin-left: calc(50% - 320px);
        margin-top: calc(50vh - 250px);
    }
</style>