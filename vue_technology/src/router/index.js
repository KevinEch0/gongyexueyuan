import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '@/views/LoginView.vue'
import HomeView from '@/views/HomeView.vue'
const routes = [
  {
    path: '/',
    name: 'login',
    component: LoginView
  },
  {
    path: '/home',
    name: 'home',
    component: HomeView,
    redirect:'/welcome',
    children:[
      {
        path:'/welcome',
        name:'welcome',
        component: () => import('../views/WelcomeView.vue')
      },
      {
        path:'/user_list',
        name:'user_list',
        component: () => import('../views/UserView.vue')
      },
      {
        path:'/role_list',
        name:'role_list',
        component: () => import('../views/MenuView.vue')
      },
      {
        path:'/author_list',
        name:'author_list',
        component: () => import('../views/AuthorView.vue') 
      },
      {
        path:'/algorithm_list',
        name:'algorithm_list',
        component: () => import('../views/AlgorithmView.vue')
      },
      {
        path:'/data_analysis',
        name:'data_analysis',
        component: () => import('../views/DataView.vue')
      },
      {
        path:'/data_visualization',
        name:'data_visualization',
        component: () => import('../views/kpiView.vue')
      },
      {
        path:'/alarm_list',
        name:'alarm_list',
        component: () => import('../views/alarmView.vue')
      },
      {
        path:'/data_analysis_realtime',
        name:'data_analysis_realtime',
        component: () => import('../views/VisualinterfaceView.vue')
      },
      {
        path:'/chuli_tuxinag',
        name:'chuli_tuxinag',
        component: () => import('../views/yuchuliView.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

// 做router跳转的login_required验证
router.beforeEach((to, from, next) => {
 if (to.path =='/'){
  next()
  }else{
  // 获取token值
  const token = sessionStorage.getItem('token')
  if (!token){
   next('/')
   }
  next()
  }
})
