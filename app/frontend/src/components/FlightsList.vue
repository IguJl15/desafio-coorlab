<script setup lang="ts">
import { Flight, type FlightType } from '@/models/Flight'
import FlightItem from '@/components/FlightItem.vue'

defineProps<{ title: string; flights: Flight[]; type: FlightType }>()
</script>

<template>
  <div>
    <div class="head">
      <div class="icon">
        <slot name="icon">i </slot>
      </div>
      <h4>{{ title }}</h4>
    </div>
    <div class="list">
      <template v-for="(item, index) in flights" :key="index">
        <FlightItem class="item" :flight="item" :type="type" />
      </template>
    </div>
  </div>
</template>

<style scoped>
.head {
  display: flex;
  align-items: center;
  gap: 8px;

  & h4 {
    margin: 0;
  }

  & .icon {
    width: 24px;
    height: 24px;

    display: flex;
    place-items: center;
    justify-content: center;

    font-size: large;
  }
}
.list {
  display: flex;
  flex-wrap: wrap;

  margin: 0 32px;

  & .item {
    background-color: var(--color-background-mute);
    width: 100%;

    margin-bottom: 12px;
  }
}

@media (min-width: 768px) {
  .list {
    & .item {
      width: 50%;
    }
  }
}
</style>
