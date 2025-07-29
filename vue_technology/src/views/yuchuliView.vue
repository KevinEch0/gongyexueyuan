<template>
  <div class="dashboard-container">
    <!-- 面包屑导航 -->
    <div class="breadcrumb-container">
      <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>可视化界面</el-breadcrumb-item>
        <el-breadcrumb-item>预处理图形</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 优化后的卡片容器 -->
    <div class="card-container">
      <el-card 
        v-for="(card, index) in cards" 
        :key="index" 
        class="preprocess-card"
        :style="{ '--card-color': cardColors[index] }"
        shadow="hover"
      >
        <template #header>
          <div class="card-header">
            <el-icon :size="20" class="card-icon">
              <component :is="cardIcons[index]" />
            </el-icon>
            <span>{{ card.name }}</span>
          </div>
        </template>
        
        <div class="card-content">
          <div class="card-description">
            {{ card.description }}
          </div>
          <div class="card-actions">
            <el-button 
              type="primary" 
              @click="showImage(index)"
              class="preprocess-btn"
              round
            >
              查看
              <el-icon class="btn-icon"><View /></el-icon>
            </el-button>

          </div>
        </div>
      </el-card>
    </div>

    <!-- 优化后的图片对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="`${cards[activeCardIndex].name} - 预处理`" 
      width="70%"
      class="image-dialog"
      top="5vh"
    >
      <div class="image-dialog-content">
        <img 
          :src="imagePath" 
          class="preview-image" 
          v-if="dialogVisible" 
          :alt="`${cards[activeCardIndex].name}预处理结果`"
        />
        <div class="algorithm-description">
          <h3>预处理介绍</h3>
          <p>{{ cards[activeCardIndex].fullDescription }}</p>

        </div>
      </div>
      
      <template #footer>
        <el-button 
          @click="dialogVisible = false" 
          class="dialog-btn"
          plain
        >
          关闭
        </el-button>

      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { 
  ArrowRight,
  View,
  Connection,
  Clock,
  PieChart,
  User,
  TrendCharts,
  MagicStick
} from '@element-plus/icons-vue';

// 卡片数据
const cards = ref([
  { 
    name: '缺失值处理',
    fullDescription: '删除法：直接删除包含缺失值的行或列。填充法：均值、中位数、众数填充（适用于数值型数据）。插值法：如线性插值、样条插值。模型预测填充：如用回归模型等预测缺失值',


  },
  { 
    name: '异常值处理：基于统计的方法',
    fullDescription: 'IQR（四分位距）原则是一种基于数据分位数的异常值检测方法，适用于非正态分布的数据。它通过计算数据的第一四分位数（Q1）和第三四分位数（Q3），得到四分位距（IQR = Q3 - Q1），然后将低于 Q1 减去 1.5 倍 IQR 或高于 Q3 加上 1.5 倍 IQR 的数据点视为异常值，这种方法对极端值具有较强的鲁棒性。3σ原则则适用于近似正态分布的数据，基于均值（μ）和标准差（σ）计算，认为超过 μ ± 3σ 范围的数据为异常值，这一范围包含了正态分布中约99.7%的数据，因此该方法主要用来识别偏离均值极远的异常点。两者在实际应用中根据数据分布特征选择使用，IQR适合偏态或不规则分布，而3σ适合钟形对称的正态数据。',
  },
  { 
    name: '异常值处理：基于算法的方法-孤立森林',
    fullDescription: '孤立森林：不支持分类或回归，是一种专门用于无监督异常检测的算法，不属于传统意义上的分类或回归方法。它的核心思想是通过构建多个随机树来“隔离”样本点，异常值因为更容易被分割（路径更短）而获得更高的异常评分。这种方法计算效率高、可扩展性强，尤其适合在缺乏标签的情况下识别工业设备异常、信用卡欺诈等问题。',
  },
  { 
    name: '异常值处理：基于算法的方法-KNN',
    fullDescription: 'knn：功能：分类一种简单直观但非常有效的监督学习方法。它的核心思想是：对一个未知样本，查找训练集中与它最“接近”的 K 个样本，根据这些邻居中出现最多的类别来决定该样本的分类。比如，在工业故障检测中，若一个新样本的周围大多数是“异常”标签样本，则它也会被判断为异常。KNN 不依赖训练过程，而是在预测时计算样本之间的距离，因此适用于样本量不大、特征维度较低的分类任务，尤其在样本分布较为清晰时表现良好。',
  },
  { 
    name: '数据转换',
    fullDescription: '归一化（Min-Max Scaling）：将数值缩放到 [0, 1] 区间。标准化（Z-score Scaling）：均值为0，方差为1。对数变换：处理右偏分布（如 log(x + 1)）',
  },
  { 
    name: '特征选择：减少维度，提升模型泛化能力。',

    fullDescription: 'nnpca ：功能：降维，在分类或回归前，可以用 NNPCA 对高维特征（如传感器数据）进行降维，提取关键变量，减少噪声、提升模型效果是一种用于降维和特征提取的无监督学习方法，它结合了传统PCA和神经网络结构的优点。与传统线性PCA不同，NNPCA利用非线性神经网络来学习数据中的主成分，能更好地保留原始数据的复杂结构。它本质上不属于分类或回归算法，而是用于将高维数据压缩到低维空间，常作为异常检测、可视化或下游模型建模的预处理手段',

  },
]);

// 卡片图标
const cardIcons = [
  MagicStick,
  Connection,
  PieChart,
  TrendCharts,
  Clock,
  User
];

// 卡片颜色
const cardColors = [
  '#409EFF',
  '#67C23A',
  '#E6A23C',
  '#F56C6C',
  '#909399',
  '#8E44AD'
];

// 图片路径
const imagePaths = [
  require('../assets/预处理/1.png'),
  require('../assets/预处理/2.png'),
  require('../assets/预处理/3.png'),
  require('../assets/预处理/4.png'),
  require('../assets/预处理/5.png'),
  require('../assets/预处理/6.png'),
];

const dialogVisible = ref(false);
const activeCardIndex = ref(0);
const imagePath = ref('');

const showImage = (index) => {
  activeCardIndex.value = index;
  imagePath.value = imagePaths[index];
  dialogVisible.value = true;
};

</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.breadcrumb-container {
  margin-bottom: 20px;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.preprocess-card {
  height: 280px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  border-top: 4px solid var(--card-color);
}

.preprocess-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.card-header {
  font-weight: bold;
  font-size: 18px;
  color: var(--card-color);
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-icon {
  margin-right: 8px;
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 0 15px 15px;
}

.card-description {
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
  flex-grow: 1;
}

.card-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preprocess-btn {
  background-color: var(--card-color);
  border-color: var(--card-color);
  padding: 12px 24px;
  font-size: 16px;
  transition: all 0.3s;
}

.preprocess-btn:hover {
  opacity: 0.9;
  transform: scale(1.05);
}

.btn-icon {
  margin-left: 6px;
}

.card-tag {
  color: white;
  border: none;
  margin-left: 10px;
}

.image-dialog-content {
  display: flex;
  gap: 20px;
}

.preview-image {
  max-width: 60%;
  max-height: 70vh;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  object-fit: contain;
}

.algorithm-description {
  flex: 1;
  padding: 0 15px;
}

.algorithm-description h3 {
  color: var(--el-color-primary);
  margin-bottom: 15px;
}

.algorithm-description p {
  line-height: 1.6;
  margin-bottom: 20px;
}



/* 响应式调整 */
@media (max-width: 992px) {
  .image-dialog-content {
    flex-direction: column;
  }
  
  .preview-image {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .card-container {
    grid-template-columns: 1fr;
  }
  
  .preprocess-card {
    height: 260px;
  }
  
  .card-actions {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .card-tag {
    margin-left: 0;
  }
}
</style>