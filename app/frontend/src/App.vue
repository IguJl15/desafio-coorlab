<script setup lang="ts">
import Home from '@/views/Home/Home.vue'
import Login from '@/views/Auth/Login.vue'
import { computed, ref } from 'vue'
import AntDesignTheme from '@/views/components/AntDesignTheme.vue'

const routes = {
  '/': Home,
  '/login': Login
}

const currentPath = ref(window.location.hash)

window.addEventListener('hashchange', () => {
  currentPath.value = window.location.hash
})

const currentView = computed(() => {
  const route = currentPath.value.slice(1) || '/'
  return routes[route] || NotFound
})
</script>

<template>
  <AntDesignTheme>
    <component :is="currentView" />
  </AntDesignTheme>
</template>
