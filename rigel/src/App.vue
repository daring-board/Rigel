<template>
  <div id="app">
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand>Rigel</b-navbar-brand>
    </b-navbar>
    <Labeling id="main"/>
  </div>
</template>

<script>
import Labeling from './components/Labeling.vue'

export default {
  name: 'app',
  components: {
    Labeling
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#main{
  padding-top: 10px;
}
</style>
