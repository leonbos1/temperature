<template>
  <div class="p-4 xl:ml-80">
    <div class="mb-12 grid gap-y-10 gap-x-6 md:grid-cols-1 xl:grid-cols-3">
      <small-graph
        graphTitle="Today"
        :temps="dailyTemps"
        v-if="dailyLoaded"
        :humidity="dailyHumidity"
        :labels="dailyLabels"
        graphNumber="1"
      />
      <small-graph
        graphTitle="Weekly"
        :temps="weeklyTemps"
        v-if="weeklyLoaded"
        :humidity="weeklyHumidity"
        :labels="weeklyLabels"
        graphNumber="2"
      />
      <small-graph
        graphTitle="Monthly"
        :temps="monthlyTemps"
        v-if="monthlyLoaded"
        :humidity="monthlyHumidity"
        :labels="monthlyLabels"
        graphNumber="3"
      />
    </div>
  </div>
</template>

<script>
import SmallGraph from "../components/small-graph.vue";
import datajson from "../data.json";

export default {
  name: "GraphRow",

  data: function () {
    return {
      dailyData: [],
      dailyTemps: [],
      dailyHumidity: [],
      dailyLabels: [],
      dailyLoaded: false,
      weeklyData: [],
      weeklyTemps: [],
      weeklyHumidity: [],
      weeklyLabels: [],
      weeklyLoaded: false,
      monthlyData: [],
      monthlyTemps: [],
      monthlyHumidity: [],
      monthlyLabels: [],
      monthlyLoaded: false,
      url: datajson["url"],
      sensor_id: 1,
      sensors: [],
      myChart: null,
      graphTitle: "Daily Temperature",
      graphType: "daily",
      
    };
  },

  components: {
    SmallGraph,
  },

  mounted() {
    this.getDailyData();
    this.getWeeklyData();
    this.getMonthlyData();
  },

  methods: {
    getDailyData() {
      fetch(this.url + "/temperature/daily?sensor_id=" + this.sensor_id, {
        method: "GET",
        headers: { token: localStorage.getItem("token") },
      })
        .then((response) => response.json())
        .then((data) => (this.dailyData = data))
        .then(() => this.setDailyTemps())
        .then(() => this.setDailyLabels())
        .then(() => (this.dailyLoaded = true));
    },

    setDailyTemps() {
      let temps = [];
      let humidity = [];
      this.dailyData.forEach((element) => {
        temps.push(element["degrees"]);
        humidity.push(element["humidity"]);
      });
      this.dailyTemps = temps;
      this.dailyHumidity = humidity;
    },

    setDailyLabels() {
      let labels = [];
      this.dailyData.forEach((element) => {
        labels.push(element["time"]);
      });
      this.dailyLabels = labels;
    },

    getWeeklyData() {
      fetch(this.url + "/temperature/weekly?sensor_id=" + this.sensor_id, {
        method: "GET",
        headers: { token: localStorage.getItem("token") },
      })
        .then((response) => response.json())
        .then((data) => (this.weeklyData = data))
        .then(() => this.setWeeklyTemps())
        .then(() => this.setWeeklyLabels())
        .then(() => (this.weeklyLoaded = true));
    },

    setWeeklyTemps() {
      let temps = [];
      let humidity = [];
      this.weeklyData.forEach((element) => {
        temps.push(element["degrees"]);
        humidity.push(element["humidity"]);
      });
      this.weeklyTemps = temps;
      this.weeklyHumidity = humidity;
    },

    setWeeklyLabels() {
      let labels = [];
      this.weeklyData.forEach((element) => {
        labels.push(element["time"]);
      });
      this.weeklyLabels = labels;
    },

    getMonthlyData() {
      fetch(this.url + "/temperature/monthly?sensor_id=" + this.sensor_id, {
        method: "GET",
        headers: { token: localStorage.getItem("token") },
      })
        .then((response) => response.json())
        .then((data) => (this.monthlyData = data))
        .then(() => this.setMonthlyTemps())
        .then(() => this.setMonthlyLabels())
        .then(() => (this.monthlyLoaded = true));
    },

    setMonthlyTemps() {
      let temps = [];
      let humidity = [];
      this.monthlyData.forEach((element) => {
        temps.push(element["degrees"]);
        humidity.push(element["humidity"]);
      });
      this.monthlyTemps = temps;
      this.monthlyHumidity = humidity;
    },

    setMonthlyLabels() {
      let labels = [];
      this.monthlyData.forEach((element) => {
        labels.push(element["time"]);
      });
      this.monthlyLabels = labels;
    },
  },
};
</script>

<style scoped>
</style>
 