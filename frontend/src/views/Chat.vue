<template>

  <v-container fluid pa-0 class="chat-container">
    <v-row align="center" justify="left">
      <v-col cols="1" lg="1" md="6" class="grey lighten-2 fill-height d-flex flex-column justify-center align-center">
        <v-card flat tile v-if="messages.length" v-for="message in messages">
          <v-img v-bind:src="imageBaseUrl + message.sender.image" height="50px" width="50px" class="ml-3 rounded-circle"></v-img>
          <v-card-title>{{ message.sender.username }}</v-card-title>
          <v-card-text>{{ message.content }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  <v-card class="message-container">
    <v-form @submit.prevent="">
      <div class="d-flex ustify-space-around">

        <v-text-field rounded label="Type message here" style="width: calc(100% - 138px)">

        </v-text-field>


        <v-btn icon="mdi-send" type="submit">
        </v-btn>
      </div>

    </v-form>
  </v-card>

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
    width: calc(100% - 250px);
    bottom: 0;
  }
</style>