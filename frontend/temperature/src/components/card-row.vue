<template>
    <div class="p-4 xl:ml-80">
      <div class="mb-12 grid gap-y-10 gap-x-6 md:grid-cols-2 xl:grid-cols-4">
        <InfoCard temperature=21 description="An hour ago" title="Current Temperature" difference=0.6 sign="+" />
        <InfoCard temperature=19 description="1 Day Ago" title="Average Today" difference=0.3 sign="+" />
        <InfoCard temperature=12 description="1 Day Ago" title="Minimum Yesterday" difference=0.8 sign="+" />
        <InfoCard temperature=23 description="1 Day Ago" title="Maximum Yesterday" difference=1.2 sign="+" />
      </div>
    </div>
</template>

<script>

import InfoCard from "../components/info-card.vue";

export default {
  name: "CardRow",

  data: function () {
    return {};
  },

  components: {
    InfoCard,
  },

  methods: {},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
 