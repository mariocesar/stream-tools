import Vue from "vue";
import App from "./App.vue";
import store from "./store";
import VueNativeSock from 'vue-native-websocket';
import "./assets/tailwind.min.css";

Vue.config.productionTip = false;

Vue.use(VueNativeSock, 'ws://localhost:3000/ws/', {
    store,
    format: "json",
    reconnection: true,
    reconnectionAttempts: 30,
    reconnectionDelay: 3000,
})

new Vue({
    store,
    render: h => h(App)
}).$mount("#app");
