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
    icon: "mdi-home",
    component: loadView("HomeView"),
    meta: {
      requiresAuth: false,
      nav: true
    }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    icon: "mdi-account-box",
    component: loadView("ProfileView"),
    meta: {
      nav: true,
      requiresAuth: true,
    }
  },
  {
    path: "/sign-up",
    name: "sign-up",
    icon: "mdi-account-plus",
    component: loadView("Auth/SignUpView"),
    meta: {
      nav: true,
      requiresAuth: false,
    }
  },
  {
    path: "/login",
    name: "login",
    component: loadView("Auth/LoginView"),
    meta: {
      nav: false,
      requiresAuth: false,
    }
  },
  {
    path: "/movies/",
    name: "movies",
    icon: "mdi-movie",
    component: loadView("MoviesView"),
    props: true,
    meta: {
      nav: true,
      requiresAuth: false,
    }
  },
  {
    path: "/movies/:id",
    name: "movie",
    component: loadView("MovieDetailView"),
    props: true,
    meta: {
      nav: false,
      requiresAuth: false,
    }
  },
  {
    path: '/profile/:id',
    name: 'profile',
    component: loadView("ProfileView"),
    props: true,
    meta: {
      nav: false,
      requiresAuth: false,
    }
  },
  {
    path: "/reviews/:id",
    name: "review",
    component: loadView("ReviewDetailView"),
    props: true,
    meta: {
      nav: false,
      requiresAuth: false,
    }
  }
]

const router = new VueRouter({
  routes,
  scrollBehavior() {
    window.scrollTo(0, 0);
  }
})

router.beforeEach((to, from, next) => {
  let isLoggedIn = store.getters["auth/isLoggedIn"]
  if (to.meta.requiresAuth && !isLoggedIn) {
    next({ name: "login" }, { query: { redirect: to.fullPath } })
  }
  else {
    next()
  }
})

export default router
