<template>
  <div class="hello">
    <p>Huidige temperatuur: {{ currentTemp }} graden</p>
  </div>
</template>

<script>
export default {
  name: "CurrentTemp",

  data: function () {
    return {
      currentTemp: 0,
    };
  },
  methods: {
    getTemp() {
      fetch("http://ronleon.nl:5000/current_temp", {
        method: "GET",
        headers: { kaas: "yoyokaas" },
      })
        .then((response) => response.text())
        .then((data) => (this.currentTemp = data));
    },
  },
  beforeMount() {
    this.getTemp()
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
