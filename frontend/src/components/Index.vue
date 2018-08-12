<template>
  <div id="index">
    <div class="container col-centered">
      <!--Settings-->
      <section>
        <span>userDbId:
          <input v-model="userDbId"/>
        </span>
        <span>userLocation:
          <span>Latitude
            <input v-model="userLocLat"/>
          </span>
          <span>Longitude
            <input v-model="userLocLon"/>
          </span>
        </span>
        <span>searchRange(km):
          <input v-model="searchRange"/>
          <span>km</span>
        </span>
      </section>
      <!--Search-->
      <section>
        <button v-on:click="changePanel">Switch</button>
        <div v-if="searchOrTopN === true">
          <div class="container">
          <div class="col align-items-center">
            <h3>Search</h3>
            <div>
              <div>
                <input type="text" placeholder="bbq"/>
                <button type="button" class="btn btn-info">
                  Search
                </button>
              </div>
            </div>
          </div>
          <div class="col align-items-center">
            <div>
              Sort by
              <span><a href="#" style="color: green">Distance</a></span>
              <span><a href="#" style="color: dodgerblue">Sentiment</a></span>
              <span><a href="#" style="color: red">Popularity</a></span>
            </div>
          </div>
        </div>
        </div>
        <div v-else>
          BALALAL
        </div>
      </section>
      <!--Search Result-->
      <section class="dashboard-counts section-padding">
        <div class="container">
          <!--Business cards-->
          <div class="row" v-for="(chunk, _i) in bizChunks" :key="_i">
            <div v-for="(biz, _j) in chunk" :key="_j" class="col-md-3">
              <div class="wrapper d-flex">
                <div class="card">
                  <div class="card-content">
                    <div class="card-body">
                      <p>{{ biz.name }}</p>
                      <p>Distance: {{ biz.dist }}</p>
                      <p>Sentiment: {{ biz.sentiment }}</p>
                      <p>Popularity: {{ biz.popularity }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <!--Friends-->
      <section></section>
      <!--Similarities-->
      <section></section>
      <!--Popularity-->
      <section></section>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import APIService from '../utils/apiservice'
const apiService = new APIService()

export default {
  name: 'Index',
  data: function () {
    return {
      loading: false,
      wordLimit: 150,
      reviews: [],
      bizes: [],
      userDbId: 1,
      userLocLat: 36.175,
      userLocLon: -115.136389,
      searchRange: 2,
      searchOrTopN: true,
      pages: [],
      pageSet: {
        totalRow: 0,
        info: true,
        language: 'en',
        pageSizeMenu: [12, 16, 20]
      }
    }
  },
  methods: {
    changePanel: function () {
      this.searchOrTopN = !this.searchOrTopN
      console.log(this.searchOrTopN)
    },
    getTopNByFriends: function (userDbId, offset = 0, limit = 12) {
      this.loading = true
      apiService.getTopNByFriends(userDbId, this.userLocLat, this.userLocLon, offset, limit).then((page) => {
        console.log(page)
        this.bizes = page
        for (let [index, biz] of this.bizes.entries()) {
          biz.index = index
        }
        this.pageSet.totalRow = page.count
      })
      this.loading = false
    }
    // pageChange: function (pInfo) {
    //   let pageSize = pInfo.pageSize
    //   let pageNumber = pInfo.pageNumber
    //   this.getReviews((pageNumber - 1) * pageSize, pageSize)
    // }
  },
  computed: {
    bizChunks: function () {
      return _.chunk(this.bizes, 4)
    }
  },
  mounted: function () {
    this.getTopNByFriends(1)
  }
}
</script>

<style scoped>
  body {
    font-family: 'Open Sans', sans-serif;
    color: #353535;
  }

  #custom-search-input{
    padding: 3px;
    border: solid 1px #E4E4E4;
    border-radius: 6px;
    background-color: #fff;
  }

  #custom-search-input input{
    border: 0;
    box-shadow: none;
  }

  #custom-search-input button{
    margin: 2px 0 0 0;
    background: none;
    box-shadow: none;
    border: 0;
    color: #666666;
    padding: 0 8px 0 10px;
    border-left: solid 1px #ccc;
  }

  #custom-search-input button:hover{
    border: 0;
    box-shadow: none;
    border-left: solid 1px #ccc;
  }

  #custom-search-input .glyphicon-search{
    font-size: 23px;
  }

  .card {
    background: #FFF;
    display: block;
    display: -webkit-box;
    display: -webkit-flex;
    display: -ms-flexbox;
    display: flex;
    border: 1px solid #AAA;
    border-bottom: 3px solid #BBB;
    padding: 0;
    /*margin-top: 5em;*/
    margin-top: 20px;
    margin-bottom: 20px;
    overflow: hidden;
    box-shadow: 0 8px 17px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    font-family: 'Roboto', sans-serif;
    -webkit-transition: box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    transition: box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .card-body {
    margin: 5%;
    padding: 5%;
    margin-bottom: 0;
    width: 250px;
    text-align: left;
    line-height: 115%;
    font-size: 105%;
    font-family: fantasy;
  }
</style>
