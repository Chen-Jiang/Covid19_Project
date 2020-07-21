<template id="app">
  <div id="home">

    <div id="top">
      <b-button block variant="outline-primary" size="lg" v-on:click="layout = 'world'">World</b-button>
      <b-button block id="us" variant="outline-primary" size="lg" v-on:click="layout = 'us'">New Zealand</b-button>
    </div>

    <div id="bottom">

      <b-container fluid v-if="layout === 'world'" class="allgrid" border-variant="primary">
        <b-row id="r1">
          <b-col cols="2">
            <b-card class="item1">
              <p>Total Confirmed</p>
              <p>{{total_num}}</p>
            </b-card>
          </b-col>

          <b-col cols="6">
            <b-card class="item2">
              <map-import>

              </map-import>

            </b-card>

          </b-col>

          <b-col cols="2">
            <b-card class="item3">
              <p>Global Death</p>
              <p>{{total_death}}</p>

              <b-container class="death_list">
                <b-table id="table2" sticky-header :items="death_list" thead-class="hidden_header"
                         tbody-class="table_body"
                         style="max-height: 180px">
                </b-table>
              </b-container>
            </b-card>
          </b-col>

          <b-col cols="2">
            <b-card class="item4"><p>US State Level</p></b-card>
          </b-col>

        </b-row>

        <b-row id="r2">
          <b-col cols="2">
            <b-card class="item5">
              <p id="confirmed">Confirmed Cases by Country/Region/Sovereignty</p>
              <!--              <b-form @submit="showCharts()">-->
              <b-container fluid class="confirm_list">
                <b-table id="table1" hover :items="confirmed_list" sticky-header
                         thead-class="hidden_header"
                         tbody-class="table_body" @row-clicked="getCountryName" style="max-height: 320px">
                </b-table>
              </b-container>
              <!--              </b-form>-->
            </b-card>
          </b-col>

          <b-col cols="1" offset-lg="1">
            <b-card class="item6">
              <p>#Country/Region</p>
              <p>{{country_num}}</p>
            </b-card>
          </b-col>

          <b-col cols="1" offset-lg="2">
            <b-card class="item7">
              <p>Update at(M/D/Y)</p>
              <p>{{today}}</p>
            </b-card>
          </b-col>

          <b-col cols="2" offset-lg="8">
            <b-card class="item8">
              <div v-if="chart_state === 'confirmed'">
                <img v-bind:src="chart" alt=""/>
              </div>

              <div v-else-if="chart_state === 'daily'">
                <!--                <img src="{{chart}}">-->
              </div>

            </b-card>
          </b-col>

        </b-row>


      </b-container>

      <b-container v-else-if="layout === 'us'">
        <p>US</p>
      </b-container>

    </div>

  </div>
</template>

<script>

  import MapImport from './Map.vue'

    export default {
        name: "Home",
        data() {
            return {
                layout: 'world',
                total_num: 1000,
                confirmed_list: [],
                total_death: 0,
                death_list: [],
                today: '',
                country_num: 0,
                chart_state: 'confirmed',
                chart: '../assets/logo.png'
            }
        },
        mounted: function () {
            this.showWorld();
            this.showChart('United States', 'confirmed');
        },
        components: {
            'map-import': MapImport
        },
        methods: {
            showWorld: function () {
                this.$http.get('http://127.0.0.1:8001/daily/homepage')
                    .then((response) => {
                        var res = JSON.parse(response.bodyText);
                        // console.log("res:", res);
                        this.total_num = res['total_num'];
                        this.confirmed_list = res['country_confirmed_list'];
                        this.total_death = res['total_death'];
                        this.death_list = res['death_list'];
                        this.today = res['today'];
                        this.country_num = res['country_num']
                    })
            },
            showUS: function () {

            },
            getCountryName: function (clicker) {
                var country = clicker.country;
                this.chart_state = 'confirmed';
                this.showChart(country, this.chart_state);
                this.getPosition(country);
                // this.showMap(country);
                console.log(clicker.country);
                console.log(clicker.num)
            },
            showChart: function (country, chart_state) {
                console.log("enter");
                this.$http.get('http://127.0.0.1:8001/daily/charts?country=' + country + '&chart_state=' + chart_state)
                    .then((response) => {
                        var res = JSON.parse(response.bodyText);
                        var l = res['chart'].length;
                        var img1 = res['chart'].substring(2, l - 1);
                        this.chart = "data:image/png;base64," + img1;
                        this.c = res['country'];
                        // console.log("res:", res);
                        // console.log(this.chart);
                        // console.log(this.c)
                    })
            },
            getPosition: function (country) {
                this.$http.get('http://127.0.0.1:8001/daily/query?country=' + country)
                    .then((response) => {
                        var res = JSON.parse(response.bodyText);
                        var posi = res['pos'];
                        console.log(posi);
                        MapImport.methods.loadMap(posi)
                    });
            },

        }
    }
</script>

<style scoped>

  @media only screen and (min-width: 600px) and (max-width: 2000px) {

    #bottom {
      margin: 1% 5% 5% 2%;
    }

    .item1 {
      height: 100px;
    }

    .item2 {
      height: 550px;
    }

    .item3, .item4 {
      height: 280px;
    }

    .item5 {
      margin-top: -250%;
      height: 420px;
    }

    .item6, .item7 {
      height: 80px;
      width: 200px;
      margin-top: 10%;
      margin-left: -85%;
    }

    .item8 {
      margin: -200% 0 0 0;
      width: 430px;
      height: 260px;
    }

    ul {
      list-style-type: none;
    }

    p {
      font-family: "Lucinda Grande", "Lucinda Sans Unicode", Helvetica, Arial, Verdana, sans-serif;
      font-size: 13px;
      font-weight: bold;
    }

    #confirmed {
      font-size: 13px;
    }

    .confirm_list {
      width: 150%;
      margin-left: -22%;
    }

    .b-list-group {
      border: none;
    }

    .death_list {
      margin-left: -27%;
      /*margin-top: 10%;*/
      width: 195px;
      /*height: 300px!important;*/
    }

    .btn-block {
      margin-left: 20%;
      width: 30% !important;
      height: 50px;
      font-size: 18px;
      font-weight: bold;
    }

    #us {
      margin: -4.0% 40% 2% 50%;
    }

    .b-table {
      font-size: 10px;
    }

    img {
      width: 400px;
      height: 240px;
      margin-top: -5%;
    }

    #table1 {
      width: 40%;
      margin-left: -5%;
    }

    #table2 {
      width: 20%;
      margin-left: -4%;
    }
  }

  @media only screen and (min-width: 2000px) {

    #bottom {
      margin: 2% 5% -10% 5%;
      height: 100%;
    }

    .item1 {
      height: 150px;
    }

    .item2 {
      height: 1000px;
    }

    .item3, .item4 {
      height: 450px;
    }

    .item5 {
      margin-top: -150%;
      height: 800px;
    }

    .item6, .item7 {
      height: 120px;
      width: 450px;
      margin-top: 10%;
    }

    .item8 {
      margin: -115% 0 0 55%;
      width: 900px;
      height: 530px;
    }

    ul {
      list-style-type: none;
    }

    p {
      font-family: "Lucinda Grande", "Lucinda Sans Unicode", Helvetica, Arial, Verdana, sans-serif;
      font-size: 26px;
      font-weight: bold;
    }

    #confirmed {
      font-size: 22px;
    }

    .b-list-group {
      border: none;
    }

    .death_list {
      /*margin-left: -11%;*/
      margin-top: 6%;
      width: 395px;
    }

    .btn-block {
      margin-left: 20%;
      width: 30% !important;
      height: 60px;
      font-size: 28px;
      font-weight: bold;
    }

    #us {
      margin: -1.55% 40% 0 50%;
    }

    .confirm_list {
      max-height: 660px !important;
      /*margin-left: -9%;*/
      margin-top: 10%;
      width: 450px;
      height: 700px !important;
    }

    img {
      width: 500px;
      height: 300px;
    }

    svg {
      height: 800px!important;
    }

  }

</style>

<style>
  .hidden_header {
    display: none;
  }

  .this_table {
    max-height: 300px !important;
    /*margin-left: -3%;*/
    /*width: 80px;*/
  }

  .table_body {
    font-size: 10px;
  }

  /*#home {*/
  /*  background-image: url('../assets/1.png');*/
  /*  background-repeat: no-repeat;*/
  /*  background-position: center;*/
  /*  background-size: auto;*/
  /*}*/

  body {
    background-color: #cfe1f5!important;
  }

</style>
