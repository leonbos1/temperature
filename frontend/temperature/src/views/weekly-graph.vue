<template>
  <div class="graph-container">
    <choose-sensor
      @setSensor="
        (sensor) => {
          sensor_id = sensor;
          this.getData();
        }
      "
    />
    <canvas id="weekly-graph"></canvas>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
import datajson from "../data.json";
import ChooseSensor from "./choose-sensor.vue";

export default {
  name: "WeeklyGraph",

  components: {
    ChooseSensor,
  },

  data: function () {
    return {
      data: [],
      url: datajson["url"],
      sensor_id: 1,
      sensors: [],
      myChart: null,
    };
  },

  mounted() {
    this.getData();
  },

  methods: {
    getData() {
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
        labels.push(element["date"]);
      });
      this.labels = labels;
    },

    createGraph() {
      if (this.myChart) {
        this.myChart.destroy();
      }
      const ctx = document.getElementById("weekly-graph");

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
              text: "Afgelopen 24 uur",
              font: {
                size: 32,
              },
            },
          },
          responsive: true,
          maintainAspectRatio: true,
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
.graph-container {
  width: 100%;
  height: 60vh;
}
</style>
