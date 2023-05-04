<template>
  <div class="home">
    <section class="hero is-medium mb-6">
      <div class="hero-body has-text-centered">
        <p class="title mb-6">
          Welcome to Harmony
        </p>
        <p class="subtitle">
          Harmony
        </p>
      </div>
    </section>

    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="title is-2 has-text-centered">Channels</h2>
      </div>
    

      <div class="column is-3" 
        v-for="channel in latestChannels"
        v-bind:key="channel.id">
      

      <div class="box">
      
        <h3 class="is-size-4">{{ channel.name }}</h3>

        <!--<router-link v-bind:to="product.get_absolute_url" class="button is-dark mt-4">View details</router-link>-->
      </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'ChatView',
  data() {
    return {
      latestChannels: []
    }
  },
  components: {
  },
  mounted() {
    this.getLatestChannels()

    document.title = 'Chat'
  },
  methods: {
    getLatestChannels() {
      
      this.axios.get('/api/v1/latest-channels/')
        .then(response => {
          this.latestChannels = response.data
        })
        .catch(error => {
          console.log(error)
        })
        
    }
  }
}
</script>

<style scoped>
.image {
  margin-top: -1.25rem;
  margin-left: -1.25rem;
  margin-right: -1.25rem;
}
</style>