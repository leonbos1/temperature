<template>
  <div class="inner">
    <div class="page">
      <button class="paginate" @click="firstPage">
        <font-awesome-icon icon="angles-left" />
      </button>
      <button class="paginate" @click="prevPage">
        <font-awesome-icon icon="chevron-left" />
      </button>
      <input @change="getData()" class="page-number" v-model="page" />
      <button class="paginate" @click="nextPage()">
        <font-awesome-icon icon="chevron-right" />
      </button>
      <button class="paginate" @click="gotoLastPage()">
        <font-awesome-icon icon="angles-right" />
      </button>
    </div>
    <table>
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Temp</th>
          <th scope="col">Humidity</th>
          <th scope="col">
            <select class="dropdown" @change="changeDate" v-model="date">
              <option value="">Date</option>
              <option v-for="date in dates" :key="date" :value="date">
                {{ date }}
              </option>
            </select>
          </th>
          <th scope="col">Time</th>
          <th scope="col">
            <select class="dropdown" @change="changeSensor" v-model="sensor_id">
              <option value="">Sensor</option>
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
          <td><input type="text" v-model="d.degrees" /></td>
          <td><input type="text" v-model="d.humidity" /></td>
          <td>{{ d.date }}</td>
          <td>{{ d.time }}</td>
          <td>{{ d.sensor_id }}</td>
          <button
            @click="editRecord(d.id, d.degrees, d.humidity, d.sensor_id)"
            class="edit"
          >
            <font-awesome-icon icon="pen" />
          </button>
          <button @click="deleteRecord(d.id)" class="delete">
            <font-awesome-icon icon="trash-can" />
          </button>
        </tr>
        <tr>
          <td></td>
          <td><input type="text" v-model="newTemp" /></td>
          <td><input type="text" v-model="newHumidity" /></td>
          <td><input type="text" v-model="newDate" /></td>
          <td><input type="text" v-model="newTime" /></td>
          <td><input type="text" v-model="newSensorId" /></td>
          <button @click="addRecord" class="add">Add</button>
        </tr>
      </tbody>
    </table>
    <div class="page">
      <button class="paginate" @click="firstPage">
        <font-awesome-icon icon="angles-left" />
      </button>
      <button class="paginate" @click="prevPage">
        <font-awesome-icon icon="chevron-left" />
      </button>
      <input @change="getData()" class="page-number" v-model="page" />
      <button class="paginate" @click="nextPage()">
        <font-awesome-icon icon="chevron-right" />
      </button>
      <button class="paginate" @click="gotoLastPage()">
        <font-awesome-icon icon="angles-right" />
      </button>
    </div>
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
      sensor_id: "",
      url: datajson["url"],
      dates: [],
      sensors: [],
      date: "",
      newTemp: "",
      newHumidity: "",
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

    gotoLastPage() {
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

    editRecord(id, degrees, humidity, sensor_id) {
      fetch(this.url, {
        method: "PUT",
        headers: {
          "x-access-tokens": localStorage.getItem("token"),
        },
        body: JSON.stringify({
          id: id,
          degrees: degrees,
          humidity: humidity,
          sensor_id: sensor_id,
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
          humidity: this.newHumidity,
          sensor: this.newSensorId,
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
.page {
  border-bottom: 1px solid rgb(0, 0, 0);
  margin-bottom: 1vh;
}

.inner {
  overflow: auto;
  white-space: nowrap;
  border: 1px solid rgb(0, 0, 0);
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

.paginate {
  border: 1px solid rgb(0, 0, 0);
  border-radius: 4px;
  background-color: #f1f1f1;
  padding: 8px;
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

table {
  border-collapse: collapse;
  width: 100%;
  border-bottom: 1px solid rgb(0, 0, 0);
}

th,
td {
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}

select {
  width: 100%;
  padding: 16px 20px;
  border: none;
  border-radius: 4px;
  background-color: #f1f1f1;
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

.page-number {
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
</style>
 