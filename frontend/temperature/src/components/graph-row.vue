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
        graphTitle="This Week"
        :temps="weeklyTemps"
        v-if="weeklyLoaded"
        :humidity="weeklyHumidity"
        :labels="weeklyLabels"
        graphNumber="2"
      />
      <small-graph
        graphTitle="This Month"
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
      sensors: [],
      myChart: null,
      graphTitle: "Daily Temperature",
      graphType: "daily",
    };
  },

  props: {
    sensor_id: {
      type: Number,
      default: 1,
    },
  },

  watch: {
    sensor_id: function () {
      this.getData();
    },
  },

  components: {
    SmallGraph,
  },

  mounted() {
    if (this.checkCache) {
      console.log("Cache not found");
      this.getData();
    }
  },

  methods: {
    getData() {
      this.getDailyData();
      this.getWeeklyData();
      this.getMonthlyData();
      this.cacheData();
    },

    checkCache() {
      if (localStorage.getItem("cacheTime") < Date.now() ) {
        return false;
      }
      if (localStorage.getItem("dailyData") == null) {
        return false;
      } else if (localStorage.getItem("weeklyData") == null) {
        return false;
      } else if (localStorage.getItem("monthlyData") == null) {
        return false;
      } else {
        this.dailyData = JSON.parse(localStorage.getItem("dailyData"));
        this.weeklyData = JSON.parse(localStorage.getItem("weeklyData"));
        this.monthlyData = JSON.parse(localStorage.getItem("monthlyData"));
        this.setDailyTemps();
        this.setDailyLabels();
        this.setWeeklyTemps();
        this.setWeeklyLabels();
        this.setMonthlyTemps();
        this.setMonthlyLabels();
        this.dailyLoaded = true;
        this.weeklyLoaded = true;
        this.monthlyLoaded = true;
        return true;
      }
    },

    cacheData() {
      localStorage.setItem("dailyData", JSON.stringify(this.dailyData));
      localStorage.setItem("weeklyData", JSON.stringify(this.weeklyData));
      localStorage.setItem("monthlyData", JSON.stringify(this.monthlyData));
      localStorage.setItem("cacheTime", Date.now() + 600000);
    },

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
        labels.push(element["date"]);
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
        labels.push(element["date"]);
      });
      this.monthlyLabels = labels;
    },
  },
};
</script>

<style scoped>
</style>
 