<template>
  <div class="hello">
    <p>Huidige temperatuur: {{ currentTemp }} graden</p>
    <p>Gemiddelde temperatuur vandaag: {{ avgToday }} graden</p>
    <p>Gemiddelde temperatuur gisteren: {{ avgyesterday }} graden</p>
  </div>
</template>

<script>
export default {
  name: "CurrentTemp",

  data: function () {
    return {
      currentTemp: 0,
      avgToday: 0,
      avgyesterday: 0,
      data: [],
    };
  },
  methods: {
    getTemp() {
      fetch("http://ronleon.nl:5000/current_temp", {
        method: "GET",
        headers: { token: localStorage.getItem("token")},
      })
        .then((response) => response.text())
        .then((data) => (this.currentTemp = data));
    },
    getData() {
      fetch("http://ronleon.nl:5000/weekly", {
        method: "GET",
        headers: { token: localStorage.getItem("token")},
      })
        .then((response) => response.json())
        .then((data) => (this.data = data))
        .then(() => this.updateAvgTemp());
    },
    updateAvgTemp() {
      var date = new Date();

      let day = date.getDate();
      let month = date.getMonth() + 1;
      if (month < 10) {
        month = "0" + month;
      }

    if (day < 10) {
      day = "0" + day;
    }

      let year = date.getFullYear();

      let today = `${year}-${month}-${day}`;

      Date.prototype.addDays = function (days) {
        var date = new Date(this.valueOf());
        date.setDate(date.getDate() - days);
        return date;
      };

      date = new Date();
      date = date.addDays(1);
      day = date.getDate();
      month = date.getMonth() + 1;
      if (month < 10) {
        month = "0" + month;
      }
      year = date.getFullYear();

      let yesterday = `${year}-${month}-${day}`;

      var counterToday = 0;
      var totalTempToday = 0;
      var counterYesterday = 0;
      var totalTempYesterday = 0;

      this.data.forEach((element) => {
        if (element[2] === today) {
          counterToday++;
          totalTempToday += element[1];
        }
        if (element[2] === yesterday) {
          counterYesterday++;
          totalTempYesterday += element[1];
        }
      });


      this.avgToday = (totalTempToday / counterToday).toFixed(2);
      this.avgyesterday = (totalTempYesterday / counterYesterday).toFixed(2);
    },
  },
  beforeMount() {
    this.getTemp();
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
