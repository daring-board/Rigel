import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";
import firebase from 'firebase'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    personal: {
      birth_day: '', last_name: '', first_name: ''
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
        last_name: state.personal.last_name,
        first_name: state.personal.first_name,
        birth_day: state.personal.birth_day
      });
    },
    getPersonal(state){
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
