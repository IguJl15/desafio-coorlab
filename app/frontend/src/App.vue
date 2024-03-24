<script setup lang="ts">
import Home from '@/views/Home/Home.vue'
</script>

<template>
  <AntDesignTheme>
    <Home />
  </AntDesignTheme>
</template>

<style scoped>
.body {
  display: flex;
  flex-direction: column;
  gap: 10px;

  /* padding: 16px; */

  border-radius: 16px;

  background-color: var(--color-background-soft);

  & .loading {
    text-align: center;
  }

  & .results {
    padding: 8px;

    display: flex;
    flex-direction: column;
  }
}

header {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
</style>
