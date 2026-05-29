import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getUsers, createUser, updateUser, deleteUser } from '../api/user';
import type { User, UserForm } from '../types';

export const useUserStore = defineStore('user', () => {
  const users = ref<User[]>([]);
  const total = ref(0);
  const loading = ref(false);

  const fetchUsers = async (skip = 0, limit = 100) => {
    loading.value = true;
    try {
      const response = await getUsers(skip, limit);
      users.value = response.data.users;
      total.value = response.data.total;
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const addUser = async (data: UserForm) => {
    loading.value = true;
    try {
      await createUser(data);
      await fetchUsers();
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const editUser = async (id: number, data: Partial<UserForm>) => {
    loading.value = true;
    try {
      await updateUser(id, data);
      await fetchUsers();
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const removeUser = async (id: number) => {
    loading.value = true;
    try {
      await deleteUser(id);
      await fetchUsers();
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  return {
    users,
    total,
    loading,
    fetchUsers,
    addUser,
    editUser,
    removeUser,
  };
});
