<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <nav>
    <RouterLink to="/">GrandPrix</RouterLink>
    <RouterLink to="/players">Players</RouterLink>
    <!-- <RouterLink to="/player">Player</RouterLink> -->
    <RouterLink to="/tournaments">Tournaments</RouterLink>
  </nav>
</template>

<style scoped>
nav {
  display: flex;
  max-width: 100vw;
  justify-content: center;
  font-size: 1.2em;
  background-color: #303833;
}

nav a {
  color: lightgray;
  margin: 0;
  padding: 1.2vw calc(5px + 1.2vw);
}

.router-link-active {
  color: lightgreen;
}

@media (min-width: 1024px) {
}
</style>
