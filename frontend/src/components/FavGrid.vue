<template>
  <h1 :style="{ fontSize: favSize + 'vw' }">Favorites</h1>
  <el-row>
    <el-col :span="6" v-for="(fav, index) of favs" :key="fav.id">
      <el-card
        :body-style="{ padding: '0px' }"
        shadow="hover"
        @mouseover="fav.showDelBtn = true"
        @mouseout="fav.showDelBtn = false"
      >
        <router-link :to="'/article/' + fav.id">
          <img :src="fav.image" class="card-image" />
          <div class="article-title">
            {{ fav.title }}
          </div>
        </router-link>
        <el-button
          class="del-btn"
          :style="{ opacity: fav.showDelBtn ? 1 : 0 }"
          type="danger"
          :icon="Close"
          circle
          size="small"
          @click="fav.showDialog = true"
        />
      </el-card>
      <el-dialog v-model="fav.showDialog" title="Notice" width="30%">
        <span>Are you sure to delete?</span>
        <template #footer>
          <span class="dialog-footer">
            <el-button round @click="fav.showDialog = false">Cancel</el-button>
            <el-button type="danger" round @click="delFav(index, fav.id)"> Confirm </el-button>
          </span>
        </template>
      </el-dialog>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { Close } from '@element-plus/icons-vue'
import { API } from '@/request'

const favs: any = ref([])
const favSize = ref(6)

onMounted(() => {
  window.addEventListener(
    'scroll',
    () => {
      const scrollPosition = window.scrollY
      if (scrollPosition < 50) {
        favSize.value = 6 - scrollPosition / 20
      }
    },
    true
  )

  API.user('/getFavs').then((resp) => {
    favs.value = resp.data
  })
})

const delFav = (index: number, id: number) => {
  favs.value[index].showDialog = false
  API.user('/delFav', {
    articleId: id
  }).then(() => {
    favs.value.splice(index, 1)
  })
}
</script>

<style scoped>
.del-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  transition: 0.2s;
}
.article-title {
  font-size: 1.2vw;
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 100px;
  line-height: 150px;
  background: linear-gradient(0deg, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 0) 100%);
  color: #fff;
  padding: 0 10px;
  box-sizing: border-box;
}
img {
  width: 100%;
  height: 16vw;
  object-fit: cover;
}
.el-card {
  margin: 0.5vw;
  height: 16vw;
}
h1 {
  font-weight: bold;
  margin-top: 20px;
  margin-bottom: 10px;
}
.el-card:hover {
  transition: 0.2s ease;
  transform: scale(1.1);
}
</style>
