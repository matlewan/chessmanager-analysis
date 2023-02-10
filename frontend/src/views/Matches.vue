<script setup>
import { computed, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'

const store = useStore()
const query = useRoute().query
const router = useRouter()

const data = store.state.data
const editions = ['All', ...new Set(Object.keys(data.tournaments).map(t => t.split('.')[0]).reverse())]
const tournaments = computed(() => ['All', 1,2,3,4,5])
const rounds = computed(() => ['All', 1, 2, 3, 4, 5, 6, 7])
const players = computed(() => ['All', ...Object.keys(data.players).sort()])

const edition = ref(query.edition ? ('#' + query.edition) : 'All')
const tournament = ref(query.t || 'All')
const round = ref('All')
const player = ref(query?.player || 'All')
const opponent = ref(query?.opponent || 'All')
const display = computed(() => 
  !(edition.value == 'All' || tournament.value == 'All') || player.value != 'All'
)
const matches = computed(() => !display.value ? [] : data.matches
  .filter(m => edition.value == 'All' || m.tournament.startsWith(edition.value))
  .filter(m => tournament.value == 'All' || m.tournament.startsWith(edition.value + '.' + tournament.value))
  .filter(m => round.value == 'All' || m.round == round.value)
  .filter(m => player.value == 'All' || m.white == player.value || m.black == player.value)
  .filter(m => opponent.value == 'All' || m.white == opponent.value || m.black == opponent.value)
)

function result(r) {
  return r==1.0 ? '1 - 0' : (r==0.5 ? '½-½' : '0 - 1')
}
function setRound(t,r) {
  const [a,b] = t.split('.')
  edition.value = a
  tournament.value = b
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
    <div class="filters">
      <div class="row">
        <label>Tournament:</label>
        <select v-model="edition"> <option v-for="e in editions">{{ e }}</option> </select>
        <select v-model="tournament"> <option v-for="t in tournaments">{{ t }}</option> </select>
        <label>Round:</label>
        <select v-model="round"> <option v-for="r in rounds">{{ r }}</option> </select>
      </div>
      <div class="row">
        <label>Player 1:</label>
        <select class="name" v-model="player"> <option v-for="p in players">{{ p }}</option> </select>
      </div>
      <div class="row">
        <label>Player 2:</label>
        <select class="name" v-model="opponent"> <option v-for="p in players">{{ p }}</option> </select>
      </div>
    </div>
    <span class="warn" v-if="!display">Select more filters</span>
    <div class="table">
      <table>
        <!-- <col width="50px" /> -->
        <col width="60px" />
        <col width="36px" />
        <col width="200px" />
        <col width="80px" />
        <col width="200px" />
        <thead>
          <tr>
            <!-- <th>No.</th> -->
            <th class="center">Tour.</th>
            <th class="center">R.</th>
            <th>White</th>
            <th class="center">Result</th>
            <th>Black</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(m,i) in matches">
            <!-- <td class="center">{{ i+1 }}.</td> -->
            <td class="center link" @click="setRound(m.tournament, 'All')">{{ m.tournament }}</td>
            <td class="center link" @click="setRound(m.tournament, m.round)">{{ m.round }}</td>
            <td class="link" @click="setPlayer(m.white)">{{ m.white }}</td>
            <td class="center">{{ result(m.result) }}</td>
            <td class="link" @click="setPlayer(m.black)">{{ m.black }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>
</template>

<style scoped>
th {
  text-align: left;
  font-weight: 550;
}
.num {
  text-align: right;
}
.center {
  text-align: center;
}
td.center {
  padding: 0 5px;
}
table {
  margin-top: 10  px;
}
select {
  margin: 5px 10px;
  height: 25px;
  width: 50px;
}
select.name {
  width: 200px;
}
.warn {
  color: orange;
}

@media (max-width: 600px) {
  .title {
    display: none;
  }
}
</style>
