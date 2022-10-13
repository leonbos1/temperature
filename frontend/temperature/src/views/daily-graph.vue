<template>
  <div class="graph-container">
    <canvas id="daily-graph"></canvas>
  </div>
</template>

<script>
import Chart from "chart.js/auto";

export default {
  name: "DailyGraph",

  data: function () {
    return {
      data: [],
      dailyData: [],
      temps: [],
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
        headers: { kaas: "yoyokaas" },
      })
        .then((response) => response.json())
        .then((data) => data.replace(/'/g, '"'))
        .then((data) => JSON.parse(data))
        .then((data) => (this.data = data))
        .then(() => this.setDailyData())
        .then(() => this.setTemps())
        .then(() => this.setLabels())
        .then(() => this.createGraph());
    },

    setTemps() {
      this.dailyData.forEach((element) => {
        this.temps.push(element[1]);
      });
    },

    setDailyData() {
      this.data.forEach((element) => {
        let date = new Date();
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

        if (today === element[2]) {
          this.dailyData.push(element);
        }
      });
    },

    setLabels() {
      let labels = [];

      this.dailyData.forEach((element) => {
        let datetime = element[2] + " " + element[3];
        labels.push(datetime);
      });
      this.labels = labels;
    },

    createGraph() {
      const ctx = document.getElementById("daily-graph");

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
              text: "Temperatuur vandaag",
              font: {
                size: 32,
              },
            },
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
