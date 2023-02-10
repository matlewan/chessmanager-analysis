<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const showScore = ref(false)
const toEdition = (t => parseInt(t.split('.')[0].replace('#','')))
const tournaments = Object.keys(store.state.data.tournaments)
const editions = ref([...new Set(tournaments.map(toEdition))].reverse())
const edition = ref(editions.value.slice(-1)[0])
const subEditions = computed(() => tournaments.filter(s => s.startsWith(`#${edition.value}.`)).length)
const sortBy = ref(-1)

const allPlayers = computed(() => {
  let players = {}
  for (let i = 1; i <= 5; i++) {
    let tournament = `#${edition.value}.${i}`
    let results = store.state.data.results[tournament] || [];
    for (let r of results) {
      let dp = store.state.data.players[r.player]
      const M = Number.MAX_VALUE;
      let p = players[r.player] = (players[r.player] || {pts: [0,0,0,0,0], name: dp['name'], title: dp['title'], place: [M,M,M,M,M]})
      p.pts[i-1] = pts(r.place, r.points)
      p.place[i-1] = r.place
    }
  }
  const col = sortBy.value
  const compare = (col < 0) ? cmp : ((a,b) => a.place[col] - b.place[col])
  return Object.keys(players).map(k => players[k]).sort(compare)
})

function cmp(p1, p2) {
  let arr = [points(p1)-points(p2), sum(p1)-sum(p2), best(p1)-best(p2)]
  return (arr < [0,0,0]) ? 1 : -1;
}

function pts(place, score) {
  return showScore.value ? score : score + (place>=16 ? 4 : [0,10,9,9,8,8,8,7,7,7,6,6,6,5,5,5][place])
}
function points(player) {
  return sum(player) - Math.min(...player.pts.slice(0, subEditions.value))
}
function sum(player) {
  return player.pts.reduce((a,b) => a+b)
}
function best(player) {
  return Math.max(...player.pts)
}

</script>

<template>
  <main>
    <div class="row">
      <div>
        <label>Edition:</label>
        <select v-model="edition">
          <option v-for="e in editions">{{ e }}</option>
        </select>
      </div>
      <div>
        <input type="checkbox" v-model="showScore" />
        <label>Score</label>
      </div>
    </div>
    <div class="table">
      <table>
        <col width="50px" />
        <col class="title" width="50px" />
        <col width="200px" />
        <col width="36px" />
        <col width="36px" />
        <col width="36px" />
        <col width="36px" />
        <col width="36px" />
        <col width="36px" />
        <col width="36px" />
        <thead>
          <tr>
            <th>No.</th>
            <th class="title"></th>
            <th>Name</th>
            <th @click="sortBy=-1" class="link center">Pts</th>
            <th class="title center">Sum</th>
            <th class="title center">Best</th>
            <th @click="sortBy=0" class="link center">#1</th>
            <th @click="sortBy=1" class="link center">#2</th>
            <th @click="sortBy=2" class="link center">#3</th>
            <th @click="sortBy=3" class="link center">#4</th>
            <th @click="sortBy=4" class="link center">#5</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(p,i) in allPlayers" :id="p.name">
            <td class="center">{{ i+1 }}.</td>
            <td class="title center">{{ p.title }}</td>
            <td class="link" @click="router.push(`/player?name=${p.name}`)">{{ p.name }}</td>
            <td class="center">{{ points(p).toFixed(1) }}</td>
            <td class="title center">{{ sum(p).toFixed(1) }}</td>
            <td class="title center">{{ best(p).toFixed(1) }}</td>
            <td v-for="t in 5" class="link center" 
              @click="router.push(`/matches?edition=${edition}&t=${t}&player=${p.name}`)">
              {{ p.pts[t-1].toFixed(1) }}
            </td>
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
.num {
  text-align: right;
}
.center {
  text-align: center;
}
td.center {
  padding: 0 0;
}
table {
  margin-top: 10  px;
}
select {
  margin: 10px;
  height: 25px;
  width: 50px;
}

@media (max-width: 600px) {
  .title {
    display: none;
  }
}
.row {
  display: flex;
}
label {
  vertical-align: middle;
  margin: auto 0;
}
input[type=checkbox] {
  height: 25px;
  margin: 10px 5px;
  vertical-align: middle;
}
</style>
