USE infection_control;
GO

-- 插入初始角色
IF NOT EXISTS (SELECT * FROM roles WHERE name = '系统管理员')
BEGIN
    INSERT INTO roles (name, description) VALUES
    ('系统管理员', '系统管理员，拥有所有权限'),
    ('院感科主任', '院感科主任，负责审核报卡'),
    ('院感专职人员', '院感专职人员，负责报卡管理'),
    ('临床医生', '临床医生，负责本科室报卡'),
    ('护士长', '护士长，负责本科室报卡审核');
END;
GO

-- 插入初始管理员用户 (密码: admin123)
-- 密码哈希使用 bcrypt 算法
IF NOT EXISTS (SELECT * FROM users WHERE username = 'admin')
BEGIN
    INSERT INTO users (username, password_hash, real_name, department, role_id, status)
    VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.pOKQh8j3pXFyMS', '系统管理员', '信息中心', 1, 'active');
END;
GO

-- 插入权限数据
IF NOT EXISTS (SELECT * FROM permissions WHERE code = 'system')
BEGIN
    INSERT INTO permissions (name, code, description, parent_id, sort_order) VALUES
    ('系统管理', 'system', '系统管理模块', NULL, 1),
    ('用户管理', 'user:management', '用户管理', 1, 1),
    ('用户列表', 'user:list', '查看用户列表', 2, 1),
    ('用户新增', 'user:create', '新增用户', 2, 2),
    ('用户编辑', 'user:edit', '编辑用户', 2, 3),
    ('用户删除', 'user:delete', '删除用户', 2, 4),
    ('权限管理', 'role:management', '权限管理', 1, 2),
    ('角色列表', 'role:list', '查看角色列表', 7, 1),
    ('角色新增', 'role:create', '新增角色', 7, 2),
    ('角色编辑', 'role:edit', '编辑角色', 7, 3),
    ('角色删除', 'role:delete', '删除角色', 7, 4),
    ('院感管理', 'report:management', '院感报卡管理', NULL, 2),
    ('报卡列表', 'report:list', '查看报卡列表', 11, 1),
    ('报卡录入', 'report:create', '录入报卡', 11, 2),
    ('报卡编辑', 'report:edit', '编辑报卡', 11, 3),
    ('报卡删除', 'report:delete', '删除报卡', 11, 4),
    ('报卡审核', 'report:review', '审核报卡', 11, 5),
    ('报卡退回', 'report:return', '退回报卡', 11, 6),
    ('仪表盘', 'dashboard:view', '查看仪表盘', NULL, 3);
END;
GO

-- 分配角色权限 (系统管理员拥有所有权限)
IF NOT EXISTS (SELECT * FROM role_permissions WHERE role_id = 1)
BEGIN
    INSERT INTO role_permissions (role_id, permission_id)
    SELECT 1, id FROM permissions;
    
    -- 院感科主任
    INSERT INTO role_permissions (role_id, permission_id)
    SELECT 2, id FROM permissions WHERE code IN ('dashboard:view', 'report:list', 'report:review', 'report:return');
    
    -- 院感专职人员
    INSERT INTO role_permissions (role_id, permission_id)
    SELECT 3, id FROM permissions WHERE code IN ('dashboard:view', 'report:list', 'report:create', 'report:edit', 'report:delete');
    
    -- 临床医生
    INSERT INTO role_permissions (role_id, permission_id)
    SELECT 4, id FROM permissions WHERE code IN ('dashboard:view', 'report:list', 'report:create');
    
    -- 护士长
    INSERT INTO role_permissions (role_id, permission_id)
    SELECT 5, id FROM permissions WHERE code IN ('dashboard:view', 'report:list', 'report:review', 'report:return');
END;
GO
