import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    component: () => import('../components/layout/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/dashboard',
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
      },
      {
        path: 'user-management',
        name: 'UserManagement',
        component: () => import('../views/UserManagement.vue'),
        meta: { permission: 'user:management' },
      },
      {
        path: 'permission-management',
        name: 'PermissionManagement',
        component: () => import('../views/PermissionManagement.vue'),
        meta: { permission: 'role:management' },
      },
      {
        path: 'infection-report',
        name: 'InfectionReportList',
        component: () => import('../views/InfectionReport/List.vue'),
      },
      {
        path: 'infection-report/new',
        name: 'InfectionReportNew',
        component: () => import('../views/InfectionReport/Form.vue'),
      },
      {
        path: 'infection-report/:id',
        name: 'InfectionReportDetail',
        component: () => import('../views/InfectionReport/Detail.vue'),
      },
      {
        path: 'infection-report/:id/edit',
        name: 'InfectionReportEdit',
        component: () => import('../views/InfectionReport/Form.vue'),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  
  if (to.meta.requiresAuth !== false && !token) {
    next('/login');
  } else if (to.path === '/login' && token) {
    next('/dashboard');
  } else {
    next();
  }
});

export default router;
