<script setup lang="ts">
import type { Flight, FlightType } from '@/models/Flight'
import { ArrowDownOutlined, ArrowRightOutlined } from '@ant-design/icons-vue'

const { flight, type } = defineProps<{ flight: Flight; type: FlightType }>()

let seatLabel: string
let seatDescription: string

switch (type) {
  case 'comfort':
    seatLabel = 'Leito'
    seatDescription = 'completo'
    break
  case 'economic':
    seatLabel = 'Assento'
    seatDescription = 'convencional'
    break
}

const numberFormatter = Intl.NumberFormat()
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
      <strong>R$ {{ numberFormatter.format(flight.price) }}</strong>
    </div>
  </div>
</template>

<style scoped>
.flight {
  display: flex;

  background-color: var(--color-background-mute);
  /* margin-top: 8px; */

  & > div {
    padding: 8px;
  }
  & h3,
  h4,
  h5 {
    margin: 0;
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
    & .header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      border-bottom: 1px solid var(--color-border);
    }

    width: 100%;
    display: flex;
    flex-direction: column;
  }

  & .right {
    display: flex;
    justify-content: center;
    flex-direction: column;

    background-color: var(--primary-color);

    line-height: normal;
    text-wrap: nowrap;
  }
}
</style>
