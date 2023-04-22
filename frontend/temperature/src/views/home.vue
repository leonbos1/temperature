<template>
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
  </div>
</template>

<script>

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
 