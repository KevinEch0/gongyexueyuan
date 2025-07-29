<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>权限管理</el-breadcrumb-item>
        <el-breadcrumb-item>角色列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-row>
            <!-- <el-button type="primary" :icon="CirclePlus">增加角色</el-button> -->
        </el-row>
        <el-row>
            <el-table :data="tableData.authorList" stripe class="table">
                <el-table-column type="expand">
                    <template #default="scope">
                        <el-row v-for="(m,i) in scope.row.menus" :key="m.id"
                            :class="['padding-l100 bottom',i===0?'top':'']">
                            <el-col :span="3"><el-tag class="margin-t10" closable @close="removeMenu(scope.row,m.id)">{{
                                    m.name }}</el-tag></el-col>
                            <el-col :span="1"><el-icon class="margin-t15" closable>
                                    <DArrowRight />
                                </el-icon></el-col>
                            <el-col :span="20">
                                <el-row v-for="cm in m.children" :key="cm.id" class="padding-l100">
                                    <el-col :span="10"><el-tag class="margin-t10" type="success" closable
                                            @close="removeMenu(scope.row,cm.id)">{{ cm.name }}</el-tag></el-col>
                                    <el-col :span="2"><el-icon class="margin-t15" closable>
                                            <DArrowRight />
                                        </el-icon></el-col>
                                    <el-col :span="12">
                                        <el-tag v-for="ccm in cm.children" :key="ccm.id" type="warning"
                                            class="margin-t10" closable @close="removeMenu(scope.row,ccm.id)">{{
                                            ccm.name }}</el-tag>
                                    </el-col>
                                </el-row>
                            </el-col>
                        </el-row>
                    </template>
                </el-table-column>
                <el-table-column prop="id" label="id" width="150" />
                <el-table-column prop="name" label="名称" />
                <el-table-column prop="desc" label="详情" />
                <el-table-column label="操作">
                    <template #default="scope">
                        <!-- <el-button size="mini"></el-button> -->
                        <el-button type="primary" size="mini" @click="showMenuDialog(scope.row)">分配权限</el-button>
                        <!-- <el-button type="danger" size="mini">删除</el-button> -->
                    </template>
                </el-table-column>
            </el-table>
        </el-row>
    </el-card>
    <el-dialog 
    v-model="menuDialogVisible" 
    title="分配权限" 
    width="40%" 
    :before-close="handleClose"

    >
        <el-tree show-checkbox :data="menuList" :props="menuProps" @node-click="handleNodeClick" node-key="id" ref="treeRef" default-expand-all/>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="menuDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="sumbitMenu">
                    确定
                </el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script setup>
  import { ArrowRight,CirclePlus } from '@element-plus/icons-vue';
  import api from "../api/index.js";
  import { onMounted, reactive,ref } from 'vue'
  import { nextTick } from 'vue';


  const tableData = reactive({
    authorList:[]
  })

  let menuDialogVisible = ref(false)
  let menuList = reactive([])
  const treeRef = ref(null)
  let rid = ref(null)

let keyList = reactive([])

  const menuProps = {
  children: 'children',
  label: 'name',
}

  onMounted(() => {
    get_author_list()
    getMenuList()
  })

  // 获取用户列表
const get_author_list = () => {
    api.get_roles().then(res => {
        console.log('角色数据:', res.data.data); 
        tableData.authorList = res.data.data
    })
}



// 删除角色权限
const removeMenu = (row, mid) => {
    ElMessageBox.confirm(
        '确实要删除该角色的权限吗？',
        '提示',
        {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(() => {
            ElMessage({
                type: 'success',
                message: '删除成功!',
            })
            api.del_role_menu(row.id, mid).then(res => {
                // console.log(res)
                get_author_list()
            })
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '已取消删除',
            })
        })
}

// const showMenuDialog = (row) => {
//   menuDialogVisible.value = true
//   // 初始化选中的菜单id
//   keyList = []
//   // 获取1级菜单
//   row.menus.forEach(item => {
//     // 获取2级菜单
//     item.children.forEach(citem => {
//         // 记录选中的菜单id
//         //keyList.push(citem.id)
//         // 遍历三级菜单（如果存在）
//         if (citem.children && citem.children.length > 0) {
//             citem.children.forEach(ccitem => {
//             keyList.push(ccitem.id) // 记录三级菜单的 ID
//             })
//         }
//     })
//   });
//   // 给叔结构设置默认选择
//   nextTick(() => { //当前dom渲染完成后执行
//     treeRef.value.setCheckedKeys(keyList)
//    })
// }

const showMenuDialog = (row) => {
  menuDialogVisible.value = true;
  keyList = [];
  
  // 仅收集当前角色的权限ID
  row.menus.forEach((item) => {
    keyList.push(item.id);  // 收集一级菜单ID
    item.children?.forEach((child) => {
      keyList.push(child.id);  // 收集二级菜单ID
      child.children?.forEach((grandChild) => {
        keyList.push(grandChild.id);  // 收集三级菜单ID
      });
    });
  });

  console.log('当前角色的权限ID:', keyList);  // 确保权限ID正确

  nextTick(() => {
    treeRef.value.setCheckedKeys(keyList);  // 设置树形结构的选中项
  });
  // 给角色id赋值
  rid.value = row.id
};



const getMenuList = () => {
  api.get_menu().then(res => {
    console.log('菜单列表:', res.data.data); // 确保打印的数据是你预期的
    menuList = res.data.data
   })
}


const sumbitMenu = () =>{
  // 获取菜单的ID
  let mids = [
    treeRef.value.getCheckedKeys(),
    treeRef.value.getHalfCheckedKeys()
   ]
   mids = mids.join(",")
//    console.log('菜单ID:', mids);
   // 获取角色id
//    console.log('角色ID:', rid.value);
   // 提交数据
   api.set_menu(rid.value,{'mids':mids}).then(res => {
     menuDialogVisible.value = false
     get_author_list()
   })


}
</script>


<style scoped>
 .box-card{
  margin-top: 20px;
  }
  .padding-l100{
    padding-left: 200px;
  }
  .top{
    border-top: 1px solid #73efd4;
  }

  .bottom{
    border-bottom: 1px solid #73efd4;

  }
  .margin-t10{
    margin: 10px;
  }

  .margin-t15{
    margin-top: 15px;
  }
</style>
