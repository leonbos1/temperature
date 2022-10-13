<template>
  <div>
  <CurrentTemp/>
  <DailyGraph/>
  <WeeklyGraph/>
  
  </div>
</template>

<script>

import CurrentTemp from './current-temp.vue'
import WeeklyGraph from './weekly-graph.vue'
import DailyGraph from './daily-graph.vue'

export default {


  name: "HomePage",

  components: {
      CurrentTemp,
      DailyGraph,
      WeeklyGraph
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
