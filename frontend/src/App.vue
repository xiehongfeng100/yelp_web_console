<template>
  <div id="app">
    <!-- Side Navbar -->
    <nav class="side-navbar">
      <div class="side-navbar-wrapper">
        <!-- Sidebar Header -->
        <div class="sidenav-header d-flex align-items-center justify-content-center">
          <!-- User Info-->
          <div class="sidenav-header-inner text-center">
            <!--<img src="assets/img/avatar.png" class="img-fluid rounded-circle">-->
            <h2 class="h5">Max Xie</h2>
            <span>Software Developer</span>
          </div>
          <!--Small Brand information, appears on minimized sidebar-->
          <!--<div class="sidenav-header-logo">-->
          <!--<a href="index.html" class="brand-small text-center">-->
          <!--<strong>B</strong>-->
          <!--<strong class="text-primary">D</strong>-->
          <!--</a>-->
          <!--</div>-->
        </div>
        <!-- Sidebar Navigation Menus-->
        <div class="main-menu">
          <h5 class="sidenav-heading">Main</h5>
          <ul id="side-main-menu" class="side-menu list-unstyled">
            <li>
              <a href="#review-menu-dropdown" aria-expanded="false" data-toggle="collapse">
                <i class="icon-interface-windows"></i>
                评论分析
              </a>
              <ul id="review-menu-dropdown" class="collapse list-unstyled ">
                <router-link to="/review-sentiment">情感分析</router-link>
                <router-link to="/review-topic">主题模型</router-link>
              </ul>
            </li>
            <li>
              <a href="#relation-menu-dropdown" aria-expanded="false" data-toggle="collapse">
                <i class="icon-interface-windows"></i>
                人际关系分析
              </a>
              <ul id="relation-menu-dropdown" class="collapse list-unstyled ">
                <router-link to="#">Page1</router-link>
                <router-link to="#">Page2</router-link>
              </ul>
            </li>
            <li>
              <a href="#recommendation-menu-dropdown" aria-expanded="false" data-toggle="collapse">
                <i class="icon-interface-windows"></i>
                推荐系统
              </a>
              <ul id="recommendation-menu-dropdown" class="collapse list-unstyled ">
                <router-link to="#">Page1</router-link>
                <router-link to="#">Page2</router-link>
              </ul>
            </li>
            <li>
              <a href="#image-classify-menu-dropdown" aria-expanded="false" data-toggle="collapse">
                <i class="icon-interface-windows"></i>
                图片分类
              </a>
              <ul id="image-classify-menu-dropdown" class="collapse list-unstyled ">
                <router-link to="#">Page1</router-link>
                <router-link to="#">Page2</router-link>
              </ul>
            </li>
          </ul>
        </div>
        <div class="other-menu">
          <h5 class="sidenav-heading">Other</h5>
          <ul id="side-other-menu" class="side-menu list-unstyled">
            <li> <a href="#"> <i class="icon-flask"> </i>Demo
              <div class="badge badge-info">Special</div></a></li>
          </ul>
        </div>
      </div>
    </nav>
    <!-- Page -->
    <div class="page">
      <!-- navbar-->
      <header class="header">
        <nav class="navbar">
          <div class="container-fluid">
            <div class="navbar-holder d-flex align-items-center justify-content-between">
              <div class="navbar-header">
                <a id="toggle-btn" href="#" class="menu-btn"><i class="icon-bars"></i></a>
                <a href="/" class="navbar-brand">
                  <div class="brand-text d-none d-md-inline-block"><span>Yelper</span></div>
                </a>
              </div>
              <ul class="nav-menu list-unstyled d-flex flex-md-row align-items-md-center">
                <!-- Log out-->
                <li class="nav-item"><a href="/" class="nav-link logout"> <span
                  class="d-none d-sm-inline-block">Logout</span><i class="fa fa-sign-out"></i></a>
                </li>
              </ul>
            </div>
          </div>
        </nav>
      </header>
      <!-- body -->
      <router-view></router-view>
      <!-- footer -->
      <footer class="main-footer">
        <div class="container-fluid">
          <div class="row">
            <div class="col-sm-6">
              <p>Your company &copy; 2017-2019</p>
            </div>
            <div class="col-sm-6 text-right">
              <p>Design by <a href="https://bootstrapious.com" class="external">Bootstrapious</a></p>
              <!-- Please do not remove the backlink to us unless you support further theme's development at https://bootstrapious.com/donate. It is part of the license conditions and it helps me to run Bootstrapious. Thank you for understanding :)-->
            </div>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script>
import Index from '@/components/Index'
import ReviewSentiment from '@/components/review/Sentiment'
import ReviewTopic from '@/components/review/Topic'

export default {
  name: 'App',
  components: {
    Index,
    ReviewSentiment,
    ReviewTopic
  }
}
</script>

<style>
  @import "assets/css/style.default.css";
  @import "assets/css/style.custom.css";
  @import "assets/css/fontastic.css";
  @import "assets/css/button.css";

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
</style>
