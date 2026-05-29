<template>
  <el-container class="main-layout">
    <el-aside :width="isCollapse ? '64px' : '240px'" class="aside">
      <div class="logo">
        <img src="/hospital-icon.svg" alt="Logo" v-if="!isCollapse" />
        <span v-if="!isCollapse">院感系统</span>
        <el-icon v-else><House /></el-icon>
      </div>
      <el-menu
        :default-active="currentRoute"
        :collapse="isCollapse"
        :router="true"
        background-color="#1E40AF"
        text-color="#fff"
        active-text-color="#60A5FA"
      >
        <el-menu-item index="/dashboard">
          <el-icon><DataAnalysis /></el-icon>
          <template #title>导航台</template>
        </el-menu-item>
        <el-menu-item index="/infection-report">
          <el-icon><Document /></el-icon>
          <template #title>院感报卡</template>
        </el-menu-item>
        <el-menu-item index="/user-management" v-if="hasPermission('user:management')">
          <el-icon><User /></el-icon>
          <template #title>用户管理</template>
        </el-menu-item>
        <el-menu-item index="/permission-management" v-if="hasPermission('role:management')">
          <el-icon><Key /></el-icon>
          <template #title>权限管理</template>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-icon size="24" @click="isCollapse = !isCollapse" class="collapse-icon">
            <Expand v-if="isCollapse" />
            <Fold v-else />
          </el-icon>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-avatar :size="32">{{ user?.real_name?.charAt(0) || 'U' }}</el-avatar>
              <span class="username">{{ user?.real_name }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const isCollapse = ref(false);
const user = computed(() => authStore.user);
const currentRoute = computed(() => route.path);
const hasPermission = (permission: string) => authStore.hasPermission(permission);

const handleCommand = async (command: string) => {
  if (command === 'logout') {
    if (confirm('确定要退出登录吗？')) {
      await authStore.logout();
      router.push('/login');
    }
  }
};
</script>

<style scoped>
.main-layout {
  height: 100vh;
}

.aside {
  background-color: #1E40AF;
  transition: width 0.3s;
  overflow-x: hidden;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: white;
  font-size: 18px;
  font-weight: bold;
  padding: 0 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo img {
  width: 32px;
  height: 32px;
}

.header {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.collapse-icon {
  cursor: pointer;
  color: #606266;
}

.collapse-icon:hover {
  color: #1E40AF;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.username {
  font-size: 14px;
  color: #303133;
}

.main-content {
  background-color: #F8FAFC;
  padding: 20px;
}

:deep(.el-menu) {
  border: none;
}

:deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
}

:deep(.el-menu-item.is-active) {
  background-color: rgba(255, 255, 255, 0.1) !important;
}
</style>
