<template>
  <div class="report-list">
    <div class="page-header">
      <h2 class="page-title">院感报卡</h2>
      <el-button type="primary" @click="$router.push('/infection-report/new')">
        <el-icon><Plus /></el-icon>
        新增报卡
      </el-button>
    </div>

    <el-card>
      <div class="filter-bar">
        <el-select v-model="filterStatus" placeholder="状态筛选" clearable @change="handleFilterChange">
          <el-option label="全部" value="" />
          <el-option label="待审核" value="pending" />
          <el-option label="已通过" value="approved" />
          <el-option label="已驳回" value="rejected" />
          <el-option label="已退回" value="returned" />
        </el-select>
        <el-button @click="handleReset">重置</el-button>
      </div>

      <el-table :data="reports" v-loading="loading">
        <el-table-column prop="report_no" label="报卡编号" width="180" />
        <el-table-column prop="patient_name" label="患者姓名" width="120" />
        <el-table-column prop="gender" label="性别" width="80" />
        <el-table-column prop="age" label="年龄" width="80" />
        <el-table-column prop="department" label="科室" width="150" />
        <el-table-column prop="infection_type" label="感染类型" width="150" />
        <el-table-column prop="report_date" label="报告日期" width="120">
          <template #default="{ row }">
            {{ row.report_date ? formatDate(row.report_date) : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="reporter" label="报告人" width="120" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="$router.push(`/infection-report/${row.id}`)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        style="margin-top: 20px; justify-content: flex-end"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useReportStore } from '../../stores/report';
import dayjs from 'dayjs';

const route = useRoute();
const reportStore = useReportStore();

const reports = computed(() => reportStore.reports);
const total = computed(() => reportStore.total);
const loading = computed(() => reportStore.loading);

const currentPage = ref(1);
const pageSize = ref(20);
const filterStatus = ref('');

onMounted(async () => {
  if (route.query.status) {
    filterStatus.value = route.query.status as string;
  }
  await fetchReports();
});

const fetchReports = async () => {
  try {
    await reportStore.fetchReports({
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      status: filterStatus.value || undefined,
    });
  } catch (error) {
    console.error('Failed to fetch reports:', error);
  }
};

const handleFilterChange = () => {
  currentPage.value = 1;
  fetchReports();
};

const handleReset = () => {
  filterStatus.value = '';
  currentPage.value = 1;
  fetchReports();
};

const handleSizeChange = () => {
  currentPage.value = 1;
  fetchReports();
};

const handleCurrentChange = () => {
  fetchReports();
};

const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD');
};

const getStatusType = (status: string) => {
  const types: Record<string, any> = {
    draft: 'info',
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
    returned: 'warning',
  };
  return types[status] || 'info';
};

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    draft: '草稿',
    pending: '待审核',
    approved: '已通过',
    rejected: '已驳回',
    returned: '已退回',
  };
  return texts[status] || status;
};
</script>

<style scoped>
.report-list {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  color: #1E293B;
  font-weight: 600;
  margin: 0;
}

.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}
</style>
