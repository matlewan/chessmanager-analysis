<script setup>
import { ref, watch, toRaw, onMounted } from 'vue'
import Range from '@/components/Range.vue'

const props = defineProps({
    modelValue: Object
})
const emit = defineEmits(['update:modelValue'])

const birthdate = ref({min:undefined, max:undefined})
const score = ref({min:undefined, max:undefined})
const rating = ref({min:undefined, max:undefined})
const pomysl_rating = ref({min:undefined, max:undefined})
const M = ref({min:undefined, max:undefined})

onMounted(() => update())
watch([score,pomysl_rating,M,rating,birthdate], () => update())

function update() {
  const filters = {
    birthdate: toRaw(birthdate.value),
    score: toRaw(score.value),
    rating: toRaw(rating.value),
    pomysl_rating: toRaw(pomysl_rating.value),
    M: toRaw(M.value)
  }
  emit('update:modelValue', filters)
}
</script>

<template>
  <div class="filters">
    <div class="row">
      <label for="birthdate">BYear:</label>
      <Range v-model="birthdate" id="birthdate" />
    </div>
    <div class="row">
      <label for="score">Score:</label>
      <Range v-model="score" id="score" />
    </div>
    <div class="row">
      <label for="rating">FIDE:</label>
      <Range v-model="rating" id="rating" />
    </div>
    <div class="row">
      <label for="pomysl_rating">Rating:</label>
      <Range v-model="pomysl_rating" id="pomysl_rating" />
    </div>
    <div class="row">
      <label for="M">M:</label>
      <Range v-model="M" id="M" />
    </div>
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
.row {
  display: none;
}
.row label {
  width: 50px;
}
</style>
