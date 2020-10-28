import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import firebase from 'firebase/app';

Vue.config.productionTip = false

var config = {
  apiKey: "AIzaSyBgC_40tfmwnLtw2r3_dBC6Hl18lp-6EdA",
  authDomain: "rigel-b11c1.firebaseapp.com",
  databaseURL: "https://rigel-b11c1.firebaseio.com",
  projectId: "rigel-b11c1",
  storageBucket: "rigel-b11c1.appspot.com",
  messagingSenderId: "113544385542",
  appId: "1:113544385542:web:43adae6f5f4b91f2789f87",
  measurementId: "G-RRBDHWQW9V"
};
firebase.initializeApp(config)

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
