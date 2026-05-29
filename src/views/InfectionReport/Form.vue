<template>
  <div class="report-form">
    <div class="page-header">
      <h2 class="page-title">{{ isEdit ? '编辑报卡' : '新增报卡' }}</h2>
      <el-button @click="$router.back()">
        <el-icon><Back /></el-icon>
        返回
      </el-button>
    </div>

    <el-card>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="report-form-body"
      >
        <el-divider content-position="left">患者基本信息</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="患者姓名" prop="patient_name">
              <el-input v-model="form.patient_name" placeholder="请输入患者姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="患者ID" prop="patient_id">
              <el-input v-model="form.patient_id" placeholder="请输入患者ID" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="form.gender">
                <el-radio label="male">男</el-radio>
                <el-radio label="female">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年龄" prop="age">
              <el-input-number v-model="form.age" :min="0" :max="150" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="科室" prop="department">
              <el-input v-model="form.department" placeholder="请输入科室" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="感染日期" prop="infection_date">
              <el-date-picker
                v-model="form.infection_date"
                type="date"
                placeholder="选择感染日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">感染信息</el-divider>

        <el-form-item label="感染类型" prop="infection_type">
          <el-select v-model="form.infection_type" placeholder="请选择感染类型" style="width: 100%">
            <el-option label="上呼吸道感染" value="上呼吸道感染" />
            <el-option label="下呼吸道感染" value="下呼吸道感染" />
            <el-option label="泌尿道感染" value="泌尿道感染" />
            <el-option label="手术部位感染" value="手术部位感染" />
            <el-option label="胃肠道感染" value="胃肠道感染" />
            <el-option label="血液感染" value="血液感染" />
            <el-option label="皮肤软组织感染" value="皮肤软组织感染" />
            <el-option label="其他感染" value="其他感染" />
          </el-select>
        </el-form-item>

        <el-form-item label="诊断" prop="diagnosis">
          <el-input
            v-model="form.diagnosis"
            type="textarea"
            :rows="3"
            placeholder="请输入诊断信息"
          />
        </el-form-item>

        <el-form-item label="症状" prop="symptoms">
          <el-input
            v-model="form.symptoms"
            type="textarea"
            :rows="3"
            placeholder="请输入症状描述"
          />
        </el-form-item>

        <el-form-item label="治疗措施" prop="treatment">
          <el-input
            v-model="form.treatment"
            type="textarea"
            :rows="3"
            placeholder="请输入治疗措施"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            提交报卡
          </el-button>
          <el-button @click="handleSave">保存草稿</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage, type FormInstance, type FormRules } from 'element-plus';
import { useReportStore } from '../../stores/report';
import type { ReportForm } from '../../types';

const route = useRoute();
const router = useRouter();
const reportStore = useReportStore();

const formRef = ref<FormInstance>();
const submitting = ref(false);
const isEdit = computed(() => route.path.includes('/edit'));

const form = reactive<ReportForm>({
  patient_name: '',
  patient_id: '',
  gender: undefined,
  age: undefined,
  department: '',
  infection_type: '',
  infection_date: '',
  diagnosis: '',
  symptoms: '',
  treatment: '',
});

const rules: FormRules = {
  patient_name: [{ required: true, message: '请输入患者姓名', trigger: 'blur' }],
  patient_id: [{ required: true, message: '请输入患者ID', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  infection_type: [{ required: true, message: '请选择感染类型', trigger: 'change' }],
};

onMounted(async () => {
  if (isEdit.value && route.params.id) {
    try {
      await reportStore.fetchReport(Number(route.params.id));
      const report = reportStore.currentReport;
      if (report) {
        Object.assign(form, {
          patient_name: report.patient_name,
          patient_id: report.patient_id,
          gender: report.gender,
          age: report.age,
          department: report.department,
          infection_type: report.infection_type,
          infection_date: report.infection_date,
          diagnosis: report.diagnosis,
          symptoms: report.symptoms,
          treatment: report.treatment,
        });
      }
    } catch (error) {
      ElMessage.error('获取报卡信息失败');
      router.push('/infection-report');
    }
  }
});

const handleSubmit = async () => {
  if (!formRef.value) return;
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true;
      try {
        if (isEdit.value && route.params.id) {
          await reportStore.editReport(Number(route.params.id), form);
          ElMessage.success('编辑成功');
        } else {
          await reportStore.addReport(form);
          ElMessage.success('提交成功');
        }
        router.push('/infection-report');
      } catch (error) {
        ElMessage.error('操作失败');
      } finally {
        submitting.value = false;
      }
    }
  });
};

const handleSave = async () => {
  submitting.value = true;
  try {
    if (isEdit.value && route.params.id) {
      await reportStore.editReport(Number(route.params.id), form);
    } else {
      await reportStore.addReport(form);
    }
    ElMessage.success('保存成功');
    router.push('/infection-report');
  } catch (error) {
    ElMessage.error('保存失败');
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.report-form {
  max-width: 1200px;
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

.report-form-body {
  max-width: 800px;
}
</style>
