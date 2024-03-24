<script setup lang="ts">
import FlightsList from './components/FlightsList.vue'
import SearchFlightsForm, { type FormDataScheme } from './components/SearchFlightsForm.vue'
import ErrorContainer from '@/views/components/ErrorContainer.vue'
import { authState } from '@/views/Auth/AuthState'

import { DollarCircleOutlined, LikeOutlined, StarOutlined } from '@ant-design/icons-vue'
import { Button, Divider } from 'ant-design-vue'

import AuthService from '@/data/AuthService'
import type { FlightsData } from '@/data/FlightService'
import FlightService from '@/data/FlightService'
import type { AppError } from '@/models/AppError'
import { ref } from 'vue'

const { isLoggedIn } = authState.value
if (!isLoggedIn) {
  redirectToLogin()
}

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

function redirectToLogin() {
  window.location.hash = '/login'
}

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

function logout() {
  AuthService.logout()
  authState.value.loggedOut()
  redirectToLogin()
}
</script>

<template>
  <div class="header-bar">
    <div class="header-bar-content">
      <img src="@/assets/logo.png" alt="CB Viagens Logo" srcset="" height="52" />
      <Button v-if="authState.isLoggedIn" type="primary" danger ghost @click="logout"
        >LogOut</Button
      >
      <!-- Just in case some delay happen on auth systems -->
      <Button v-else type="primary" @click="redirectToLogin">Login</Button>
    </div>
  </div>

  <header>
    <h1>Calculadora de Viagens Aéreas</h1>
  </header>
  <main class="body">
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

.header-bar {
  position: absolute;

  top: 0;
  left: 0;
  right: 0;

  padding: 16px 8px;

  background-color: var(--vt-c-black-soft);

  & .header-bar-content {
    margin: 0 auto;
    max-width: 1280px;

    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;

    & img {
      height: 32px;
    }
  }
}
</style>
