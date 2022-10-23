<template>
  <div class="table-container">

    <table>
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Username</th>
          <th scope="col">Last login</th>
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in data" v-bind:key="user">
          <td>{{ user.id }}</td>
          <input v-model="user.username"/>
          <td>{{ user.last_login }}</td>
          <button @click="editRecord(user.id, user.username)" class="edit">Edit</button>
          <button @click="deleteRecord(user.id)" class="delete">Delete</button>
        </tr>
        <tr>
          <td></td>
          <td><input type="text" v-model="newTemp" /></td>
          <td><input type="text" v-model="newDate" /></td>
          <td><input type="text" v-model="newTime" /></td>
          <button @click="addRecord" class="add">Add</button>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import datajson from "../data.json";

//TODO add a form to add password to an account when making a new one

export default {
  name: "ManagePage",

  mounted() {
    this.getData();
  },

  data: function () {
    return {
      data: [],
      url: datajson["url"],
    };
  },
  methods: {
    getData() {
      fetch(this.url + "/user", {
        method: "GET",
        headers: {
          'x-access-tokens': localStorage.getItem("token"),
        },
      })
        .then((response) => response.json())
        .then((data) => this.showData(data))
    },

    showData(data) {
      data.forEach((element) => {
        let newData = {};
        newData.id = element['id'];
        newData.public_id = element['public_id'];
        newData.username = element['username'];
        newData.last_login = element['last_login'];
        this.data.push(newData);
      });
    },

    deleteRecord(id) {
      fetch(this.url+'user', {
        method: "DELETE",
        headers: {
          'x-access-tokens': localStorage.getItem("token"),
        },
        body: JSON.stringify({
          id: id,
        }),
      }).then(() => this.getData());
    },

    editRecord(id, username) {
      fetch(this.url+'user', {
        method: "PUT",
        headers: {
          'x-access-tokens': localStorage.getItem("token"),
        },
        body: JSON.stringify({
          id: id,
          username: username
        }),
      }).then(() => this.getData());
    },

    addRecord() {
      fetch(this.url, {
        method: "POST",
        headers: {
          'x-access-tokens': localStorage.getItem("token"),
        },
        body: JSON.stringify({
          degrees: this.newTemp,
          date: this.newDate,
          time: this.newTime,
        }),
      }).then(() => this.getData());
    },

  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.table-container {
  overflow: auto;
  white-space: nowrap;
  /*min-height: 70vh;*/
}
.table-container table {
  width: 100%;
  text-align: center;
}
.table-container th {
  background-color: #18b68e;
  color: white;
}
.table-container td,
th {
  text-align: left;
  padding: 8px;
}
.table-container tr:nth-child(even) {
  background-color: #f2f2f2;
}

button {
  border: none;
  color: white;
  padding: 4px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}
.delete {
  background-color: #f44336;
}
.edit {
  background-color: #4caf50;
}

.add {
  background-color: #2196f3;
}

div .page {
  display: flex;
  justify-content: center;
  align-items: center;

  button {
    background-color: #18b68e;
  }
  p {
    margin-left: 1vw;
    margin-right: 1vw;
  }
}

th {
  text-align: center;
}

td {
  text-align: center;
}

input {
  text-align: center;
}
</style>
