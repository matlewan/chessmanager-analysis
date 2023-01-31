<script setup>
import Navbar from '@/components/Navbar.vue'
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
