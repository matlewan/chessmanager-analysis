<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import Filters from '@/components/Filters.vue'

const router = useRouter()
const store = useStore()
const ASC = -1, DESC = 1
let sortMode = ref(DESC)
let sortBy = ref("score")
let allPlayers = ref([])
let filters = ref({})
let players = computed(() => {
  let f = filters.value
  let cmp = (a,b) => (a[sortBy.value] < b[sortBy.value] ? sortMode.value : -sortMode.value)
  if (f.name === undefined) {
    return allPlayers.value.sort(cmp);
  }
  const MAX = 999999999999
  return allPlayers.value
    .filter(p => p.name.toLowerCase().includes((f.name || "").toLowerCase()))
    .filter(p => p.birthdate >= (f.birthdate.min || 0) && p.birthdate <= (f.birthdate.max || MAX))
    .filter(p => p.M >= (f.M.min || 0) && p.M <= (f.M.max || MAX))
    .filter(p => p.score >= (f.score.min || 0) && p.score <= (f.score.max || MAX))
    .filter(p => p.rating >= (f.fide.min || 0) && p.rating <= (f.fide.max || MAX))
    .filter(p => p.pomysl_rating >= (f.rating.min || 0) && p.pomysl_rating <= (f.rating.max || MAX))
    .sort(cmp)
})
onMounted(() => update())
watch(() => store.state.data, () => update())
function update() {
  let list = store.state.data['players'] || [];
  list = Object.keys(list).map(k => list[k])
  list.sort((a,b) => b.pomysl_rating - a.pomysl_rating)
  allPlayers.value = list
}

function sort(field) {
  if (field === sortBy.value) {
    sortMode.value = -sortMode.value
  }
  else {
    sortBy.value = field;
    sortMode.value = DESC
  }
}

function refresh(newFilters) {
  filters.value = newFilters;
}
</script>

<template>
  <main>
    <div class="table">
      <table>
        <colgroup>
          <col width="50px" />
          <col class="title" width="50px" />
          <col width="200px" />
          <col width="50px" />
          <col width="36px" />
          <col width="36px" />
          <col width="36px" />
          <col width="36px" />
          <col width="100px" />
        </colgroup>
        <thead>
          <tr>
            <th>No.</th>
            <th class="title"></th>
            <th @click="sort('name')" class="link">Name</th>
            <th @click="sort('birthdate')" class="link center">BYear</th>
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
            <td class="link" @click="router.push('/player?name=' + p.name)">{{ p.name }}</td>
            <td class="center">{{ p.birthdate }}</td>
            <td class="center">{{ p.rating }}</td>
            <td class="center">{{ Math.round(p.pomysl_rating) }}</td>
            <td class="center">{{ p.score.toFixed(2) }}</td>
            <td class="center">{{ p.M }}</td>
            <td class="title center">{{ p.W }}-{{ p.D }}-{{ p.L }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <Filters @change="refresh" />
  </main>
</template>

<style scoped>
table {
  table-layout: fixed;
}
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
  margin-top: 10  px;
}
@media (max-width: 650px) {
  .title {
    display: none;
  }
}
</style>
