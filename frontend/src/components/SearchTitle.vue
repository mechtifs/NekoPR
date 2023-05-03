<template>
  <h1 :style="{ fontSize: titleSize + 'vw' }">Search results</h1>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
const titleSize = ref(6)

onMounted(() => {
  window.addEventListener('scroll', () => {
    const scrollPosition = window.scrollY
    if (scrollPosition < 50) {
      titleSize.value = 6 - scrollPosition / 20
    }
  })
})
</script>
