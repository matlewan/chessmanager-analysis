<script setup>
import { computed, ref, toRaw } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import Filters from '@/components/Filters.vue'

const router = useRouter()
const store = useStore()
const DESC = 1

// Variables
const sortMode = ref(DESC)
const sortBy = ref("score")
const filters = ref({})
const fname = ref("")

// Computed
const allPlayers = computed(() => {
  const list = store.state.data.players
  return Object.keys(list).map(k => list[k])
})
const players = computed(() => {
  const f = toRaw(filters.value)
  const cmp = (a,b) => (a[sortBy.value] < b[sortBy.value] ? sortMode.value : -sortMode.value)
  if (f.score === undefined) {
    return []
  }
  return allPlayers.value
    .filter(p => p.name.toLowerCase().includes(fname.value.toLowerCase()))
    .filter(p => inRange(p.birthdate, f.birthdate))
    .filter(p => inRange(p.M, f.M))
    .filter(p => inRange(p.score, f.score))
    .filter(p => inRange(p.rating, f.rating))
    .filter(p => inRange(p.pomysl_rating, f.pomysl_rating))
    .sort(cmp)
})

// Functions
function sort(field) {
  if (field === sortBy.value) {
    sortMode.value = -sortMode.value
  }
  else {
    sortBy.value = field;
    sortMode.value = DESC
  }
}
function inRange(value, range) {
  return (isNaN(range.min) || value >= range.min) && (isNaN(range.max) || value <= range.max)
}
</script>

<template>
  <main>
    <div class="table">
      <div class="row">
        <label>Name:</label>
        <input v-model="fname" />
      </div>
      <table class="fixed-table">
        <thead>
          <tr>
            <th class="center">#</th>
            <th class="title"></th>
            <th @click="sort('name')" class="link">Name</th>
            <th @click="sort('birthdate')" class="title link center">BYear</th>
            <th @click="sort('rating')" class="link center">FIDE</th>
            <th @click="sort('pomysl_rating')" class="link center">Rating</th>
            <th @click="sort('score')" class="link center">Score</th>
            <th @click="sort('M')" class="link center">M</th>
            <th class="title center">W-D-L</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(p,i) in players" :id="p.name">
            <td class="center">{{ i+1 }}.</td>
            <td class="title  center">{{ p.title }}</td>
            <td class="link" @click="router.push(`/player?name=${p.name}`)">{{ p.name }}</td>
            <td class="title center">{{ p.birthdate }}</td>
            <td class="center">{{ p.rating }}</td>
            <td class="center">{{ Math.round(p.pomysl_rating) }}</td>
            <td class="center">{{ p.score.toFixed(1) }}%</td>
            <td class="center">{{ p.M }}</td>
            <td class="title center">{{ p.W }}-{{ p.D }}-{{ p.L }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <Filters v-model="filters" />
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-wrap: wrap;
  gap: 40px;
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
  padding: 0 5px;
}
table {
  margin-top: 10px;
}
div.table {
  margin: 0 auto;
}
@media (max-width: 650px) {
  .title {
    display: none;
  }
}
.row {
  display: none;
  margin: 10px 10px 10px 0px;
}
.row input {
  margin-left: 10px;
  width: 250px;
}
</style>
