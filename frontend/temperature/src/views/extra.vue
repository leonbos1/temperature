<template>
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th scope="col">Datum</th>
          <th scope="col">Gemiddelde</th>
          <th scope="col">Laagste</th>
          <th scope="col">Hoogste</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="d in formattedData" v-bind:key="d">
          <td>{{ d.date }}</td>
          <td>{{ d.avgTemp }}</td>
          <td>{{ d.lowest }}</td>
          <td>{{ d.highest }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import datajson from "../data.json";
export default {
  name: "ExtraPage",

  components: {},

  data: function () {
    return {
      data: [],
      formattedData: [],
      url: datajson["url"],
    };
  },

  methods: {
    getData() {
      fetch(this.url + "/weekly", {
        method: "GET",
        headers: { token: localStorage.getItem("token")},
      })
        .then((response) => response.json())
        .then((data) => (this.data = data))
        .then(() => this.formatData());
    },

    formatData() {
      let totalTemp = 0;

      let dateNow = "";
      let counter = 0;
      let highest = -999;
      let lowest = 999;

      this.data.forEach((element) => {
        if (dateNow === "") {
          dateNow = element[2];
        } else {
          if (dateNow === element[2]) {
            totalTemp += element[1];
            counter++;
            if (lowest > element[1]) {
              lowest = element[1];
            }
            if (highest < element[1]) {
              highest = element[1];
            }
          } else {
            let toAdd = {};
            toAdd.avgTemp = (totalTemp / counter).toFixed(2);
            toAdd.date = dateNow;
            toAdd.lowest = lowest;
            toAdd.highest = highest;
            this.formattedData.push(toAdd);
            dateNow = element[2];
            totalTemp = element[1];
            counter = 1;
            lowest = 999;
            highest = -999;
          }
        }
      });
      let toAdd = {};
      toAdd.avgTemp = (totalTemp / counter).toFixed(2);
      toAdd.date = dateNow;
      toAdd.lowest = lowest;
      toAdd.highest = highest;
      this.formattedData.push(toAdd);
    },
  },

  beforeMount() {
    this.getData();
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
</style>
 