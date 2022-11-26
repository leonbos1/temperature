<template>
  <div class="table-container">
    <div>
      <select class="dropdown" @change="changeDate" v-model="date">
        <option value="">All</option>
        <option v-for="date in dates" :key="date" :value="date">
          {{ date }}
        </option>
      </select>
    </div>
    <div class="page">
      <button @click="firstPage">First</button>
      <button @click="prevPage">Previous</button>
      <input v-model="page"/>
      <button @click="nextPage">Next</button>
      <button @click="lastPage">Last</button>
    </div>
    <table>
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Temp</th>
          <th scope="col">Date</th>
          <th scope="col">Time</th>
          <th scope="col">Sensor id</th>
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
          <button @click="editRecord(d.id, d.degrees)" class="edit">Edit</button>
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
    this.getData()
  },

  data: function () {
    return {
      data: [],
      page: 1,
      perPage: 50,
      sensor_id: 1,
      url: datajson["url"],
      dates: [],
      date: "",
      newTemp: "",
      newDate: "",
      newTime: "",
      newSensorId: 1,

    };
  },
  methods: {
    getData() {
      fetch(this.url + "/?page="+this.page+"&per_page="+this.perPage+"&sensor_id="+this.sensor_id+"&selected_date="+this.date, {
        method: "GET",
        headers: {
          token: localStorage.getItem("token"),
        },
      })
        .then((response) => {
          if (response.status == 404) {
            this.page--;
            this.getData();
          }
          else {
            return response.json();
          }
        })
        .then((data) => (this.data = data))
    },

    changeDate() {
      this.page = 1;
      this.getData();
    },

    setDates() {
      this.dates = [];
      fetch(this.url+"/dates?page="+this.page+"&per_page="+this.perPage, {
        method: "GET",
        headers: {
          token: localStorage.getItem("token"),
        },
      })
      .then((response) => response.json())
      .then((data) => {
        for (var i = 0; i < data.length; i++) {
          if (!this.dates.includes(data[i].date)) {
            this.dates.push(data[i].date);
          }
        }
      })
    },

    nextPage() {
      fetch(this.url + "/last_page", {
        method: "GET",
        headers: {
          token: localStorage.getItem("token"),
          page : this.page,
          per_page: this.perPage,
          selected_date: this.date,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (this.page < data.last_page) {
            this.page++;
            this.getData();
          }
        });
    },

    prevPage() {
      if (this.page > 1) {
        this.page --;
        this.getData();
      }
    },

    firstPage() {
      this.page = 1;
      this.getData();
    },

    lastPage() {
      fetch(this.url + "/last_page?page="+this.page+"&per_page="+this.perPage+"&selected_date="+this.date+"&sensor_id="+this.sensor_id, {
        method: "GET",
        headers: {
          token: localStorage.getItem("token"),
        },
      })
        .then((response) => response.json())
        .then((data) => (this.page = data.last_page))
        .then(() => this.getData());
    },

    deleteRecord(id) {
      fetch(this.url, {
        method: "DELETE",
        headers: {
          'x-access-tokens': localStorage.getItem("token"),
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
          'x-access-tokens': localStorage.getItem("token"),
        },
        body: JSON.stringify({
          id: id,
          degrees: degrees+''
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
  }
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
 