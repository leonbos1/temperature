<template>
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Name</th>
          <th scope="col">Location</th>
          <th scope="col">last_temp</th>
          <th scope="col">last_send</th>
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="sensor in sensors" v-bind:key="sensor.id">
          <td>{{ sensor.id }}</td>
          <td><input type="text" v-model="sensor.name" /> </td>
          <td><input type="text" v-model="sensor.location" /></td>
          <td>{{ sensor.last_temp }}</td>
          <td>{{ sensor.last_send }}</td>
          <button
            @click="editRecord(sensor.id, sensor.name, sensor.location)"
            class="edit"
          >
            Edit
          </button>
          <button @click="deleteRecord(sensor.id)" class="delete">
            Delete
          </button>
        </tr>

        <tr>
          <td></td>
          <td><input type="text" v-model="newName" /></td>
          <td><input type="text" v-model="newLocation" /></td>
          <td></td>
          <td></td>
          <button @click="addRecord" class="add">Add</button>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import datajson from "../data.json";

export default {
  name: "ManageSensorsPage",

  mounted() {
    this.getData();
  },

  data: function () {
    return {
      sensors: [],
      url: datajson["url"],
      newName: "",
      newLocation: "",
    };
  },
  methods: {
    getData() {
      fetch(this.url + "/sensors", {
        method: "GET",
        headers: {
          token: localStorage.getItem("token"),
        },
      })
        .then((response) => response.json())

        .then((data) => (this.sensors = data));
    },

    deleteRecord(id) {
      fetch(this.url+"/sensors", {
        method: "DELETE",
        headers: {
          "x-access-tokens": localStorage.getItem("token"),
        },
        body: JSON.stringify({
          id: id,
        }),
      }).then(() => this.getData());
    },

    editRecord(id, name, location) {
      fetch(this.url+"/sensors", {
        method: "PUT",
        headers: {
          "x-access-tokens": localStorage.getItem("token"),
        },
        body: JSON.stringify({
          id: id,
          name: name,
          location: location,
        }),
      }).then(() => this.getData());
    },

    addRecord() {
      fetch(this.url+"/sensors", {
        method: "POST",
        headers: {
          token: localStorage.getItem("token"),
        },
        body: JSON.stringify({
          name: this.newName,
          location: this.newLocation,
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

.dropdown {
  position: relative;
  display: inline-block;
  background-color: #18b68e;
  color: white;
  padding: 4px 16px;
  text-align: center;
  text-decoration: none;
  font-size: 16px;
  margin: 2px 2px;
}

option {
  text-align: center;
}
</style>
 