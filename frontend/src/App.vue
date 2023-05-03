<template>
  <el-container>
    <el-header>
      <nav-bar />
    </el-header>
    <el-main>
      <router-view v-slot="{ Component, route }">
        <component :is="Component" :key="route.path" />
      </router-view>
    </el-main>
  </el-container>
</template>

<style>
.el-main {
  padding: 0;
  justify-content: center;
}
.el-header {
  padding: 0;
  height: 60px;
}
</style>
