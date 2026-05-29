export interface User {
  id: number;
  username: string;
  real_name: string;
  department?: string;
  role?: string;
  permissions: string[];
  status: string;
  created_at: string;
  last_login_at?: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: User;
}

export interface UserForm {
  username: string;
  password?: string;
  real_name: string;
  department?: string;
  role_id: number;
}

export interface Role {
  id: number;
  name: string;
  description?: string;
  created_at: string;
  permissions: Permission[];
}

export interface Permission {
  id: number;
  name: string;
  code: string;
  description?: string;
  parent_id?: number;
  sort_order: number;
}

export interface Report {
  id: number;
  report_no: string;
  patient_name: string;
  patient_id: string;
  gender?: string;
  age?: number;
  department?: string;
  infection_type?: string;
  infection_date?: string;
  diagnosis?: string;
  symptoms?: string;
  treatment?: string;
  status: string;
  reporter?: string;
  report_date?: string;
  reviewer?: string;
  review_date?: string;
  review_comment?: string;
  created_at: string;
  updated_at: string;
}

export interface ReportForm {
  patient_name: string;
  patient_id: string;
  gender?: string;
  age?: number;
  department?: string;
  infection_type?: string;
  infection_date?: string;
  diagnosis?: string;
  symptoms?: string;
  treatment?: string;
}

export interface TimelineNode {
  id: number;
  report_id: number;
  action: string;
  actor?: string;
  timestamp: string;
  comment?: string;
  previous_status?: string;
  new_status?: string;
}

export interface DashboardStats {
  today_reports: number;
  pending_reviews: number;
  monthly_total: number;
  approved_rate: number;
  weekly_trend: Array<{ date: string; count: number }>;
  infection_type_distribution: Array<{ type: string; count: number }>;
}

export interface ReviewRequest {
  comment?: string;
}
