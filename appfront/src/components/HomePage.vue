<template>
  <div id="home">
    <div id="top">
      <button v-on:click="layout = 'world'">World</button>
      <button v-on:click="layout = 'us'">U.S.</button>
    </div>

    <div id="bottom">
      <b-container fluid v-if="layout === 'world'" class="allgrid" border-variant="primary">

        <b-row>
          <b-col cols="1">
            <b-card>
              <p>Total Confirmed</p> {{total_num}}
            </b-card>
          </b-col>

          <b-col cols="8">
            <b-card>
              <p>World Map</p>
            </b-card>
          </b-col>

          <b-col cols="1">
            <b-card>
              <p>Global Death</p>
              <p id="death_num">{{total_death}}</p>

              <b-container class="death_list">
                  <b-table sticky-header :items="death_list" thead-class="hidden_header" tbody-class="table_body" style="max-height: 100px">
                  </b-table>
                </b-container>
            </b-card>
          </b-col>

          <b-col cols="1">
              <b-card class="item4"><p>US State Level</p></b-card>
          </b-col>


        </b-row>


      </b-container>
    </div>

  </div>
</template>

<script>
    export default {
        name: "HomePage",
        data() {
            return {
                layout: 'world'
            }
        }
    }
</script>

<style scoped>

</style>
