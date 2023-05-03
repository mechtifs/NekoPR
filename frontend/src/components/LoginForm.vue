<template>
  <el-card>
    <el-container id="title-container">
      <div
        class="title"
        id="login-title"
        :style="{ fontSize: isLogin ? '40px' : '20px' }"
        @click="isLogin = !isLogin"
      >
        Login
      </div>
      <div
        class="title"
        id="register-title"
        :style="{ fontSize: isLogin ? '20px' : '40px' }"
        @click="isLogin = !isLogin"
      >
        Register
      </div>
      <div
        id="title-underline"
        :style="{
          left: isLogin ? '10px' : '250px',
          right: isLogin ? '300px' : '10px'
        }"
      />
    </el-container>
    <el-form :label-position="'right'" label-width="80px">
      <el-form-item label="Username">
        <el-input v-model="form.username" />
      </el-form-item>
      <el-form-item label="Password">
        <el-input v-model="form.password" type="password" show-password />
      </el-form-item>
      <el-form-item
        label="Confirm"
        id="confirm"
        :style="
          isLogin
            ? {
                height: '0',
                opacity: '0',
                visibility: 'hidden',
                marginBottom: '0'
              }
            : {
                height: '32px',
                opacity: '1',
                visibility: 'visible',
                marginBottom: '18px'
              }
        "
      >
        <el-input v-model="form.confirm" type="password" show-password />
      </el-form-item>
      <el-form-item label="Captcha">
        <el-col :span="14">
          <el-input v-model="form.captcha" />
        </el-col>
        <el-col class="captcha-wrapper" :span="8" :offset="2">
          <img
            class="captcha"
            @click="getCaptcha()"
            :src="'data:image/png;base64,' + captcha"
            alt="captcha"
          />
        </el-col>
      </el-form-item>
      <div class="btn">
        <el-button type="primary" round @click="isLogin ? login() : register()">
          {{ isLogin ? 'Login' : 'Register' }}
        </el-button>
      </div>
    </el-form>
  </el-card>
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted } from 'vue'
import { API } from '@/request'
import router from '@/router'

const isLogin = ref(true)
const form = reactive({
  username: '',
  password: '',
  confirm: '',
  captcha: ''
})
const captcha = ref('')

const login = () => {
  API.user('/login', form).then((resp) => {
    if (resp.status === 0) {
      localStorage.setItem('token', resp.data)
      router.push('/profile')
    }
  })
}

const register = () => {
  let formData = new FormData()
  formData.append('username', form.username)
  formData.append('password', form.password)
  formData.append('captcha', form.captcha)

  API.user('/register', form).then((resp) => {
    if (resp.status === 0) {
      localStorage.setItem('token', resp.data)
      router.push('/profile')
    }
  })
}

const getCaptcha = () => {
  API.user('/genCaptcha').then((resp) => {
    console.log(resp)
    captcha.value = resp.data
  })
}

onMounted(() => {
  getCaptcha()
})
</script>

<style scoped>
.btn {
  padding-top: 20px;
  display: flex;
  justify-content: flex-end;
}
h1 {
  font-size: 30px;
  font-weight: bold;
  margin-bottom: 20px;
}
.el-card {
  width: 400px;
  border-radius: 12px;
}
.el-form-item {
  transition: 0.2s ease;
}
#title-container {
  display: flex;
  height: 80px;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 40px;
}
.title {
  font-weight: 600;
  transition: 0.2s ease;
  user-select: none;
  padding-left: 10px;
  padding-right: 10px;
}
.title:hover {
  cursor: pointer;
  transform: scale(1.1);
}
#confirm {
  transition: 0.2s ease;
}
#title-underline {
  position: absolute;
  bottom: 0;
  height: 6px;
  background-color: #409eff;
  transition: 0.4s ease;
  border-radius: 12px;
}
.captcha {
  height: 100%;
  cursor: pointer;
  border-radius: 2px;
}
.captcha-wrapper {
  height: 32px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
