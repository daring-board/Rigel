import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";
import firebase from 'firebase/app';
import 'firebase/database';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    personal: {
      birth_day: '', nickname: ''
    },
    vaccinations: null,
    month: 0,
  },
  mutations: {
    setMonth(state, month){
      state.month = month;
    },
    setPersonal(state, personal){
      state.personal = personal;
      firebase.database().ref(`/users/${firebase.auth().currentUser.uid}`).set({
        nickname: state.personal.nickname,
        birth_day: state.personal.birth_day
      });
    },
    getPersonal(state){
      console.log(firebase.auth().currentUser);
      firebase.database().ref(`/users/${firebase.auth().currentUser.uid}`).once('value').then(function(snapshot) {
        state.personal = snapshot.val();
      });
    },
    getVaccinations(state){
      firebase.database().ref('/vaccinations/').once('value').then(function(snapshot) {
        state.vaccinations = snapshot.val();
      });
    }
  },
  actions: {
  },
  modules: {
  },
  plugins: [createPersistedState({
    key: 'rigel-calendar',
    paths: ['rigel-calendar'],
    storage: window.sessionStorage
})]
})
