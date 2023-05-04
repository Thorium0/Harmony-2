import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import AboutView from '../views/About.vue'
import ProductView from '../views/Product.vue'
import store from '../store'
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/:category_slug/:product_slug',
    name: 'product',
    component: ProductView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
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
})

export default router
