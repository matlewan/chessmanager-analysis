<script setup>
import { computed, ref, toRaw } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'

const store = useStore()
const query = useRoute().query
const router = useRouter()

const data = toRaw(store.state.data)
const tournament = data.tournaments['#' + query.name]
const numRounds = tournament.n_rounds;
const round = ref('1')

const edition = ref(query.edition ? ('#' + query.edition) : 'All')
const player = ref(query?.player || 'All')
const opponent = ref(query?.opponent || 'All')
if (!query.edition && !query.t && !query.player) {
  const lastTournament = Math.max(...Object.keys(data.tournaments).map(t => parseInt(t.replace('#','').replace('.',''))))
  edition.value = '#' + Math.floor(lastTournament/10)
  tournament.value = lastTournament % 10
  round.value = 1
}
const allMatches = computed(() => {
    let ans = []
    for (const t of Object.values(data.tournaments)) {
      for (const r of t.rounds) {
        for (const m of r.matches)
          ans.push({ tournament:t.name, round:r.num, ...m })
      }
    }
    return ans;
  }
)
const matches = computed(() => allMatches.value
  .filter(m => m.tournament == tournament.name)
  .filter(m => round.value=='All' || m.round == round.value)
  .filter(m => player.value == 'All' || m.white == player.value || m.black == player.value)
  .filter(m => opponent.value == 'All' || m.white == opponent.value || m.black == opponent.value)
)
const results = computed(() => {
  const r = tournament.results;
  const playersMap = tournament.players.reduce((map, player) => {
    map[player.name] = player;
    return map
  }, {});
  for (const rr of r) {
    rr.p = playersMap[rr.player]
  }
  return r;
});

function result(r) {
  return r==1.0 ? '1 : 0' : (r==0.5 ? '½:½' : '0 : 1')
}
function setRound(r) {
  player.value = 'All'
  round.value = r
}
function setPlayer(p) {
  round.value = 'All'
  player.value = p
  opponent.value = 'All'
}
</script>

<template>
  <main>
    <h2 class="tournament">
      Tournament {{ tournament.name }}
    </h2>
    <div class="filters">
      <div class="rounds">
        <div class="round" @click="round=(round==1 ? 1 : round-1)">&lt;</div>
        <div :class="['round', i==round ? 'selected' : '']" v-for="i in numRounds"
          @click="setRound(i)">{{ i }}</div>
        <div class="round" @click="round=(round==numRounds ? numRounds : round+1)">&gt;</div>
      </div>
    </div>
    <div class="games">
      <table>
        <tbody>
          <tr v-for="(m,i) in matches">
            <!-- <td>{{ i+1 }}.</td> -->
            <td class="name white" @click="setPlayer(m.white)">{{ m.white }}</td>
            <td>{{ result(m.result) }}</td>
            <td class="name black" @click="setPlayer(m.black)">{{ m.black }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="results">
      <table>
        <table>
          <thead>
            <th>#</th>
            <th class="name">Player</th>
            <th>Pts</th>
            <th>BHC1</th>
            <th>BH</th>
          </thead>
          <tbody>
            <tr v-for="r in results">
             <td>{{ r.place }}.</td>
             <td class="name" @click="setPlayer(r.p.name)">{{ r.p.name }}</td>
             <td>{{ r.points.toFixed(1) }}</td>
             <td>{{ r.bch1.toFixed(1) }}</td>
             <td>{{ r.bch.toFixed(1) }}</td> 
            </tr>
          </tbody>
        </table>
      </table>
    </div>
  </main>
</template>

<style scoped>
th {
  text-align: left;
  font-weight: 550;
}
td {
  padding: 0 0.3em;
  text-align: center;
}
td.name {
  cursor: pointer;
  width: calc(10em + 4vw);
  text-align: left;
}
div.results {
  margin-top: .5em;
  padding-top: .5em;
  border-top: 1px dashed black;
}
main {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.tournament {
  margin-top: 0.5em;
}
.filters {
  margin: 0.5em 0;
  line-height: 2em;
  display: grid;
  grid-template-columns: 1fr;
}
.rounds {
  display: flex;
}
.round {
  cursor: pointer;
  user-select: none;
  border: 1px solid black;
  margin-right: -1px;
  width: 2em;
  height: 2em;
  background-color: rgb(199, 238, 218);
  text-align: center;
}
.round.selected {
  background-color: rgb(149,188,168);
}
.games td.white {
  text-align: right;
}
.games {
  display: inline;
}
.results th,td {
  text-align: center;
}
.results th.name {
  text-align: left;
}
</style>
