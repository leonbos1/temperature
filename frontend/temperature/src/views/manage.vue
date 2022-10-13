<template>
  <div class="table-container">
    <button @click="getData()">Show data</button>
    <button @click="hideData()">Hide data</button>
    <table>
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Temp</th>
          <th scope="col">Date</th>
          <th scope="col">Time</th>
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="d in data" v-bind:key="d">
          <td>{{ d.id }}</td>
          <td>{{ d.temp }}</td>
          <td>{{ d.date }}</td>
          <td>{{ d.time }}</td>
          <button @click="deleteRecord(d.id)" class="delete">Delete</button>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "ManagePage",

  data: function () {
    return {
      data: [],
    };
  },
  methods: {
    getData() {
      fetch("http://ronleon.nl:5000/weekly", {
        method: "GET",
        headers: {
          kaas: "yoyokaas",
        },
      })
        .then((response) => response.json())
        .then((data) => data.replace(/'/g, '"'))
        .then((data) => JSON.parse(data))
        .then((data) => this.showData(data));
    },

    hideData() {
      this.data = [];
    },

    showData(data) {
      this.data = [];
      data.forEach((element) => {
        let newData = {};
        newData.id = element[0];
        newData.temp = element[1];
        newData.date = element[2];
        newData.time = element[3];
        this.data.push(newData);
      });
    },

    deleteRecord(id) {
      fetch(`http://ronleon.nl:5000/${id}`, {
        method: "DELETE",
        headers: {
          token: localStorage.getItem("token"),
        },
      }).then(() => this.getData());
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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
.delete {
  width: 50px;
  height: 20px;
}
</style>
