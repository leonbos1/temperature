<template>
  <div class="container">
      <ul>
        <li><a class="active" href="/">Home</a></li>
        <li><a href="/daily">Today</a></li>
        <li><a href="/weekly">Weekly</a></li>
        <li><a href="/monthly">Monthly</a></li>
        <li v-if="loggedIn"><a href="/managetemps">Manage temps</a></li>
        <li v-if="loggedIn"><a href="/manageusers">Manage users</a></li>
        <li v-if="loggedIn"><a href="/managesensors">Manage sensors</a></li>
        <li class="right" v-if="!loggedIn"><a href="/login">Login</a></li>
        <li class="right" v-if="loggedIn" @click="logout"><a>Logout</a></li>
      </ul>
 
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script>
 
import datajson from "./data.json";

export default {
  name: "App",
  data: function () {
    return {
      loggedIn: false,
      url: datajson['url'],
    };
  },
  mounted() {
    this.checkLogin();
  },
  methods: {
    checkLogin() {
      fetch(this.url + "/checklogin", {
        method: "GET",
        headers: { token: localStorage.getItem("token") },
      })
        .then((data) => {
          if (data.status == 200) {
            this.loggedIn = true;

          } else {
            this.loggedIn = false;
          }
        });

    },
    logout() {
      localStorage.removeItem("token");
      this.loggedIn = false;
      window.location.href = "/";
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}

.container {
  width: 100%;
  text-align: center;
  margin: 0 auto;
  margin-top: 0px;
}

.content {
  width: 100%;
  text-align: center;
  margin: 0 auto;
}

@media (min-width: 480px) {
  .content {
    width: 80%;
    
  }
}

ul {
  list-style-type: none;
  padding: 0;
  overflow: hidden;
  background-color: #272727;
  position: absolute;
  margin-top: 0;
  width: 100%;
  
}

li {
  float: left;
}

li a {
  display: block;
  color: white;
  text-align: center;
  padding: 18px 20px;
  text-decoration: none;
}

li a:hover:not(.active) {
  background-color: #111;
}

.active {
  background-color: #18b68e;
}

body, html {
    margin:0;
}

.right {
  right: 0;
  top: 0;
}
</style>
