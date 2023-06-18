<template>
    <v-card class="navbar rounded-0">
        <div class="d-flex ustify-space-around">
            <v-btn icon="mdi-menu" @click="toggleShowsidebar"></v-btn>

            <v-dialog v-model="leaveDialog" width="auto">
                <template v-slot:activator="{ props }">
                    <v-btn class="bg-red text-black" icon="mdi-exit-run" v-bind="props"></v-btn>
                </template>
                <v-card>
                    <v-card-title>Leave Channel</v-card-title>
                    <v-card-text>Are you sure you want to leave this channel?</v-card-text>
                    <v-card-actions>
                        <v-btn color="red" text @click="leaveGroup">Leave</v-btn>
                        <v-btn color="green" text @click="leaveDialog = false">Cancel</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>



            <v-card-title class="white--text">{{ chatTitle.replace("$", "") }}</v-card-title>
            <v-btn class="call-btn" icon="mdi-phone" @click="call()"></v-btn>
        </div>
    </v-card>

    <v-container fluid class="chat-container scroll">
        <v-row align="center" v-if="messages.length" v-for="message in messages" class="message-row">
            <v-card-title class="font-weight-bold">{{ message.sender.username }}</v-card-title>
            <div class="d-flex ustify-space-around message-div">


                <v-img v-bind:src="imageBaseUrl + message.sender.image" height="50px" width="50px"
                    class="rounded-circle">
                </v-img>
                <v-card flat tile class="message-card">
                    <v-card-text class="timestamp">{{ message.created }}</v-card-text>
                    <v-card-text class="message-text">{{ message.content }}</v-card-text>
                    <v-img v-if="message.image" v-bind:src="imageBaseUrl + message.image" height="200px" width="200px"
                        class="rounded ma-1" />
                </v-card>
            </div>

        </v-row>
    </v-container>

    <v-form @submit.prevent="sendMessage" class="message-container">
        <div class="d-flex ustify-space-around">

            <v-file-input accept="image/*" v-model="messageImage" :hide-input="true" class="fileInput" />


            <v-text-field v-model="message" class="pl-2 pr-2 message-text-container" variant="solo-filled" rounded
                label="Type message here" style="width: calc(100% - 138px)">
                <EmojiPicker v-if="!isMobile()" class="emoji-picker" :native="true" theme="dark" pickerType="input"
                    @select="onSelectEmoji" />
            </v-text-field>




            <v-btn icon="mdi-send" type="submit">
            </v-btn>
        </div>

    </v-form>


</template>

<script>
    import EmojiPicker from 'vue3-emoji-picker'

    import 'vue3-emoji-picker/css'

    export default {
        name: 'ChatView',
        data() {
            return {
                imageBaseUrl: process.env.VUE_APP_AXIOS_URL,
                messages: [],
                chatTitle: "Chat - " + localStorage.selectedChannelName,
                message: "",
                lastMessageId: null,
                messageImage: null,
                username: localStorage.username,
                leaveDialog: false,
            }
        },
        components: {
            EmojiPicker
        },
        updated() {
           
            $(".v3-emoji-picker-input").remove();
            $(".fileInput .v-input__control").remove();

        },
        mounted() {
            document.title = this.chatTitle.replace("$", "")
            this.interval = setInterval(() => {
                var route = this.$router.currentRoute.value.name;

                if (route != 'chat') {
                    clearInterval(this.interval)
                    return
                }

                this.getMessagesForChannel()
            }, 1000);
        },
        beforeUpdate() {
            this.getMessagesForChannel()
        },
        methods: {
            onSelectEmoji(emoji) {
                this.message += emoji.i
            },
            call() {
                this.message = "[USER STARTED CALL]"
                this.sendMessage()
                this.$router.push('/call/null')
            },
            async getMessagesForChannel() {
                this.$store.commit('setIsLoading', true)
                const channel_id = this.$store.state.selectedChannelId
                if (channel_id == null || !this.$store.state.isAuthenticated) {
                    return
                }
                this.chatTitle = "Chat - " + localStorage.selectedChannelName
                this.axios.get("/api/v1/channel/messages/" + channel_id).then(response => {
                    this.messages = response.data
                    const lastMessageId = this.messages[this.messages.length - 1].id
                    if (lastMessageId != this.lastMessageId || lastMessageId == null) {
                        setTimeout(() => {
                            this.scrollToEnd()
                        }, 100);

                    }
                    this.lastMessageId = lastMessageId

                }).catch(error => {
                    console.log(JSON.stringify(error))
                })

                this.$store.commit('setIsLoading', false)
            },
            sendMessage() {
                const channel_id = this.$store.state.selectedChannelId
                if (channel_id == null || !this.$store.state.isAuthenticated) {
                    return
                }
                const message = this.message
                if ((message == null || message == "") && this.messageImage == null) {
                    return
                }
                var formData = new FormData();

                formData.append("content", message)

                if (this.messageImage != null) {
                    formData.append("image", this.messageImage[0])
                }
                const headers = {
                    'Content-Type': 'multipart/form-data'
                }
                this.axios.post("/api/v1/channel/messages/" + channel_id, formData, {
                    headers: headers
                }).then(response => {
                    this.message = ""
                    this.messageImage = null
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
            scrollToEnd() {
                var container = document.querySelector(".scroll");
                container.scrollTop = container.scrollHeight;

            },
            toggleShowsidebar() {
                var showSidebar = this.$store.state.showSidebar;

                this.$store.commit('setShowSidebar', !showSidebar)

            },
            leaveGroup() {
                var channelName = localStorage.selectedChannelName
                if (channelName.charAt(0) == "$") {
                    channelName = channelName.substring(1)
                    const formData = {
                        "name": channelName,
                        "action": "leave"
                    }
                    this.axios.post("/api/v1/channel/group/", formData).then(response => {
                        this.leaveDialog = false;
                        this.$router.push('/')
                    }).catch(error => {
                        console.log(JSON.stringify(error))
                    });


                } else {
                    const username = localStorage.selectedChannelName
                    this.axios.get("/api/v1/request/"+username).then(response => {
                        const requestId = response.data["id"]
                        const formData = {
                            "id": requestId,
                            "status": "R"
                        }
                        this.axios.post("/api/v1/request/set/", formData).then(response => {
                            this.leaveDialog = false;
                            this.$router.push('/')
                        }).catch(error => {
                            console.log(JSON.stringify(error))
                        });
                        
                    }).catch(error => {
                        console.log(JSON.stringify(error))
                    });
                    
                }

            },
            isMobile() {
   if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
     return true
   } else {
     return false
   }
 }
        },
    }
</script>

<style scoped lang="scss">
    .chat-container {
        height: calc(100vh - 110px);
        overflow-y: auto;
        overflow-x: hidden;
    }

    .call-btn {
        float: right;
        margin-left: auto;
        margin-right: 0;
    }

    .message-container {
        padding-top: 3px;
        height: 60px;
        position: relative;
        width: 100%;
        bottom: 0;
    }

    @media only screen and (max-width: 600px) {
        .message-container {
            position: fixed;
            height: 70px;
            z-index: 5;
        }
        .chat-container {
            height: calc(100vh - 130px);
        }

        .navbar {
            position: fixed;
            z-index: 10;
        }
    }

    .message-text-container {
        margin-left: 20px
    }

    .navbar {
        background-color: #616161;
        width: 100%;
    }

    .timestamp {
        color: #BDBDBD;
        position: absolute;
        right: 0
    }


    .emoji-picker {
        position: absolute;
        right: 0;
        top: 15px;
    }

    .message-text {
        margin-right: 140px;
    }

    .message-row {
        width: 100%;
        margin: 4px;
    }

    .message-div {
        width: 100%;
    }

    .message-card {
        width: 100%;
        background-color: #424242;
        margin-left: 4px;
    }

    .fileInput {
        position: absolute;
        top: 30%;
    }
</style>