<template>
  <div id="app">
      <!-- Main -->
      <router-view></router-view>
  </div>
</template>

<script>
import Index from '@/components/Index'

export default {
  name: 'App',
  components: {
    Index
  }
}
</script>

<style>
  @import "assets/css/style.default.css";
  /*@import "assets/css/style.custom.css";*/
  /*@import "assets/css/fontastic.css";*/
  /*@import "assets/css/button.css";*/

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
</style>
