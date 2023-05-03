<script lang="ts" setup></script>

<template>
  <el-container>
    <el-col :span="5" :offset="3">
      <el-affix :offset="100">
        <user-info />
      </el-affix>
    </el-col>
    <el-col class="fav-grid" :span="11" :offset="1">
      <fav-grid />
    </el-col>
  </el-container>
</template>

<style scoped>
.fav-grid {
  height: 100vh;
}
</style>
