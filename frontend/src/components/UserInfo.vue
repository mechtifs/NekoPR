<template>
  <el-container direction="vertical" class="user-info">
    <el-container direction="vertical">
      <!-- <el-avatar :src="userInfo.avatar" /> -->
      <User class="user-icon" />
      <div class="user-nickname">{{ userInfo.nickname }}</div>
      <div class="user-username">{{ '@' + userInfo.username }}</div>
      <div class="user-description">{{ userInfo.description }}</div>
      <div class="user-email">{{ userInfo.email }}</div>
    </el-container>
    <el-button
      :icon="Operation"
      class="admin-button"
      v-if="displayAdminEntry"
      type="primary"
      round
      @click="router.push('/admin')"
      >Admin page</el-button
    >
    <el-button :icon="Edit" class="pwd-button" round @click="pwdFormVisible = true"
      >Change password</el-button
    >
    <el-container class="btns">
      <el-button round class="change-info-button" @click="infoFormVisible = true">
        Change Info
      </el-button>
      <el-popconfirm title="Are you sure to log out?" width="200" @confirm="logout()">
        <template #reference>
          <el-button round class="log-out-button" type="danger"> Log Out </el-button>
        </template>
      </el-popconfirm>
    </el-container>
  </el-container>

  <el-dialog v-model="infoFormVisible" title="Change information">
    <el-form :model="infoForm">
      <el-form-item label="Nick name" label-width="150px">
        <el-input v-model="infoForm.nickname" autocomplete="off" />
      </el-form-item>
      <el-form-item label="E-mail address" label-width="150px">
        <el-input v-model="infoForm.email" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Description" label-width="150px">
        <el-input v-model="infoForm.description" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button round @click="infoFormVisible = false">Cancel</el-button>
        <el-button type="primary" round @click="changeInfo()"> Confirm </el-button>
      </span>
    </template>
  </el-dialog>

  <el-dialog v-model="pwdFormVisible" title="Change information">
    <el-form :model="pwdForm">
      <el-form-item label="Old password" label-width="150px">
        <el-input v-model="pwdForm.oldPassword" type="password" show-password autocomplete="off" />
      </el-form-item>
      <el-form-item label="New password" label-width="150px">
        <el-input v-model="pwdForm.newPassword" type="password" show-password autocomplete="off" />
      </el-form-item>
      <el-form-item label="Confirm" label-width="150px">
        <el-input v-model="pwdForm.confirm" type="password" show-password autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button round @click="pwdFormVisible = false">Cancel</el-button>
        <el-button type="primary" round @click="changePwd()"> Confirm </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { API } from '@/request'
import { Edit, Operation, User } from '@element-plus/icons-vue'
import router from '@/router'

const userInfo: any = ref({})
const infoFormVisible = ref(false)
const pwdFormVisible = ref(false)
const displayAdminEntry = ref(false)
const infoForm = ref({
  nickname: '',
  email: '',
  description: ''
})

const pwdForm = ref({
  oldPassword: '',
  newPassword: '',
  confirm: ''
})

onMounted(() => {
  API.user('/getInfo')
    .then((resp) => {
      userInfo.value = resp.data
      console.log(userInfo.value.role)
      infoForm.value.nickname = userInfo.value.nickname
      infoForm.value.email = userInfo.value.email
      infoForm.value.description = userInfo.value.description
      if (userInfo.value.role === 1) {
        displayAdminEntry.value = true
      }
    })
    .catch((err) => {
      console.log(err)
      router.push('/login')
    })
})

const changeInfo = () => {
  if (
    infoForm.value.nickname == '' ||
    infoForm.value.email == '' ||
    infoForm.value.description == ''
  ) {
    ElMessage.error('Input cannot be empty!')
    return
  } else {
    infoFormVisible.value = false
    ElMessage.success('Success!')
    API.user('/updInfo', infoForm.value).then((resp) => {
      if (resp.status === 0) {
        userInfo.value.nickname = infoForm.value.nickname
        userInfo.value.email = infoForm.value.email
        userInfo.value.description = infoForm.value.description
      }
    })
  }
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

const changePwd = () => {
  if (
    pwdForm.value.oldPassword == '' ||
    pwdForm.value.newPassword == '' ||
    pwdForm.value.confirm == ''
  ) {
    ElMessage.error('Input cannot be empty!')
    return
  }
  if (pwdForm.value.newPassword !== pwdForm.value.confirm) {
    ElMessage.error('Password does not match!')
    return
  }
  API.user('/updPwd', pwdForm.value).then((resp) => {
    if (resp.status === 0) {
      pwdFormVisible.value = false
    }
  })
}
</script>

<style scoped>
.user-info {
  height: 500px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.btns {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
.user-nickname {
  font-size: 30px;
  font-weight: bold;
  margin-top: 10px;
}
.user-username {
  color: #bbb;
}
.el-avatar {
  margin: 0 auto;
  display: block;
  height: 200px;
  width: 200px;
}
/* hover avatar to display edit */
.el-avatar {
  border: solid 4px #eee;
}
.el-avatar:hover {
  cursor: pointer;
}
.user-icon {
  border: solid 4px #eee;
  margin: 0 auto;
  display: block;
  height: 200px;
  width: 200px;
  border-radius: 200px;
  color: #aaa;
}
.admin-button,
.pwd-button {
  margin-top: 20px;
  width: 200px;
  margin-left: 0;
}
</style>
