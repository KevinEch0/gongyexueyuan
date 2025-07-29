<template>
  <div class="common-layout container">
    <el-container class="container">
      <el-header class="header">
        <div class="logo">
          <img src="../assets/logo.png" alt="">
          <span>工业学院数据分析与管理系统</span>
        </div>
        <div class="user">
          <el-button type="danger" class="logout-btn" @click="logout">退出</el-button>
        </div>
      </el-header>
      <el-container>
        <el-aside class="aside">
          <div class="aside-content">

            <el-menu active-text-color="#ffd04b" background-color="#545c64" class="el-menu-vertical-demo"
              default-active="2" text-color="#fff" unique-opened router>

              <el-sub-menu :index="index + ' '" v-for="(item, index) in menuList.menus">
                <template #title>
                  <el-icon>
                    <component :is="menuList.icons[item.id]"></component>
                  </el-icon>
                  <span>{{ item.name }}</span>
                </template>

                <!-- 二级菜单项 -->
                <template v-for="childItem in item.children">
                  <!-- 如果有三级菜单，则渲染为 el-sub-menu -->
                  <el-sub-menu v-if="childItem.children && childItem.children.length" :index="childItem.path"
                    :key="childItem.path">
                    <template #title>{{ childItem.name }}</template>
                    <!-- 三级菜单项 -->
                    <el-menu-item v-for="grandChild in childItem.children" :index="grandChild.path"
                      :key="grandChild.path">
                      {{ grandChild.name }}
                    </el-menu-item>
                  </el-sub-menu>

                  <!-- 如果没有三级菜单，则渲染为普通菜单项 -->
                  <el-menu-item v-else :index="childItem.path" >
                    {{ childItem.name }}
                  </el-menu-item>
                </template>
              </el-sub-menu>
            </el-menu>
          </div>
        </el-aside>
        <el-main class="main">
          <div class="main-content">
            <router-view />
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>


<script setup>

  import { useRouter,useRoute } from 'vue-router'
  import api from '../api/index.js'
  import { onMounted, reactive } from 'vue'

  const menuList = reactive({
    // menu: [],
    menus: [],
    icons: {
      '1':'User',
      '2':'Setting',
      '3':'FolderOpened',
      '4':'Files',
      '5':'Platform'
    },
  })

  const router = useRouter()
  const route = useRoute() // 获取当前路由信息


  // 当Dom元素加载完毕，调用get_menu方法
  onMounted(() => {
    
    fetchMenuByRole()
    // get_menu()
    // 打印路由参数
    console.log('接收到的路由参数:', route.query)
    if (route.query.role !== undefined) {
      console.log('role参数值:', route.query.role)
    }
  })

  // 退出登录
  const logout = () => {
    // 退出登录，从sessionStorage中删除token值
    sessionStorage.removeItem('token')
    // 跳转回登录页面
    router.push('/login')
  }

  // 获取菜单
  // const get_menu = () => {
  //   api.get_menu().then(res => { 
  //     menuList.menus = res.data.data
  //     console.log(menuList.menus)
  //   }) 
  // }
// 根据角色获取菜单
const fetchMenuByRole = () => {
  const role = route.query.role
  console.log('当前角色:', role)
  const ID = localStorage.getItem('userRole');
  if (ID ==='4') {
    

    api.get_menu().then(res => {
    menuList.menus = res.data.data
    console.log('角色0菜单:', menuList.menus)
  }).catch(err => {
    console.error('获取角色0菜单失败:', err)
    menuList.menus = [] // 出错时设置为空数组
  })
  } 
  if (ID === '1') {
    api.get_menu_1().then(res => {
    menuList.menus = res.data.data
    console.log('角色1菜单:', menuList.menus)
  }).catch(err => {
    console.error('获取角色1菜单失败:', err)
    menuList.menus = [] // 出错时设置为空数组
  })
 
  } else {
    console.warn('未知角色，使用默认菜单')
    menuList.menus = [] // 默认空菜单
  }
}




</script>

<style scoped>
.container {
  height: 100vh;
  overflow: hidden;
}

.header {
  background: linear-gradient(135deg, #1a2980, #26d0ce);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  font-size: 20px;
  color: white;
  height: 60px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30px;
  position: relative;
  z-index: 10;
}

.header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
}

.logo {
  display: flex;
  align-items: center;
  height: 100%;
}

.logo img {
  width: 40px;
  height: 40px;
  margin-right: 15px;
  filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.5));
}

.logo span {
  font-weight: bold;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
  letter-spacing: 1px;
}

.user {
  display: flex;
  align-items: center;
  height: 100%;
}

.logout-btn {
  /* color: white !important; */
  font-size: 14px;
  padding: 8px 15px;
  border-radius: 4px;
  transition: all 0.3s;
  /* background: rgba(255, 255, 255, 0.1); */
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.aside {
  width: 220px !important;
  background: linear-gradient(to bottom, #2c3e50, #34495e);
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.aside::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.05),
    transparent
  );
  animation: shine 3s infinite;
}

@keyframes shine {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.aside-content {
  height: 100%;
  border-right: 1px solid rgba(255, 255, 255, 0.05);
}

.main {
  background: #f5f7fa;
  position: relative;
}

.main-content {
  height: 100%;
  background: white;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
  border-radius: 8px 0 0 0;
  border-left: 1px solid #e6e6e6;
}
</style>