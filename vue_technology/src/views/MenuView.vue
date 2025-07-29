<template>
 <el-breadcrumb :separator-icon="ArrowRight">
  <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
  <el-breadcrumb-item>权限管理</el-breadcrumb-item>
  <el-breadcrumb-item>权限列表</el-breadcrumb-item>
 </el-breadcrumb>

 <el-card class="box-card">
  <el-row>
   <el-table :data="tableData.menu_list.slice((currentPage - 1) * pageSize, currentPage * pageSize)" stripe class="table">
    <el-table-column prop="id" label="id" width="300" />
    <el-table-column prop="name" label="菜单名" width="300" />
    <el-table-column prop="level" label="等级" width="300">
      <template #default="scope">
        <el-tag v-if="scope.row.level == 1">1级菜单</el-tag>
        <el-tag type="success" v-else-if="scope.row.level == 2">2级菜单</el-tag>
        <el-tag type="warning" v-else-if="scope.row.level == 3">3级菜单</el-tag>
        

      </template>
    </el-table-column>
    <el-table-column prop="path" label="路径" />
   </el-table>
   
   <!-- 分页组件 -->
   <el-pagination
    class="pagination"
    v-model:current-page="currentPage"
    v-model:page-size="pageSize"
    :page-sizes="[1, 5, 10, 15]"
    :small="false"
    :background="true"
    layout="total, sizes, prev, pager, next, jumper"
    :total="tableData.menu_list.length"
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
   />
  </el-row>
 </el-card>
</template>

<script setup>
import { ArrowRight } from '@element-plus/icons-vue'
import { reactive, onMounted, ref } from 'vue'
import api from '../api/index.js'

let tableData = reactive({
  menu_list: []
})

// 分页相关变量
const currentPage = ref(1)
const pageSize = ref(10)

onMounted(() => {
 get_menu_list()
})

const get_menu_list = () => {
 api.get_menu_list().then(res => {
  tableData.menu_list = res.data.data
 })
}

// 分页方法
const handleSizeChange = (val) => {
  pageSize.value = val
}

const handleCurrentChange = (val) => {
  currentPage.value = val
}
</script>

<style scoped>
.box-card {
  margin-top: 20px;
}
.pagination {
  margin-top: 20px;
  justify-content: flex-end;
}
</style>