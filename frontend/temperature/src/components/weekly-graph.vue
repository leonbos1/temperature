<template>
  <canvas id="graph"></canvas>
</template>

<script>
import Chart from "chart.js/auto";

export default {
  name: "WeeklyGraph",

  data: function () {
    return {
      data: [],
    };
  },

  props: {
    msg: String,
  },

  mounted() {
      this.getData()
  },

  methods: {
    getData() {
      fetch("http://ronleon.nl:5000/weekly", {
        method: "GET",
        headers: { kaas: "yoyokaas" },
      })
        .then((response) => response.json())
        .then((data) => data.replace(/'/g, '"'))
        .then((data) => JSON.parse(data))
        .then((data) => (this.data = data))
        .then(() => this.setTemps())
        .then(() => this.setLabels())
        .then(() => (this.createGraph()))
    },

    setTemps() {
      let temps = [];

      console.log(this.data[0])

      this.data.forEach((element) => {
        temps.push(element[1]);
      });
      this.temps = temps
    },

    setLabels() {
      let labels = [];

      this.data.forEach((element) => {
        let datetime = element[2] + " " + element[3];
        labels.push(datetime);
      });
      this.labels = labels
    },

    createGraph() {

      const ctx = document.getElementById("graph");

      const labels = this.labels;

      const myChart = new Chart(ctx, {
        type: "line",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Temperature",
              data: this.temps,
              fill: false,
              borderColor: "rgb(75, 192, 192)",
              tension: 0.1,
            },
          ],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
      myChart;
    },
  },


};
</script>

<style scoped>
</style>
