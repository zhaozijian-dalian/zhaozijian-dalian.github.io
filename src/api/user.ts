import api from './axios';
import type { User, UserForm } from '../types';

interface UserListResponse {
  total: number;
  users: User[];
}

export const getUsers = (skip = 0, limit = 100) => {
  return api.get<UserListResponse>('/users', { params: { skip, limit } });
};

export const getUser = (id: number) => {
  return api.get<User>(`/users/${id}`);
};

export const createUser = (data: UserForm) => {
  return api.post<User>('/users', data);
};

export const updateUser = (id: number, data: Partial<UserForm>) => {
  return api.put<User>(`/users/${id}`, data);
};

export const deleteUser = (id: number) => {
  return api.delete(`/users/${id}`);
};
