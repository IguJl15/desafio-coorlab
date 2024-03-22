<script setup lang="ts">
import type { Flight, Airport } from '@/models/Flight'
import { ref, onMounted } from 'vue'

type Data = {
  isLoading: boolean
  error: string | null
  data: {
    comfortFlights: Flight[]
    economicFlights: Flight[]
    othersFlights: Flight[]
  } | null
}

const flightsEventData = ref<Data>({
  isLoading: false,
  error: null,
  data: null
})

const formData = ref({
  destination: '',
  date: Date.now()
})

const airportList: Airport[] = [{ code: 'THE', name: 'Teresina' }]

onMounted(() => {
  console.log(`Alo, on mounted! Counter is ${flightsEventData.value}`)
})

function search() {
  clearResults()
  flightsEventData.value.isLoading = true
  // validate data

  setTimeout(() => {
    flightsEventData.value.isLoading = false
    flightsEventData.value.data = {
      comfortFlights: [],
      economicFlights: [],
      othersFlights: []
    }
  }, 1000)
}

function clearResults() {
  flightsEventData.value.data = null
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
        <input type="text" v-model="formData.destination" list="cities-list" />
        <datalist id="cities-list">
          <option value="Internet"></option>
          <template v-for="(item, index) in airportList" :key="index">
            <option :value="item.code">{{ item.name }}</option>
          </template>
          <option></option>
        </datalist>
        <input type="date" v-model="formData.date" />
        <button type="button" @click.prevent="search">Procurar</button>
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
