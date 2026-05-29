import api from './axios';
import type { Role, Permission } from '../types';

interface RoleListResponse {
  total: number;
  roles: Role[];
}

export const getRoles = (skip = 0, limit = 100) => {
  return api.get<RoleListResponse>('/roles', { params: { skip, limit } });
};

export const getRole = (id: number) => {
  return api.get<Role>(`/roles/${id}`);
};

export const createRole = (data: { name: string; description?: string; permission_ids: number[] }) => {
  return api.post<Role>('/roles', data);
};

export const updateRole = (id: number, data: { name?: string; description?: string; permission_ids?: number[] }) => {
  return api.put<Role>(`/roles/${id}`, data);
};

export const deleteRole = (id: number) => {
  return api.delete(`/roles/${id}`);
};

export const getPermissions = () => {
  return api.get<Permission[]>('/roles/permissions');
};
