<script setup>
import { computed, ref, toRaw } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'

const query = useRoute().query
const router = useRouter()
const data = toRaw(useStore().state.data)

const allTournaments = Object.values(data.tournaments)
const editions = Math.ceil(allTournaments.length / 5)
const rounds = computed(() => ['All', 1, 2, 3, 4, 5, 6, 7])
const players = computed(() => ['All', ...Object.keys(data.players).sort()])

const edition = ref(query.edition ? ('#' + query.edition) : 'All')
const tournament = ref(query.t || 'All')
const results = computed(() => {
  const key = edition.value + '.' + tournament.value;
  const t = data.tournaments[key];
  const r = t.results;
  const playersMap = t.players.reduce((map, player) => {
    map[player.name] = player;
    return map
  }, {});
  for (const rr of r) {
    rr.p = playersMap[rr.player]
  }
  return r;
});

function tournaments(edition) {
    return allTournaments.filter(t => t.name.startsWith('#' + edition + '.')).reverse();
}
</script>

<template>
  <main>
    <div class="edition" v-for="i in editions" :set="e = editions-i+1">
        <div class="tournament" v-for="t in tournaments(e)"
          @click="router.push(`/tournament?name=${t.name.slice(1)}`)" >
            <p>{{ t.name.slice(1) }}</p>
            <small>{{ t.date }}</small>
        </div>
    </div>
  </main>
</template>

<style scoped>
main {
    padding-top: 1em;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.edition {
    display: flex;
    align-items: start;
}
.tournament {
    cursor: pointer;
    font-size: 0.9em;
    margin-right: -1px;
    margin-top: -1px;
    border: solid 1px black;
    width: calc(10vw + 20px);
    height: 4em;
    text-align: center;
    padding: 0.3em 0;
    background-color: rgb(199, 238, 218);
}
</style>
