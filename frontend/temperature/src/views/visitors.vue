<template>
  <div class="container">
    <h1>This website has {{ visitors }} clicks</h1>
  </div>
</template>
  
  <script>
import data from "../data.json";

export default {
  name: "ExtraPage",

  components: {},

  data: function () {
    return {
      visitors: 0,
      url: data["url"],
    };
  },

  methods: {
    increaseVisitors() {
      //post to api
      fetch(this.url + "/visitors", {
        method: "POST",
      })
        .then((response) => response.json())
        .then((data) => (this.visitors = data["visitors"]));
    },
  },

  mounted() {
    this.increaseVisitors();
  },
};
</script>
  

  <style scoped>
</style>
  