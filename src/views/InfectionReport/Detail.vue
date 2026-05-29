<template>
  <div class="report-detail">
    <div class="page-header">
      <h2 class="page-title">报卡详情</h2>
      <div class="header-actions">
        <el-button @click="$router.back()">
          <el-icon><Back /></el-icon>
          返回
        </el-button>
        <el-button
          type="primary"
          v-if="canEdit"
          @click="$router.push(`/infection-report/${report?.id}/edit`)"
        >
          编辑
        </el-button>
        <el-button
          type="danger"
          v-if="canDelete"
          @click="handleDelete"
        >
          删除
        </el-button>
      </div>
    </div>

    <el-row :gutter="20">
      <el-col :xs="24" :lg="16">
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span>报卡信息</span>
              <el-tag :type="getStatusType(report?.status || '')" size="large">
                {{ getStatusText(report?.status || '') }}
              </el-tag>
            </div>
          </template>

          <el-descriptions :column="2" border>
            <el-descriptions-item label="报卡编号">
              {{ report?.report_no }}
            </el-descriptions-item>
            <el-descriptions-item label="报告日期">
              {{ report?.report_date ? formatDate(report.report_date) : '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="患者姓名">
              {{ report?.patient_name }}
            </el-descriptions-item>
            <el-descriptions-item label="患者ID">
              {{ report?.patient_id }}
            </el-descriptions-item>
            <el-descriptions-item label="性别">
              {{ report?.gender === 'male' ? '男' : report?.gender === 'female' ? '女' : '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="年龄">
              {{ report?.age || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="科室">
              {{ report?.department || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="感染类型">
              {{ report?.infection_type || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="感染日期">
              {{ report?.infection_date ? formatDate(report.infection_date) : '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="报告人">
              {{ report?.reporter || '-' }}
            </el-descriptions-item>
          </el-descriptions>

          <el-divider />

          <el-descriptions :column="1" border>
            <el-descriptions-item label="诊断">
              {{ report?.diagnosis || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="症状">
              {{ report?.symptoms || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="治疗措施">
              {{ report?.treatment || '-' }}
            </el-descriptions-item>
          </el-descriptions>

          <template v-if="report?.review_comment">
            <el-divider />
            <div class="review-section">
              <h4>审核意见</h4>
              <p>{{ report.review_comment }}</p>
              <div class="review-info">
                <span>审核人: {{ report.reviewer }}</span>
                <span v-if="report.review_date">审核时间: {{ formatDateTime(report.review_date) }}</span>
              </div>
            </div>
          </template>
        </el-card>

        <el-card class="action-card" v-if="canReview">
          <template #header>
            <div class="card-header">
              <span>审核操作</span>
            </div>
          </template>
          
          <el-form :model="reviewForm" label-width="80px">
            <el-form-item label="审核意见">
              <el-input
                v-model="reviewForm.comment"
                type="textarea"
                :rows="3"
                placeholder="请输入审核意见"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="success" @click="handleApprove">审核通过</el-button>
              <el-button type="warning" @click="handleReturn">退回修改</el-button>
              <el-button type="danger" @click="handleReject">驳回</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="8">
        <el-card class="timeline-card">
          <template #header>
            <div class="card-header">
              <span>操作时间轴</span>
            </div>
          </template>
          
          <div class="timeline">
            <el-timeline>
              <el-timeline-item
                v-for="item in timeline"
                :key="item.id"
                :timestamp="formatDateTime(item.timestamp)"
                :color="getTimelineColor(item.action)"
                placement="top"
              >
                <el-card>
                  <h4>{{ item.action }}</h4>
                  <p v-if="item.actor">操作人: {{ item.actor }}</p>
                  <p v-if="item.comment">说明: {{ item.comment }}</p>
                  <p v-if="item.previous_status || item.new_status" class="status-change">
                    {{ getStatusText(item.previous_status || '') }}
                    <el-icon><Right /></el-icon>
                    {{ getStatusText(item.new_status || '') }}
                  </p>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useReportStore } from '../../stores/report';
import { useAuthStore } from '../../stores/auth';
import dayjs from 'dayjs';

const route = useRoute();
const router = useRouter();
const reportStore = useReportStore();
const authStore = useAuthStore();

const reviewForm = reactive({
  comment: '',
});

const report = computed(() => reportStore.currentReport);
const timeline = computed(() => reportStore.timeline);

const canEdit = computed(() => {
  return report.value?.status === 'draft' || report.value?.status === 'returned';
});

const canDelete = computed(() => {
  return report.value?.status === 'draft' || report.value?.status === 'returned';
});

const canReview = computed(() => {
  return report.value?.status === 'pending' && authStore.hasPermission('report:review');
});

onMounted(async () => {
  const id = Number(route.params.id);
  try {
    await Promise.all([
      reportStore.fetchReport(id),
      reportStore.fetchTimeline(id),
    ]);
  } catch (error) {
    ElMessage.error('获取报卡信息失败');
    router.push('/infection-report');
  }
});

const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD');
};

const formatDateTime = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm');
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

const getTimelineColor = (action: string) => {
  if (action.includes('通过')) return '#67C23A';
  if (action.includes('驳回')) return '#F56C6C';
  if (action.includes('退回')) return '#E6A23C';
  if (action.includes('创建') || action.includes('提交')) return '#409EFF';
  return '#909399';
};

const handleApprove = async () => {
  try {
    await ElMessageBox.confirm('确定要审核通过吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'success',
    });
    
    await reportStore.reviewApprove(report.value!.id, reviewForm.comment);
    await reportStore.fetchTimeline(report.value!.id);
    ElMessage.success('审核通过');
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败');
    }
  }
};

const handleReturn = async () => {
  if (!reviewForm.comment) {
    ElMessage.warning('请输入退回意见');
    return;
  }
  
  try {
    await ElMessageBox.confirm('确定要退回修改吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    });
    
    await reportStore.reviewReturn(report.value!.id, reviewForm.comment);
    await reportStore.fetchTimeline(report.value!.id);
    ElMessage.success('已退回');
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败');
    }
  }
};

const handleReject = async () => {
  if (!reviewForm.comment) {
    ElMessage.warning('请输入驳回意见');
    return;
  }
  
  try {
    await ElMessageBox.confirm('确定要驳回吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'error',
    });
    
    await reportStore.reviewReject(report.value!.id, reviewForm.comment);
    await reportStore.fetchTimeline(report.value!.id);
    ElMessage.success('已驳回');
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败');
    }
  }
};

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定要删除此报卡吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'error',
    });
    
    await reportStore.removeReport(report.value!.id);
    ElMessage.success('删除成功');
    router.push('/infection-report');
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
    }
  }
};
</script>

<style scoped>
.report-detail {
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

.header-actions {
  display: flex;
  gap: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #1E293B;
}

.info-card,
.action-card,
.timeline-card {
  margin-bottom: 20px;
}

.review-section {
  padding: 16px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.review-section h4 {
  margin: 0 0 8px 0;
  color: #1E293B;
}

.review-section p {
  margin: 0 0 8px 0;
  color: #606266;
}

.review-info {
  display: flex;
  justify-content: space-between;
  color: #909399;
  font-size: 13px;
}

.timeline {
  padding: 20px 0;
}

.status-change {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #409EFF;
  margin-top: 8px !important;
}
</style>
