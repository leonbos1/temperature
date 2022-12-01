<template>
  <div class="graph-container">
    <choose-sensor
    @setSensor="(sensor) => {
      sensor_id = sensor;
      this.getData();
    }"
    />
    <canvas id="weekly-graph"></canvas>
  </div>
</template>
  
  <script>
import Chart from "chart.js/auto";
import datajson from "../data.json";
import ChooseSensor from "./choose-sensor.vue";

export default {
  name: "MonthlyGraph",

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

  props: {
    msg: String,
  },

  mounted() {
    this.getData();
  },

  methods: {
    getData() {
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
      this.temps = [];
      this.data.forEach((element) => {
        this.temps.push(element["degrees"]);
      });
    },

    setLabels() {
      this.labels = [];
      this.data.forEach((element) => {
        this.labels.push(element["date"]);
      });
    },

    createGraph() {
      if (this.myChart) {
        this.myChart.destroy();
      }

      const ctx = document.getElementById("weekly-graph");

      this.myChart = new Chart(ctx, {
        type: "line",
        data: {
          labels: this.labels,
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
              text: "Temperatuur afgelopen maand",
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
  