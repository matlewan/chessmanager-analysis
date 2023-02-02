<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">GrandPrix</RouterLink>
      <RouterLink to="/players">Players</RouterLink>
      <!-- <RouterLink to="/player">Player</RouterLink> -->
      <!-- <RouterLink to="/matches">Matches</RouterLink> -->
    </nav>
  </header>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

nav {
  padding: 10px 0;
  width: 100%;
  font-size: 1rem;
  background-color: #303833;
}

nav a {
  color: lightgray;
  margin: 0;
  padding: 10px 30px;
  border: solid lightgray;
  border-width: 0 2px 0 0;  
}

.router-link-active {
  color: lightgreen;
}

@media (min-width: 1024px) {
}
</style>
