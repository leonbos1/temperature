<template>
    <div class="container">

        <h1>{{visitors}} visitors today</h1>

    </div>
  </template>
  
  <script>
  export default {
    name: "ExtraPage",
  
    components: {},
  
    data: function () {
      return {
        visitors: 0,
      };
    },
  
    methods: {
        increaseVisitors() {
            this.visitors++;
        },
    },
 
    beforeMount() {

    },
  };
  </script>
  

  <style scoped>

  </style>
  