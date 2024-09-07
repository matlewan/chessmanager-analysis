<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<template>
  <Navbar />
  <router-view></router-view>
</template>

<style scoped>
main {
  max-width: 100%;
  margin: 0 auto;
}
@media (max-width: 500px) {
  body {
    
  }
}
</style>
