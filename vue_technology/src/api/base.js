

/**
 * 存放所有网络请求地址
 */
const base = {
  baseUrl:"http://localhost:5000",     // 公共地址
  login:"/user/login/",           // 登录地址 
  get_menu:"/menu/menus/?user_id=4&type_=tree",           // 获取菜单
  get_menu_1:"/menu/menus/?user_id=1&type_=tree",           // 获取菜单
  get_menu_list:'/menu/menus2/',           // 获取菜单列表
  get_users:'/user/users/',        //获取用户列表
  get_user_by_id:'/user/user/',   //根据id获取用户信息
  delete_user:'/user/user/',      //删除用户
  get_roles:'/roles/',       //获取角色列表
  del_role_menu:'/role/',         //删除角色菜单
  set_menu:'/role/',           //设置角色菜单
  
}
export default base
