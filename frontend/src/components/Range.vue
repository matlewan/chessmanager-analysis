<script setup>
import { ref } from 'vue';

const props = defineProps({ 
    modelValue: { type: Object, required: true }
})

const emit = defineEmits(['update:modelValue'])
let min = ref(props.modelValue.min)
let max = ref(props.modelValue.max)

function handleInput (e) {
    let obj = { min: parseFloat(min.value), max: parseFloat(max.value) }
    emit('update:modelValue', obj)
}

</script>

<template>
    <div class="range">
        <input type="number" v-model="min" @focusout="handleInput" />
        <label> - </label>
        <input type="number" v-model="max" @focusout="handleInput" />
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
