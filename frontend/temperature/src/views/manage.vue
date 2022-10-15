<template>
  <div class="table-container">
    <div class="page">
      <button @click="prevPage">Previous</button>
      <p>{{page}}</p>
      <button @click="nextPage">Next</button>
    </div> 
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
          <input type="text" v-model="d.temp" />
          <td>{{ d.date }}</td>
          <td>{{ d.time }}</td>
          <button @click="editRecord(d.id, d.temp)" class="edit">Edit</button>
          <button @click="deleteRecord(d.id)" class="delete">Delete</button>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "ManagePage",

  mounted() {
    this.getData();
  },

  data: function () {
    return {
      allData: [],
      data: [],
      page: 1,
      perPage: 50,
    };
  },
  methods: {
    getData() {
      fetch("http://ronleon.nl:5000/weekly", {
        method: "GET",
        headers: {
          token: "ABHJ",
        },
      })
        .then((response) => response.json())
        .then((allData) => this.showData(allData))
        .then(()=>
        this.selectedData(this.page * this.perPage - this.perPage, this.page * this.perPage)
        );
    },

    showData(data) {
      this.allData = [];
      data.forEach((element) => {
        let newData = {};
        newData.id = element[0];
        newData.temp = element[1];
        newData.date = element[2];
        newData.time = element[3];
        this.allData.push(newData);
      });
    },

    selectedData(firstIndex, secondIndex) {
      this.data = this.allData.slice(firstIndex, secondIndex);
    },

    nextPage() {
      if (this.page < this.allData.length / this.perPage) {
        this.page++;
        this.selectedData(this.page * this.perPage - this.perPage, this.page * this.perPage);
      }
    },

    prevPage() {
      if (this.page > 1) {
        this.page--;
        this.selectedData(this.page * this.perPage, this.page * this.perPage + this.perPage);
      }
    },

    deleteRecord(id) {
      fetch(`http://ronleon.nl:5000/`, {
        method: "DELETE",
        headers: {
          token: localStorage.getItem("token"),
        },
        body: JSON.stringify({
          id: id,
        }),
      }).then(() => this.getData());
    },

    editRecord(id, temp) {
      fetch(`http://ronleon.nl:5000/`, {
        method: "PUT",
        headers: {
          token: localStorage.getItem("token"),
        },
        body: JSON.stringify({
          id: id,
          degrees: temp+''
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

div .page {
  display: flex;
  justify-content: center;
  align-items: center;

  button {
    background-color: #18b68e;
    margin-left: 1vw;
    margin-right: 1vw;
  }
}

</style>
