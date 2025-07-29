<template>
  <div class="history-data-container">
    <!-- 面包屑导航 -->
    <el-breadcrumb :separator-icon="ArrowRight" class="breadcrumb">
      <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
      <el-breadcrumb-item>数据管理</el-breadcrumb-item>
      <el-breadcrumb-item>数据分析与挖掘</el-breadcrumb-item>
      <el-breadcrumb-item>历史数据展示</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 页面标题和操作区 -->
    <div class="page-header">
      <h2>历史数据分析</h2>
      <div class="header-actions">
        <el-button type="primary" @click="generateReport">生成报表</el-button>
      </div>
    </div>

    <!-- 查询条件区域 -->
    <div class="query-section">
      <el-form :model="queryParams" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="时间范围">
              <el-date-picker
                v-model="queryParams.timeRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="时间粒度">
              <el-select v-model="queryParams.timeGranularity" placeholder="请选择">
                <el-option
                  v-for="item in timeGranularityOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="设备">
              <el-select v-model="queryParams.device" placeholder="请选择设备" clearable>
                <el-option
                  v-for="item in deviceOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-button type="primary" @click="handleQuery">查询</el-button>
            <el-button @click="resetQuery">重置</el-button>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="工位">
              <el-select v-model="queryParams.workstation" placeholder="请选择工位" clearable>
                <el-option
                  v-for="item in workstationOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="产品批次">
              <el-select v-model="queryParams.batch" placeholder="请选择批次" clearable>
                <el-option
                  v-for="item in batchOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </div>

    <!-- 数据表格展示 -->
<el-card>
  <el-table :data="tableData" border style="width: 100%">
    <el-table-column prop="id" label="序号" width="60" />
    <el-table-column prop="device" label="设备" />
    <el-table-column prop="workstation" label="工位" />
    <el-table-column prop="batch" label="批次" />
    <el-table-column prop="timestamp" label="时间戳" />
    <el-table-column prop="value" label="值" />
  </el-table>

  <!-- 分页组件 -->
  <el-pagination
    style="margin-top: 20px; text-align: right"
    background
    layout="prev, pager, next, jumper"
    :current-page="queryParams.pageNum"
    :page-size="queryParams.pageSize"
    :total="allData.length"
    @current-change="val => queryParams.pageNum = val"
  />
</el-card>

    <!-- 报表生成对话框 -->
    <el-dialog v-model="reportDialogVisible" title="生成报表" width="50%">
      <el-form :model="reportForm" label-width="100px">
        <el-form-item label="报表名称">
          <el-input v-model="reportForm.name" placeholder="请输入报表名称" />
        </el-form-item>
        <el-form-item label="报表类型">
          <el-select v-model="reportForm.type" placeholder="请选择报表类型">
            <el-option label="生产报表" value="production" />
            <el-option label="质量报表" value="quality" />
            <el-option label="综合报表" value="comprehensive" />
          </el-select>
        </el-form-item>
        <el-form-item label="导出格式">
          <el-select v-model="reportForm.format" placeholder="请选择导出格式">
            <el-option label="PDF" value="pdf" />
            <el-option label="Excel" value="excel" />
            <el-option label="Word" value="word" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="reportDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmGenerateReport">确认生成</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed} from 'vue'
import { ArrowRight, ElMessage } from '@element-plus/icons-vue'


// 模拟生成100条数据
const allData = ref([])
for (let i = 1; i <= 100; i++) {
  allData.value.push({
    id: i,
    device: '设备' + ((i % 3) + 1),
    workstation: '工位' + ((i % 3) + 1),
    batch: '00' + ((i % 3) + 1),
    timestamp: `2025-07-${(i % 30 + 1).toString().padStart(2, '0')} 08:00:00`,
    value: Math.floor(Math.random() * 100)
  })
}

// 当前页数据（分页）
const tableData = computed(() => {
  const start = (queryParams.value.pageNum - 1) * queryParams.value.pageSize
  const end = start + queryParams.value.pageSize
  return allData.value.slice(start, end)
})

// 模拟查询（这里只是重置页码并触发重新计算）
const handleQuery = () => {
  queryParams.value.pageNum = 1
}



// 查询参数
const queryParams = ref({
  timeRange: [],
  timeGranularity: 'day',
  device: '',
  workstation: '',
  batch: '',
  pageNum: 1,
  pageSize: 10
})

const timeGranularityOptions = [
  { value: 'hour', label: '小时' },
  { value: 'shift', label: '班次' },
  { value: 'day', label: '日' },
  { value: 'month', label: '月' },
  { value: 'year', label: '年' }
]

const deviceOptions = [
  { value: 'device1', label: '设备1' },
  { value: 'device2', label: '设备2' },
  { value: 'device3', label: '设备3' }
]

const workstationOptions = [
  { value: 'station1', label: '工位1' },
  { value: 'station2', label: '工位2' },
  { value: 'station3', label: '工位3' }
]

const batchOptions = [
  { value: 'batch001', label: '001' },
  { value: 'batch002', label: '002' },
  { value: 'batch003', label: '003' }
]


// 报表生成相关
const reportDialogVisible = ref(false)
const reportForm = ref({
  name: '',
  type: 'production',
  format: 'pdf'
})

// 重置查询
const resetQuery = () => {
  queryParams.value = {
    timeRange: [],
    timeGranularity: 'day',
    device: '',
    workstation: '',
    batch: '',
    pageNum: 1,
    pageSize: 10
  }
  handleQuery()
}



// 生成报表
const generateReport = () => {
  reportDialogVisible.value = true
}

// 确认生成报表
const confirmGenerateReport = () => {
  console.log('生成报表:', reportForm.value)
  // 这里调用生成报表的API
  reportDialogVisible.value = false
  ElMessage.success('报表生成任务已提交，请稍后在报表中心查看')
}

</script>

<style scoped>
.history-data-container {
  height: calc(100vh - 170px); /* 比如减去顶部导航高度 */
  overflow-y: auto;
  background-color: #f5f7fa;
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.query-section {
  background-color: #fff;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

</style>