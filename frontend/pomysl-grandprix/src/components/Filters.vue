<script setup>
import { ref, watch } from 'vue'
import Range from '@/components/Range.vue'

const emit = defineEmits(['change'])

let name = ref("")
let birthdate = ref({min:undefined, max:undefined})
let score = ref({min:undefined, max:undefined})
let fide = ref({min:undefined, max:undefined})
let rating = ref({min:undefined, max:undefined})
let M = ref({min:undefined, max:undefined})

watch([name,score,rating,M,fide,birthdate], () => {
  const filters = {
    "name": name,
    "birthdate": birthdate,
    "score": score,
    "fide": fide,
    "rating": rating,
    "M": M
  }
  emit('change', filters)
})
</script>

<template>
  <div class="filters">
    <label for="name">Name:</label> <input v-model="name" id="name" />
    <label for="birthdate">BYear:</label> <Range v-model="birthdate" id="birthdate" />
    <label for="score">Score:</label> <Range v-model="score" id="score" />
    <label for="fide">FIDE:</label> <Range v-model="fide" id="fide" />
    <label for="rating">Rating:</label> <Range v-model="rating" id="rating" />
    <label for="M">M:</label> <Range v-model="M" id="M" />
  </div>
</template>

<style scoped>
.filters {
  padding: 10px;
  width: auto;
  display: grid;
  margin-bottom: auto;
}
label {
  grid-column-start: 1;
  margin-right: 5px;
  text-align: right;
  margin-bottom: 5px;
}
input {
  height: 25px;
  grid-column-start: 2;
  margin-bottom: 5px;
  width: 300px;
}
</style>
