import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

// route level code-splitting
// this generates a separate chunk (about.[hash].js) for this route
// which is lazy-loaded when the route is visited.
function loadView(view) {
  return () => import(`../views/${view}.vue`);
}
const routes = [
  {
    path: '/',
    name: 'home',
    component: loadView("HomeView")
  },
  {
    path: '/about',
    name: 'about',
    component: loadView("AboutView"),
    props: route => ({ query: route.query })
  },
  {
    path: "/sign-up",
    name: "sign-up",
    component: loadView("Auth/SignUpView")
  },
  {
    path: "/login",
    name: "login",
    component: loadView("Auth/LoginView")
  },
]

const router = new VueRouter({
  routes
})

export default router
