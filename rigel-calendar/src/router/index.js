import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../components/Home.vue'
import Vaccination from '../components/Vaccination.vue'
import Registration from '../components/Registration.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },{
    path: '/vaccination/:month',
    name: 'Vaccination',
    component: Vaccination,
    props: true 
  },{
    path: '/registration',
    name: 'Registration',
    component: Registration
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
