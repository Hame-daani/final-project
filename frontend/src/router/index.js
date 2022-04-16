import Vue from 'vue'
import VueRouter from 'vue-router'
import store from "@/store"

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
    component: loadView("HomeView"),
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: loadView("Auth/DashboardView"),
    meta: { requiresAuth: true }
  },
  {
    path: "/sign-up",
    name: "sign-up",
    component: loadView("Auth/SignUpView"),
  },
  {
    path: "/login",
    name: "login",
    component: loadView("Auth/LoginView"),
  },
]

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  let isLoggedIn = store.getters["auth/isLoggedIn"]
  if (to.meta.requiresAuth && !isLoggedIn) {
    next("login/", { query: { redirect: to.fullPath } })
  }
  else {
    next()
  }
})

export default router
