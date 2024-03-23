<script setup lang="ts">
import type { AppError } from '@/models/AppError'

defineProps<{ error: AppError }>()
</script>

<template>
  <div class="error-container">
    <strong v-if="!(typeof error == 'string')">
      {{ error.title }}
    </strong>
    <span>{{ error.detail || error }}</span>
  </div>
</template>

<style scoped>
.error-container {
  background-color: rgba(255, 30, 0, 0.1);

  border: 2px solid rgb(141, 28, 13);
  border-radius: 8px;
  padding: 8px;

  display: flex;
  flex-direction: column;
}
</style>
