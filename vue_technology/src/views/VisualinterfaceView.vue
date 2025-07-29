<template>
  <div class="dashboard-container">
    <!-- 面包屑导航 -->
    <div class="breadcrumb-container">
      <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>可视化界面</el-breadcrumb-item>
        <el-breadcrumb-item>工站概览/主仪表盘</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!-- 设备状态栏 -->
    <div class="status-bar">
      <div class="status-info">
        <span class="status-title">当前设备状态:</span>
        <span class="status-value">{{ deviceStatusText }}</span>
      </div>
      <div class="indicator-container">
        <div class="indicator" :class="{ active: deviceStatus === 'running' }">
          <div class="light green"></div>
          <span class="label">运行</span>
        </div>
        <div class="indicator" :class="{ active: deviceStatus === 'stopped' }">
          <div class="light yellow"></div>
          <span class="label">停止</span>
        </div>
        <div class="indicator" :class="{ active: deviceStatus === 'fault' }">
          <div class="light red"></div>
          <span class="label">故障</span>
        </div>
      </div>
      <div class="real-time">
        <span class="time">{{ currentTime }}</span>
        <span class="date">{{ currentDate }}</span>
      </div>
    </div>
    <!-- KPI卡片区域 -->
    <div class="kpi-container">
      <!-- OEE卡片 -->
      <el-card class="kpi-card oee-card">
        <template #header>
          <div class="card-header">
            <div class="card-title">
              <el-icon class="card-icon">
                <DataAnalysis />
              </el-icon>
              <span>设备整体效率 (OEE)</span>
            </div>
            <el-tag :type="getOeeTagType(oee)" effect="dark" round class="card-tag">
              {{ (oee * 100).toFixed(1) }}%
            </el-tag>
          </div>
        </template>
        <div class="card-content">
          <div class="kpi-item">
            <div class="kpi-info">
              <el-icon class="kpi-icon">
                <Opportunity />
              </el-icon>
              <div class="kpi-label">当前产能</div>
            </div>
            <div class="kpi-value-container">
              <div class="kpi-value">{{ currentCapacity }}</div>
              <div class="kpi-unit">件/小时</div>
            </div>
          </div>
          <div class="kpi-item">
            <div class="kpi-info">
              <el-icon class="kpi-icon">
                <SuccessFilled />
              </el-icon>
              <div class="kpi-label">当日合格率</div>
            </div>
            <div class="kpi-value-container">
              <div class="kpi-value">{{ (yieldRate * 100).toFixed(1) }}</div>
              <div class="kpi-unit">%</div>
            </div>
          </div>
          <div class="kpi-item">
            <div class="kpi-info">
              <el-icon class="kpi-icon">
                <WarningFilled />
              </el-icon>
              <div class="kpi-label">故障停机时间</div>
            </div>
            <div class="kpi-value-container">
              <div class="kpi-value">{{ formatDowntime(downtime) }}</div>
            </div>
          </div>
        </div>

      </el-card>

      <!-- MTBF/MTTR卡片 -->
      <el-card class="kpi-card reliability-card">
        <template #header>
          <div class="card-header">
            <div class="card-title">
              <el-icon class="card-icon">
                <Timer />
              </el-icon>
              <span>设备可靠性指标</span>
            </div>
            <el-tag type="info" effect="dark" round class="card-tag">MTBF/MTTR</el-tag>
          </div>
        </template>
        <div class="card-content">
          <div class="kpi-item">
            <div class="kpi-info">
              <el-icon class="kpi-icon">
                <Lightning />
              </el-icon>
              <div class="kpi-label">当前能耗</div>
            </div>
            <div class="kpi-value-container">
              <div class="kpi-value">{{ currentPower }}</div>
              <div class="kpi-unit">kW</div>
            </div>
          </div>
          <div class="kpi-item">
            <div class="kpi-info">
              <el-icon class="kpi-icon">
                <DataLine />
              </el-icon>
              <div class="kpi-label">累计能耗</div>
            </div>
            <div class="kpi-value-container">
              <div class="kpi-value">{{ totalEnergy }}</div>
              <div class="kpi-unit">kWh</div>
            </div>
          </div>
        </div>

      </el-card>
    </div>
    <!-- 图形显示 -->
    <div id="chart" class="chart"></div>
    <!-- 最新事件/报警列表 -->
    <el-card class="event-card">
      <template #header>
        <div class="card-header">
          <div class="card-title">
            <el-icon class="card-icon">
              <Bell />
            </el-icon>
            <span>最新事件与报警</span>
          </div>
          <el-link type="primary" :underline="false" @click="goToAlarmCenter">
            查看全部 <el-icon>
              <ArrowRight />
            </el-icon>
          </el-link>
        </div>
      </template>
      <el-table :data="alarmList" style="width: 100%" :show-header="false" @row-click="handleRowClick">
        <el-table-column prop="time" label="时间" width="120">
          <template #default="{ row }">
            <div class="alarm-time">{{ row.time }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="getAlarmTagType(row.level)" size="small" effect="plain">
              {{ row.type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="content" label="内容">
          <template #default="{ row }">
            <div class="alarm-content">{{ row.content }}</div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ArrowRight, DataAnalysis,Opportunity,SuccessFilled,WarningFilled,Timer,Lightning,DataLine, Bell } from '@element-plus/icons-vue'
import { ref, onMounted, onBeforeUnmount, computed, getCurrentInstance } from 'vue'
import { useRouter } from 'vue-router'

// 设备状态（模拟数据，实际应从API获取）
const deviceStatus = ref('running') // running/stopped/fault

// 计算设备状态文本
const deviceStatusText = computed(() => {
  switch (deviceStatus.value) {
    case 'running': return '运行中'
    case 'stopped': return '已停止'
    case 'fault': return '故障中'
    default: return '未知状态'
  }
})

// 实时时间
const currentTime = ref('')
const currentDate = ref('')

// 更新时间函数
function updateTime() {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString()
  currentDate.value = now.toLocaleDateString()
}

// OEE相关数据
const oee = ref(0.82) // OEE值，范围0-1
const currentCapacity = ref(120) // 当前产能
const yieldRate = ref(0.95) // 合格率
const downtime = ref(126) // 故障停机时间（分钟）

// MTBF/MTTR相关数据
const currentPower = ref(45.6) // 当前功率（kW）
const totalEnergy = ref(12560) // 累计能耗（kWh）




// 格式化停机时间
const formatDowntime = (minutes) => {
  if (minutes < 60) {
    return `${minutes}分钟`
  } else {
    const hours = (minutes / 60).toFixed(1)
    return `${hours}小时`
  }
}

// 根据OEE值获取标签类型
const getOeeTagType = (value) => {
  if (value >= 0.85) return 'success'
  if (value >= 0.7) return 'warning'
  return 'danger'
}

// 定时器
let timer

onMounted(() => {
  // 初始化时间
  updateTime()
  // 设置定时器每秒更新时间
  timer = setInterval(updateTime, 1000)
  
  // 模拟数据变化（实际应用中应从API获取）
  // setInterval(() => {
  //   oee.value = Math.min(0.95, Math.max(0.6, oee.value + (Math.random() - 0.5) * 0.05))
  //   currentCapacity.value = Math.round(100 + Math.random() * 50)
  // }, 5000)
})

onBeforeUnmount(() => {
  // 清除定时器
  clearInterval(timer)
})


// 获取当前实例
const { proxy } = getCurrentInstance();
const colors = ['#5470C6', '#91CC75', '#EE6666'];
let option1 = { 
  color: colors,
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross'
    }
  },
  grid: {
    right: '20%'
  },
  toolbox: {
    feature: {
      dataView: { show: true, readOnly: false },
      restore: { show: true },
      saveAsImage: { show: true }
    }
  },
  legend: {
    data: ['振动', '电流', '温度']
  },
  xAxis: [
    {
      type: 'category',
      axisTick: {
        alignWithLabel: true
      },
      // prettier-ignore
      data: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    }
  ],
  yAxis: [
    {
      type: 'value',
      name: '振动',
      position: 'right',
      alignTicks: true,
      axisLine: {
        show: true,
        lineStyle: {
          color: colors[0]
        }
      },
      axisLabel: {
        formatter: '{value} μm'
      }
    },
    {
      type: 'value',
      name: '电流',
      position: 'right',
      alignTicks: true,
      offset: 80,
      axisLine: {
        show: true,
        lineStyle: {
          color: colors[1]
        }
      },
      axisLabel: {
        formatter: '{value} A'
      }
    },
    {
      type: 'value',
      name: '温度',
      position: 'left',
      alignTicks: true,
      axisLine: {
        show: true,
        lineStyle: {
          color: colors[2]
        }
      },
      axisLabel: {
        formatter: '{value} °C'
      }
    }
  ],
  series: [
    {
      name: '振动',
      type: 'bar',
      data: [
        2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 35.6, 162.2, 32.6, 20.0, 6.4, 3.3
      ]
    },
    {
      name: '电流',
      type: 'bar',
      yAxisIndex: 1,
      data: [
        2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3
      ]
    },
    {
      name: '温度',
      type: 'line',
      yAxisIndex: 2,
      data: [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2]
    }
  ]
};

// 页面渲染完运行
onMounted(() => {
    proxy.$echarts('chart',option1)

})


// 添加报警列表数据
const alarmList = ref([
  {
    id: 1,
    time: '08:23:45',
    type: '报警',
    level: 'high',
    content: '设备1温度超过阈值(85°C)'
  },
  {
    id: 2,
    time: '09:12:33',
    type: '事件',
    level: 'medium',
    content: '设备B完成自动校准'
  },
  {
    id: 3,
    time: '10:45:21',
    type: '报警',
    level: 'high',
    content: '传送带速度异常波动'
  },
  {
    id: 4,
    time: '11:30:15',
    type: '提醒',
    level: 'low',
    content: '设备C需要例行维护'
  },
  {
    id: 5,
    time: '12:05:42',
    type: '事件',
    level: 'medium',
    content: '生产批次12345已完成'
  }
])

// 获取报警标签类型
const getAlarmTagType = (level) => {
  switch (level) {
    case 'high': return 'danger'
    case 'medium': return 'warning'
    case 'low': return 'info'
    default: return ''
  }
}
const router = useRouter()
// 跳转到报警中心
const goToAlarmCenter = () => {
  // 这里替换为实际的路由跳转逻辑
  console.log('跳转到报警与事件中心')
  router.push('/alarm_list')
}

</script>

<style scoped lang="scss">
.dashboard-container {
  padding: 20px;
  background-color: #f5f7fa;
  height: calc(100vh - 100px); // 减去padding
  overflow-y: auto;
  box-sizing: border-box; // 确保padding包含在高度内
}

/* 状态栏样式 */
.status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.status-info {
  display: flex;
  align-items: center;
}

.status-title {
  font-weight: bold;
  margin-right: 10px;
  color: #333;
  font-size: 15px;
}

.status-value {
  color: #409EFF;
  font-weight: bold;
  font-size: 15px;
}

.real-time {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f0f7ff;
  padding: 8px 15px;
  border-radius: 8px;
}

.time {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.date {
  font-size: 13px;
  color: #666;
}

/* 指示灯容器 */
.indicator-container {
  display: flex;
  gap: 20px;
}

.indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  opacity: 0.3;
  transition: all 0.3s;
  padding: 8px 12px;
  border-radius: 8px;
}

.indicator.active {
  opacity: 1;
  background-color: rgba(245, 245, 245, 0.8);
  transform: translateY(-2px);
}

.light {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin-bottom: 5px;
  box-shadow: 0 0 8px currentColor;
  transition: all 0.3s;
}

.light.green {
  background-color: #67C23A;
  color: #67C23A;
}

.light.yellow {
  background-color: #E6A23C;
  color: #E6A23C;
}

.light.red {
  background-color: #F56C6C;
  color: #F56C6C;
}

.label {
  font-size: 13px;
  color: #666;
  font-weight: 500;
}

/* KPI卡片区域 */
.kpi-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.kpi-card {
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  border: none;
  transition: transform 0.3s, box-shadow 0.3s;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 18px 0 rgba(0, 0, 0, 0.08);
  }
  
  :deep(.el-card__header) {
    padding: 18px 20px;
    border-bottom: 1px solid #f0f0f0;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  display: flex;
  align-items: center;
  font-weight: 600;
  color: #333;
  font-size: 16px;
  
  .card-icon {
    margin-right: 10px;
    font-size: 18px;
    color: var(--el-color-primary);
  }
}

.card-tag {
  font-weight: bold;
  font-size: 13px;
}

.card-content {
  padding: 15px 20px;
}

.kpi-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
  padding-bottom: 18px;
  border-bottom: 1px dashed #eee;
  
  &:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
  }
}

.kpi-info {
  display: flex;
  align-items: center;
  flex: 1;
}

.kpi-icon {
  margin-right: 12px;
  font-size: 18px;
  color: var(--el-color-primary);
}

.kpi-label {
  color: #666;
  font-size: 14px;
  font-weight: 500;
}

.kpi-value-container {
  display: flex;
  align-items: flex-end;
}

.kpi-value {
  font-weight: bold;
  font-size: 18px;
  color: #333;
  text-align: right;
}

.kpi-unit {
  font-size: 13px;
  color: #999;
  margin-left: 4px;
  margin-bottom: 2px;
}





/* 卡片主题样式 */
.oee-card {
  :deep(.el-card__header) {
    background: linear-gradient(90deg, rgba(64, 158, 255, 0.1) 0%, rgba(64, 158, 255, 0.05) 100%);
  }
}

.reliability-card {
  :deep(.el-card__header) {
    background: linear-gradient(90deg, rgba(103, 194, 58, 0.1) 0%, rgba(103, 194, 58, 0.05) 100%);
  }
}

.breadcrumb-container {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

// 图形
.chart {
    width: 100%;
    height: 300px;
    margin-top: 20px;

}
// 报警
.event-card {
  margin-top: 20px;
  border-radius: 12px;
  
  :deep(.el-card__header) {
    padding: 15px 20px;
    background: linear-gradient(90deg, rgba(245, 108, 108, 0.1) 0%, rgba(245, 108, 108, 0.05) 100%);
  }
  
  :deep(.el-table) {
    --el-table-border-color: transparent;
    --el-table-tr-bg-color: transparent;
  }
  
  :deep(.el-table__row) {
    cursor: pointer;
    
    &:hover {
      background-color: #f5f7fa;
    }
    
    td {
      padding: 12px 0;
    }
  }
}

.alarm-time {
  color: #666;
  font-size: 13px;
}

.alarm-content {
  font-size: 14px;
  color: #333;
}

/* 调整卡片标题样式 */
.card-header {
  .card-title {
    .card-icon {
      color: #f56c6c; /* 报警图标使用红色 */
    }
  }
}
</style>