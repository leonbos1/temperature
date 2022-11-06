<template>
  <div class="graph-container">
    <canvas id="weekly-graph"></canvas>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
import datajson from "../data.json";

export default {
  name: "WeeklyGraph",

  data: function () {
    return {
      data: [],
      url: datajson['url'],
    };
  },

  props: {
    msg: String,
  },

  mounted() {
    this.getData();
  },

  methods: {
    getData() {
      fetch(this.url + "/weekly", {
        method: "GET",
        headers: { token: localStorage.getItem("token")},
      })
        .then((response) => response.json())
        .then((data) => (this.data = data))
        .then(() => this.setTemps())
        .then(() => this.setLabels())
        .then(() => this.createGraph())
    },

    setTemps() {
      let temps = [];

      this.data.forEach((element) => {
          temps.push(element['degrees']);
        }
      );
      this.temps = temps; 
    },

    setLabels() {
      let labels = [];

      this.data.forEach((element) => {
        labels.push(element['date']);
        }
      );
      this.labels = labels;
    },

    createGraph() {
      const ctx = document.getElementById("weekly-graph");

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
           plugins: {
                title: {
                    display: true,
                    text: "Temperatuur afgelopen week",
                    font: {
                        size: 32
                    }
                }
            },
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: false,
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
.graph-container {
    width: 100%;
    height: 60vh;
}
</style>
