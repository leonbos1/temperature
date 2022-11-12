<template>
    <div class="graph-container">
      <canvas id="weekly-graph"></canvas>
    </div>
  </template>
  
  <script>
  import Chart from "chart.js/auto";
  import datajson from "../data.json";
  
  export default {
    name: "MonthlyGraph",
  
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
        fetch(this.url + "/temperature/monthly", {
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
        this.temps = [];
        this.data.forEach((element) => {
          this.temps.push(element['degrees']);
        });
      },
  
      setLabels() {
        this.labels = [];
        this.data.forEach((element) => {
          this.labels.push(element['id']);
        });
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
                      text: "Temperatuur afgelopen maand",
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
  