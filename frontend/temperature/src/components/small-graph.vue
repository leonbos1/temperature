<template>
  <div
    class="relative flex flex-col bg-clip-border rounded-xl bg-white text-gray-700 shadow-md"
  >
    <div
      class="relative bg-clip-border mx-4 rounded-xl overflow-hidden bg-gradient-to-tr from-blue-600 to-blue-400 text-white shadow-blue-500/40 shadow-lg mt-12"
    >
      <div style="min-height: 235px">
        <div class="h-72">
          <canvas
            class="-translate-y-10"
            :id="'graph-canvas-' + graphNumber"
          ></canvas>
        </div>
      </div>
    </div>
    <div class="p-6">
      <h6
        class="block antialiased tracking-normal font-sans text-base font-semibold leading-relaxed text-blue-gray-900"
      >
        Website View
      </h6>
      <p
        class="block antialiased font-sans text-sm leading-normal font-normal text-blue-gray-600"
      >
        Last Campaign Performance
      </p>
    </div>
    <div class="p-6 border-t border-blue-gray-50 px-6 py-5">
      <p
        class="antialiased font-sans text-sm leading-normal flex items-center font-normal text-blue-gray-600"
      >
        &nbsp;Updated 3 minutes ago
      </p>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto";

export default {
  name: "SmallGraph",

  data: function () {
    return {
      myChart: null,
    };
  },

  props: {
    graphNumber: {
      type: String,
      required: true,
    },
    graphTitle: {
      type: String,
      required: true,
    },
    temps: {
      type: Array,
      required: true,
    },
    humidity: {
      type: Array,
      required: true,
    },
    labels: {
      type: Array,
      required: true,
    }
  },

  mounted() {
    this.createGraph();
  },

  methods: {
    createGraph() {
      if (this.myChart) {
        this.myChart.destroy();
      }
      const ctx = document.getElementById("graph-canvas-" + this.graphNumber);

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
              cubicInterpolationMode: "monotone",
              tension: 0.1,
              yAxisID: "temp",
            },
            {
              label: "Humidity",
              data: this.humidity,
              fill: false,
              borderColor: "rgb(75, 192, 192)",
              cubicInterpolationMode: "monotone",
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
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
 