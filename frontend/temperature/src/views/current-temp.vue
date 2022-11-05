<template>
  <div class="hello">
    <p>Huidige temperatuur: {{ currentTemp }} graden</p>
    <p>Gemiddelde temperatuur vandaag: {{ avgToday }} graden</p>
    <p>Gemiddelde temperatuur gisteren: {{ avgyesterday }} graden</p>
  </div>
</template>

<script>

import datajson from "../data.json";

export default {

  name: "CurrentTemp",

  data: function () {
    return {
      currentTemp: 0,
      avgToday: 0,
      avgyesterday: 0,
      data: [],
      url: datajson['url'],
    };
  },
  methods: {

    getData() {
      fetch(this.url + "/extra", {
        method: "GET",
        headers: { token: localStorage.getItem("token")},
      })
        .then((response) => response.json())
        .then((data) => (this.data = data))
        .then(() => {
          this.currentTemp = this.data['current_temp'];
          this.avgToday = this.data['daily_average'];
          this.avgyesterday = this.data['average_yesterday'];
          console.log(this.data);
        });
    },
  },
  beforeMount() {
    this.getData();
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
