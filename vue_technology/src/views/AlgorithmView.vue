<template>
  <div class="algorithm-container">
    <el-breadcrumb :separator-icon="ArrowRight">
      <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
      <el-breadcrumb-item>算法管理</el-breadcrumb-item>
      <el-breadcrumb-item>算法列表</el-breadcrumb-item>
    </el-breadcrumb>
    
    <!-- 头部区域 -->
    <div class="header">
      <h2>算法列表</h2>
      <div class="actions">
        <el-input
          v-model="searchQuery"
          placeholder="搜索算法..."
          style="width: 300px; margin-right: 20px;"
          :prefix-icon="Search"
          clearable
        />
        <el-button type="info" @click="handleAutoSelect">自动选择算法</el-button>
      </div>
    </div>
    
    <!-- 筛选区域 -->
    <div class="filter-section">
      <el-radio-group v-model="filterType" @change="handleFilterChange">
        <el-radio-button label="all">全部</el-radio-button>
        <el-radio-button label="classification">分类算法</el-radio-button>
        <el-radio-button label="regression">回归算法</el-radio-button>
        <el-radio-button label="clustering">聚类算法</el-radio-button>
      </el-radio-group>
    </div>
    
    <!-- 算法卡片区域 -->
    <div class="algorithm-list">
      <el-row :gutter="20">
        <el-col 
          v-for="algorithm in filteredAlgorithms" 
          :key="algorithm.id" 
          :xs="24" 
          :sm="12" 
          :md="8" 
          :lg="6"
        >
          <el-card 
            class="algorithm-card" 
            :class="{ 'selected': selectedAlgorithm === algorithm.id }"
            @click="selectAlgorithm(algorithm.id)"
            shadow="hover"
          >
            <div class="card-header">
              <el-tag :type="getAlgorithmTypeTag(algorithm.type)">{{ algorithm.typeLabel }}</el-tag>
            </div>
            <h3>{{ algorithm.name }}</h3>
            <p class="description">{{ algorithm.description }}</p>
            <div class="card-footer">
              <el-button 
                type="primary" 
                size="small" 
                @click.stop="showDetails(algorithm)"
              >
                详情
              </el-button>
              <el-button 
                type="success" 
                size="small" 
                @click.stop="handleRun(algorithm)"
              >
                运行
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 详情对话框 -->
    <el-dialog 
      title="算法详情" 
      v-model="detailDialogVisible" 
      width="500px"
    >
      <div v-if="currentAlgorithm">
        <h3>{{ currentAlgorithm.name }}</h3>
        <p><strong>类型：</strong>{{ currentAlgorithm.typeLabel }}</p>
        <p><strong>核心思想：</strong>{{ currentAlgorithm.sixiang }}</p>
        <p><strong>优势：</strong>{{ currentAlgorithm.youshi}}</p>
        <p><strong>应用场景：</strong>{{ currentAlgorithm.yYONG}}</p>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ArrowRight, Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// 模拟算法数据
const algorithms = ref([
  { id: 1, name: '孤立森林', type: 'classification', 
    typeLabel: '分类', 
    sixiang: '孤立森林基于一个简单直观的假设：异常点通常稀少且与正常点差异较大，因此更容易被“孤立”。正常点：分布在密集区域，需要更多步骤才能将其隔离。异常点：分布在稀疏区域，只需少量步骤即可被隔离。算法通过随机划分（类似随机森林）的方式，计算每个样本被隔离所需的平均路径长度（即分割次数），路径越短，异常得分越高。',
    youshi: '1:计算效率高，特别适合高维数据集 2:无需预先定义正常数据的分布 3:对内存需求较低，适合大规模数据集分析',
    yYONG:'1:欺诈检测 2:网络入侵识别 3:工业设备异常监测 4:医疗异常病例筛查',
    description:'无监督的异常监测算法，适用于监测高维数据中的异常点'
   },
  { id: 2, name: 'LSTM', type: 'classification', 
    typeLabel: '分类', 
    description: '模型基于输入数据预测输出（即模型的前向计算过程）',
    sixiang: 'LSTM通过引入精妙设计的"门控机制"和"记忆单元"，能够选择性地记住或遗忘信息，从而有效捕捉长期依赖关系。与传统RNN的关键区区别:传统RNN：只有简单的重复模块（如tanh层），难以维持长期记忆,LSTM：包含复杂的记忆单元和三个门控结构（输入门、遗忘门、输出门）',
    youshi: '1:解决长期依赖问题：可以记住数百步前的信息 2:避免梯度消失：通过恒定误差传送带(CEC)机制 3:选择性记忆：智能决定记住/遗忘哪些信息 4:广泛适用性：在多种序列任务中表现优异',
    yYONG:'1:自然语言处理(NLP) 2:时间序列预测 3:语音识别 '
  },
  { id: 3, name: 'NNPCA', type: 'regression', typeLabel: '回归', description: '通过线性组合特征来预测连续值的简单算法',
    sixiang: 'NNPCA使用自编码器（Autoencoder）架构来学习数据的非线性主成分，相比传统PCA只能进行线性变换，NNPCA能够发现数据中更复杂的非线性结构。与传统PCA的关键区别: 传统PCA：基于线性变换，通过特征分解找到最大方差方向 NNPCA：通过神经网络实现非线性变换，能捕捉更复杂的数据结构',
    youshi: '1:非线性特征提取：能发现数据中非线性关系 2:灵活性：可通过网络结构设计适应不同数据特性 3:端到端学习：无需手动设计特征变换 4:大数据适应性：适合处理高维复杂数据',
    yYONG:'1:高维数据可视化 2:特征提取与降维 3:数据去噪 4:生物信息学中的基因表达分析 5:图像压缩与重建 '    
  },
  { id: 4, name: 'KNN 异常检测', type: 'clustering', typeLabel: '聚类', description: '将数据划分为K个簇的无监督学习算法',
    sixiang: 'KNN异常检测通过计算每个数据点与其K个最近邻的距离来衡量该点的异常程度：正常点：与K个邻居的距离较小（位于密集区域） 异常点：与K个邻居的距离较大（位于稀疏区域）',
    youshi: '1:直观易懂：基于简单的距离概念 2:无参数假设：不对数据分布做任何假设 3:适用性广：可用于各种数据类型 4:可解释性强：异常原因可追溯为"远离多数点" ',
    yYONG:'1:金融欺诈检测 2:网络入侵识别 3:工业设备异常监控 4:医疗异常病例筛查 5:数据清洗（识别错误记录）'
   },
  { id: 5, name: 'SOM', type: 'clustering', typeLabel: '聚类', description: '用于二分类问题的线性模型',
    sixiang: 'SOM模拟了人脑神经元的自组织特性，通过竞争学习（Competitive Learning）使相似的输入数据在输出空间（映射空间）中彼此靠近，从而形成 有序的特征映射。竞争机制：神经元（节点）竞争对输入数据的响应权，获胜的神经元（Best Matching Unit, BMU）及其邻近神经元会调整权重，使其更接近输入数据。拓扑保持：高维空间中相似的数据点在低维映射中也会相邻。',
    youshi: '1:降维可视化：将高维数据映射到 2D/3D 网格，便于观察数据分布。 2:拓扑保持性：相似数据在 SOM 上位置相近。 3:无监督学习：无需标签，自动发现数据内在结构。 4:聚类能力：可用于数据分组，类似 K-Means，但更适用于非线性数据。',
    yYONG:'1:数据可视化：探索高维数据的结构（如基因表达数据、市场细分） 2:聚类分析：替代 K-Means，处理非线性数据。 3:异常检测：异常点在 SOM 上远离主要聚类区域。 4:图像压缩：用 SOM 学习颜色表，减少颜色数量。 5:推荐系统：用户/商品特征映射，发现相似用户。'
   },
  { id: 6, name: '梯度提升树', type: 'regression', typeLabel: '回归', description: '通过迭代地添加决策树来改进预测的集成方法',
    sixiang: 'GBDT 基于 Boosting（提升） 思想，采用 梯度下降（Gradient Descent） 优化损失函数：逐步优化：每次训练一个新的决策树，拟合前一轮的 残差（预测误差）。梯度下降：用损失函数的负梯度（近似残差）指导模型优化。模型组合：所有树的预测结果 加权求和，得到最终预测。',
    youshi: '1:高精度：在结构化数据上通常优于随机森林、SVM等算法。 2:灵活性：支持自定义损失函数（回归、分类、排序均可）。 3:特征重要性：可评估特征对模型的贡献度。4: 鲁棒性：对异常值和缺失值有一定容忍度。',
    yYONG:'1:回归问题：房价预测、销量预测 2:分类问题：广告点击率预测、金融风控 3:排序任务：搜索引擎、推荐系统 4:特征工程：生成特征重要性，辅助特征选择'
   }
])

const searchQuery = ref('')
const filterType = ref('all')
const selectedAlgorithm = ref(null)

// 详情对话框控制
const detailDialogVisible = ref(false)
const currentAlgorithm = ref(null)

// 过滤算法列表
const filteredAlgorithms = computed(() => {
  let result = algorithms.value
  if (filterType.value !== 'all') {
    result = result.filter(item => item.type === filterType.value)
  }
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(item => 
      item.name.toLowerCase().includes(query) || 
      item.description.toLowerCase().includes(query)
    )
  }
  return result
})

// 选择算法
const selectAlgorithm = (id) => {
  selectedAlgorithm.value = selectedAlgorithm.value === id ? null : id
}

// 显示详情
const showDetails = (algorithm) => {
  currentAlgorithm.value = algorithm
  detailDialogVisible.value = true
}

// 获取算法类型对应的标签样式
const getAlgorithmTypeTag = (type) => {
  const map = {
    classification: 'success',
    regression: 'warning',
    clustering: 'info'
  }
  return map[type] || ''
}

// 运行算法
const handleRun = (algorithm) => {
  ElMessage.success(`运行算法: ${algorithm.name}`)
}

// 自动选择算法
const handleAutoSelect = () => {
  ElMessage.info('自动选择算法逻辑执行')
}

// 筛选变更
const handleFilterChange = () => {
  selectedAlgorithm.value = null
}
</script>

<style scoped>
.algorithm-container {
  padding: 20px;
  background-color: #f5f7fa;
  height: 80vh;
  overflow-y: auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 20px 0;
}

.algorithm-list {
  margin-top: 30px;
}

.algorithm-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.algorithm-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.algorithm-card.selected {
  border: 2px solid var(--el-color-primary);
  background-color: rgba(64, 158, 255, 0.05);
}

.card-header {
  margin-bottom: 10px;
}

.description {
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin: 10px 0;
  height: 60px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;

}

.card-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}
</style>