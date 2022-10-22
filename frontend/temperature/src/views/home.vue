<template>
  <div>
  <Visitors class="visitors"/>
  <CurrentTemp/>
  
  </div>
</template>

<script>

import CurrentTemp from './current-temp.vue'
import Visitors from './visitors.vue';

export default {


  name: "HomePage",

  components: {
    CurrentTemp,
    Visitors
},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
