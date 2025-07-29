<template>
  <div class="real-time-data-container">
    <!-- 面包屑导航 -->
    <el-breadcrumb :separator-icon="ArrowRight" class="breadcrumb">
      <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
      <el-breadcrumb-item>数据管理</el-breadcrumb-item>
      <el-breadcrumb-item>数据监控与历史趋势分析</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 标题和操作按钮 -->
    <div class="header">
      <h2>实时数据监控与历史趋势分析</h2>
    </div>

    <!-- KPI指标卡片 -->
    <div class="kpi-cards">
      <el-card shadow="hover" v-for="(kpi, index) in kpiList" :key="index">
        <template #header>
          <div class="kpi-header">
            <span>{{ kpi.name }}</span>
          </div>
        </template>
          <div class="kpi-content">
            <div class="kpi-value">{{ kpi.value }}</div>
          </div>
      </el-card>
    </div>  
    
    <!-- 故障诊断与预测 -->
    <div class="fault-analysis">
        <el-card shadow="hover">
          <template #header>
            <div class="fault-header">
              <span>设备故障诊断与预测</span>
            </div>
          </template>
          <div class="fault-content">
            <!-- 故障预警 -->
            <div class="fault-warning">
              <h4>故障预警</h4>
              <el-table :data="faultWarnings" style="width: 100%">
                <el-table-column prop="equipment" label="设备名称" width="180" />
                <el-table-column prop="warningType" label="预警类型" width="120">
                  <template #default="{ row }">
                    <el-tag :type="getWarningType(row.warningLevel)">
                      {{ row.warningType }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="warningTime" label="预警时间" width="180" />
                <el-table-column prop="probability" label="故障概率" width="120">
                  <template #default="{ row }">
                    {{ row.probability }}%
                  </template>
                </el-table-column>
                <el-table-column prop="suggestion" label="处理建议" />
              </el-table>
            </div>
          </div>
        </el-card>
      </div>


  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ArrowRight, Top, Bottom } from '@element-plus/icons-vue'

// KPI数据
const kpiList = ref([
  {
    name: 'OEE(整体设备效率)',
    value: '85.6%',
  },
  {
    name: '产能',
    value: '1,245',

  },
  {
    name: '能耗',
    value: '1,856',

  },
  {
    name: 'MTBF(平均故障间隔时间/分钟）',
    value: '156',

  },
  {
    name: 'MTTR(平均修复时间/分钟)',
    value: '2.3',

  },
  {
    name: '停机时间/分钟',
    value: '0',
  }
])

// 故障诊断与预测
const faultWarnings = ref([
      {
        equipment: 'CNC-001',
        warningType: '主轴过热',
        warningLevel: 'high',
        warningTime: '2025-05-15 10:23:45',
        probability: 78,
        possibleCauses: '冷却系统故障或轴承磨损',
        impactScope: '可能导致主轴损坏，停机8小时以上',
        suggestion: '立即检查冷却系统，建议在2小时内停机检修'
      },
      {
        equipment: 'AGV-002',
        warningType: '电池衰减',
        warningLevel: 'medium',
        warningTime: '2025-05-15 09:12:33',
        probability: 65,
        possibleCauses: '电池老化，充电周期已达设计寿命80%',
        impactScope: '可能导致运输中断，影响生产效率',
        suggestion: '建议在下个维护周期更换电池'
      },
      {
        equipment: 'Robot-003',
        warningType: '关节异常',
        warningLevel: 'low',
        warningTime: '2025-05-14 16:45:21',
        probability: 42,
        possibleCauses: '润滑不足或减速器磨损',
        impactScope: '可能导致定位精度下降',
        suggestion: '增加润滑频率，监测关节运行数据'
      },
      {
        equipment: 'Robot-003',
        warningType: '关节异常',
        warningLevel: 'low',
        warningTime: '2025-05-14 16:45:21',
        probability: 42,
        possibleCauses: '润滑不足或减速器磨损',
        impactScope: '可能导致定位精度下降',
        suggestion: '增加润滑频率，监测关节运行数据'
      },
      {
        equipment: 'Robot-003',
        warningType: '关节异常',
        warningLevel: 'low',
        warningTime: '2025-05-14 16:45:21',
        probability: 42,
        possibleCauses: '润滑不足或减速器磨损',
        impactScope: '可能导致定位精度下降',
        suggestion: '增加润滑频率，监测关节运行数据'
      },
      {
        equipment: 'Robot-003',
        warningType: '关节异常',
        warningLevel: 'low',
        warningTime: '202-05-14 16:45:21',
        probability: 42,
        possibleCauses: '润滑不足或减速器磨损',
        impactScope: '可能导致定位精度下降',
        suggestion: '增加润滑频率，监测关节运行数据'
      },
    ])

// 根据预警级别返回对应的tag类型
const getWarningType = (level) => {
  switch (level) {
    case 'high':
      return 'danger'
    case 'medium':
      return 'warning'
    case 'low':
      return 'info'
    default:
      return ''
  }
}

</script>

<style scoped>
.real-time-data-container {
  padding: 20px;
  background-color: #f5f7fa;
  height: 80vh;
  overflow-y: auto;
}

.breadcrumb {
  margin-bottom: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.kpi-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.kpi-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.kpi-content {
  display: flex;
  align-items: flex-end;
  margin: 10px 0;
}

.kpi-value {
  font-size: 24px;
  font-weight: bold;
  margin-right: 10px;
  color: #6edfe7;
}

.fault-analysis {
  margin-bottom: 20px;
}
.fault-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
}

.fault-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.fault-warning h4{
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #ea0e07;
  font-weight: bold;
  text-align: center;
}
.fault-trend h4 {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #303133;
}


</style>