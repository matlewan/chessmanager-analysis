import { createRouter, createWebHistory } from 'vue-router'
import Classification from '@/views/Classification.vue'
import Players from '@/views/Players.vue'
import Matches from '@/views/Matches.vue'
import Player from '@/views/Player.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Classification
    },
    {
      path: '/players',
      component: Players
    },
    {
      path: '/matches',
      component: Matches
    },
    {
      path: '/player',
      name: 'player',
      component: Player
    }
  ]
})

export default router
