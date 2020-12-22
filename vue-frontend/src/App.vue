<template>
  <div id="app">
    <ImagesComponent/>
  </div>
</template>

<script>
import ImagesComponent from "@/components/ImagesComponent";

export default {
  name: 'App',
  components: {
    ImagesComponent
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
