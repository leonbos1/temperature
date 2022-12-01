<template>
  <select class="dropdown" v-model="sensorId">
    <option @change="sendSensorId()" v-for="sensor in sensors" :key="sensor.id" :value="sensor.id">
      {{ sensor.location }}
    </option>
  </select>
</template>

<script>
import data from "../data.json";

export default {
  name: "ChooseSensor",
  data: function () {
    return {
      sensors: [],
      sensorId: 1,
      url: data["url"],
    };
  },
  mounted() {
    this.getSensors();
  },
  methods: {
    getSensors() {
      fetch(this.url + "/sensors", {
        method: "GET",
        headers: { token: localStorage.getItem("token") },
      })
        .then((response) => response.json())
        .then((data) => (this.sensors = data))
        .then(() => this.$emit("ready", this.sensors));
    },

    sendSensorId() {

      this.$emit("sensorId", this.sensorId);
    },
  },
};
</script>
