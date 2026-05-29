# 医院感染控制系统

医院感染控制系统（Hospital Infection Control System，HICS）是一款面向医疗机构感染管理部门的专业化信息系统。

## 技术栈

### 前端
- Vue 3 + TypeScript
- Vite 5
- Pinia (状态管理)
- Vue Router
- Element Plus (UI组件库)
- ECharts (数据可视化)
- Axios (HTTP客户端)
- dayjs (日期处理)

### 后端
- Python 3.11+
- FastAPI
- SQLAlchemy
- PyJWT
- Passlib
- pymssql (SQL Server驱动)

### 数据库
- SQL Server 2019+

## 项目结构

```
├── api/                    # Python后端项目
│   ├── config.py          # 配置文件
│   ├── database.py        # 数据库连接
│   ├── main.py            # 应用入口
│   ├── middleware/        # 中间件
│   ├── models/            # 数据模型
│   ├── routers/           # API路由
│   ├── schemas/           # 数据验证
│   ├── services/          # 业务逻辑
│   ├── utils/             # 工具函数
│   ├── migrations/        # 数据库迁移脚本
│   └── requirements.txt   # Python依赖
│
├── src/                   # Vue前端项目
│   ├── api/              # API调用
│   ├── components/       # 组件
│   ├── router/           # 路由配置
│   ├── stores/           # Pinia状态管理
│   ├── types/            # TypeScript类型
│   ├── views/            # 页面视图
│   └── ...
│
├── public/               # 静态资源
├── .env                  # 环境变量
└── package.json          # 前端依赖
```

## 快速开始

### 1. 环境要求

- Node.js >= 16
- Python >= 3.11
- SQL Server 2019+

### 2. 前端设置

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 类型检查
npm run check
```

### 3. 后端设置

```bash
# 进入后端目录
cd api

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 4. 数据库配置

1. 创建SQL Server数据库：
```sql
CREATE DATABASE infection_control;
```

2. 执行数据库迁移脚本：
```bash
# 使用sqlcmd或SSMS执行
sqlcmd -S localhost -U sa -P your_password -d infection_control -i migrations/001_init_schema.sql
sqlcmd -S localhost -U sa -P your_password -d infection_control -i migrations/002_seed_data.sql
```

3. 配置数据库连接：
编辑 `api/config.py` 或创建 `.env` 文件：
```env
DATABASE_SERVER=localhost
DATABASE_NAME=infection_control
DATABASE_USER=sa
DATABASE_PASSWORD=your_password
JWT_SECRET_KEY=your-secret-key-change-in-production
```

### 5. 启动后端服务

```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API文档将运行在 http://localhost:8000/docs

### 6. 访问应用

- 前端：http://localhost:5173
- 后端API：http://localhost:8000

## 默认账号

- 用户名：admin
- 密码：admin123

## 主要功能

### 1. 登录模块
- 用户名/密码登录
- Token认证
- 会话管理

### 2. 导航台
- 数据概览卡片（今日报卡、待审核、本月累计、通过率）
- 统计图表（7天趋势、感染类型分布）
- 待审核列表

### 3. 用户管理
- 用户列表展示
- 新增/编辑/删除用户
- 角色分配

### 4. 权限管理
- 角色列表
- 权限配置（树形结构）
- 角色权限分配

### 5. 院感报卡
- 报卡录入（患者信息、感染信息、诊断等）
- 报卡列表（状态筛选、搜索）
- 报卡详情
- 审核功能（通过、驳回、退回）
- 时间轴展示（操作记录）

## API接口

详细API文档请访问：http://localhost:8000/docs

### 认证接口
- POST /api/auth/login - 用户登录
- POST /api/auth/logout - 用户登出
- GET /api/auth/current-user - 获取当前用户

### 用户管理
- GET /api/users - 获取用户列表
- POST /api/users - 创建用户
- PUT /api/users/:id - 更新用户
- DELETE /api/users/:id - 删除用户

### 角色管理
- GET /api/roles - 获取角色列表
- POST /api/roles - 创建角色
- PUT /api/roles/:id - 更新角色
- DELETE /api/roles/:id - 删除角色
- GET /api/roles/permissions - 获取权限列表

### 报卡管理
- GET /api/infection-reports - 获取报卡列表
- POST /api/infection-reports - 创建报卡
- GET /api/infection-reports/:id - 获取报卡详情
- PUT /api/infection-reports/:id - 更新报卡
- DELETE /api/infection-reports/:id - 删除报卡
- POST /api/infection-reports/:id/approve - 审核通过
- POST /api/infection-reports/:id/reject - 审核驳回
- POST /api/infection-reports/:id/return - 退回修改
- GET /api/infection-reports/:id/timeline - 获取时间轴
- GET /api/infection-reports/dashboard/stats - 获取统计数据

## 开发说明

### 代码规范
- 前端：Vue 3 + TypeScript，使用Composition API
- 后端：Python FastAPI，使用Pydantic进行数据验证
- 数据库：SQL Server，使用SQLAlchemy ORM

### 安全考虑
- 用户密码使用bcrypt加密
- JWT Token认证
- 敏感操作日志记录
- 权限控制

## 许可证

MIT License
