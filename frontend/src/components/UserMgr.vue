<template>
  <el-table :data="users" style="width: 100%">
    <el-table-column fixed prop="id" label="ID" width="50" />
    <el-table-column prop="username" label="Username" />
    <el-table-column prop="nickname" label="Nickname" />
    <el-table-column prop="email" label="Email" />
    <el-table-column prop="description" label="Description" />
    <el-table-column fixed="right" label="Operations" width="220">
      <template #default="scope">
        <el-button round size="small" v-if="!scope.row.role" @click="rstUserPwd(scope.row.id)">Reset password</el-button>
        <el-popconfirm
          title="Are you sure to delete?"
          width="200"
          @confirm="delUser(scope.$index, scope.row.id)"
        >
          <template #reference v-if="!scope.row.role">
            <el-button round type="danger" size="small"> Delete </el-button>
          </template>
        </el-popconfirm>
      </template>
    </el-table-column>
  </el-table>
</template>

<script lang="ts" setup>
import 'element-plus/theme-chalk/el-message-box.css'
import { API } from '@/request'
import { ref, onMounted } from 'vue'
import { ElMessageBox } from 'element-plus'

const users: any = ref([])

onMounted(() => {
  API.admin('/getUsers').then((resp) => {
    users.value = resp.data
  })
})

const delUser = (index: number, id: number) => {
  API.admin('/delUser', {
    userId: id
  }).then(() => {
    users.value.splice(index, 1)
  })
}

const rstUserPwd = (id: number) => {
  API.admin('/rstUserPwd', {
    userId: id
  }).then((resp) => {
    ElMessageBox.alert(resp.data, 'Reset password', {
      confirmButtonText: 'OK'
    })
  })
}
</script>
