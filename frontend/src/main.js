import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import 'animate.css'
import '@/assets/css/style.css'
import '@/assets/css/loaders.css'




import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from "@/router"

import App from './App.vue'

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

app.mount("#app");