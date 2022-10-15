<template>
  <div class="container">
    <div class="login">
      <form v-on:submit="loginMethod">
        <input type="password" v-model="login" placeholder="Password" />
        <button type="submit">Submit</button>
      </form>
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
    loginMethod(e) {
      e.preventDefault();
      fetch("http://ronleon.nl:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          password: this.login,
        }),
      })
        .then((response) => response.json())
        //.then((data) => data.text())
        .then((data) => {
          console.log(data)
          if (data == "ABHJ") {
            localStorage.setItem("token", data);
            this.$router.push("/manage");
          }
        });
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
