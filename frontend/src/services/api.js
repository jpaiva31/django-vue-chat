import axios from 'axios'
import router from '../router' // se quiser redirecionar pro login após erro

const api = axios.create({
  baseURL: 'http://localhost:8000',
})

export default api
