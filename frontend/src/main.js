import { createApp } from 'vue'
import { createStore } from 'vuex'
import App from './App.vue'
import router from './router'

import './assets/main.css'

const app = createApp(App)
const store = createStore({
   state() {
      return {
         data: {}
      }
   },
})
app.use(router)
app.use(store)
fetch('./out.json')
   .then(resp => resp.json())
   .then(data => {
      store.state.data = data;
      app.mount('#app') 
   })
