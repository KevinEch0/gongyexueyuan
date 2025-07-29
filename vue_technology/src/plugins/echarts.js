

import * as echarts from 'echarts';


export default {
    // echarts 作为全局变量
    install:app => {
        // 配置 echarts 作为全局变量,element 代表将图表渲染到那个元素上
        app.config.globalProperties.$echarts = (element,option) => {
            // 创建一个 echarts 实例
            let myChart =  echarts.init(document.getElementById(element));
            // 创建图标需要显示的数据

            // 渲染图表
            myChart.setOption(option);
            
            }
           
        }
    }
