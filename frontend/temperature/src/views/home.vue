<template>
  <div class="content">
    <div class="inner">
      <Visitors class="visitors" />

   
      <CurrentTemp />
    </div>
  </div>
</template>

<script>
import CurrentTemp from "./current-temp.vue";
import Visitors from "./visitors.vue";
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
  text-align: center;
  align-items: center;
  padding: 20px;
}

.inner {
  margin-top: 20vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  text-align: center;
  align-items: center;
  border: 1px solid #ddd;
  padding: 20px;
}

@media screen and (max-width: 500px) {
  .content {
    max-width: 80vw;
  }

  .inner {
    margin-top: 30vh;
  }
}
</style>
 