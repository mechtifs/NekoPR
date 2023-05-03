<template>
  <el-container>
    <el-col :span="4" :offset="2">
      <el-affix :offset="100">
        <left-side-panel />
      </el-affix>
    </el-col>
    <el-col :span="10" :offset="1">
      <page-list class="list-view" />
    </el-col>
    <el-col :span="4" :offset="1">
      <el-affix :offset="100">
        <right-side-panel />
      </el-affix>
    </el-col>
  </el-container>
</template>

<style scoped>
.list-view {
  margin-top: 40px;
}
</style>
