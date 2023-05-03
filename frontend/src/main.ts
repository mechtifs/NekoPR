import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import './assets/main.css'
import 'element-plus/theme-chalk/el-message.css'

const app = createApp(App)

app.use(router)

app.mount('#app')

router.afterEach(() => {
  window.scrollTo(0, 0)
})
