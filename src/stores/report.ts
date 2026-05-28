import { defineStore } from 'pinia';
import { ref } from 'vue';
import {
  getReports,
  getReport,
  createReport,
  updateReport,
  deleteReport,
  approveReport,
  rejectReport,
  returnReport,
  getTimeline,
  getDashboardStats,
} from '../api/report';
import type { Report, ReportForm, TimelineNode, DashboardStats } from '../types';

export const useReportStore = defineStore('report', () => {
  const reports = ref<Report[]>([]);
  const currentReport = ref<Report | null>(null);
  const timeline = ref<TimelineNode[]>([]);
  const stats = ref<DashboardStats | null>(null);
  const total = ref(0);
  const loading = ref(false);

  const fetchReports = async (params?: { skip?: number; limit?: number; status?: string }) => {
    loading.value = true;
    try {
      const response = await getReports(params);
      reports.value = response.data.reports;
      total.value = response.data.total;
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const fetchReport = async (id: number) => {
    loading.value = true;
    try {
      const response = await getReport(id);
      currentReport.value = response.data;
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const addReport = async (data: ReportForm) => {
    loading.value = true;
    try {
      const response = await createReport(data);
      return response.data;
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const editReport = async (id: number, data: Partial<ReportForm>) => {
    loading.value = true;
    try {
      const response = await updateReport(id, data);
      currentReport.value = response.data;
      return response.data;
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const removeReport = async (id: number) => {
    loading.value = true;
    try {
      await deleteReport(id);
      await fetchReports();
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const reviewApprove = async (id: number, comment?: string) => {
    loading.value = true;
    try {
      const response = await approveReport(id, { comment });
      currentReport.value = response.data;
      return response.data;
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const reviewReject = async (id: number, comment?: string) => {
    loading.value = true;
    try {
      const response = await rejectReport(id, { comment });
      currentReport.value = response.data;
      return response.data;
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const reviewReturn = async (id: number, comment?: string) => {
    loading.value = true;
    try {
      const response = await returnReport(id, { comment });
      currentReport.value = response.data;
      return response.data;
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const fetchTimeline = async (id: number) => {
    try {
      const response = await getTimeline(id);
      timeline.value = response.data;
    } catch (error) {
      throw error;
    }
  };

  const fetchStats = async () => {
    loading.value = true;
    try {
      const response = await getDashboardStats();
      stats.value = response.data;
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  return {
    reports,
    currentReport,
    timeline,
    stats,
    total,
    loading,
    fetchReports,
    fetchReport,
    addReport,
    editReport,
    removeReport,
    reviewApprove,
    reviewReject,
    reviewReturn,
    fetchTimeline,
    fetchStats,
  };
});
