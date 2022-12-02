<template>
<div class="dropdown">
  <select class="dropdown-content" @change="$emit('setSensor', this.sensorId)" v-model="sensorId">
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
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
}
</style>
