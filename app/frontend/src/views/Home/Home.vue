<script setup lang="ts">
import SearchFlightsForm, { type FormDataScheme } from './components/SearchFlightsForm.vue'
import FlightsList from './components/FlightsList.vue'
import ErrorContainer from '@/views/components/ErrorContainer.vue'

import { Button, Divider } from 'ant-design-vue'
import { DollarCircleOutlined, StarOutlined, LikeOutlined } from '@ant-design/icons-vue'

import type { FlightsData } from '@/data/FlightService'
import FlightService from '@/data/FlightService'
import { ref } from 'vue'
import AuthService from '@/data/AuthService'
import type { AppError } from './models/AppError'

type Data = {
  isLoading: boolean
  error: AppError | null
  data: FlightsData | null
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

    const result = await FlightService.searchFlights(formData.destination, formData.date)

    setTimeout(() => {
      flightsEventData.value.data = result

      flightsEventData.value.isLoading = false
    }, 500)
  } catch (error: AppError) {
    flightsEventData.value.error = error
    flightsEventData.value.isLoading = false
  }
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
    <Button type="primary" ghost @click="login">Login</Button>
  </header>
  <main class="body">
    <!-- .body = light color (50% transparent) -->
    <SearchFlightsForm @form-button-click="search" />
    <ErrorContainer
      class="error-container"
      v-if="flightsEventData.error != null"
      :error="flightsEventData.error"
    />
    <h5 class="loading" v-if="flightsEventData.isLoading">Procurando os melhores voos...</h5>
    <div style="text-align: center" v-if="flightsEventData.data != null">
      <strong>Estas são as melhores alternativas de viagens para a sua data de decolagem</strong>
    </div>
    <div class="results" v-if="flightsEventData.data != null">
      <FlightsList title="Voo mais confortável e rápido" :flights="flightsEventData.data.comfort">
        <template #icon><StarOutlined /></template>
      </FlightsList>
      <Divider />
      <FlightsList title="Voo que cabe no seu bolso" :flights="flightsEventData.data.economic">
        <template #icon><DollarCircleOutlined /></template>
      </FlightsList>
      <Divider />
      <FlightsList title="Outros voos que voce pode gostar" :flights="flightsEventData.data.others">
        <template #icon><LikeOutlined /></template>
      </FlightsList>
    </div>
  </main>
</template>

<style scoped>
.body {
  display: flex;
  flex-direction: column;
  gap: 10px;

  /* padding: 16px; */

  border-radius: 16px;

  background-color: var(--color-background-soft);

  & .loading {
    text-align: center;
  }

  & .results {
    padding: 8px;

    display: flex;
    flex-direction: column;
  }
}

header {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
</style>
