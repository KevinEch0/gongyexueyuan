<template>
    <div class="fault-container">
        <!-- 面包屑导航 -->
        <el-breadcrumb :separator-icon="ArrowRight" class="breadcrumb">
            <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
            <el-breadcrumb-item>数据管理</el-breadcrumb-item>
            <el-breadcrumb-item>报警与事件中心</el-breadcrumb-item>
        </el-breadcrumb>

        <!-- 主内容区域 -->
        <div class="main-content">
            <!-- 数据统计卡片 -->
            <div class="stat-cards">
                <el-row :gutter="20">

                    <el-col :span="6">
                        <el-card shadow="hover">
                            <div class="card-content">
                                <div class="card-icon danger">
                                    <el-icon>
                                        <CircleClose />
                                    </el-icon>
                                </div>
                                <div class="card-info">
                                    <div class="card-title">故障设备</div>
                                    <div class="card-value">{{ stats.faultDevices }}台</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="6">
                        <el-card shadow="hover">
                            <div class="card-content">
                                <div class="card-icon success">
                                    <el-icon>
                                        <SuccessFilled />
                                    </el-icon>
                                </div>
                                <div class="card-info">
                                    <div class="card-title">已修复</div>
                                    <div class="card-value">{{ stats.repairedDevices }}台</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="6">
                        <el-card shadow="hover">
                            <div class="card-content">
                                <div class="card-icon primary">
                                    <el-icon>
                                        <TrendCharts />
                                    </el-icon>
                                </div>
                                <div class="card-info">
                                    <div class="card-title">待处理</div>
                                    <div class="card-value">{{ stats.pendingDevices }}台</div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
            </div>

            <!-- 设备列表和预测结果 -->
            <div class="device-list">
                <el-card shadow="hover">
                    <template #header>
                        <div class="table-header">
                            <span>设备故障列表</span>
                        </div>
                    </template>
                    <el-table :data="deviceList" stripe style="width: 100%">
                        <el-table-column prop="id" label="设备ID" width="100" />
                        <el-table-column prop="name" label="设备名称" width="180" />
                        <el-table-column prop="status" label="设备状态" width="120">
                            <template #default="{ row }">
                                <el-tag :type="getStatusTagType(row.status)">
                                    {{ row.status }}
                                </el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column prop="faultType" label="故障类型" width="150" />
                        <el-table-column prop="detectedTime" label="检测时间" width="180" />
                        <el-table-column prop="processStatus" label="处理状态" width="120">
                            <template #default="{ row }">
                                <el-tag :type="getProcessStatusTagType(row.processStatus)">
                                    {{ row.processStatus }}
                                </el-tag>
                            </template>
                        </el-table-column>
                        <!-- 设备列表操作列 -->

                        <el-table-column label="操作" width="220" fixed="right">
                            <template #default="{ row }">
                                <el-button size="small" @click="handleDetail(row)">详情</el-button>
                                <el-button size="small" :type="row.processStatus === '已处理' ? 'info' : 'warning'"
                                    @click="handleProcess(row)"
                                    :disabled="row.status === '正常' || row.processStatus === '已处理'">
                                    {{ row.processStatus === '已处理' ? '查看处理记录' : '待处理' }}
                                </el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <div class="pagination">
                        <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :total="total"
                            :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" />
                    </div>
                </el-card>
            </div>

            <!-- 处理记录弹窗 -->
            <el-dialog v-model="processDialogVisible"
                :title="`${currentDevice.processStatus === '已处理' ? '查看' : '记录'}处理信息 - ${currentDevice.name}`"
                width="50%">
                <el-form :model="processForm" label-width="100px" :disabled="isViewMode">
                    <el-form-item label="处理人">
                        <el-input v-model="processForm.processor" placeholder="请输入处理人姓名" />
                    </el-form-item>
                    <el-form-item label="处理时间">
                        <el-date-picker v-model="processForm.processTime" type="datetime" placeholder="选择处理时间"
                            value-format="YYYY-MM-DD HH:mm:ss" />
                    </el-form-item>
                    <el-form-item label="处理结果">
                        <el-select v-model="processForm.result" placeholder="请选择处理结果">
                            <el-option label="已修复" value="已修复" />

                            <el-option label="无法修复" value="无法修复" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="处理说明">
                        <el-input v-model="processForm.remark" type="textarea" :rows="3" placeholder="请输入处理说明" />
                    </el-form-item>
                </el-form>
                <template #footer>
                    <el-button @click="processDialogVisible = false">关闭</el-button>
                    <el-button type="primary" @click="confirmProcess" v-if="!isViewMode">
                        确认处理
                    </el-button>
                </template>
            </el-dialog>

            <!-- 预测分析弹窗 -->
            <el-dialog v-model="predictionDialogVisible" title="故障预测分析" width="80%">
                <div class="prediction-dialog">

                    <div class="prediction-result">
                        <h4>预测结果分析</h4>
                        <el-card shadow="never">
                            <div class="result-content">
                                <div class="result-summary">
                                    <el-tag type="warning" size="large">高风险</el-tag>
                                    <div class="result-text">
                                        <p>
                                            预测该设备在未来7天内发生故障的概率为
                                            <span class="risk-high">78%</span>，建议立即进行检修。
                                        </p>
                                        <p>最可能故障类型：<strong>电机过热</strong></p>
                                    </div>
                                </div>
                                <div class="result-suggestions">
                                    <h5>建议措施：</h5>
                                    <ul>
                                        <li>检查电机冷却系统是否正常工作</li>
                                        <li>监测电机负载情况，避免过载运行</li>
                                        <li>清理电机散热片上的灰尘和杂物</li>
                                        <li>建议在48小时内安排预防性维护</li>
                                    </ul>
                                </div>
                            </div>
                        </el-card>
                    </div>
                </div>
                <template #footer>
                    <el-button @click="predictionDialogVisible = false">关闭</el-button>
                </template>
            </el-dialog>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ArrowRight, Warning, CircleClose, SuccessFilled, TrendCharts } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// 设备列表
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(50)

const deviceList = ref([
  {
    id: 'DEV001',
    name: '1',
    type: 'CNC机床',
    status: '故障',
    faultType: '主轴振动异常',
    detectedTime: '2023-07-15 14:30',
    processStatus: '待处理',
    processRecord: null,
    prediction: true,
    predictionRisk: 78
  },
  {
    id: 'DEV002',
    name: '3',
    type: '注塑机',
    status: '故障',
    faultType: '液压系统泄漏',
    detectedTime: '2023-07-14 09:15',
    processStatus: '待处理',
    processRecord: null,
    prediction: true,
    prediction: false
  },
  {
    id: 'DEV003',
    name: '2',
    type: '包装机',
    status: '正常',
    faultType: '-',
    detectedTime: '2023-07-16 16:45',
    processStatus: '无需处理',
    processRecord: null,
    prediction: true,
    predictionRisk: 35
  },
  {
    id: 'DEV004',
    name: '4',
    type: '工业机器人',
    status: '故障',
    faultType: '伺服电机过热',
    detectedTime: '2023-07-13 11:20',
    processStatus: '待处理',
    processRecord: null,
    prediction: true,
    prediction: false
  },
  {
    id: 'DEV005',
    name: '5',
    type: '输送设备',
    status: '故障',
    faultType: '皮带磨损',
    detectedTime: '2023-07-15 08:10',
    processStatus: '待处理',
    processRecord: null,
    prediction: true,
    predictionRisk: 62
  }
])

// 计算统计数量
const stats = computed(() => {
  return {
    faultDevices: deviceList.value.filter(device => device.status === '故障').length,
    repairedDevices: deviceList.value.filter(device => 
      device.processStatus === '已处理' && device.processRecord?.result === '已修复'
    ).length,
    pendingDevices: deviceList.value.filter(device => 
      device.processStatus === '待处理' && (device.status === '故障')
    ).length
  }
})

// 处理记录表单
const processForm = ref({
  processor: '',
  processTime: '',
  result: '',
  remark: ''
})

const currentDevice = ref({})
const processDialogVisible = ref(false)
const predictionDialogVisible = ref(false)

// 计算属性：判断是否为查看模式
const isViewMode = computed(() => {
  return currentDevice.value.processStatus === '已处理'
})
// 方法
const handleProcess = (row) => {
  // 添加状态检查，防止正常状态的设备被处理
  if (row.status === '正常') {
    ElMessage.warning('正常状态的设备无需处理')
    return
  }
  
  currentDevice.value = row
  if (row.processStatus === '已处理') {
    // 查看模式，填充已有数据
    processForm.value = {
      processor: row.processRecord.processor,
      processTime: row.processRecord.processTime,
      result: row.processRecord.result,
      remark: row.processRecord.remark
    }
  } else {
    // 处理模式，初始化表单
    processForm.value = {
      processor: '',
      processTime: new Date().toISOString().replace('T', ' ').substring(0, 19),
      result: '',
      remark: ''
    }
  }
  processDialogVisible.value = true
}

const getStatusTagType = (status) => {
  switch (status) {
    case '正常':
      return 'success'
    case '预警':
      return 'warning'
    case '故障':
      return 'danger'
    case '维修中':
      return 'info'
    default:
      return ''
  }
}

const getProcessStatusTagType = (status) => {
  switch (status) {
    case '已处理':
      return 'success'
    case '待处理':
      return 'danger'
    case '无需处理':
      return 'info'
    default:
      return ''
  }
}



const handleDetail = (row) => {
  console.log('查看详情', row)
  predictionDialogVisible.value = true
}

const confirmProcess = () => {
  const record = {
    processor: processForm.value.processor,
    processTime: processForm.value.processTime,
    result: processForm.value.result,
    remark: processForm.value.remark
  }
  
  // 更新设备处理状态
  const index = deviceList.value.findIndex(device => device.id === currentDevice.value.id)
  if (index !== -1) {
    deviceList.value[index].processStatus = '已处理'
    deviceList.value[index].processRecord = record
    
    // 如果处理结果是"已修复"，更新设备状态为"正常"
    if (processForm.value.result === '已修复') {
      deviceList.value[index].status = '正常'
      // 同时更新故障类型为空或修复信息
      deviceList.value[index].faultType = '已修复'
    }
  }
  
  processDialogVisible.value = false
  ElMessage.success('处理记录已保存')
}
</script>

<style scoped>
.fault-container {
  padding: 20px;
  background-color: #f5f7fa;
  height: 80vh;
  overflow-y: auto;
}

.breadcrumb {
  margin-bottom: 20px;
}

.main-content {
  background-color: #fff;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.stat-cards {
  margin-bottom: 20px;
}

.card-content {
  display: flex;
  align-items: center;
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 24px;
  color: white;
}



.card-icon.danger {
  background-color: #F56C6C;
}

.card-icon.success {
  background-color: #67C23A;
}

.card-icon.primary {
  background-color: #409EFF;
}





.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.prediction-dialog {
  padding: 10px;
}



.prediction-result {
  margin-top: 20px;
}

.result-content {
  padding: 15px;
}

.result-summary {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
}

.result-text {
  margin-left: 15px;
  flex: 1;
}

.result-text p {
  margin: 5px 0;
}

.risk-high {
  color: #F56C6C;
  font-weight: bold;
}

.result-suggestions h5 {
  margin: 15px 0 10px;
  color: #606266;
}

.result-suggestions ul {
  padding-left: 20px;
  color: #606266;
}

.result-suggestions li {
  margin-bottom: 8px;
}
</style>