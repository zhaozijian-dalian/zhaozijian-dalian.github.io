<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="login-header">
          <h2>🏥 医院感染控制系统</h2>
          <p>Hospital Infection Control System</p>
        </div>
      </template>
      
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            size="large"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            class="login-button"
            @click="handleLogin"
          >
            登 录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-footer">
        <el-alert
          title="测试账号"
          type="info"
          :closable="false"
          show-icon
        >
          <template #default>
            用户名: admin<br/>
            密码: admin123
          </template>
        </el-alert>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const formRef = ref();
const loading = ref(false);

const form = reactive({
  username: 'admin',
  password: 'admin123',
});

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
  ],
};

const handleLogin = async () => {
  if (!formRef.value) return;
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      try {
        await authStore.login({
          username: form.username,
          password: form.password,
        });
        ElMessage.success('登录成功');
        router.push('/dashboard');
      } catch (error: any) {
        const message = error.response?.data?.detail || '登录失败，请检查用户名和密码';
        ElMessage.error(message);
      } finally {
        loading.value = false;
      }
    }
  });
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 450px;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-header {
  text-align: center;
  padding: 10px 0;
}

.login-header h2 {
  margin: 0 0 8px 0;
  color: #1E40AF;
  font-size: 24px;
  font-weight: 700;
}

.login-header p {
  margin: 0;
  color: #64748B;
  font-size: 14px;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
}

.login-footer {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #E2E8F0;
}
</style>
