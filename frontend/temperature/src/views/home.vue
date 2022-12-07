<template>
  <div class="content">
    <div class="info">
      <Visitors class="visitors" />
      <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec
        ultricies, nisl et ultricies aliquet, nisl nisl aliquet nisl, eget
        aliquet nunc nisl eget nisl. Nulla facilisi. Nulla facilisi. Nulla
        facilisi. Nulla facilisi. Nulla facilisi. Nulla facilisi. Nulla
        facilisi. Nulla facilisi. Nulla facilisi. Nulla facilisi. Nulla
        facilisi. Nulla facilisi. Nulla facilisi. Nulla facilisi. Nulla
        facilisi. Nulla facilisi. Nulla facilisi. Nulla facilisi. Nulla
      </p>
    </div>

    <div class="sensor">
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
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ddd;
  padding: 20px;
}

.info {
  width: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.sensor {
  width: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>
 