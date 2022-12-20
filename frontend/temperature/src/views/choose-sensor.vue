<template>
<div class="dropdown">
  <font-awesome-icon icon="location-dot" />
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

div {
  display: flex;
  justify-content: center;
  align-items: center;
}

select {
  width: 100%;
  height: 50px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f8f8f8;
  font-size: 16px;
  padding: 10px;
  margin: 10px;
}

option {
  font-size: 16px;
  padding: 10px;
  margin: 10px;
}


</style>
