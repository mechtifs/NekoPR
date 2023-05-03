<template>
  <h1 :style="{ fontSize: favSize + 'vw' }">Admin</h1>
  <el-tabs type="card" class="demo-tabs" v-model="activeName">
    <el-tab-pane label="Articles" name="first">
      <article-mgr />
    </el-tab-pane>
    <el-tab-pane label="Users" name="second">
      <user-mgr />
    </el-tab-pane>
  </el-tabs>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'

const favSize = ref(6)
const activeName = ref('first')

onMounted(() => {
  window.addEventListener('scroll', () => {
    const scrollPosition = window.scrollY
    if (scrollPosition < 50) {
      favSize.value = 6 - scrollPosition / 20
    }
  })
})
</script>

<style scoped>
h1 {
  font-weight: bold;
  margin-top: 20px;
  margin-bottom: 10px;
}
</style>
