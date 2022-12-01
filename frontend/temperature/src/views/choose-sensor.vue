<template>
<div>
  <select class="dropdown" @change="$emit('setSensor', this.sensorId)" v-model="sensorId">
    <option v-for="sensor in sensors" :key="sensor.id" :value="sensor.id">
      {{ sensor.location }}
    </option>

  </select>
</div>
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

<style scoped>

button {
  background-color: #4CAF50; /* Green */
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  height: 50px;
}

</style>
