<template>
  <div class="content">
    <div class="page">
      <div class="filter"></div>

      <button @click="firstPage">First</button>
      <button @click="prevPage">Previous</button>
      <input v-model="page" />
      <button @click="nextPage()">Next</button>
      <button @click="lastPage">Last</button>
    </div>
    <table>
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Temp</th>
          <th scope="col">
            <select class="dropdown" @change="changeDate" v-model="date">
              <option value="">All</option>
              <option v-for="date in dates" :key="date" :value="date">
                {{ date }}
              </option>
            </select>
          </th>
          <th scope="col">Time</th>
          <th scope="col">
            <select class="dropdown" @change="changeSensor" v-model="sensor_id">
              <option value="">All</option>
              <option
                v-for="sensor in sensors"
                :key="sensor.id"
                :value="sensor.id"
              >
                {{ sensor.location }}
              </option>
            </select>
          </th>
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="d in data" v-bind:key="d">
          <td>{{ d.id }}</td>
          <input type="text" v-model="d.degrees" />
          <td>{{ d.date }}</td>
          <td>{{ d.time }}</td>
          <td>{{ d.sensor_id }}</td>
          <button @click="editRecord(d.id, d.degrees)" class="edit">
            Edit
          </button>
          <button @click="deleteRecord(d.id)" class="delete">Delete</button>
        </tr>
        <tr>
          <td></td>
          <td><input type="text" v-model="newTemp" /></td>
          <td><input type="text" v-model="newDate" /></td>
          <td><input type="text" v-model="newTime" /></td>
          <td><input type="text" v-model="newSensorId" /></td>
          <button @click="addRecord" class="add">Add</button>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import datajson from "../data.json";

export default {
  name: "ManageTempsPage",

  mounted() {
    this.setDates();
    this.getData();
    this.getSensors();
  },

  data: function () {
    return {
      data: [],
      page: 1,
      perPage: 50,
      sensor_id: 1,
      url: datajson["url"],
      dates: [],
      sensors: [],
      date: "",
      newTemp: "",
      newDate: "",
      newTime: "",
      newSensorId: 1,
    };
  },
  methods: {
    getData() {
      fetch(
        this.url +
          "/?page=" +
          this.page +
          "&per_page=" +
          this.perPage +
          "&sensor_id=" +
          this.sensor_id +
          "&selected_date=" +
          this.date,
        {
          method: "GET",
          headers: {
            token: localStorage.getItem("token"),
          },
        }
      )
        .then((response) => {
          return response.json();
        })
        .then((data) => (this.data = data))
        .then(() => this.getLastPage());
    },

    getLastPage() {
      fetch(
        this.url +
          "/last_page?page=" +
          this.page +
          "&per_page=" +
          this.perPage +
          "&sensor_id=" +
          this.sensor_id +
          "&selected_date=" +
          this.date,
        {
          method: "GET",
          headers: {
            token: localStorage.getItem("token"),
          },
        }
      )
        .then((response) => {
          return response.json();
        })
        .then((data) => (this.lastPage = data["last_page"]));
    },

    getSensors() {
      fetch(this.url + "/sensors", {
        method: "GET",
        headers: {
          token: localStorage.getItem("token"),
        },
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => (this.sensors = data));
    },

    changeDate() {
      this.page = 1;
      this.getData();
    },

    changeSensor() {
      this.page = 1;
      this.getData();
    },

    setDates() {
      this.dates = [];
      fetch(
        this.url + "/dates?page=" + this.page + "&per_page=" + this.perPage,
        {
          method: "GET",
          headers: {
            token: localStorage.getItem("token"),
          },
        }
      )
        .then((response) => response.json())
        .then((data) => {
          for (var i = 0; i < data.length; i++) {
            if (!this.dates.includes(data[i].date)) {
              this.dates.push(data[i].date);
            }
          }
        });
    },

    nextPage() {
      if (this.page < this.lastPage) {
        this.page++;
        this.getData();
      }
    },

    prevPage() {
      if (this.page > 1) {
        this.page--;
        this.getData();
      }
    },

    firstPage() {
      this.page = 1;
      this.getData();
    },

    lastPage() {
      fetch(
        this.url +
          "/last_page?page=" +
          this.page +
          "&per_page=" +
          this.perPage +
          "&sensor_id=" +
          this.sensor_id,
        {
          method: "GET",
          headers: {
            token: localStorage.getItem("token"),
          },
        }
      )
        .then((response) => response.json())
        .then((data) => {
          this.page = data.last_page;
          this.last_page = data.last_page;
        })
        .then(() => this.getData());
    },

    deleteRecord(id) {
      fetch(this.url, {
        method: "DELETE",
        headers: {
          "x-access-tokens": localStorage.getItem("token"),
        },
        body: JSON.stringify({
          id: id,
        }),
      }).then(() => this.getData());
    },

    editRecord(id, degrees) {
      fetch(this.url, {
        method: "PUT",
        headers: {
          "x-access-tokens": localStorage.getItem("token"),
        },
        body: JSON.stringify({
          id: id,
          degrees: degrees + "",
        }),
      }).then(() => this.getData());
    },

    addRecord() {
      fetch(this.url, {
        method: "POST",
        headers: {
          token: localStorage.getItem("token"),
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
.content {
  margin: 0 auto;
  width: 100%;
  padding: 20px;
  text-align: center;
  border: 1px solid rgb(0, 0, 0);
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

button {
  border: none;
  color: rgb(0, 0, 0);
  padding: 4px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border: 1px solid rgb(0, 0, 0);
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

.page {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

tr {
  border: 1px solid rgb(109, 109, 109);
}

td {
  border: 1px solid rgb(82, 82, 82);
}

table {
  border: 1px solid rgb(102, 102, 102);
  border-collapse: collapse;
  width: 100%;
}

select {
  width: 100%;
  border: none;
  border-radius: 4px;
  background-color: #f1f1f1;
  border: 1px solid rgb(0, 0, 0);
}

option {
  width: 100%;
  padding: 16px 20px;
  border: none;
  border-radius: 4px;
  background-color: #f1f1f1;
}

.filters {
  float: left;
}
</style>
 