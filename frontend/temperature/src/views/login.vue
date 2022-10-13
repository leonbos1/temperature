<template>
  <div class="container">
    <div class="login">
      <input v-model="login" v-on:input="test" placeholder="Password" />
      <button>Submit</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginPage",

  data: function () {
    return {
      login: "",
    };
  },

  components: {},

  methods: {
    test() {
      if (this.login === "kaaspassword") {
        localStorage.setItem("token", "ABHJ");
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.login {
  background-color: #18b68e;
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  padding: 50px;
  width: 20%;
  height: 30%;
  border-color: black;
  border-style: solid;
  border-radius: 10px;
  border-width: 2px;
}

.container {
  height: 200px;
  position: relative;
}

input {
  width: 80%;
}
</style>
