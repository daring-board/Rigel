import Vue from 'vue'
import Vuex from 'vuex';
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import firebase from 'firebase/app'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './assets/custom.css'
import store from './store'

Vue.use(BootstrapVue)
Vue.use(Vuex);

Vue.config.productionTip = false

const config = {
  apiKey: "AIzaSyBgC_40tfmwnLtw2r3_dBC6Hl18lp-6EdA",
  authDomain: "rigel-b11c1.firebaseapp.com",
  databaseURL: "https://rigel-b11c1.firebaseio.com",
  projectId: "rigel-b11c1",
  storageBucket: "rigel-b11c1.appspot.com",
  messagingSenderId: "113544385542",
  appId: "1:113544385542:web:43adae6f5f4b91f2789f87",
  measurementId: "G-RRBDHWQW9V"
}
firebase.initializeApp(config);

new Vue({
  render: h => h(App),
  store,
}).$mount('#app')
