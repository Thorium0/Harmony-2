<template>
  <div class="about">
    <h1 class="title">Welcome to Harmony!</h1>
  </div>
</template>


<script>
export default {
  name: 'AboutView',
  mounted() {
    document.title = 'About'
  },
}
</script>

<style scoped>

.title {
  font-size: 3em;
  text-align: center;
  color: #1abc9c;
  margin-top: 0.5em;
  margin-bottom: 0.5em;
}

</style>