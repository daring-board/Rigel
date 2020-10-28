import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../components/Home.vue'
import Vaccination from '../components/Vaccination.vue'
import Registration from '../components/Registration.vue'
import Login from '../components/Login.vue'
import firebase from 'firebase/app';
import 'firebase/auth';

Vue.use(VueRouter)

const routes = [
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiredAuth: true }
  },{
    path: '/vaccination',
    name: 'Vaccination',
    component: Vaccination,
    meta: { requiredAuth: true }
  },{
    path: '/registration',
    name: 'Registration',
    component: Registration,
    meta: { requiredAuth: true }
  },{
    path: '/',
    name: 'Login',
    component: Login,
    meta: { requiredAuth: false }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) =>{
  if (to.matched.some(record => record.meta.requiredAuth)) {
    if (firebase.auth().currentUser) {
      console.log(firebase.auth().currentUser);
      next();
      return;
    }
    firebase.auth().onAuthStateChanged(user => {
      if (user) {
        next();
      } else {
        next({name: 'Login'})
      } 
    })
  }
  next();
})

export default router
