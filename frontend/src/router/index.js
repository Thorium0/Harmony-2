import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/Login.vue'
import AboutView from '../views/About.vue'
import ChatView from '../views/Chat.vue'
import store from '../store'
const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/', // '/:category_slug/:product_slug',
    name: 'chat',
    component: ChatView,
    meta: {
      requiresAuth: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    if (!store.getters.isLoggedIn) {
      next({ name: 'login' })
    } else {
      next() // go to wherever I'm going
    }
  } else {
    next() // does not require auth, make sure to always call next()!
  }
  
})

router.beforeResolve((to, from, next) => {
  if (to.name) {
    // Get the value of the isLoading variable from the store
    store.commit('setIsLoading', true)
  }
  next()
  
})

router.afterEach(() => {
  store.commit('setIsLoading', false)

  if (router.currentRoute.value.name == 'login') {
    store.commit('setIsOnLoginPage', true)
} else {
    store.commit('setIsOnLoginPage', false)
}
  
})



export default router
