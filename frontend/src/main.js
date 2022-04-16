import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import store from './store'
import Axios from 'axios';

Vue.config.productionTip = false

Axios.defaults.baseURL = "http://localhost:8000/api/"

new Vue({
  vuetify,
  router,
  store,
  render: h => h(App)
}).$mount('#app')
