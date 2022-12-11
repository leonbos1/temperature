<template>
  <div class="content">
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
          window.location.href = "/";
        });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.content {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 80vw;
}

.login {
  //center
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  border-radius: 10px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  padding: 40px;
  margin: 40px;
  border: 2px solid #ccc;
}

input {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  width: 100%;
  background-color: #18b68e;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
 