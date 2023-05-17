<template>
 
    <v-container fluid pa-0 class="chat-container">
      <v-row align="center" justify="left">
                <v-col cols="1" lg="1" md="6" class="grey lighten-2 fill-height d-flex flex-column justify-center align-center">
                    <v-card flat tile>
                        <v-card-text>Message</v-card-text>
                    </v-card>
                </v-col>
            </v-row>
    </v-container>
    <v-card height="150px">
      <v-form @submit.prevent="">
        <div class="d-flex ustify-space-around">
       
              <v-text-field rounded label="Type message here" style="width: calc(100% - 138px)">

              </v-text-field>
        
           
              <v-btn icon="mdi-send" type="submit">
                </v-btn>
     </div>>
        
      </v-form>
    </v-card>
 
</template>

<script>

export default {
  name: 'ChatView',
  data() {
    return {
      
    }
  },
  components: {
  },
  mounted() {
    document.title = 'Chat'

    console.log(this.$route.params.chat_id)
  },
  methods: {
    
  }
}
</script>

<style scoped>
.chat-container {
  height: calc(100vh - 138px);
}
</style>