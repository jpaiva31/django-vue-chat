import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)

app.mount('#app')

// REMOVA TUDO AQUI DE BAIXO.
// ESPECIALMENTE qualquer coisa de Vue 2.
