<script setup lang="ts">
import SearchFlightsForm, { type FormDataScheme } from '@/components/SearchFlightsForm.vue'
import ErrorContainer from '@/components/ErrorContainer.vue'

import type { FlightsResponse } from '@/data/FlightService'
import FlightService from '@/data/FlightService'
import { ref } from 'vue'
import AuthService from './data/AuthService'
import type { AppError } from './models/AppError'

type Data = {
  isLoading: boolean
  error: AppError | null
  data: FlightsResponse | null
}

const flightsEventData = ref<Data>({
  isLoading: false,
  error: null,
  data: null
})

async function search(formData: FormDataScheme): Promise<void> {
  clearData()
  try {
    flightsEventData.value.isLoading = true
    // validate data

    const result = await FlightService.searchFlights(formData.destination, formData.date)

    flightsEventData.value.data = result
  } catch (error: AppError) {
    flightsEventData.value.error = error
  }

  flightsEventData.value.isLoading = false
}

function clearData() {
  flightsEventData.value.data = null
  flightsEventData.value.error = null
}

function login() {
  AuthService.login('igorj', 'admin')
}
</script>

<template>
  <header class="">
    <h1>Calculadora de Viagens Aéreas</h1>
    <button type="button" @click="login"></button>
  </header>
  <main class="body">
    <!-- .body = light color (50% transparent) -->
    <SearchFlightsForm @form-button-click="search" />
    <ErrorContainer v-if="flightsEventData.error != null" :error="flightsEventData.error" />
    <div v-if="flightsEventData.isLoading">Loading...</div>
    <div v-if="flightsEventData.data != null" class="results">
      <div class="comfort">
        <h3>Conforto {{ flightsEventData.data.comfort.length }}</h3>

        <div v-if="flightsEventData.data.comfort.length > 0">
          <div class="info" v-for="(flight, index) in flightsEventData.data.comfort" :key="index">
            <h4>{{ flight.company_name }}</h4>
            <span> Destino: {{ flight.city_destination }} </span>
            <span>Duração estimada: {{ flight.duration }} </span>
            <span> Preço: {{ flight.price_comfort }} </span>
            <span> Leito: {{ flight.comfort_bed_location }} (Completo) </span>
          </div>
        </div>
        <div v-else>Nenhum voo encontrado</div>
      </div>

      <div class="economic">
        <h3>Econômico {{ flightsEventData.data.economic.length }}</h3>

        <div v-if="flightsEventData.data.economic.length > 0">
          <div class="info" v-for="(flight, index) in flightsEventData.data.economic" :key="index">
            <h4>{{ flight.company_name }}</h4>
            <span>Destino: {{ flight.city_destination }}</span>
            <span>Duração estimada: {{ flight.duration }} </span>
            <span>Preço: {{ flight.price_economic }}</span>
            <span>Assento: {{ flight.economic_seat_location }}</span>
          </div>
        </div>
        <div v-else>Nenhum voo encontrado</div>
      </div>
      <div class="others">
        <h3>Outros {{ flightsEventData.data.others.length }}</h3>

        <div v-if="flightsEventData.data.others.length > 0">
          <div class="info" v-for="(flight, index) in flightsEventData.data.others" :key="index">
            <h4>{{ flight.company_name }}</h4>
            <span> Destino: {{ flight.city_destination }} </span>
            <span>Duração estimada: {{ flight.duration }} </span>
            <div>
              Preços:
              <span>Econômica: {{ flight.price_economic }}</span>
              <span>Comfort: {{ flight.price_comfort }}</span>
            </div>
            <div>
              Assentos:
              <span>Econômica: {{ flight.economic_seat_location }}</span>
              <span>Comfort: {{ flight.comfort_bed_location }}</span>
            </div>
          </div>
        </div>
        <div v-else>Nenhum voo encontrado</div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.info {
  display: flex;
  flex-direction: column;

  background-color: darkslategray;

  padding: 8px;
  margin-bottom: 4px;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
