<template>
    <div class="main">
        <!-- 移除原有的四个角元素 -->
        
        <div class="login-panel">
            <div class="logo-container">
                <img src="../assets/logo1.png" alt="Tech Logo" class="logo-img">
                <div class="scanline"></div>
            </div>
            <el-form :model="user" class="user_form" :rules="userRules" ref="userFormRef">
                <el-form-item prop="name">
                    <el-input v-model="user.name" placeholder="用户名" :prefix-icon="User"/>
                </el-form-item>
                <el-form-item prop="pwd">
                    <el-input v-model="user.pwd" placeholder="密码" :prefix-icon="Lock" show-password/>
                </el-form-item>
                <el-form-item class="btns">
                    <el-button type="primary" @click="submitForm(userFormRef)">登录</el-button>
                    <el-button type="success" @click="resetForm(userFormRef)">重置</el-button>
                </el-form-item>
            </el-form>
        </div>

        <!-- 替换为粒子网络背景 -->
        <div class="particle-network" ref="particleNetwork"></div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Lock, User } from '@element-plus/icons-vue'
import api from "../api/index.js"
import { useRouter } from 'vue-router'

// 表单数据
const user = reactive({
    name: '',
    pwd: ''
})

// 表单规则
const userRules = reactive({
    name: [
        { required: true, message: '用户名不能为空', trigger: 'blur' },
        { min: 3, max: 10, message: '长度在3到10个字符', trigger: 'blur' }
    ],
    pwd: [
        { required: true, message: '密码不能为空', trigger: 'blur' },
    ]
})

// 创建路由对象
const router = useRouter()

// 定义表单ref
const userFormRef = ref(null)
const particleNetwork = ref(null)

// 定义重置表单的方法
const resetForm = (formRef) => {
    formRef.resetFields();
}

// 定义登录功能
const submitForm = (formRef) => {
    formRef.validate((valid) => {
        if (valid) {
            console.log('验证通过，可以提交')
            api.getLogin(user).then(res => {
                if (res.data.status == 400) {
                    // 登录失败
                    ElMessage.error(res.data.msg)
                }
                else {
                    ElMessage({
                        message: res.data.msg,
                        type: 'success',
                    })
                    // 记录登录的Token值
                    sessionStorage.setItem('token', res.data.data.token)
                    localStorage.setItem('userRole', res.data.status);
    
                    // 跳转到主页
                    router.push({
                        path: '/home',
                        query: { role: res.data.status }  // 传递参数1
                    })
                }
            })
        } else {
            console.log('验证失败')
            return false
        }
    })
}

// 初始化粒子网络
onMounted(() => {
    initParticleNetwork();
})

const initParticleNetwork = () => {
    const container = particleNetwork.value;
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    let particles = [];
    const particleCount = 100;
    
    canvas.width = container.offsetWidth;
    canvas.height = container.offsetHeight;
    container.appendChild(canvas);
    
    // 创建粒子
    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.vx = -0.5 + Math.random();
            this.vy = -0.5 + Math.random();
            this.radius = 1 + Math.random() * 2;
            this.color = `rgba(0, 180, 255, ${Math.random() * 0.2 + 0.05})`;
        }
        
        update() {
            this.x += this.vx;
            this.y += this.vy;
            
            if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
            if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
        }
        
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.fill();
        }
    }
    
    // 初始化粒子
    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }
    
    // 绘制连接线
    function drawLines() {
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 150) {
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(0, 180, 255, ${1 - distance/150})`;
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
    }
    
    // 动画循环
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(particle => {
            particle.update();
            particle.draw();
        });
        
        drawLines();
        requestAnimationFrame(animate);
    }
    
    animate();
    
    // 窗口大小改变时重设画布
    window.addEventListener('resize', () => {
        canvas.width = container.offsetWidth;
        canvas.height = container.offsetHeight;
    });
}
</script>

<style scoped>
.main {
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    overflow: hidden;
    background-color: #f5f7fa;
}

.login-panel {
    width: 450px;
    height: 400px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 8px;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.1);
    padding: 30px;
    position: relative;
    overflow: hidden;
    z-index: 10;
}

.logo-container {
    width: 100%;
    height: 200px;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    margin-bottom: 30px;
}

.logo-img {
    max-width: 80%;
    max-height: 80%;
    filter: drop-shadow(0 0 10px rgba(145, 150, 152, 0.7));
}

.scanline {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        to bottom,
        transparent 0%,
        rgba(0, 180, 255, 0.1) 50%,
        transparent 100%
    );
    animation: scan 3s linear infinite;
    opacity: 0.5;
}

.particle-network {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
}

.user_form {
    display: flex;
    flex-direction: column;
    z-index: 20;
}

.btns {
    display: flex;
    justify-content: space-between;
}

.btns button {
    flex: 1;
}

@keyframes scan {
    from { transform: translateY(-100%); }
    to { transform: translateY(100%); }
}
</style>