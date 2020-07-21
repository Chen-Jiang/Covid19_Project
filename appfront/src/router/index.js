import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Home from '@/components/Home'
import HomePage from '@/components/HomePage'
import Map from '@/components/Map'
import VueResource from 'vue-resource'
import { BootstrapVue, IconsPlugin, LayoutPlugin, ModalPlugin, VBScrollspy, VBScrollspyPlugin } from 'bootstrap-vue'

Vue.use(Router)
Vue.use(VueResource)
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(LayoutPlugin)
Vue.use(ModalPlugin)
Vue.directive('b-scrollspy', VBScrollspy)
Vue.use(VBScrollspyPlugin)


export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/',
      name: 'Map',
      component: Map
    }
  ]
})
