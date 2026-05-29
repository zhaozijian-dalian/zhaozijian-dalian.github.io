import axios from 'axios';
import type { AxiosInstance, AxiosError } from 'axios';
import { ElMessage } from 'element-plus';

const baseURL = '/api';

const api: AxiosInstance = axios.create({
  baseURL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: AxiosError) => {
    if (error.response) {
      const status = error.response.status;
      const data = error.response.data as any;
      
      if (status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        ElMessage.error('登录已过期，请重新登录');
        window.location.href = '/login';
      } else if (status === 403) {
        ElMessage.error(data.detail || '没有权限执行此操作');
      } else if (status === 404) {
        ElMessage.error(data.detail || '资源不存在');
      } else if (status >= 500) {
        ElMessage.error('服务器错误，请稍后重试');
      } else {
        ElMessage.error(data.detail || '操作失败');
      }
    } else {
      ElMessage.error('网络错误，请检查网络连接');
    }
    
    return Promise.reject(error);
  }
);

export default api;
