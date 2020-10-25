import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    personal: {
      birth_day: '',
      last_name: '',
      first_name: ''
    },
    vaccinations: {
      hiv_1: {
        display_name: 'ヒブ（インフルエンザ菌B型）:1期',
        status: 0,
        needed: 3,
        required: true, 
        spans: [2, 3, 4, 5, 6],
        recommends: [2, 3, 4],
        interval: {num: 6, unit: 'day'}
      },
      hiv_2: {
        display_name: 'ヒブ（インフルエンザ菌B型）:2期',
        status: 0,
        needed: 1,
        required: true, 
        spans: [12, 13, 14, 15, 16, 17, 18, 19, 20],
        recommends: [12, 13, 14],
        interval: {num: 6, unit: 'day'}
      },
      pcv13_1: {
        display_name: '肺炎球菌:1期',
        status: 0,
        needed: 3,
        required: true, 
        spans: [2, 3, 4, 5, 6],
        recommends: [2, 3, 4],
        interval: {num: 6, unit: 'day'}
      },
      pcv13_2: {
        display_name: '肺炎球菌:2期',
        status: 0,
        needed: 1,
        required: true, 
        spans: [12, 13, 14],
        recommends: [12, 13, 14],
        interval: {num: 6, unit: 'day'}
      },
      HepatitisB: {
        display_name: 'B型肺炎',
        status: 0,
        needed: 3,
        required: true,
        spans: [2, 3, 4, 5, 6, 7, 8],
        recommends: [2, 3, 7],
        interval: {num: 6, unit: 'day'}
      }
    }
  },
  mutations: {
    setPersonal(state, personal){
      state.personal.last_name = personal.last_name;
      state.personal.first_name = personal.first_name;
      state.personal.birth_day = personal.birth_day;
    }
  },
  actions: {
  },
  modules: {
  }
})
