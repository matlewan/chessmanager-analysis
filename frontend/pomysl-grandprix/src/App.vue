<script setup>
import Navbar from '@/components/Navbar.vue'
import { onMounted } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

onMounted(() => {
  fetch('/out.json')
    .then(resp => resp.json())
    .then(data => {
        store.commit('setData', data);
    });
})
</script>

<template>
  <Navbar />
  
  <router-view></router-view>
  
</template>

<style scoped>
@media (min-width: 1024px) {
  main {
    margin: 0 100px;
  }
}
@media (max-width: 1024px) {
  main {
    margin: 0 5px;
  }
}
</style>
