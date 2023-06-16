import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import VueAxios from 'vue-axios'
import '@mdi/font/css/materialdesignicons.css'


// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'


const vuetify = createVuetify({
    components,
    directives,
    theme: {
        defaultTheme: 'dark'
    }
})

axios.defaults.baseURL = process.env.VUE_APP_AXIOS_URL;


const app = createApp(App);

app.use(store);
app.use(router);
app.use(VueAxios, axios);
app.use(vuetify)

app.mount('#app')