import api from './axios';
import type { Report, ReportForm, TimelineNode, DashboardStats, ReviewRequest } from '../types';

interface ReportListResponse {
  total: number;
  reports: Report[];
}

export const getReports = (params?: { skip?: number; limit?: number; status?: string }) => {
  return api.get<ReportListResponse>('/infection-reports', { params });
};

export const getReport = (id: number) => {
  return api.get<Report>(`/infection-reports/${id}`);
};

export const createReport = (data: ReportForm) => {
  return api.post<Report>('/infection-reports', data);
};

export const updateReport = (id: number, data: Partial<ReportForm>) => {
  return api.put<Report>(`/infection-reports/${id}`, data);
};

export const deleteReport = (id: number) => {
  return api.delete(`/infection-reports/${id}`);
};

export const approveReport = (id: number, data: ReviewRequest) => {
  return api.post<Report>(`/infection-reports/${id}/approve`, data);
};

export const rejectReport = (id: number, data: ReviewRequest) => {
  return api.post<Report>(`/infection-reports/${id}/reject`, data);
};

export const returnReport = (id: number, data: ReviewRequest) => {
  return api.post<Report>(`/infection-reports/${id}/return`, data);
};

export const getTimeline = (id: number) => {
  return api.get<TimelineNode[]>(`/infection-reports/${id}/timeline`);
};

export const getDashboardStats = () => {
  return api.get<DashboardStats>('/infection-reports/dashboard/stats');
};
