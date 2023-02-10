<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement)

const store = useStore()
const router = useRouter()
const players = store.state.data.players
const tournaments = Object.keys(store.state.data.tournaments).reverse()
const names = Object.keys(players).sort()

const name = ref(useRoute().query.name)
const results = computed(() => tournaments.map(t => result(t, name.value)))
const player = computed(() => players[name.value])
const duels = computed(() => 
    store.state.data.duels
      .filter(d => d.player == name.value)
      .filter(d => d.opponent != "No Opponent")
      .map(d => ({ ...d, rating: players[d.opponent].pomysl_rating }))
      .sort((a,b) => b.rating - a.rating)
)
const W = computed(() => players[name.value].W)
const D = computed(() => players[name.value].D)
const L = computed(() => players[name.value].L)
const chartData = computed(() => {
  return {
    labels: tournaments,
    datasets: [ 
      { label: name.value, data: results.value, borderColor: '#0078ba', backgroundColor: '#0078ba' } ,
    ]
  }
})
const chartOptions = {
  scales: { y: { min: 0, max: 8 } },
  responsive: true,
  maintainAspectRatio: true, 
}
function result(t, name) {
  const r = store.state.data.results[t].find(r => r.player == name)
  return r ? parseFloat(r.points) : undefined
}
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
          <th>W - D - L</th>
        </tr>
        <tr>
          <td>{{ player.birthdate }}</td>
          <td>{{ player.rating }}</td>
          <td>{{ Math.round(player.pomysl_rating) }}</td>
          <td>{{ player.score.toFixed(2) }}</td>
          <td>{{ player.M }}</td>
          <td>{{ W }} - {{ D }} - {{ L }}</td>
        </tr>
      </table>
    </div>
    <Line type="line" :width="100" :data="chartData" :options="chartOptions" />
    <div class="table">
      <table>
        <col width="200px" />
        <col width="70px" />
        <col width="100px" />
        <thead>
          <tr>
            <th>Opponent</th>
            <th class="center">Rating</th>
            <th class="center">W-D-L</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in duels">
            <td @click="name=d.opponent" class="link">{{ d.opponent }}</td>
            <td class="center">{{ Math.round(d.rating) }}</td>
            <td class="link center" @click="router.push(`/matches?player=${name}&opponent=${d.opponent}`)">{{ d.W }}-{{ d.D }}-{{ d.L }}</td>
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
canvas {
  width: 100%;
  max-width: 800px;
  max-height: 400px;
}
</style>
