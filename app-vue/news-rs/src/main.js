import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import VueNeo4j from "vue-neo4j";
// import { GraphlyD3 } from "@livereader/graphly-d3-vue";
// import "@livereader/graphly-d3-vue/style.css";
// import { ref, onMounted } from "vue";
//import { ForceSimulation } from "@livereader/graphly-d3";
//import "@livereader/graphly-d3/style.css";

//Vue.use(GraphlyD3);
Vue.use(VueNeo4j);

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
