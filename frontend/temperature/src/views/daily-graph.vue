<template>
  <div class="graph-container">
    <choose-sensor
      :sensor_id="sensorId"
    />
    <canvas id="daily-graph"></canvas>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
import datajson from "../data.json";
import ChooseSensor from "./choose-sensor.vue";

export default {
  components: {
    ChooseSensor,
  },
  name: "DailyGraph",

  data: function () {
    return {
      data: [],
      dailyData: [],
      temps: [],
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

    setTemps() {
      let temps = [];
      this.data.forEach((element) => {
        temps.push(element["degrees"]);
      });
      this.temps = temps;
    },

    setLabels() {
      let labels = [];
      this.data.forEach((element) => {
        labels.push(element["time"]);
      });
      this.labels = labels;
    },

    // getSensors() {
    //   fetch(this.url + "/sensors", {
    //     method: "GET",
    //     headers: { token: localStorage.getItem("token")},
    //   })
    //     .then((response) => response.json())
    //     .then((data) => (this.sensors = data));
    // },

    createGraph() {
      if (this.myChart) {
        this.myChart.destroy();
      }
      const ctx = document.getElementById("daily-graph");

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
              borderColor: "rgb(75, 192, 192)",
              tension: 0.1,
            },
          ],
        },
        options: {
          plugins: {
            title: {
              display: true,
              text: "Temperatuur van de afgelopen 24 uur",
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
 