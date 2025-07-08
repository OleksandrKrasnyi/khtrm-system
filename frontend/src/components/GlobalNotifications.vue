<template>
  <div class="notifications-container">
    <!-- Toast notifications будут автоматически отображаться здесь -->
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useToast } from "vue-toastification";

// Инициализация toast системы
const toast = useToast();

onMounted(() => {
  console.log("GlobalNotifications component mounted");
});
</script>

<style scoped>
.notifications-container {
  /* Стили для контейнера уведомлений, если нужны */
}
</style>
