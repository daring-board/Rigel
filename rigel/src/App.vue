<template>
  <div id="app">
	<b-navbar toggleable="lg">
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
        画像判別機を作成できます！
      </b-card-header>
      <b-card-body>
        <ML1/>
      </b-card-body>
    </b-card>
  </div>
</template>

<script>
import Roulet from './components/Roulet.vue'
import ML1 from './components/ML1.vue'

export default {
  name: 'app',
  components: {
    Roulet,
    ML1,
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #fafdff;
}
#main{
  padding-top: 10px;
}
</style>
