import Vue from 'vue'
import Router from 'vue-router'
import vPage from 'v-page'
import StarRating from 'vue-star-rating'
import Index from '@/components/Index'
import ReviewSentiment from '@/components/review/Sentiment'
import ReviewTopic from '@/components/review/Topic'

Vue.use(Router)
Vue.use(vPage)
Vue.component('star-rating', StarRating)

export default new Router({
  routes: [
    {
      path: '',
      redirect: '/index'
    },
    {
      path: '/index',
      name: 'index',
      component: Index
    },
    {
      path: '/review-sentiment',
      name: 'review-sentiment',
      component: ReviewSentiment
    },
    {
      path: '/review-topic',
      name: 'review-topic',
      component: ReviewTopic
    }
  ]
})
