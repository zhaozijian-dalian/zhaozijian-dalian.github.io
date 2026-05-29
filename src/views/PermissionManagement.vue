<template>
  <div class="permission-management">
    <div class="page-header">
      <h2 class="page-title">权限管理</h2>
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>
        新增角色
      </el-button>
    </div>

    <el-row :gutter="20">
      <el-col :xs="24" :lg="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>角色列表</span>
            </div>
          </template>
          <el-table :data="roles" v-loading="loading" @row-click="handleRowClick">
            <el-table-column prop="name" label="角色名称" />
            <el-table-column prop="description" label="描述" />
            <el-table-column label="权限数" width="100">
              <template #default="{ row }">
                {{ row.permissions.length }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button type="primary" link @click.stop="handleEdit(row)">编辑</el-button>
                <el-button type="danger" link @click.stop="handleDelete(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :xs="24" :lg="12">
        <el-card v-if="selectedRole">
          <template #header>
            <div class="card-header">
              <span>角色: {{ selectedRole.name }}</span>
            </div>
          </template>
          <div class="permission-tree">
            <el-tree
              ref="treeRef"
              :data="treeData"
              :props="treeProps"
              node-key="id"
              :default-checked-keys="selectedPermissions"
              show-checkbox
              @check-change="handleCheckChange"
            />
          </div>
          <div class="permission-actions" v-if="hasChanges">
            <el-button type="primary" @click="handleSavePermissions" :loading="saving">
              保存权限
            </el-button>
          </div>
        </el-card>
        <el-card v-else>
          <el-empty description="请选择左侧角色进行权限配置" />
        </el-card>
      </el-col>
    </el-row>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑角色' : '新增角色'"
      width="500px"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus';
import { useRoleStore } from '../stores/role';
import type { Role, Permission } from '../types';

const roleStore = useRoleStore();

const roles = computed(() => roleStore.roles);
const permissions = computed(() => roleStore.permissions);
const loading = computed(() => roleStore.loading);

const dialogVisible = ref(false);
const submitting = ref(false);
const saving = ref(false);
const isEdit = ref(false);
const editingId = ref<number | null>(null);

const selectedRole = ref<Role | null>(null);
const selectedPermissions = ref<number[]>([]);
const originalPermissions = ref<number[]>([]);
const treeRef = ref();
const hasChanges = computed(() => {
  return JSON.stringify(selectedPermissions.value.sort()) !== JSON.stringify(originalPermissions.value.sort());
});

const treeData = computed(() => {
  const permissionMap = new Map<number | null, Permission[]>();
  permissions.value.forEach(p => {
    const parentId = p.parent_id;
    if (!permissionMap.has(parentId)) {
      permissionMap.set(parentId, []);
    }
    permissionMap.get(parentId)!.push(p);
  });
  
  const buildTree = (parentId: number | null): any[] => {
    const items = permissionMap.get(parentId) || [];
    return items.map(p => ({
      id: p.id,
      label: p.name,
      children: buildTree(p.id),
    }));
  };
  
  return buildTree(null);
});

const treeProps = {
  children: 'children',
  label: 'label',
};

const formRef = ref<FormInstance>();
const form = reactive({
  name: '',
  description: '',
  permission_ids: [] as number[],
});

const rules: FormRules = {
  name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }],
};

onMounted(async () => {
  await roleStore.fetchRoles();
  await roleStore.fetchPermissions();
});

const handleRowClick = (row: Role) => {
  selectedRole.value = row;
  selectedPermissions.value = row.permissions.map(p => p.id);
  originalPermissions.value = [...selectedPermissions.value];
};

const handleCheckChange = () => {
  if (treeRef.value) {
    selectedPermissions.value = treeRef.value.getCheckedKeys(true);
  }
};

const handleSavePermissions = async () => {
  if (!selectedRole.value) return;
  
  saving.value = true;
  try {
    await roleStore.editRole(selectedRole.value.id, {
      permission_ids: selectedPermissions.value,
    });
    await roleStore.fetchRoles();
    
    const updatedRole = roles.value.find(r => r.id === selectedRole.value?.id);
    if (updatedRole) {
      selectedRole.value = updatedRole;
      originalPermissions.value = [...selectedPermissions.value];
    }
    
    ElMessage.success('权限保存成功');
  } catch (error) {
    ElMessage.error('权限保存失败');
  } finally {
    saving.value = false;
  }
};

const handleAdd = () => {
  isEdit.value = false;
  editingId.value = null;
  form.name = '';
  form.description = '';
  dialogVisible.value = true;
};

const handleEdit = (role: Role) => {
  isEdit.value = true;
  editingId.value = role.id;
  form.name = role.name;
  form.description = role.description || '';
  dialogVisible.value = true;
};

const handleDelete = async (role: Role) => {
  try {
    await ElMessageBox.confirm(`确定要删除角色 ${role.name} 吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    });
    await roleStore.removeRole(role.id);
    
    if (selectedRole.value?.id === role.id) {
      selectedRole.value = null;
      selectedPermissions.value = [];
      originalPermissions.value = [];
    }
    
    ElMessage.success('删除成功');
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
    }
  }
};

const handleSubmit = async () => {
  if (!formRef.value) return;
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true;
      try {
        if (isEdit.value && editingId.value) {
          await roleStore.editRole(editingId.value, {
            name: form.name,
            description: form.description,
          });
          ElMessage.success('编辑成功');
        } else {
          await roleStore.addRole({
            name: form.name,
            description: form.description,
            permission_ids: [],
          });
          ElMessage.success('新增成功');
        }
        dialogVisible.value = false;
      } catch (error) {
        ElMessage.error('操作失败');
      } finally {
        submitting.value = false;
      }
    }
  });
};
</script>

<style scoped>
.permission-management {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  color: #1E293B;
  font-weight: 600;
  margin: 0;
}

.card-header {
  font-weight: 600;
  color: #1E293B;
}

.permission-tree {
  max-height: 400px;
  overflow-y: auto;
}

.permission-actions {
  margin-top: 20px;
  text-align: right;
}
</style>
