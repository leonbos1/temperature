<template>
  <div class="container">
    <div class="content">
      <CurrentTemp />
      <DailyGraph />
      <WeeklyGraph />
    <!--  <Manage/> -->
    </div>
  </div>
</template>


<script>
import CurrentTemp from "./components/current-temp.vue";
import DailyGraph from "./components/daily-graph.vue";
import WeeklyGraph from "./components/weekly-graph.vue";
//import Manage from "./components/manage.vue"

export default {
  name: "App",
  components: {
    CurrentTemp,
    DailyGraph,
    WeeklyGraph,
   // Manage
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

.container {
  width: 100%;
  text-align: center;
  margin: 0 auto;
  margin-top: 0px;
}

.content {
  width: 100%;
  text-align: center;
  margin: 0 auto;
}

@media (min-width: 480px) {
  .content {
    width: 80%;
  }
}

ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #333;
}

li {
  float: left;
}

li a {
  display: block;
  color: white;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}

li a:hover:not(.active) {
  background-color: #111;
}

.active {
  background-color: #00c58a;
}
</style>
