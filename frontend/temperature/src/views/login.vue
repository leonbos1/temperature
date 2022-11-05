<template>
  <div class="container">
    <div class="login">
      <form v-on:submit="loginMethod">
        <input type="text" v-model="username" placeholder="Username" />
        <input type="password" v-model="password" placeholder="Password" />
        <button type="submit">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
import datajson from "../data.json";
export default {
  name: "LoginPage",

  data: function () {
    return {
      username: "",
      password: "",
      url: datajson["url"],
    };
  },

  components: {},

  methods: {
    loginMethod(e) {
      e.preventDefault();
      fetch(this.url + "/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      })
        .then((response) => response.json())
        //.then((data) => data.text())
        .then((data) => {
          localStorage.setItem("token", data["token"]);
          localStorage.setItem("username", data["user"]);
          this.$router.push("/manage");
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
  height: 300px;
  position: relative;
}

input {
  width: 80%;
  height: 30px;
  border-radius: 5px;
  border-color: black;
  border-style: solid;
  border-width: 2px;
  margin-bottom: 10px;
}

button {
  background-color: #18b68e;
  border: none;
  color: white;
  padding: 8px 40px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 10px;
  border-color: black;
  border-style: solid;  
  border-width: 2px;
  
}
</style>
 