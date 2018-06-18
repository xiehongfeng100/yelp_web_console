<template>
    <div id="review-sentiment">
      <!-- Counts Section -->
      <section class="dashboard-counts section-padding">
        <div class="container">
          <div class="row">
            <!-- Count item widget-->
            <div class="col-xl-2 col-md-4 col-6 col-centered">
              <div class="wrapper count-title d-flex">
                <div class="icon"><i class="icon-user"></i></div>
                <div class="name"><strong class="text-uppercase">评论总数</strong><span>Last 7 days</span>
                  <div class="count-number">25</div>
                </div>
              </div>
            </div>
            <!-- Count item widget-->
            <div class="col-xl-2 col-md-4 col-6 col-centered">
              <div class="wrapper count-title d-flex">
                <div class="icon"><i class="icon-padnote"></i></div>
                <div class="name"><strong class="text-uppercase">正面评论总数</strong><span>Last 5 days</span>
                  <div class="count-number">400</div>
                </div>
              </div>
            </div>
            <!-- Count item widget-->
            <div class="col-xl-2 col-md-4 col-6 col-centered">
              <div class="wrapper count-title d-flex">
                <div class="icon"><i class="icon-check"></i></div>
                <div class="name"><strong class="text-uppercase">负面评论总数</strong><span>Last 2 months</span>
                  <div class="count-number">342</div>
                </div>
              </div>
            </div>
            <!-- Count item widget-->
            <div class="col-xl-2 col-md-4 col-6 col-centered">
              <div class="wrapper count-title d-flex">
                <div class="icon"><i class="icon-bill"></i></div>
                <div class="name"><strong class="text-uppercase">中性评论总数</strong><span>Last 2 days</span>
                  <div class="count-number">123</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <!-- Review Section -->
      <section class="dashboard-counts section-padding">
        <div class="container">
          <!--review cards-->
          <div class="row" v-for="(chunk, _i) in reviewChunks" :key="_i">
            <div v-for="(review, _j) in chunk" :key="_j" class="col-md-3">
              <div class="wrapper d-flex">
                <div class="card">
                  <div class="card-content">
                    <div class="shape" :class="shapeColorClass(review.sentiment)">
                      <div class="shape-text">
                        {{ review.sentiment }}
                      </div>
                    </div>
                    <div class="card-body">
                      <div v-if="review.scrollable">
                        <p class="card-p pre-scrollable">
                          {{ review.text }}
                        </p>
                      </div>
                      <div v-else>
                        <div v-if="review.textLen > wordLimit">
                          {{ review.text.substr(0, wordLimit + 1) + '...' }}
                        </div>
                        <div v-else>
                          {{ review.text }}
                        </div>
                      </div>
                      <div v-if="review.textLen > wordLimit">
                        <div v-if="review.scrollable">
                          <button @click="continueReading(review)" class="button button-tiny button-circle"><i
                            class="fa fa-minus"></i></button>
                        </div>
                        <div v-else>
                          <button @click="continueReading(review)" class="button button-tiny button-circle"><i
                            class="fa fa-plus"></i></button>
                        </div>
                      </div>
                      <div class="pull-left">
                        <star-rating :star-size="15" :rating="review.stars" :read-only="true"
                                     :show-rating="false"></star-rating>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
</template>

<script>
import _ from 'lodash'
import APIService from '../../utils/apiservice'
const apiService = new APIService()

export default {
  name: 'review-sentiment',
  data: function () {
    return {
      loading: false,
      wordLimit: 200,
      reviews: [],
      pages: [],
      numOfPages: 0,
      nextPageURL: '',
      previousPageURL: ''
    }
  },
  methods: {
    shapeColorClass: function (sentiment) {
      let result = 'medium'
      if (sentiment < 2.5) {
        result = 'bad'
      } else if (sentiment > 3.5) {
        result = 'good'
      }
      return result
    },
    continueReading: function (review) {
      // console.log(review.scrollable)
      review.scrollable = !review.scrollable
      this.$set(this.reviews, review.index, review) // This is one way to update/render DOM accordingly when item changes in a array, plz refer to https://vuejs.org/v2/guide/list.html#Caveats
    },
    getReviews: function (offset = 0, limit = 12) {
      apiService.getReviews(offset, limit).then((page) => {
        // console.log(page)
        this.reviews = page.results
        for (let [index, review] of this.reviews.entries()) {
          review.index = index
          review.scrollable = false
          review.textLen = review.text.length
        }
        this.numOfPages = page.numpages
        this.nextPageURL = page.nextlink
        this.previousPageURL = page.prelink
      })
    }
  },
  computed: {
    reviewChunks: function () {
      return _.chunk(this.reviews, 4)
    }
  },
  mounted: function () {
    this.getReviews()
  }
}
</script>

<style scoped>
  .card {
    background: #FFF;
    display: block;
    display: -webkit-box;
    display: -webkit-flex;
    display: -ms-flexbox;
    display: flex;
    border: 1px solid #AAA;
    border-bottom: 3px solid #BBB;
    padding: 0px;
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
    text-align: left;
    line-height: 115%;
    font-size: 105%;
    font-family: fantasy;
  }

  .pull-left {
    float: left;
    padding-left: 0;
  }

  .shape {
    border-style: solid;
    border-width: 0 70px 40px 0;
    float: right;
    height: 0px;
    width: 0px;
    -ms-transform: rotate(360deg); /* IE 9 */
    -o-transform: rotate(360deg); /* Opera 10.5 */
    -webkit-transform: rotate(360deg); /* Safari and Chrome */
    transform: rotate(360deg);
  }

  .good {
    border-color: transparent #5cb85c transparent transparent;
    border-color: rgba(255,255,255,0) #5cb85c rgba(255,255,255,0) rgba(255,255,255,0);
  }

  .medium {
    border-color: transparent #999999 transparent transparent;
    border-color: rgba(255,255,255,0) #999999 rgba(255,255,255,0) rgba(255,255,255,0);
  }

  .bad {
    border-color: transparent #d9534f transparent transparent;
    border-color: rgba(255,255,255,0) #d9534f rgba(255,255,255,0) rgba(255,255,255,0);
  }

  .shape-text {
    color: #fff;
    font-size: 12px;
    font-weight: bold;
    position: relative;
    right: -40px;
    top: 2px;
    white-space: nowrap;
    -ms-transform: rotate(30deg); /* IE 9 */
    -o-transform: rotate(360deg); /* Opera 10.5 */
    -webkit-transform: rotate(30deg); /* Safari and Chrome */
    transform: rotate(30deg);
  }

  .pre-scrollable {
    width: 110%;
    max-height: 200px;
    overflow-y: scroll;
  }
</style>
