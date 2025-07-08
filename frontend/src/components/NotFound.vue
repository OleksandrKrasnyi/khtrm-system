<template>
  <div class="not-found">
    <div class="not-found-content">
      <div class="error-icon">
        <i class="fas fa-exclamation-triangle"></i>
      </div>
      <h1>404</h1>
      <h2>Сторінку не знайдено</h2>
      <p>Вибачте, але сторінка, яку ви шукаєте, не існує.</p>
      <router-link to="/dashboard" class="back-btn">
        <i class="fas fa-arrow-left"></i>
        Повернутися на головну
      </router-link>
    </div>
  </div>
</template>

<script setup>
// Простой компонент, не требует логики
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.not-found-content {
  text-align: center;
  color: white;
  max-width: 500px;
}

.error-icon {
  font-size: 4rem;
  color: #ffd700;
  margin-bottom: 1rem;
}

.not-found-content h1 {
  font-size: 6rem;
  font-weight: 700;
  margin: 0;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.not-found-content h2 {
  font-size: 2rem;
  margin: 1rem 0;
  color: white;
}

.not-found-content p {
  font-size: 1.1rem;
  margin: 1rem 0 2rem;
  opacity: 0.9;
  line-height: 1.5;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  color: #2c3e50;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.back-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}
</style>
