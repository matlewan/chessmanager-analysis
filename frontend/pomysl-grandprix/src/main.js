import { createApp } from 'vue'
import { createStore } from 'vuex'
import App from './App.vue'
import router from './router'

import './assets/main.css'

const resp = await fetch('/out.json')
const data = await resp.json()
const app = createApp(App)
const store = createStore({
   state() {
      return {
         data: data
      }
   },
})

app.use(router)
app.use(store)
app.mount('#app')
