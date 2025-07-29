<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>用户管理</el-breadcrumb-item>
        <el-breadcrumb-item>用户列表</el-breadcrumb-item>
    </el-breadcrumb>


    <el-card class="box-card">
        <el-row :gutter="12">
            <el-col :span="8">
                <el-input v-model="user_data.queryName" placeholder="输入要搜索的账号" class="input-with-select">
                    <template #append>
                        <el-button :icon="Search" @click="searchUser" />
                    </template>
                </el-input>
            </el-col>
            <el-col :span="1">
                <el-button type="primary" :icon="CirclePlus" @click="addDialogVisible = true">增加用户</el-button>
            </el-col>
        </el-row>
        <el-row>
            <el-table :data="user_data.tableData" stripe class="table">
                <el-table-column prop="id" label="id" width="320" />
                <el-table-column prop="name" label="账号" width="320" />
                <el-table-column prop="role_name" label="角色" width="320" />
                <el-table-column label="操作">
                    <template #default="scope">
                        <!-- <el-button size="small" @click="handleEdit(scope.$index, scope.row)">Edit
                        </el-button> -->
                        <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">Delete
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-row>


        <el-pagination v-model:current-page="user_data.pageNum" v-model:page-size="user_data.pageSize"
            :page-sizes="pageSizes" :small="small" :disabled="disabled" :background="background"
            layout="total, sizes, prev, pager, next, jumper" :total="user_data.total" @size-change="handleSizeChange"
            @current-change="handleCurrentChange" class="table" />
    </el-card>


    <!-- 增加用户对话框 -->
    <el-dialog v-model="addDialogVisible" title="增加用户" :before-close="addFormRest">
        <el-form :model="user_form" :rules="user_rules" ref="addFormRef">
            <el-form-item label="用户名" :label-width="formLabelWidth" prop="name">
                <el-input v-model="user_form.name" autocomplete="off" />
            </el-form-item>
            <el-form-item label="密码" :label-width="formLabelWidth" prop="pwd">
                <el-input v-model="user_form.pwd" autocomplete="off" />
            </el-form-item>
            <el-form-item label="确认密码" :label-width="formLabelWidth" prop="real_pwd">
                <el-input v-model="user_form.real_pwd" autocomplete="off" />
            </el-form-item>
            <el-form-item label="角色" :label-width="formLabelWidth" prop="rold_id">
                <el-select v-model="user_form.role_id" placeholder="请选择角色">
                    <el-option :label="r.name" :value="r.id" v-for="r in roles" :key="r.id" />
                </el-select>
            </el-form-item>

        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="addFormRest">取消</el-button>
                <el-button type="primary" @click="addUser(addFormRef)">
                    确定
                </el-button>
            </span>
        </template>
    </el-dialog>

    <!-- 编辑用户 -->
    <el-dialog v-model="editDialogVisible" title="修改用户">
        <el-form :model="edit_form" :rules="edit_rules" ref="editFormRef">
            <el-form-item label="用户名" :label-width="formLabelWidth" prop="name">
                <el-input v-model="edit_form.name" autocomplete="off" disabled/>
            </el-form-item>
            <el-form-item label="角色" :label-width="formLabelWidth" prop="rold_id">
                <el-select v-model="edit_form.role_id" placeholder="请选择角色">
                    <el-option :label="r.name" :value="r.id" v-for="r in roles" :key="r.id" />
                </el-select>
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="editFormRest">取消</el-button>
                <el-button type="primary" @click="editUser(editFormRef)">
                    确定
                </el-button>
            </span>
        </template>
    </el-dialog>

    <!-- 删除用户 -->
    <el-dialog v-model="deleteDialogVisible" title="删除用户">
        <span>确定删除账号:{{ remove_user.name }}, 的用户吗？</span>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="deleteDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="deleteUser">
                    确定
                </el-button>
            </span>
        </template>
    </el-dialog>



</template>


<script setup>
import { ArrowRight,Search,CirclePlus, Edit  } from '@element-plus/icons-vue'
import api from '../api/index.js'
import { onMounted,reactive,ref} from 'vue'



const tableData = [
  {
  id: '2016-05-03',
  name: 'Tom',
  
  },
  {
  id: '2016-05-02',
  name: 'Tom',

  },
  {
  id: '2016-05-04',
  name: 'Tom',

  },
  {
  id: '2016-05-01',
  name: 'Tom',

  },
]

const user_data = reactive({
    tableData:[],
    total:10,
    pageNum:1,
    pageSize:3,
    queryName:'',
})


  const user_form = reactive({
   name: null,
   pwd: null,
   real_pwd: null,
   role_id: null,

   })

  let edit_form = reactive({
   name: null,
   role_id: null,


   })

   let remove_user = reactive({
   name: null,
   id: null,
   })

  // 定义验证确认密码的规则
  const validatePass2 = (rule, value, callback) => {
   if (value === '') {
    callback(new Error('请输入确认密码'))
    } else if (value !== user_form.pwd) {
    callback(new Error("2次密码不匹配!"))
    } else {
    callback()
    }
   }

  let pageSizes = ref([1,2,5,10])
  const small = ref(false)
  const background = ref(false)
  const disabled = ref(false)
  const addDialogVisible = ref(false)
  const formLabelWidth = ref('80px')
  const editDialogVisible = ref(false)
  const editFormRef = ref(null)
  const userID = ref(0)
  const deleteDialogVisible = ref(false)
  let roles = ref([])

  const user_rules = reactive({
   name: [
   { required: true, message: '请输入用户名', trigger: 'blur' },
   { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
   ],
   pwd:[
     { required: true, message: '请输入密码', trigger: 'blur' },
     { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
    ],
   real_pwd:[
     { required: true, message: '请输入确认密码', trigger: 'blur' },
     { validator: validatePass2, trigger: 'blur' }
    ],
  })



const get_user_list = () => { 
    let params = {
        'pnum':user_data.pageNum,
        'psize':user_data.pageSize,
        'name':user_data.queryName
    }
    api.get_user_list({params}).then(res => { 
      // 更新用户列表数据
      user_data.tableData = res.data.data.data
      // 更新分页数据总数
      user_data.total = res.data.data.total
    }).catch(error => {
  console.error("请求失败:", error);
});

}

onMounted(() => { 
    get_user_list()
    get_author_list()
})


  const handleSizeChange = (val) => {
   // 修改每页显示多少条数据
   user_data.pageSize = val
   // 重新获取用户列表数据
   get_user_list()
   }
  const handleCurrentChange = (val) => {
   //修改显示第几页数据
   user_data.pageNum = val
   // 重新获取用户列表数据
   get_user_list()
   }

    const searchUser = () => {
   //初始化页码
   user_data.pageNum = 1
   // 重新获取用户列表数据
   get_user_list()
   }

const addFormRef = ref(null)
  const addFormRest = () => {
  // 重置表单
  addFormRef.value.resetFields()
  // 关闭对话框
  addDialogVisible.value = false
}


// 添加用户
const addUser = (formRef) => {
 formRef.validate((valid) => {
    if (valid) {
      console.log('验证通过，可以提交')
      api.add_user(user_form).then(res => {
        //根据响应的结果进行处理
        if (res.data.status == 200){
          ElMessage({
            message: res.data.msg,
            type: 'success',
           })
          // 重置表单
          addFormRest()
          // 重新获取数据
          get_user_list()
         }else{
          ElMessage.warning(res.data.msg)
         }
       })
     } else {
      console.log('验证失败')
      return false
     }
   })
}

// 编辑用户
const handleEdit = (index,row) => {
  // 显示编辑对话框
  editDialogVisible.value = true
  // edit_form = row //把当前行的数据赋值给编辑表单
  // 从数据库获取当前用户的数据
  api.get_user_by_id(row.id).then(res => {
    // 把当前行的数据赋值给编辑表单
    // edit_form = res.data.data
    edit_form.name = res.data.data.name
    edit_form.role_id = res.data.data.role_id

   })
} 

// 获取角色列表
const get_author_list = () => {
  api.get_roles().then(res => {
   roles = res.data.data
   })
}


// 删除用户控制器
const handleDelete =(index,row) =>{
 remove_user.id = row.id
 remove_user.name = row.name
 deleteDialogVisible.value = true
}


// 删除用户操作
const deleteUser = () =>{
 // 请求删除用户的API调用
 api.delete_user(remove_user.id).then(res => {
  if(res.status == 200){
   ElMessage({
    message: res.data.msg,
    type: 'success',
    })
   deleteDialogVisible.value = false
   get_user_list()
   }else{
   ElMessage.warning(res.data.msg)
   }
  })
}



</script>


<style scoped>
 .box-card{
  margin-top: 20px;
  }
 .table{
  margin-top: 10px;
  }
</style>
