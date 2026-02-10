import { createApp } from "vue";
import App from "./App.vue";
import PrimeVue from "primevue/config";
import Nora from "@primeuix/themes/Nora";
import "primeicons/primeicons.css";
import router from "./router"; // ✅ import your router

const app = createApp(App);

app.use(router); // ✅ register router
app.use(PrimeVue, {
  theme: {
    preset: Nora,
  },
});

app.mount("#app");
