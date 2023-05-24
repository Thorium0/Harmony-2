<template>

  <v-container fluid pa-0 class="chat-container">
    <v-row align="center" v-if="messages.length" v-for="message in messages" class="message-row">
      <v-card-title class="font-weight-bold">{{ message.sender.username }}</v-card-title>
        <div class="d-flex ustify-space-around message-div">
         
        <v-img v-bind:src="imageBaseUrl + message.sender.image" height="50px" width="50px" class="rounded-circle"></v-img>
        <v-card flat tile class="message-card" color="grey-darken-1">
          <v-card-text class="timestamp">{{ message.timestamp }}</v-card-text>
          <v-card-text class="message-text">{{ message.content }}</v-card-text>
        </v-card>
      </div>
    
    </v-row>
  </v-container>
  
    <v-form @submit.prevent="" class="message-container">
      <div class="d-flex ustify-space-around">

        <v-text-field rounded label="Type message here" style="width: calc(100% - 138px)">

        </v-text-field>


        <v-btn icon="mdi-send" type="submit">
        </v-btn>
      </div>

    </v-form>
 

</template>

<script>
  export default {
    name: 'ChatView',
    data() {
      return {
        imageBaseUrl: "http://localhost:8000",
        messages: [],
      }
    },
    components: {},
    mounted() {
      document.title = 'Chat'
      this.getMessagesForChannel()
      this.interval = setInterval(() => {
          this.getMessagesForChannel()
      }, 2000);

    },
    methods: {
      getMessagesForChannel() {
        var channel_id = this.$store.state.selectedChannelId
        if (channel_id == null) {
          return
        }

        this.axios.get("/api/v1/channel/messages/" + channel_id).then(response => {
        
          this.messages = response.data

        }).catch(error => {
          console.log(JSON.stringify(error))
        })
      },
    },
    updated() {
      console.log(window.messages)
    }
  }
</script>

<style scoped>
  .chat-container {
    height: calc(100vh - 60px);
    overflow-y: auto;
    position: relative;
  }

  .message-container {
    height: 60px;
    position: fixed;
    width: calc(100% - 310px);
    bottom: 0;
  }

  .timestamp {
        color: #424242;
        position: absolute;
        right:0
  }

  .message-text {
    margin-right: 140px;
  }

  .message-row {
    height: 80px;
    width: 90%;
    margin: 4px;
  }

  .message-div {
    width: 100%;
  }

  .message-card {
    width: 100%;
    margin-left: 4px;
  }
</style>