import axios from "../utils/requests.js"
import base from "./base.js"


const api = {
  /**
   * 登录
   */
  getLogin(params) {
    return axios.post(base.baseUrl + base.login, params)
   },
  get_menu(params) {
    return axios.get(base.baseUrl + base.get_menu,params)
  },
  get_menu_1(params) {
    return axios.get(base.baseUrl + base.get_menu_1,params)
  },
  get_menu_list(params) {
    return axios.get(base.baseUrl + base.get_menu_list,params)
  },
  get_user_list(params) {
    return axios.get(base.baseUrl + base.get_users,params)
  },
  add_user(params) {
    return axios.post(base.baseUrl + base.get_users,params)
  },
  get_user_by_id(id) {
    return axios.get(base.baseUrl + base.get_user_by_id + id+ "/")
  },
  delete_user(id) {
    return axios.delete(base.baseUrl + base.delete_user + id+ "/")
  },
  get_roles(params) {
    return axios.get(base.baseUrl + base.get_roles,params)
  },
  del_role_menu(rid,mid){
    return axios.get(base.baseUrl+base.del_role_menu+rid+'/'+mid+'/')
   },
  set_menu(rid,params){
    return axios.post(base.baseUrl+base.set_menu+rid+'/',params)
   },
 
}


export default api
