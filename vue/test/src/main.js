import './assets/main.css'

import { createApp } from 'vue'

// import componente principale di App
import App from './App.vue'

// createApp(App) crea istanza dell'app
// .mount('#app') dice di inserire il
// contenuto all'interno dell'elemento che ha
// id #app
createApp(App).mount('#app')
