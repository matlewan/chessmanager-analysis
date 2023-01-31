<script setup>
import { ref, watch } from 'vue';

const props = defineProps({ 
    modelValue: { type: Object, required: true }
})

const emit = defineEmits(['update:modelValue'])
const min = ref(props.modelValue.min)
const max = ref(props.modelValue.max)

watch([min, max], () => {
    let obj = { min: parseFloat(min.value), max: parseFloat(max.value) }
    emit('update:modelValue', obj)
})
</script>

<template>
    <div class="range">
        <input type="number" v-model="min" />
        <label> - </label>
        <input type="number" v-model="max" />
    </div>
</template>

<style scoped>
.range {
    display: flex;
    gap: 5px;
}
.range input {
  height: 25px;
  width: 70px;
}
</style>
