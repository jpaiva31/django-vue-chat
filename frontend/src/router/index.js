import { createRouter, createWebHashHistory } from 'vue-router'

import ConversationPage from '../views/ConversationPage.vue'  // ← A nova página do chat
import HomePage from '../views/HomePage.vue'


const routes = [
  {
    path: "/conversation/:id",
    name: "Conversation",
    component: ConversationPage,
  },
  {
    path: "/",
    name: "Home",
    component: HomePage
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior(to) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      }
    }
  },
})


export default router
