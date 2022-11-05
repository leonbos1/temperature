<template>
  <div>
  <Visitors class="visitors"/>
  <CurrentTemp/>
  <DailyGraph/>
  <WeeklyGraph/>
  
  </div>
</template>

<script>

import CurrentTemp from './current-temp.vue'
import WeeklyGraph from './weekly-graph.vue'
import DailyGraph from './daily-graph.vue'
import Visitors from './visitors.vue';

export default {


  name: "HomePage",

  components: {
    CurrentTemp,
    DailyGraph,
    WeeklyGraph,
    Visitors
},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
 