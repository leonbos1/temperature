<template>
  <div class="hello">
    <p>Current temperature: {{ currentTemp }} graden</p>
    <p>Current humidity: {{ currentHumidity }} %</p>
    <p>Average temperature today: {{ avgToday }} graden</p>
    <p>Average temperature yesterday: {{ avgyesterday }} graden</p>
    <choose-sensor
      @setSensor="
        (sensor) => {
          sensor_id = sensor;
          this.getData();
        }
      "
    />
  </div>
</template>

<script>
import datajson from "../data.json";
import ChooseSensor from "./choose-sensor.vue";

export default {
  name: "CurrentTemp",

  components: {
    ChooseSensor,
  },

  data: function () {
    return {
      currentTemp: 0,
      currentHumidity: 0,
      avgToday: 0,
      avgyesterday: 0,
      data: [],
      url: datajson["url"],
      sensor_id: 1,
    };
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
          this.avgyesterday = this.data["average_yesterday"];
        });
    },
  },
  beforeMount() {
    this.getData();
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
 