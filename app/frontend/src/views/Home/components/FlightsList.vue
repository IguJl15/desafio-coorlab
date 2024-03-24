<script setup lang="ts">
import { Flight, type FlightType } from '@/models/Flight'
import FlightItem from '@/views/Home/components/FlightItem.vue'

defineProps<{ title: string; flights: Flight[] }>()
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
      <div class="empty-list-alert" v-if="flights.length == 0">
        Infelizmente não encontramos voos com essas especificações. <br />
        O que acha de testar outra data ou destino?
      </div>
      <template v-for="(item, index) in flights" :key="index">
        <FlightItem class="item" :flight="item" />
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
  justify-content: space-between;
  flex-wrap: wrap;

  margin: 0 32px;

  & .item {
    background-color: var(--color-background-mute);
    width: 100%;

    margin-bottom: 12px;
  }
}
.empty-list-alert {
  width: 100%;
  text-align: center;

  background-color: var(--color-background-mute);
  color: var(--color-heading);
  padding: 8px 0;
  border-radius: 8px;

  line-height: normal;
  letter-spacing: -0.2px;
}

@media (min-width: 768px) {
  .list {
    & .item {
      width: 49%;
    }
  }
}
</style>
