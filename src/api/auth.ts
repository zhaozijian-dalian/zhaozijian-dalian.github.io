import api from './axios';
import type { LoginRequest, LoginResponse, User } from '../types';

export const login = (data: LoginRequest) => {
  return api.post<LoginResponse>('/auth/login', data);
};

export const logout = () => {
  return api.post('/auth/logout');
};

export const getCurrentUser = () => {
  return api.get<User>('/auth/current-user');
};
