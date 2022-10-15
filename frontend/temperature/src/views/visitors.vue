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
            //post to api
            fetch("http://ronleon.nl:5000/visitors", {
                method: "POST",
              })
                .then((response) => response.json())
                .then((data) => this.visitors = data)
        },
    },
 
    mounted() {
        this.increaseVisitors();
    },
  };
  </script>
  

  <style scoped>

  </style>
  