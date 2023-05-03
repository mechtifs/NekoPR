<template>
  <div class="header-image">
    <img :style="{ opacity: imgOpacity }" :src="article.image" />
  </div>
  <el-container>
    <el-col :span="12" :offset="6">
      <div class="article-title">
        <h1 :style="{ fontSize: titleSize + 'vw' }">{{ article.title }}</h1>
      </div>
      <div class="article-body">
        {{ article.content }}
      </div>
    </el-col>
  </el-container>
  <el-button
    v-if="logged"
    class="fav-button"
    :type="article.isFaved ? 'primary' : ''"
    :icon="Star"
    circle
    @click="onFav()"
  />
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { Star } from '@element-plus/icons-vue'
import { API } from '@/request'
import router from '@/router'

const articleId = router.currentRoute.value.params.id
const logged = ref(false)
const article: any = ref({})
const titleSize = ref(6)
const imgOpacity = ref(1)

const onFav = () => {
  if (article.value.isFaved) {
    API.user('/delFav', { articleId: articleId })
  } else {
    API.user('/addFav', { articleId: articleId })
  }
  article.value.isFaved = !article.value.isFaved
}

onMounted(() => {
  logged.value = localStorage.getItem('token') ? true : false
  window.addEventListener(
    'scroll',
    () => {
      const scrollPosition = window.scrollY
      if (scrollPosition < 100) {
        titleSize.value = 6 - scrollPosition / 40
      } else {
        imgOpacity.value = 1 - (scrollPosition - 100) / 400
      }
    },
    true
  )

  API.index('/getArticle', {
    articleId: articleId
  })
    .then((resp) => {
      article.value = resp.data
    })
    .catch((err) => {
      console.log(err)
    })

  if (logged.value) {
    API.user('/chkFav', {
      articleId: articleId
    })
      .then((resp) => {
        article.value.isFaved = resp.data
      })
      .catch((err) => {
        console.log(err)
      })
  }
})
</script>

<style scoped>
img {
  top: -60px;
  width: 100%;
  height: 60vh;
  object-fit: cover;
  z-index: -1;
}
h1 {
  font-size: 2em;
  font-weight: bold;
}
.article-title {
  margin-top: 30px;
  margin-bottom: 20px;
}
.article-body {
  margin-bottom: 20px;
  font-size: large;
  text-align: justify;
  white-space: pre-wrap;
}
.el-button {
  width: 60px;
  height: 60px;
  position: fixed;
  right: 0;
  bottom: 0;
  margin: 60px;
  font-size: 30px;
}
</style>
