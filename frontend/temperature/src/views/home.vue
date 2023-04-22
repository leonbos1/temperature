<template>
  <div class="content">
      <Visitors class="visitors" />
      <CurrentTemp />
  </div>
</template>

<script>
import CurrentTemp from "./current-temp.vue";
import Visitors from "./visitors.vue";

export default {
  name: "HomePage",

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
 