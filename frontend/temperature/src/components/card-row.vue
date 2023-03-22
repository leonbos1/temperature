<template>
  <div class="p-4 xl:ml-80">
    <div class="mb-12 grid gap-y-10 gap-x-6 md:grid-cols-2 xl:grid-cols-4">
      <InfoCard
        :sensor_id="sensor_id"
        :temperature="currentTemp"
        description="An hour ago"
        title="Current Temperature"
        difference="0.0"
        sign="+"
      />
      <InfoCard
        :sensor_id="sensor_id"
        :temperature="avgToday"
        description="An hour ago"
        title="Average Today"
        difference="0.0"
        sign="+"
      />
      <InfoCard
        :sensor_id="sensor_id"
        :temperature="avgYesterday"
        description="An hour ago"
        title="Average Yesterday"
        difference="0.0"
        sign="+"
      />
      <InfoCard
        :sensor_id="sensor_id"
        :temperature="23"
        description="An hour ago"
        title="Maximum Yesterday"
        difference="0.0"
        sign="+"
      />
    </div>
  </div>
</template>

<script>
import InfoCard from "../components/info-card.vue";
import datajson from "../data.json";

export default {
  name: "CardRow",

  data: function () {
    return {
      data: [],
      currentTemp: 0,
      currentHumidity: 0,
      avgToday: 0,
      avgYesterday: 0,
      url: datajson["url"],
      sensors: [],
      dataLoaded: false,
    };
  },

  watch: {
    sensor_id: function () {
      this.getData();
    },
  },

  components: {
    InfoCard,
  },
  props: {
    sensor_id: {
      type: Number,
      default: 1,
    },
  },

  mounted() {
    if (this.checkCache()) {
      return;
    }

    this.getData();
  },

  methods: {
    getData() {
      fetch(this.url + "/temperature/current?sensor_id=" + this.sensor_id, {
        method: "GET",
        headers: { token: localStorage.getItem("token") },
      })
        .then((response) => response.json())
        .then((data) => (this.data = data))
        .then(() => {
          this.currentTemp = this.data["current_temp"];
          this.currentHumidity = this.data["current_humidity"];
          this.avgToday = this.data["daily_average"];
          this.avgYesterday = this.data["average_yesterday"];
          this.dataLoaded = true;
          this.cacheData();
        });
    },

    checkCache() {
      if (
        localStorage.getItem("data-" + this.sensor_id) &&
        localStorage.getItem("data-" + this.sensor_id + "-timestamp") &&
        Date.now() -
          localStorage.getItem("data-" + this.sensor_id + "-timestamp") <
          10 * 60 * 1000
      ) {
        this.data = JSON.parse(localStorage.getItem("data-" + this.sensor_id));
        this.currentTemp = this.data["current_temp"];
        this.currentHumidity = this.data["current_humidity"];
        this.avgToday = this.data["daily_average"];
        this.avgYesterday = this.data["average_yesterday"];
        this.dataLoaded = true;

        return true;
      } else {
        return false;
      }
    },

    cacheData() {
      localStorage.setItem("data-" + this.sensor_id, JSON.stringify(this.data));
      localStorage.setItem("data-" + this.sensor_id + "-timestamp", Date.now());
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
 