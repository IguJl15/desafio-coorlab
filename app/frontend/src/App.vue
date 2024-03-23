<script setup lang="ts">
import type { FlightsResponse } from '@/data/FlightService'
import FlightService from '@/data/FlightService'
import type { Airport } from '@/models/Flight'
import { computed, ref } from 'vue'

const airportList: Airport[] = [
  { code: 'THE', name: 'Teresina' },
  { code: 'CWB', name: 'Curitiba' }
]

type Data = {
  isLoading: boolean
  error: string | null
  data: FlightsResponse | null
}

const flightsEventData = ref<Data>({
  isLoading: false,
  error: null,
  data: null
})

const formData = ref({
  destination: airportList[0],
  date: new Date()
})

async function search() {
  try {
    flightsEventData.value.isLoading = true
    // validate data

    const result = await FlightService.searchFlights(
      formData.value.destination,
      formData.value.date
    )
    console.log(result)

    flightsEventData.value.isLoading = false
    flightsEventData.value.data = result
  } catch (error) {
    flightsEventData.value.error = error.toString()
  }

  flightsEventData.value.isLoading = false
}

// Computed references to enhance form data handle
const dateInputComp = computed({
  get() {
    return formData.value.date.toISOString().substring(0, 10)
  },
  set(newValue) {
    formData.value.date = newValue as unknown as Date
  }
})

const destinationInputComp = computed({
  get() {
    return formatVerboseDestination(formData.value.destination)
  },
  set(newValue) {
    const code = newValue.split(' - ')[0]
    formData.value.destination = airportList.filter((airport) => airport.code == code)[0]
  }
})

function formatVerboseDestination(dest: Airport) {
  return `${dest.code} - ${dest.name}`
}
</script>

<template>
  <header class="">
    <h1>Calculadora de Viagens Aéreas</h1>
  </header>
  <main class="body">
    <!-- .body = light color (50% transparent) -->
    <div class="search-form-container">
      <h2>Encontre o melhor voo para a sua viagem</h2>
      <p>Insira abaixo as informações da viagem que você planeja</p>
      <form action="" method="get">
        <select v-model="destinationInputComp" list="cities-list">
          <template v-for="(item, index) in airportList" :key="index">
            <option :value="formatVerboseDestination(item)">
              {{ formatVerboseDestination(item) }}
            </option>
          </template>
          <option></option>
        </select>
        <input
          type="date"
          @input="(event) => (dateInputComp = event.target!.valueAsDate)"
          :value="dateInputComp"
        />
        <button type="submit" @click="search">Procurar</button>
      </form>
    </div>
    <div v-if="flightsEventData.isLoading">Loading...</div>
    <div v-if="flightsEventData.data != null" class="results">
      <div class="comfort">Conforto de {{ flightsEventData }}</div>
      <div class="economic">Economia</div>
      <div class="others">e outros</div>
    </div>
  </main>
</template>

<style scoped>
.search-form-container {
  display: flex;
  flex-direction: column;

  & form {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
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
