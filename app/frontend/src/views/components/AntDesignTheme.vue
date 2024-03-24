<script setup lang="ts">
import { ConfigProvider, theme } from 'ant-design-vue'
import { ref } from 'vue'

// MediaQueryList
const darkModePreference = window.matchMedia('(prefers-color-scheme: dark)')

const scheme = ref<'light' | 'dark'>(darkModePreference.matches ? 'dark' : 'light')

// recommended method for newer browsers: specify event-type as first argument
darkModePreference.addEventListener('change', (e) => changeScheme(e.matches))
// deprecated method for backward compatibility
darkModePreference.addListener((e) => changeScheme(e.matches))

function changeScheme(isDark: boolean) {
  if (isDark) {
    scheme.value = 'dark'
  } else {
    scheme.value = 'light'
  }
}
</script>

<template>
  <ConfigProvider
    :theme="{
      algorithm: scheme == 'dark' ? theme.darkAlgorithm : theme.defaultAlgorithm
    }"
  >
    <slot></slot>
  </ConfigProvider>
</template>
