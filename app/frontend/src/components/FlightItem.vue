<script setup lang="ts">
import type { Flight } from '@/models/Flight'
import { ArrowDownOutlined, ArrowRightOutlined } from '@ant-design/icons-vue'

const { flight } = defineProps<{ flight: Flight }>()

let seatLabel: string
let seatDescription: string

switch (flight.type) {
  case 'comfort':
    seatLabel = 'Leito'
    seatDescription = 'completo'
    break
  case 'economic':
    seatLabel = 'Assento'
    seatDescription = 'convencional'
    break
}

console.log(seatLabel)
console.log(seatDescription)
console.log(flight);


const numberFormatter = Intl.NumberFormat(undefined, {
  style: 'currency',
  currency: 'BRL',
  currencyDisplay: 'code'
})
</script>

<template>
  <div class="flight">
    <div class="left">
      <span>{{ flight.origin.code }}</span>
      <ArrowDownOutlined />
      <span>{{ flight.destination.code }}</span>
    </div>
    <div class="flight-info">
      <div class="header">
        <h4>{{ flight.company_name.toUpperCase() }}</h4>
        <span> {{ flight.origin.name }} <ArrowRightOutlined /> {{ flight.destination.name }} </span>
      </div>
      <span>{{ seatLabel }}: {{ flight.seat }} ({{ seatDescription }})</span>
      <span>Tempo estimado: {{ flight.duration }} </span>
    </div>
    <div class="right">
      <span>Valor:</span>
      <strong>R${{ numberFormatter.format(flight.price).replace('BRL', '') }}</strong>
    </div>
  </div>
</template>

<style scoped>
.flight {
  display: flex;

  background-color: var(--color-background-mute);
  /* margin-top: 8px; */
  border-radius: 4px;
  overflow: hidden;

  & h3,
  h4,
  h5 {
    margin: 0;
  }

  & .left,
  .right {
    padding: 8px;
    color: var(--vt-c-text-dark-1);
  }

  & .left {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    /* gap: 8px; */

    padding: 0 24px;

    background-color: var(--primary-color-dark);

    line-height: normal;
  }

  & .flight-info {
    background-color: var(--primary-color-darker);

    width: 100%;
    display: flex;
    flex-direction: column;

    & .header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      border-bottom: 1px solid var(--color-border);

      padding: 8px 0;
    }

    & * {
      padding: 0 8px;
    }
  }

  & .right {
    width: 100px;
    display: flex;
    justify-content: center;
    flex-direction: column;

    background-color: var(--primary-color);

    line-height: normal;
    text-wrap: nowrap;
  }
}

@media (max-width: 460px) {
  .flight {
    flex-direction: column;
    & .left {
      display: none;
    }

    & .right {
      width: 100%;
    }
  }
}
</style>
