<template>
  <div class="notifications-container">
    <!-- Toast notifications will be automatically displayed here -->
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

// This component serves as a container for vue-toastification
// Toast notifications are automatically displayed through the useNotifications composable

export default defineComponent({
  name: 'GlobalNotifications'
});
</script>

<style scoped>
.notifications-container {
  /* Styles for notifications container if needed */
}
</style>
