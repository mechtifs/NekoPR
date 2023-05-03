<template>
  <el-card class="carousel-container" :body-style="{ padding: '0px' }" shadow="hover">
    <el-carousel height="10vw" indicator-position="none" :interval="2000">
      <el-carousel-item v-for="item in banners" :key="item.id">
        <img :src="item.img" />
      </el-carousel-item>
    </el-carousel>
  </el-card>
  <el-card v-for="ad in ads" shadow="never" :key="ad.id">
    <template #header>
      <span>{{ ad.title }}</span>
    </template>
    <p>{{ ad.desc }}</p>
  </el-card>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const ads = ref([
  {
    id: 0,
    title: 'NekoPR',
    desc: 'http://neko.swjtunsa.com'
  },
  {
    id: 1,
    title: 'SWJTU NSA',
    desc: 'http://swjtunsa.com'
  }
])

const banners = ref([
  {
    id: 0,
    img: '/src/assets/img/nsa.png',
    url: 'swjtunsa.com'
  },
  {
    id: 1,
    img: '/src/assets/img/ctf.png',
    url: 'swjtunsa.com'
  },
  {
    id: 2,
    img: '/src/assets/img/nsa-welcome.png',
    url: 'swjtunsa.com'
  }
])
</script>

<style scoped>
.el-carousel__item {
  display: flex;
  justify-content: center;
  align-items: center;
  object-fit: cover;
}
img {
  width: 100%;
  height: auto;
}
span {
  font-weight: bold;
}
.el-card {
  margin-top: 0px;
  margin-bottom: 10px;
}
</style>
