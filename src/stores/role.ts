import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getRoles, createRole, updateRole, deleteRole, getPermissions } from '../api/role';
import type { Role, Permission } from '../types';

export const useRoleStore = defineStore('role', () => {
  const roles = ref<Role[]>([]);
  const permissions = ref<Permission[]>([]);
  const total = ref(0);
  const loading = ref(false);

  const fetchRoles = async (skip = 0, limit = 100) => {
    loading.value = true;
    try {
      const response = await getRoles(skip, limit);
      roles.value = response.data.roles;
      total.value = response.data.total;
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const fetchPermissions = async () => {
    try {
      const response = await getPermissions();
      permissions.value = response.data;
    } catch (error) {
      throw error;
    }
  };

  const addRole = async (data: { name: string; description?: string; permission_ids: number[] }) => {
    loading.value = true;
    try {
      await createRole(data);
      await fetchRoles();
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const editRole = async (id: number, data: { name?: string; description?: string; permission_ids?: number[] }) => {
    loading.value = true;
    try {
      await updateRole(id, data);
      await fetchRoles();
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const removeRole = async (id: number) => {
    loading.value = true;
    try {
      await deleteRole(id);
      await fetchRoles();
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  return {
    roles,
    permissions,
    total,
    loading,
    fetchRoles,
    fetchPermissions,
    addRole,
    editRole,
    removeRole,
  };
});
