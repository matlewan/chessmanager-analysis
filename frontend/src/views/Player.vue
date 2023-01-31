<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'

const store = useStore()
let name = ref(useRoute().query.name)
const router = useRouter()

const players = store.state.data.players
const names = Object.keys(players).sort()
const player = computed(() => players[name.value])
const allDuels = store.state.data.duels
const duels = computed(() => allDuels
  .filter(d => d.player == name.value)
  .filter(d => d.opponent != "No Opponent")
  .map(d => ({ ...d, rating: players[d.opponent].pomysl_rating }))
  .sort((a,b) => b.rating - a.rating)
)
const W = computed(() => players[name.value].W + players[name.value].D/2)
const L = computed(() => players[name.value].L + players[name.value].D/2)
</script>

<template>
  <main>
    <div>
      <div class="row">
        <label>Player:</label>
        <select v-model="name">
          <option v-for="n in names">{{ n }}</option>
        </select>
      </div>
      <table class="info" v-if="name">
        <tr>
          <th>BYear</th>
          <th>FIDE</th>
          <th>Rating</th>
          <th>Score</th>
          <th>M</th>
          <th>Result</th>
        </tr>
        <tr>
          <td>{{ player.birthdate }}</td>
          <td>{{ player.rating }}</td>
          <td>{{ Math.round(player.pomysl_rating) }}</td>
          <td>{{ player.score.toFixed(2) }}</td>
          <td>{{ player.M }}</td>
          <td>{{ W }} - {{ player.L }}</td>
        </tr>
      </table>
    </div>
    <div class="table">
      <table>
        <col width="200px" />
        <col width="70px" />
        <col width="100px" />
        <thead>
          <tr>
            <th>Opponent</th>
            <th class="center">Rating</th>
            <th class="center">Result</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in duels">
            <td @click="name=d.opponent" class="link">{{ d.opponent }}</td>
            <td class="center">{{ Math.round(d.rating) }}</td>
            <td class="link center" @click="router.push('/matches?player=' + name + '&opponent=' + d.opponent)">{{ d.W }} - {{ d.L }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>
</template>

<style scoped>
table {
  table-layout: fixed;
}
th {
  text-align: left;
  font-weight: 550;
}
.info th, .info td {
  padding-right: 20px !important;
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
  height: 25px;
  width: 200px;
}
label {
  margin-right: 10px;
}
.row {
  margin: 5px 0;
  display: flex;
}

@media (max-width: 600px) {
  .title {
    display: none;
  }
}
</style>
