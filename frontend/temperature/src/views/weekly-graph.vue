<template>
  <div class="graph-container">
    <canvas id="weekly-graph"></canvas>
  </div>
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
    this.getData();
  },

  methods: {
    getData() {
      fetch("http://ronleon.nl:5000/weekly", {
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
      let counter = 0;
      let totalTemp = 0;

      this.data.forEach((element) => {
        counter++;
        totalTemp += element[1];
        
        if (counter > 30) {
          temps.push(totalTemp / counter);
          counter = 0;
          totalTemp = 0;
        }
      });
      this.temps = temps;
    },

    setLabels() {
      let labels = [];
      let counter = 0;

      this.data.forEach((element) => {
        counter++;
        if (counter > 30) {
          let datetime = element[2] + " " + element[3];
          labels.push(datetime);
          counter = 0;
        }
      });
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
                    text: "Temperature this week",
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
