<template>
  <div class="graph-container">
    <div class="graph-buttons">
      <choose-sensor
        @setSensor="
          (sensor) => {
            sensor_id = sensor;
            this.getData();
          }
        "
      />

      <font-awesome-icon icon="calendar-days" />
      <button
        class="graph-button"
        :class="{ active: graphType === 'daily' }"
        @click="
          graphType = 'daily';
          graphTitle = 'Daily Temperature';
          getData();
        "
      >
        Daily
      </button>
      <button
        class="graph-button"
        :class="{ active: graphType === 'weekly' }"
        @click="
          graphType = 'weekly';
          graphTitle = 'Weekly Temperature';
          getData();
        "
      >
        Weekly
      </button>
      <button
        class="graph-button"
        :class="{ active: graphType === 'monthly' }"
        @click="
          graphType = 'monthly';
          graphTitle = 'Monthly Temperature';
          getData();
        "
      >
        Monthly
      </button>
    </div>

    <canvas id="graph-canvas"></canvas>
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
  name: "GraphPage",

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
.graph-container {
  width: 100%;
  height: 60vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 7.5vh;
}

.graph-buttons {
  border: 1px solid black;
  border-radius: 5px;
  padding: 10px;
  width: 20vw;
}

.graph-button {
  background-color: #fff;
  border: none;
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
}
</style>
 