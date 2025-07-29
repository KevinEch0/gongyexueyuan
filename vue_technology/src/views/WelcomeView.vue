<template>
  <div class="minimal-welcome">
    <div class="particle-network"></div>
    <h1 class="welcome-text">欢迎使用<br>管理系统</h1>
  </div>
</template>

<style scoped>
.minimal-welcome {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
  overflow: hidden;
  position: relative;
}

.welcome-text {
  font-size: 4rem;
  font-weight: 300;
  color: #2c3e50;
  text-align: center;
  line-height: 1.3;
  z-index: 10;
  opacity: 0;
  animation: fadeIn 2s ease-out forwards;
  animation-delay: 0.5s;
}

.particle-network {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

@keyframes fadeIn {
  to { opacity: 1; }
}

@media (max-width: 768px) {
  .welcome-text {
    font-size: 2.5rem;
  }
}
</style>

<script>
export default {
  mounted() {
    this.initParticleNetwork();
  },
  methods: {
    initParticleNetwork() {
      const container = document.querySelector('.particle-network');
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
          this.color = `rgba(44, 62, 80, ${Math.random() * 0.2 + 0.05})`;
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
              ctx.strokeStyle = `rgba(44, 62, 80, ${1 - distance/150})`;
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
  }
}
</script>