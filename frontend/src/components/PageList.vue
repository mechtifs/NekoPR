<template>
  <el-container v-if="articles.length" direction="vertical">
    <el-row v-for="article in articles" justify="center" :key="article.id">
      <el-card :body-style="{ padding: '0px' }" shadow="hover">
        <router-link :to="'/article/' + article.id">
          <img :src="article.image" class="card-image" />
        </router-link>
        <div class="card-text">
          <div>
            <div class="article-title">
              {{ article.title }}
            </div>
            <div class="article-abstract">
              {{ article.abstract }}
            </div>
          </div>
          <div class="card-button" v-if="logged">
            <el-button
              v-if="logged"
              :type="article.isFaved ? 'primary' : ''"
              :icon="Star"
              circle
              @click="onFav(article)"
            />
          </div>
        </div>
      </el-card>
    </el-row>
  </el-container>
  <h2 v-else>Nothing here!</h2>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { Star } from '@element-plus/icons-vue'
import { API } from '@/request'

const articles: any = ref([])

const logged = ref(false)

onMounted(() => {
  logged.value = localStorage.getItem('token') ? true : false
  let paramString = window.location.href.split('?')[1]
  let query = ''
  if (paramString) {
    let params_arr = paramString.split('&')
    for (let i = 0; i < params_arr.length; i++) {
      let pair = params_arr[i].split('=')
      if (pair[0] == 'q') {
        query = pair[1]
      }
    }
  }
  API.index('/getArticles?q=' + query).then((resp) => {
    articles.value = resp.data
  })
  if (logged.value) {
    API.user('/getFavIds').then((resp) => {
      articles.value.forEach((article: any) => {
        if (resp.data.includes(article.id)) {
          article.isFaved = true
        } else {
          article.isFaved = false
        }
      })
    })
  }
})

const onFav = (article: any) => {
  if (article.isFaved) {
    API.user('/delFav', {
      articleId: article.id
    })
  } else {
    API.user('/addFav', {
      articleId: article.id
    })
  }
  article.isFaved = !article.isFaved
}
</script>

<style scoped>
img {
  border-radius: 12px;
}
img:hover {
  cursor: pointer;
}
.card-image {
  width: 100%;
  height: 25vh;
  object-fit: cover;
}
.el-card {
  width: 100%;
  margin-bottom: 20px;
  text-align: left;
  transition: 0.5s ease;
}
.card-text {
  padding: 20px;
  padding-top: 10px;
  display: flex;
  align-content: center;
  justify-content: space-between;
}
.card-button {
  display: flex;
  align-items: flex-end;
}
.article-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 5px;
}
</style>
