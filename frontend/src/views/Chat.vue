<template>
  <v-card class="navbar">
    <div class="d-flex ustify-space-around">
      <v-btn icon="mdi-menu" @click="toggleShowsidebar"></v-btn>
    <v-card-title class="white--text">{{ chatTitle }}</v-card-title>
    <v-btn class="call-btn" icon="mdi-phone" @click="call()"></v-btn>
  </div>
  </v-card>

  <v-container fluid class="chat-container scroll">
    <v-row align="center" v-if="messages.length" v-for="message in messages" class="message-row">
      <v-card-title class="font-weight-bold">{{ message.sender.username }}</v-card-title>
      <div class="d-flex ustify-space-around message-div">


        <v-img v-bind:src="imageBaseUrl + message.sender.image" height="50px" width="50px" class="rounded-circle">
        </v-img>
        <v-card flat tile class="message-card">
          <v-card-text class="timestamp">{{ message.created }}</v-card-text>
          <v-card-text class="message-text">{{ message.content }}</v-card-text>
        </v-card>
      </div>

    </v-row>
  </v-container>

  <v-form @submit.prevent="sendMessage" class="message-container">
    <div class="d-flex ustify-space-around">
      
      
      <v-text-field v-model="message" class="pl-2 pr-2" variant="solo-filled" rounded label="Type message here"
        style="width: calc(100% - 138px)">
        <EmojiPicker class="emoji-picker" :native="true" theme="dark" pickerType="input" @select="onSelectEmoji" />
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
        imageBaseUrl: "http://thorium.ddns.net:8000",
        messages: [],
        chatTitle: "Chat - " + localStorage.selectedChannelName,
        message: "",
        lastMessageId: null,
        username: localStorage.username,
      }
    },
    components: {
      EmojiPicker
    },
    updated() {
      var element = document.getElementsByClassName("v3-emoji-picker-input")[0];
      if (element) {
        element.remove();
      }
    },
    mounted() {
      document.title = this.chatTitle
      this.interval = setInterval(() => {
        var route = this.$router.currentRoute.value.name;
        
        if (route == 'login' || route == 'register') {
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
        const lastMessageId = this.messages[this.messages.length-1].id
        if (lastMessageId != this.lastMessageId || lastMessageId == null) {
          setTimeout(() => {
            this.scrollToEnd()
          }, 100
          );
          
        }
        this.lastMessageId = lastMessageId

        }).catch(error => {
          //console.log(JSON.stringify(error))
        })
        
        this.$store.commit('setIsLoading', false)
      },
      sendMessage() {
        const channel_id = this.$store.state.selectedChannelId
        if (channel_id == null || !this.$store.state.isAuthenticated) {
          return
        }
        const message = this.message
        if (message == null || message == "") {
          return
        }
        this.axios.post("/api/v1/channel/messages/" + channel_id, {
          content: message
        }).then(response => {
          this.message = ""
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
 
      }
    },
  }
</script>

<style scoped>


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

  .navbar {
    background-color: #424242;
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
</style>