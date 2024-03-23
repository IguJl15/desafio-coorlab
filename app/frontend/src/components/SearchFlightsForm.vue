<script setup lang="ts">
import { formatVerboseDestination } from '@/misc/helper'
import type { Airport } from '@/models/Flight'
import { computed, ref } from 'vue'

import airports from '@/data/airports.json'

export type FormDataScheme = {
  destination: Airport
  date: Date
}

defineEmits<{
  (e: 'form-button-click', data: FormDataScheme): void
}>()

const airportList: Airport[] = [{ code: 'THE', name: 'Teresina' }, ...airports]

const formData = ref<FormDataScheme>({
  destination: airportList[0],
  date: new Date()
})

// Computed references to enhance form data handle
const dateInputComp = computed({
  get() {
    return formData.value.date.toISOString().substring(0, 10)
  },
  // expect string but receives Date from "valueAsDate" property
  set(newValue: unknown) {
    formData.value.date = newValue as Date
  }
})

const destinationInputComp = computed({
  get() {
    return formatVerboseDestination(formData.value.destination)
  },
  set(newValue: string) {
    const code = newValue.split(' - ')[0]

    const airportHasCode = (airport: Airport) => airport.code == code

    if (code.length > 1 && airportList.some(airportHasCode)) {
      formData.value.destination = airportList.filter(airportHasCode)[0]
    }
  }
})
</script>

<template>
  <div class="search-form-container">
    <h2>Encontre o melhor voo para a sua viagem</h2>
    <p>Insira abaixo as informações da viagem que você planeja</p>
    <form action="/" method="get">
      <select v-model="destinationInputComp" list="cities-list">
        <template
          v-for="(item, index) in airportList.sort((a, b) => a.name.localeCompare(b.name))"
          :key="index"
        >
          <option :value="formatVerboseDestination(item)">
            {{ item.name }}
          </option>
        </template>
        <option></option>
      </select>
      <input
        type="date"
        @input="(event) => (dateInputComp = (event.target! as HTMLInputElement).valueAsDate)"
        :value="dateInputComp"
      />
      <button type="submit" @click.prevent="$emit('form-button-click', formData)">Procurar</button>
    </form>
  </div>
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

form input,
form select {
  padding: 4px;
}
</style>
