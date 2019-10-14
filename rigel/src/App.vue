<template>
  <div id="app">
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand>DIY</b-navbar-brand>
    </b-navbar>
    <b-card>
      <b-card-header>
        晩御飯ルーレット
      </b-card-header>
      <b-card-body>
        <Roulet/>
      </b-card-body>
    </b-card>
    <b-card>
      <b-card-header>
        ストⅡ コスプレ判定機
      </b-card-header>
      <b-card-body>
        <Labeling id="main"/>
      </b-card-body>
    </b-card>
  </div>
</template>

<script>
import Labeling from './components/Labeling.vue'
import Roulet from './components/Roulet.vue'

export default {
  name: 'app',
  components: {
    Labeling,
    Roulet
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
