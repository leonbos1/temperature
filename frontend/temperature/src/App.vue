<template>
  <div>
    <CurrentTemp />
    <WeeklyGraph />
  </div>
</template>

<script>
import CurrentTemp from "./components/current-temp.vue";
import WeeklyGraph from "./components/weekly-graph.vue";

export default {
  name: "App",
  components: {
    CurrentTemp,
    WeeklyGraph,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
