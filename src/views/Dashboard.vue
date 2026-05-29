<template>
  <div class="dashboard">
    <h2 class="page-title">导航台</h2>
    
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :lg="6">
        <div class="stat-card stat-primary">
          <div class="stat-icon">
            <el-icon size="40"><Document /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats?.today_reports || 0 }}</div>
            <div class="stat-label">今日报卡</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :lg="6">
        <div class="stat-card stat-warning">
          <div class="stat-icon">
            <el-icon size="40"><Clock /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats?.pending_reviews || 0 }}</div>
            <div class="stat-label">待审核</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :lg="6">
        <div class="stat-card stat-success">
          <div class="stat-icon">
            <el-icon size="40"><Folder /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats?.monthly_total || 0 }}</div>
            <div class="stat-label">本月累计</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :lg="6">
        <div class="stat-card stat-info">
          <div class="stat-icon">
            <el-icon size="40"><CircleCheck /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats?.approved_rate || 0 }}%</div>
            <div class="stat-label">审核通过率</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :xs="24" :lg="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>近7天报卡趋势</span>
            </div>
          </template>
          <div ref="trendChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :lg="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>感染类型分布</span>
            </div>
          </template>
          <div ref="distributionChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="todo-card">
      <template #header>
        <div class="card-header">
          <span>待审核列表</span>
          <el-button type="primary" link @click="$router.push('/infection-report?status=pending')">
            查看更多
          </el-button>
        </div>
      </template>
      <el-table :data="pendingReports" v-loading="loading">
        <el-table-column prop="report_no" label="报卡编号" width="150" />
        <el-table-column prop="patient_name" label="患者姓名" width="120" />
        <el-table-column prop="department" label="科室" width="150" />
        <el-table-column prop="infection_type" label="感染类型" width="150" />
        <el-table-column prop="report_date" label="报告日期" width="120" />
        <el-table-column prop="reporter" label="报告人" width="120" />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="$router.push(`/infection-report/${row.id}`)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useReportStore } from '../stores/report';
import * as echarts from 'echarts';
import type { ECharts } from 'echarts';

const authStore = useAuthStore();
const reportStore = useReportStore();

const trendChartRef = ref<HTMLDivElement | null>(null);
const distributionChartRef = ref<HTMLDivElement | null>(null);
let trendChart: ECharts | null = null;
let distributionChart: ECharts | null = null;

const stats = computed(() => reportStore.stats);
const pendingReports = computed(() => reportStore.reports.slice(0, 5));
const loading = computed(() => reportStore.loading);

onMounted(async () => {
  if (!authStore.token) {
    return;
  }
  await fetchData();
  initCharts();
});

const fetchData = async () => {
  if (!authStore.token) {
    return;
  }
  try {
    await Promise.all([
      reportStore.fetchStats(),
      reportStore.fetchReports({ status: 'pending', limit: 5 }),
    ]);
  } catch (error) {
    console.error('Failed to fetch data:', error);
  }
};

const initCharts = () => {
  if (trendChartRef.value) {
    trendChart = echarts.init(trendChartRef.value);
    updateTrendChart();
  }
  
  if (distributionChartRef.value) {
    distributionChart = echarts.init(distributionChartRef.value);
    updateDistributionChart();
  }
};

const updateTrendChart = () => {
  if (!trendChart || !stats.value) return;
  
  const option = {
    tooltip: {
      trigger: 'axis',
    },
    xAxis: {
      type: 'category',
      data: stats.value.weekly_trend.map(item => item.date),
    },
    yAxis: {
      type: 'value',
      name: '报卡数',
    },
    series: [
      {
        name: '报卡数',
        type: 'line',
        smooth: true,
        data: stats.value.weekly_trend.map(item => item.count),
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(30, 64, 175, 0.3)' },
            { offset: 1, color: 'rgba(30, 64, 175, 0.05)' },
          ]),
        },
        lineStyle: {
          color: '#1E40AF',
          width: 3,
        },
        itemStyle: {
          color: '#1E40AF',
        },
      },
    ],
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
  };
  
  trendChart.setOption(option);
};

const updateDistributionChart = () => {
  if (!distributionChart || !stats.value) return;
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)',
    },
    legend: {
      orient: 'vertical',
      left: 'left',
    },
    series: [
      {
        name: '感染类型',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: {
          show: false,
          position: 'center',
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold',
          },
        },
        labelLine: {
          show: false,
        },
        data: stats.value.infection_type_distribution.map((item, index) => ({
          value: item.count,
          name: item.type,
          itemStyle: {
            color: ['#1E40AF', '#0891B2', '#059669', '#DC2626', '#D97706'][index % 5],
          },
        })),
      },
    ],
  };
  
  distributionChart.setOption(option);
};

watch(
  () => stats.value,
  () => {
    updateTrendChart();
    updateDistributionChart();
  },
  { deep: true }
);
</script>

<style scoped>
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

.page-title {
  font-size: 24px;
  color: #1E293B;
  margin-bottom: 24px;
  font-weight: 600;
}

.stats-row {
  margin-bottom: 24px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 24px;
  border-radius: 12px;
  color: white;
  margin-bottom: 20px;
}

.stat-primary {
  background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
}

.stat-warning {
  background: linear-gradient(135deg, #D97706 0%, #F59E0B 100%);
}

.stat-success {
  background: linear-gradient(135deg, #059669 0%, #10B981 100%);
}

.stat-info {
  background: linear-gradient(135deg, #0891B2 0%, #06B6D4 100%);
}

.stat-icon {
  margin-right: 20px;
  opacity: 0.9;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.chart-card {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #1E293B;
}

.chart-container {
  width: 100%;
  height: 300px;
}

.todo-card {
  margin-top: 24px;
}
</style>
