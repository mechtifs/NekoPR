<template>
  <el-affix>
    <el-menu id="nav-bar" mode="horizontal" :ellipsis="false">
      <router-link to="/">
        <el-container>
          <div class="logo img">
            <img src="@/assets/logo.png" width="35" height="35" />
          </div>
          <div class="title">NekoPR</div>
        </el-container>
      </router-link>
      <div class="flex-grow" />
      <el-input
        v-model="input"
        class="search-bar"
        placeholder="Search..."
        :prefix-icon="Search"
        @keyup.enter="onSearch"
      />
      <router-link to="/profile">
        <div class="avatar img">
          <!-- <el-avatar
            src="https://avatars.githubusercontent.com/u/18751876?v=4"
          /> -->
          <User class="user-icon" />
        </div>
      </router-link>
    </el-menu>
  </el-affix>
</template>

<script lang="ts" setup>
import { Search } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { User } from '@element-plus/icons-vue'

const input = ref('')

const onSearch = () => {
  window.location.href = '/search?q=' + input.value
}
</script>

<style scoped>
.logo {
  padding-top: 6px;
}
.search-bar {
  margin-right: 4vw;
  width: 200px;
}
.el-menu {
  padding-left: 8vw;
  padding-right: 8vw;
  align-items: center;
}
.flex-grow {
  flex-grow: 1;
}
.title {
  display: flex;
  font-size: 20px;
  font-weight: bold;
  padding: 0 20px;
  align-items: center;
}
.logo {
  margin-left: 10px;
  margin-right: 10px;
}
.el-avatar {
  height: 40px;
  width: 40px;
  border: 2px;
  border: solid 2px #eee;
}
#nav-bar {
  height: 60px;
}
.user-icon {
  width: 36px;
  height: 36px;
  margin-top: 10px;
  margin-left: 10px;
  border: solid 2px #eee;
  color: #777;
  border-radius: 20px;
}
</style>
