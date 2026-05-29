import { defineStore } from 'pinia';
import { ref } from 'vue';
import { login as loginApi, logout as logoutApi, getCurrentUser } from '../api/auth';
import type { LoginRequest, User } from '../types';

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'));
  const user = ref<User | null>(JSON.parse(localStorage.getItem('user') || 'null'));
  const loading = ref(false);

  const login = async (credentials: LoginRequest) => {
    loading.value = true;
    try {
      const response = await loginApi(credentials);
      token.value = response.data.token;
      user.value = response.data.user;
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      return true;
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const logout = async () => {
    try {
      if (token.value) {
        await logoutApi();
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      token.value = null;
      user.value = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  };

  const logoutLocal = () => {
    token.value = null;
    user.value = null;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  const fetchCurrentUser = async () => {
    if (!token.value) return;
    try {
      const response = await getCurrentUser();
      user.value = response.data;
      localStorage.setItem('user', JSON.stringify(response.data));
    } catch (error) {
      console.error('Fetch current user error:', error);
      logoutLocal();
    }
  };

  const hasPermission = (permission: string): boolean => {
    return user.value?.permissions.includes(permission) || false;
  };

  return {
    token,
    user,
    loading,
    login,
    logout,
    logoutLocal,
    fetchCurrentUser,
    hasPermission,
  };
});
