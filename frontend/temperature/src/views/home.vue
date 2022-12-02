<template>
  <div class="content">
  <Visitors class="visitors"/>
  <CurrentTemp/>
  </div>
</template>

<script>

import CurrentTemp from './current-temp.vue'
import Visitors from './visitors.vue';
import data from "../data.json";

export default {

  name: "HomePage",

  components: {
    CurrentTemp,
    Visitors,
},

  data: function () {
    return {
      url: data["url"],
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

.content {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ddd;
}

</style>
 