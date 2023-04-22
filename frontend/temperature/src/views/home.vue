<template>
<<<<<<< HEAD
  <div class="mt-12">
    <div class="p-4 xl:ml-80">
      <div class="">
        <label for="sensors" class="block text-sm font-medium text-gray-700">
          Room
        </label>
        <select
          id="sensors"
          name="sensors"
          class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          v-model="sensor_id"
        >
          <option v-for="sensor in sensors" :value="sensor.id" :key="sensor.id">
            {{ sensor.name }}
          </option>
        </select>
      </div>
    </div>

    <card-row :sensor_id="sensor_id" />
    <graph-row :sensor_id="sensor_id" />
=======
  <div class="content">
      <Visitors class="visitors" />
      <CurrentTemp />
>>>>>>> parent of aa8562a (frontend updates)
  </div>
</template>

<script>
<<<<<<< HEAD
import CardRow from "../components/card-row.vue";
import GraphRow from "../components/graph-row.vue";
import datajson from "../data.json";
=======
import CurrentTemp from "./current-temp.vue";
import Visitors from "./visitors.vue";
>>>>>>> parent of aa8562a (frontend updates)

export default {
  name: "HomePage",

  data: function () {
    return {
      url: datajson["url"],
      sensor_id: 1,
      sensors: [],
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
        .then((data) => (this.sensors = data));
    },
  },

  components: {
    CurrentTemp,
    Visitors,
  },
};
</script>

<style scoped>

.content {
  margin-top: 10vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 70%;
  background-color: #f5f5f5;
}

</style>
 