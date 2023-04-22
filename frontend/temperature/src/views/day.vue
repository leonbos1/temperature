<template>
  <div class="flex h-1/2">
    <canvas id="graph-canvas"></canvas>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
import datajson from "../data.json";

export default {
  components: {
  },
  name: "DayPage",

  data: function () {
    return {
      data: [],
      dailyData: [],
      temps: [],
      humidity: [],
      url: datajson["url"],
      sensor_id: 1,
      sensors: [],
      myChart: null,
      graphTitle: "Daily Temperature",
      graphType: "daily",
    };
  },

  mounted() {
    this.getData();
  },

  methods: {
    getData() {
      if (this.graphType == "daily") {
        this.getDailyData();
      } else if (this.graphType == "weekly") {
        this.getWeeklyData();
      } else if (this.graphType == "monthly") {
        this.getMonthlyData();
      }
      this.disableButtons();
    },

    disableButtons() {
      //disable buttons for 1 second

      let buttons = document.getElementsByClassName("graph-button");
      for (let i = 0; i < buttons.length; i++) {
        buttons[i].disabled = true;
      }
      setTimeout(() => {
        for (let i = 0; i < buttons.length; i++) {
          buttons[i].disabled = false;
        }
      }, 1500);
    },

    getDailyData() {
      fetch(this.url + "/temperature/daily?sensor_id=" + this.sensor_id, {
        method: "GET",
        headers: { token: localStorage.getItem("token") },
      })
        .then((response) => response.json())
        .then((data) => (this.data = data))
        .then(() => this.setTemps())
        .then(() => this.setLabels())
        .then(() => this.createGraph());
    },

    getWeeklyData() {
      fetch(this.url + "/temperature/weekly?sensor_id=" + this.sensor_id, {
        method: "GET",
        headers: { token: localStorage.getItem("token") },
      })
        .then((response) => response.json())
        .then((data) => (this.data = data))
        .then(() => this.setTemps())
        .then(() => this.setLabels())
        .then(() => this.createGraph());
    },

    getMonthlyData() {
      fetch(this.url + "/temperature/monthly?sensor_id=" + this.sensor_id, {
        method: "GET",
        headers: { token: localStorage.getItem("token") },
      })
        .then((response) => response.json())
        .then((data) => (this.data = data))
        .then(() => this.setTemps())
        .then(() => this.setLabels())
        .then(() => this.createGraph());
    },

    setTemps() {
      let temps = [];
      let humidity = [];
      this.data.forEach((element) => {
        temps.push(element["degrees"]);
        humidity.push(element["humidity"]);
      });
      this.temps = temps;
      this.humidity = humidity;
    },

    setLabels() {
      let labels = [];
      this.data.forEach((element) => {
        if (this.graphType == "daily") {
          labels.push(element["time"]);
        } else {
          labels.push(element["date"]);
        }
      });
      this.labels = labels;
    },

    createGraph() {
      if (this.myChart) {
        this.myChart.destroy();
      }
      const ctx = document.getElementById("graph-canvas");

      const labels = this.labels;

      this.myChart = new Chart(ctx, {
        type: "line",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Temperature",
              data: this.temps,
              fill: false,
              borderColor: "rgb(255, 0, 0)",
              tension: 0.1,
              yAxisID: "temp",
            },
            {
              label: "Humidity",
              data: this.humidity,
              fill: false,
              borderColor: "rgb(75, 192, 192)",
              tension: 0.1,
              yAxisID: "humidity",
            },
          ],
        },
        options: {
          plugins: {
            title: {
              display: true,
              text: this.graphTitle,
              font: {
                size: 32,
              },
            },
          },
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            temp: {
              type: "linear",
              display: true,
              position: "left",
            },
            humidity: {
              type: "linear",
              display: true,
              position: "right",
            },
            x: {
              ticks: {
                beginAtZero: true,
              },
            },
          },
        },
      });
      this.myChart;
    },
  },
};
</script>

<style scoped>
</style>
 