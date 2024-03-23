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
