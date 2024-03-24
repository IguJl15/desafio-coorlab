<script setup lang="ts">
import { formatVerboseDestination } from '@/misc/helper'
import type { Airport } from '@/models/Flight'
import { computed, ref } from 'vue'

import { Button, Form, FormItem, Input, Select, SelectOption } from 'ant-design-vue'
import {
  ArrowRightOutlined,
  LoginOutlined,
  LogoutOutlined,
  SearchOutlined
} from '@ant-design/icons-vue'

import airports from '@/data/airports.json'

export type FormDataScheme = {
  destination: Airport
  date: Date
}

defineEmits<{
  (e: 'form-button-click', data: FormDataScheme): void
}>()

const airportList: Airport[] = [{ code: 'THE', name: 'Teresina' }, ...airports]

const formState = ref<FormDataScheme>({
  destination: airportList[0],
  date: new Date()
})

// Computed references to enhance form data handle
const dateInputComp = computed({
  get() {
    return formState.value.date?.toISOString().substring(0, 10)
  },
  // expect string but receives Date from "valueAsDate" property
  set(newValue) {
    if (newValue) formState.value.date = newValue as Date
  }
})

const destinationInputComp = computed({
  get() {
    return formatVerboseDestination(formState.value.destination)
  },
  set(newValue: string) {
    const code = newValue.split(' - ')[0]

    const airportHasCode = (airport: Airport) => airport.code == code

    if (code.length > 1 && airportList.some(airportHasCode)) {
      formState.value.destination = airportList.filter(airportHasCode)[0]
    }
  }
})
</script>

<template>
  <div class="search-form-container">
    <div>
      <h3>Encontre o melhor voo para a sua viagem</h3>
      <p>Insira abaixo as informações da viagem que você planeja</p>
    </div>

    <Form
      class="search-form"
      layout="vertical"
      @finish="$emit('form-button-click', formState)"
      :model="formState"
    >
      <FormItem
        class="form-item"
        label="Destino"
        :rules="[{ required: true, message: 'Escolha seu destino' }]"
      >
        <!-- event has the value of the "value" prop from SelectOption  -->
        <Select
          show-search
          name="destination"
          :value="destinationInputComp"
          @change="
            (event) => {
              destinationInputComp = event?.toString() ?? ''
            }
          "
        >
          <template #placeholder> <LogoutOutlined style="color: black" /> Busca </template>
          <template
            v-for="(item, index) in airportList.sort((a, b) => a.name.localeCompare(b.name))"
            :key="index"
          >
            <SelectOption :value="formatVerboseDestination(item)">
              {{ item.name }}
            </SelectOption>
          </template>
        </Select>
      </FormItem>
      <ArrowRightOutlined style="color: white" />
      <FormItem class="form-item" label="Data da viagem">
        <Input
          name="date"
          type="date"
          placeholder="Procure a cidade de destino"
          @input="(event) => (dateInputComp = (event.target! as HTMLInputElement).valueAsDate)"
          :value="dateInputComp"
        >
          <template #prefix>
            <LoginOutlined />
          </template>
        </Input>
      </FormItem>
      <Button class="button" type="primary" html-type="submit">
        <template #icon>
          <SearchOutlined />
        </template>
        Procurar Voos
      </Button>
    </Form>
  </div>
</template>

<style scoped>
.search-form-container {
  display: flex;
  flex-direction: column;
  gap: 8px;

  padding: 16px;
  border-radius: 12px;

  background-color: var(--color-background-soft);

  & h3,
  p {
    margin: 0;
  }

  & .search-form {
    display: flex;
    flex-direction: row;
    place-items: center;
    gap: 8px;

    & .button {
      align-self: end;

      margin-bottom: 6px;
    }

    & .form-item {
      width: 100%;

      background-color: var(--color-background);
      padding: 6px;
      border-radius: 6px;

      margin: 0;
    }
  }
}
</style>
