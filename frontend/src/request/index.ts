import axios from 'axios'
import router from '../router'
import { ElMessage } from 'element-plus'

const requests = axios.create({
  baseURL: '/api',
  timeout: 60000,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
})

requests.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers!.Authorization = 'Bearer ' + token
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

requests.interceptors.response.use(
  (resp) => {
    if (resp.data.msg != '' && resp.data.msg != undefined) {
      ElMessage({
        type: resp.data.status ? 'error' : 'success',
        message: resp.data.msg
      })
    }
    console.log(resp.data)
    return resp.data
  },
  (error) => {
    if (error.response.status === 401 || error.response.status === 422) {
      localStorage.removeItem('token')
      router.push('/login')
    }
    return Promise.reject(error.response.data)
  }
)

export const API = {
  index: (url: string, data: any = undefined) => {
    return requests.post(url, data)
  },
  user: (url: string, data: any = undefined) => {
    return requests.post('/user' + url, data)
  },
  admin: (url: string, data: any = undefined) => {
    return requests.post('/admin' + url, data)
  }
}
