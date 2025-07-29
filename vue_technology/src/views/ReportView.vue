<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>数据管理</el-breadcrumb-item>
        <el-breadcrumb-item>数据可视化与报表</el-breadcrumb-item>
        <el-breadcrumb-item>报表下载</el-breadcrumb-item>
    </el-breadcrumb>
</template>


<script setup>
import { ArrowRight,Search,CirclePlus, Edit  } from '@element-plus/icons-vue'

</script>