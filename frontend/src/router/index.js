import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

// route level code-splitting
// this generates a separate chunk (about.[hash].js) for this route
// which is lazy-loaded when the route is visited.
const AboutView = () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
const HomeView = () => import(/* webpackChunkName: "home" */ '../views/HomeView.vue')

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView,
    props: route => ({ query: route.query })
  }
]

const router = new VueRouter({
  routes
})

export default router
