-- 创建数据库
-- IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'infection_control')
-- BEGIN
--     CREATE DATABASE infection_control;
-- END;
-- GO

USE infection_control;
GO

-- 用户表
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'users')
BEGIN
    CREATE TABLE users (
        id INT PRIMARY KEY IDENTITY(1,1),
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        real_name VARCHAR(100) NOT NULL,
        department VARCHAR(100),
        role_id INT,
        status VARCHAR(20) DEFAULT 'active',
        created_at DATETIME DEFAULT GETDATE(),
        last_login_at DATETIME
    );
    
    CREATE INDEX idx_users_username ON users(username);
    CREATE INDEX idx_users_role ON users(role_id);
END;
GO

-- 角色表
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'roles')
BEGIN
    CREATE TABLE roles (
        id INT PRIMARY KEY IDENTITY(1,1),
        name VARCHAR(50) UNIQUE NOT NULL,
        description VARCHAR(255),
        created_at DATETIME DEFAULT GETDATE()
    );
END;
GO

-- 添加外键
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'users')
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_users_roles')
    BEGIN
        ALTER TABLE users ADD CONSTRAINT FK_users_roles FOREIGN KEY (role_id) REFERENCES roles(id);
    END;
END;
GO

-- 权限表
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'permissions')
BEGIN
    CREATE TABLE permissions (
        id INT PRIMARY KEY IDENTITY(1,1),
        name VARCHAR(100) NOT NULL,
        code VARCHAR(100) UNIQUE NOT NULL,
        description VARCHAR(255),
        parent_id INT,
        sort_order INT DEFAULT 0
    );
END;
GO

-- 角色权限关联表
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'role_permissions')
BEGIN
    CREATE TABLE role_permissions (
        role_id INT NOT NULL,
        permission_id INT NOT NULL,
        PRIMARY KEY (role_id, permission_id)
    );
    
    ALTER TABLE role_permissions ADD CONSTRAINT FK_rp_roles FOREIGN KEY (role_id) REFERENCES roles(id);
    ALTER TABLE role_permissions ADD CONSTRAINT FK_rp_permissions FOREIGN KEY (permission_id) REFERENCES permissions(id);
END;
GO

-- 添加权限表外键
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'permissions')
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_permissions_parent')
    BEGIN
        ALTER TABLE permissions ADD CONSTRAINT FK_permissions_parent FOREIGN KEY (parent_id) REFERENCES permissions(id);
    END;
END;
GO

-- 院感报卡表
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'infection_reports')
BEGIN
    CREATE TABLE infection_reports (
        id INT PRIMARY KEY IDENTITY(1,1),
        report_no VARCHAR(50) UNIQUE NOT NULL,
        patient_name NVARCHAR(100) NOT NULL,
        patient_id VARCHAR(50) NOT NULL,
        gender NVARCHAR(10),
        age INT,
        department NVARCHAR(100),
        infection_type NVARCHAR(100),
        infection_date DATE,
        diagnosis NVARCHAR(500),
        symptoms NVARCHAR(MAX),
        treatment NVARCHAR(MAX),
        status NVARCHAR(20) DEFAULT 'draft',
        reporter_id INT,
        report_date DATE,
        reviewer_id INT,
        review_date DATETIME,
        review_comment NVARCHAR(MAX),
        created_at DATETIME DEFAULT GETDATE(),
        updated_at DATETIME DEFAULT GETDATE()
    );
    
    CREATE INDEX idx_reports_status ON infection_reports(status);
    CREATE INDEX idx_reports_reporter ON infection_reports(reporter_id);
    CREATE INDEX idx_reports_report_date ON infection_reports(report_date);
END;
GO

-- 添加报卡表外键
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'infection_reports')
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_reports_reporter')
    BEGIN
        ALTER TABLE infection_reports ADD CONSTRAINT FK_reports_reporter FOREIGN KEY (reporter_id) REFERENCES users(id);
    END;
    
    IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_reports_reviewer')
    BEGIN
        ALTER TABLE infection_reports ADD CONSTRAINT FK_reports_reviewer FOREIGN KEY (reviewer_id) REFERENCES users(id);
    END;
END;
GO

-- 时间轴记录表
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'timeline')
BEGIN
    CREATE TABLE timeline (
        id INT PRIMARY KEY IDENTITY(1,1),
        report_id INT NOT NULL,
        action NVARCHAR(100) NOT NULL,
        actor_id INT,
        timestamp DATETIME DEFAULT GETDATE(),
        comment NVARCHAR(MAX),
        previous_status NVARCHAR(20),
        new_status NVARCHAR(20)
    );
    
    CREATE INDEX idx_timeline_report ON timeline(report_id);
    
    ALTER TABLE timeline ADD CONSTRAINT FK_timeline_report FOREIGN KEY (report_id) REFERENCES infection_reports(id);
    ALTER TABLE timeline ADD CONSTRAINT FK_timeline_actor FOREIGN KEY (actor_id) REFERENCES users(id);
END;
GO

-- 操作日志表
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'operation_logs')
BEGIN
    CREATE TABLE operation_logs (
        id INT PRIMARY KEY IDENTITY(1,1),
        user_id INT,
        action NVARCHAR(100) NOT NULL,
        resource_type NVARCHAR(50),
        resource_id INT,
        timestamp DATETIME DEFAULT GETDATE(),
        ip_address VARCHAR(50),
        details NVARCHAR(MAX)
    );
    
    CREATE INDEX idx_logs_user ON operation_logs(user_id);
    CREATE INDEX idx_logs_timestamp ON operation_logs(timestamp);
    
    ALTER TABLE operation_logs ADD CONSTRAINT FK_logs_user FOREIGN KEY (user_id) REFERENCES users(id);
END;
GO
