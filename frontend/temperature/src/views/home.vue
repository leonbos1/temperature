<template>
  <div class="mt-12">
    <card-row />
    <graph-row />
  </div>
</template>

<script>

import CardRow from "../components/card-row.vue";
import GraphRow from "../components/graph-row.vue";

export default {
  name: "HomePage",

  components: {
    CardRow,
    GraphRow,
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
 