<template>
  <el-table :data="articles" style="width: 100%">
    <el-table-column fixed prop="id" label="ID" width="50" />
    <el-table-column prop="title" label="Title" width="200" />
    <el-table-column prop="abstract" label="Abstract" />
    <el-table-column fixed="right" label="Operations" width="220">
      <template #default="scope">
        <el-button round size="small" @click="handleEdit(scope.row.id)">Edit</el-button>
        <el-popconfirm
          title="Are you sure to delete?"
          width="200"
          @confirm="delArticle(scope.$index, scope.row.id)"
        >
          <template #reference>
            <el-button round type="danger" size="small"> Delete </el-button>
          </template>
        </el-popconfirm>
      </template>
    </el-table-column>
  </el-table>
  <el-button
    :icon="Plus"
    size="large"
    class="add-btn"
    type="primary"
    @click="dialogFormVisible = true"
    >Add new</el-button
  >

  <el-dialog v-model="dialogFormVisible" title="Article">
    <el-form :model="form">
      <el-form-item label="Title" :label-width="formLabelWidth">
        <el-input v-model="form.title" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Image" :label-width="formLabelWidth">
        <el-input v-model="form.image" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Content" :label-width="formLabelWidth">
        <el-input
          v-model="form.content"
          type="textarea"
          :autosize="{ minRows: 2, maxRows: 8 }"
          autocomplete="off"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="closeDialog">Cancel</el-button>
        <el-button type="primary" @click="handleSubmit"> Confirm </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { API } from '@/request'
import { ref, reactive, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'

const articles: any = ref([])

const dialogFormVisible = ref(false)
const formLabelWidth = '140px'

const form = reactive({
  articleId: 0,
  title: '',
  image: '',
  content: ''
})

onMounted(() => {
  getArticles()
})

const getArticles = () => {
  API.index('/getArticles').then((resp) => {
    articles.value = resp.data
  })
}

const delArticle = (index: number, id: number) => {
  console.log(id)
  API.admin('/delArticle', {
    articleId: id
  }).then(() => {
    articles.value.splice(index, 1)
  })
}

const handleEdit = (id: number) => {
  form.articleId = id
  API.index('/getArticle', {
    articleId: id
  }).then((resp) => {
    form.title = resp.data.title
    form.image = resp.data.image
    form.content = resp.data.content
  })
  dialogFormVisible.value = true
}

const handleUpdateSubmit = () => {
  API.admin('/updArticle', form).then(() => {
    dialogFormVisible.value = false
    articles.value = articles.value.map((article: any) => {
      if (article.id === form.articleId) {
        article.title = form.title
        article.image = form.image
        article.abstract = form.content.slice(0, 20)
      }
      return article
    })
  })
}

const handleAddSubmit = () => {
  API.admin('/addArticle', form).then(() => {
    dialogFormVisible.value = false
    getArticles()
  })
}

const handleSubmit = () => {
  if (form.articleId) {
    handleUpdateSubmit()
  } else {
    handleAddSubmit()
  }
}

const closeDialog = () => {
  dialogFormVisible.value = false
  form.articleId = 0
  form.title = ''
  form.image = ''
  form.content = ''
}
</script>

<style scoped>
.add-btn {
  margin-top: 20px;
  float: right;
}
.cell {
  font-size: large;
}
</style>
