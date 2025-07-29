<template>
    <div class="kpi-container">
        <el-breadcrumb :separator-icon="ArrowRight">
            <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
            <el-breadcrumb-item>数据管理</el-breadcrumb-item>
            <el-breadcrumb-item>统计报表与KPI分析</el-breadcrumb-item>
        </el-breadcrumb>

        <!-- 标题和操作按钮 -->
        <div class="header">
            <h2>统计报表与KPI分析</h2>
        </div>

        <!-- 查询条件区域 -->
        <div class="query-section">
            <el-form :model="queryParams" label-width="100px">
                <el-row :gutter="20">
                    <el-col :span="8">
                        <el-form-item label="时间范围">
                            <el-date-picker v-model="queryParams.timeRange" type="daterange" range-separator="至"
                                start-placeholder="开始日期" end-placeholder="结束日期" value-format="YYYY-MM-DD" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item label="时间粒度">
                            <el-select v-model="queryParams.timeGranularity" placeholder="请选择">
                                <el-option v-for="item in timeGranularityOptions" :key="item.value" :label="item.label"
                                    :value="item.value" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="4">
                        <el-button type="primary" @click="handleQuery">查询</el-button>
                        <el-button @click="resetQuery">重置</el-button>
                    </el-col>
                </el-row>
            </el-form>

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
            <!-- 小图表区域 -->
            <div class="sub-charts-container">
                <div class="sub-chart-card">
                    <div class="chart-title">产品产量分布</div>
                    <div id="chart1" class="sub-chart"></div>
                </div>
                <div class="sub-chart-card">
                    <div class="chart-title">停机原因占比</div>
                    <div id="chart2" class="sub-chart"></div>
                </div>
                <div class="sub-chart-card">
                    <div class="chart-title">合格品/不合格品比例</div>
                    <div id="chart3" class="sub-chart"></div>
                </div>
            </div>
        </div>
    </div>

</template>


<script setup>
import { ArrowRight, } from '@element-plus/icons-vue'
import { ref,onMounted,getCurrentInstance  } from 'vue'



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
  { value: 'day', label: '日' },
  { value: 'month', label: '月' },
  { value: 'year', label: '年' }
]


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


// 获取当前实例
const { proxy } = getCurrentInstance();
// 产品产量分布
let option1 = {
  xAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [120, 200, 150, 80, 70, 110, 130],
      type: 'bar'
    }
  ]
};

// 停机原因占比
let option2 = {
    // title: {
    //     text: '停机原因占比分析',
    //     subtext: '各停机原因所占比例',
    //     left: 'center'
    // },
    tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data: ['设备故障', '计划维护', '原料短缺', '电力中断', '人为操作失误', '其他']
    },
    series: [
        {
            name: '停机原因',
            type: 'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
            },
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '18',
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            data: [
                {value: 35, name: '设备故障'},
                {value: 25, name: '计划维护'},
                {value: 15, name: '原料短缺'},
                {value: 10, name: '电力中断'},
                {value: 10, name: '人为操作失误'},
                {value: 5, name: '其他'}
            ]
        }
    ],
    color: ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83']
};

// 合格品/不合格品比例
let option3 = {
  tooltip: {
    trigger: 'item'
  },
  legend: {
    top: '5%',
    left: 'center'
  },
  series: [
    {
      name: 'Access From',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 40,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: 1048, name: '合格' },
        { value: 735, name: '不合格' },
      ]
    }
  ]
};


// 页面渲染完运行
onMounted(() => {
    proxy.$echarts('chart1', option1);
    proxy.$echarts('chart2', option2);
    proxy.$echarts('chart3', option3);
  
});


</script>


<style scoped>
.kpi-container{
  padding: 20px; 
  background-color: #f5f7fa;
  height: 80vh;
  overflow-y: auto;
}
.query-section {
  background-color: #fff;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
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
.sub-charts-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.sub-chart-card {
  padding: 15px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  transition: all 0.3s;
}

.sub-chart-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 21, 41, 0.1);
}
.sub-chart {
  width: 100%;
  height: 250px;
}

</style>