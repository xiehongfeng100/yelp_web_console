<template>
  <div id="index">
    <div class="row">
      <div class="container col-centered">
        <!--Search-->
        <section>
          <div class="panel-header">
            <div v-if="panelNumber === 0">
              <div class="container">
                <div class="col align-items-center">
                  <h3>搜索</h3>
                  <div>
                    <div>
                      <input type="text" style="margin-bottom: 7px" v-model="keyword" @keyup.enter="searchAndRank"/>
                    </div>
                  </div>
                </div>
                <div class="col align-items-center">
                  <div>
                    排序
                    <span><a class="order-by-link" :class="{ 'with-border': orderByWithBorder === 0 }" @click="changOrderBy('dist')">Distance</a></span>
                    <span><a class="order-by-link" :class="{ 'with-border': orderByWithBorder === 1 }" @click="changOrderBy('sentiment')">Sentiment</a></span>
                    <span><a class="order-by-link" :class="{ 'with-border': orderByWithBorder === 2 }" @click="changOrderBy('popularity')">Popularity</a></span>
                  </div>
                </div>
              </div>
            </div>
            <div v-else-if="panelNumber === 1">
              <h3>TopN</h3>
              <button type="button" class="btn" :class="{ 'btn-info': topNBtnWithFilling === 0, 'btn-outline-info': topNBtnWithFilling !== 0 }" @click="getTopN('friends')">
                TopN by Friends
              </button>
              <button type="button" class="btn" :class="{ 'btn-info': topNBtnWithFilling === 1, 'btn-outline-info': topNBtnWithFilling !== 1 }" @click="getTopN('similarities')">
                TopN by Similarities
              </button>
              <button type="button" class="btn" :class="{ 'btn-info': topNBtnWithFilling === 2, 'btn-outline-info': topNBtnWithFilling !== 2 }" @click="getTopN('popularities')">
                TopN by Popularity
              </button>
              <button type="button" class="btn" :class="{ 'btn-info': topNBtnWithFilling === 3, 'btn-outline-info': topNBtnWithFilling !== 3 }" @click="getTopN('dists')">
                TopN by Dists
              </button>
            </div>
            <div v-else-if="panelNumber === 2">
              <div class="user-setting">
                <h3>用户信息</h3>
                <p>
                  <span>DB ID</span>
                  <input v-model="userDbId"/>
                  <span>所在纬度</span>
                  <input v-model="userLocLat"/>
                  <span>所在经度</span>
                  <input v-model="userLocLon"/>
                </p>
              </div>
            </div>
          </div>
          <div class="panel-switch">
            <button type="button" class="btn btn-sm" v-on:click="changePanel(0)">搜索面板</button>
            <button type="button" class="btn btn-sm" v-on:click="changePanel(1)">TopN面板</button>
            <button type="button" class="btn btn-sm" v-on:click="changePanel(2)">用户信息面板</button>
          </div>
        </section>
        <!--Search Result-->
        <section class="section-padding">
          <div class="container">
            <!--Business cards-->
            <div class="row" v-for="(chunk, _i) in bizChunks" :key="_i">
              <div v-for="(biz, _j) in chunk" :key="_j" class="col-md-3">
                <div class="wrapper d-flex">
                  <div class="card">
                    <div class="card-content">
                      <div class="card-body">
                        <h5>{{ biz.name }}</h5>
                        <p class="metric">Distance: {{ biz.dist }}</p>
                        <p class="metric">Sentiment: {{ biz.sentiment }}</p>
                        <p class="metric">Popularity: {{ biz.popularity }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
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
      // Settings
      userDbId: 1,
      userLocLat: 36.175,
      userLocLon: -115.136389,
      // distRange: 2,
      bizes: [],
      panelNumber: 0,
      // Search and Rank
      keyword: 'bbq',
      orderBy: 'dist',
      // Style
      orderByWithBorder: 0,
      topNBtnWithFilling: 0
    }
  },
  methods: {
    changePanel: function (num = 0) {
      this.panelNumber = num
    },
    changOrderBy: function (orderBy) {
      if (orderBy === 'dist') {
        this.orderByWithBorder = 0
      } else if (orderBy === 'sentiment') {
        this.orderByWithBorder = 1
      } else if (orderBy === 'popularity') {
        this.orderByWithBorder = 2
      }
      this.orderBy = orderBy
      this.searchAndRank()
    },
    getTopN: function (type = 'friends', offset = 0, limit = 16) {
      if (type === 'friends') {
        this.topNBtnWithFilling = 0
        apiService.getTopNByFriends(this.userDbId, this.userLocLat, this.userLocLon, offset, limit).then((page) => {
          this.bizes = page
        })
      } else if (type === 'similarities') {
        this.topNBtnWithFilling = 1
        apiService.getTopNBySimilarities(this.userDbId, this.userLocLat, this.userLocLon, offset, limit).then((page) => {
          this.bizes = page
        })
      } else if (type === 'popularities') {
        this.topNBtnWithFilling = 2
        apiService.getTopNByPopularities(this.userLocLat, this.userLocLon, offset, limit).then((page) => {
          this.bizes = page
        })
      } else if (type === 'dists') {
        this.topNBtnWithFilling = 3
        apiService.getTopNByDists(this.userLocLat, this.userLocLon, offset, limit).then((page) => {
          this.bizes = page
        })
      }
    },
    searchAndRank: function (offset = 0, limit = 16) {
      apiService.searchAndRank(this.keyword, this.userLocLat, this.userLocLon, this.orderBy, offset, limit).then((page) => {
        this.bizes = page
      })
    }
  },
  computed: {
    bizChunks: function () {
      return _.chunk(this.bizes, 4)
    }
  },
  mounted: function () {
    this.searchAndRank()
  }
}
</script>

<style scoped>
  body {
    font-family: 'Open Sans', sans-serif;
    color: #353535;
  }

  .section-padding {
    padding: 2rem 0;
  }

  .panel-header {
    padding-top: 25px;
    height: 120px;
  }

  .panel-switch {
    float: right;
    padding-right: 15px;
  }

  .order-by-link {
    cursor: pointer;
  }

  .with-border {
    border: 1px solid;
  }

  input[type=text] {
    padding: 3px;
    text-align: center;
    border: 0;
    border-bottom: 2px solid salmon;
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
    margin-left: 5%;
    margin-bottom: 0;
    padding: 5%;
    width: 250px;
    text-align: left;
    line-height: 115%;
    font-size: 105%;
    font-family: fantasy;
  }

  .metric {
    margin-bottom: 5px;
  }
</style>
