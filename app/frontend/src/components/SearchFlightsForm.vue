<script setup lang="ts">
import { formatVerboseDestination } from '@/misc/helper'
import type { Airport } from '@/models/Flight'
import { reactive, ref, toRaw } from 'vue'
import { Dayjs } from 'dayjs'

import { Button, Form, FormItem, DatePicker, Select, SelectOption } from 'ant-design-vue'
import type { Rule } from 'ant-design-vue/es/form'
import type { ValidateErrorEntity } from 'ant-design-vue/es/form/interface'
import {
  ArrowRightOutlined,
  LoginOutlined,
  LogoutOutlined,
  SearchOutlined
} from '@ant-design/icons-vue'

import airports from '@/data/airports.json'

const emit = defineEmits<{
  (e: 'form-button-click', data: FormDataScheme): void
}>()

export type FormDataScheme = {
  destination: Airport
  date: Date
}

const formRef = ref()
const rules: Record<string, Rule> = {
  origin: { required: true, message: 'Escolha de onde você irá viajar', trigger: 'change' },
  destination: { required: true, message: 'Escolha o destino da sua viagem', trigger: 'change' },
  date: {
    required: true,
    message: 'Escolha a data da sua viagem',
    trigger: 'change',
    type: 'object'
  }
}

const mockAirport = { code: 'THE', name: 'Teresina' }
const airportList: Airport[] = [mockAirport, ...airports]

const formState = reactive<{
  origin: string | undefined
  destination: string
  date: Dayjs | undefined
}>({
  origin: undefined,
  destination: airportList[0].name,
  date: undefined
})

function onSubmit() {
  console.log('Validating')

  formRef.value
    .validate()
    .then(() => {
      console.log('values', formState, toRaw(formState))
      emit('form-button-click', {
        date: formState.date!.toDate(),
        destination: airportList.filter((air) => air.name == formState.destination)[0]
      })
    })
    .catch((error: any) => {
      console.log('error', error)
    })
}

// dialog
const dialogRef = ref<HTMLDialogElement>()
const dialogErrors = ref<string[] | undefined>()

function onFormError(errors: ValidateErrorEntity) {
  console.log('errors', errors)
  dialogErrors.value = errors.errorFields.reduce<string[]>((list, err) => {
    list.push(...err.errors)
    return list
  }, [])
  dialogRef.value?.showModal()
}
</script>

<template>
  <div class="search-form-container">
    <div>
      <h3>Encontre o melhor voo para a sua viagem</h3>
      <p>Insira abaixo as informações da viagem que você planeja</p>
    </div>

    <Form
      ref="formRef"
      layout="vertical"
      class="search-form"
      :model="formState"
      :rules="rules"
      @finish="onSubmit"
      @finish-failed="onFormError"
    >
      <FormItem class="form-item" ref="origin" name="origin" label="Origem">
        <div class="input-row-icon">
          <Select show-search placeholder="De onde viemos" v-model:value="formState.origin">
            <SelectOption :value="mockAirport.name">
              {{ mockAirport.name }}
            </SelectOption>
          </Select>
          <LogoutOutlined />
        </div>
      </FormItem>
      <ArrowRightOutlined :class="'arrow'" style="color: white" />
      <FormItem class="form-item" ref="destination" name="destination" label="Destino">
        <!-- event has the value of the "value" prop from SelectOption  -->
        <div class="input-row-icon">
          <LoginOutlined />
          <Select
            show-search
            placeholder="Encontre seu destino"
            v-model:value="formState.destination"
          >
            <template
              v-for="(item, index) in airportList.sort((a, b) => a.name.localeCompare(b.name))"
              :key="index"
            >
              <SelectOption :value="formatVerboseDestination(item)">
                {{ item.name }}
              </SelectOption>
            </template>
          </Select>
        </div>
      </FormItem>
      <FormItem class="form-item" ref="date" name="date" label="Data da viagem">
        <DatePicker
          type="date"
          placeholder="Procure a cidade de destino"
          v-model:value="formState.date"
        >
          <!-- <template #prefix>
            <LoginOutlined />
          </template> -->
        </DatePicker>
      </FormItem>
      <Button class="button" type="primary" html-type="submit">
        <template #icon>
          <SearchOutlined />
        </template>
        Procurar Voos
      </Button>
    </Form>
  </div>
  <dialog class="dialog" ref="dialogRef">
    <strong>Insira os dados corretos para pesquisar por voos disponíveis</strong>
    <ul>
      <li v-for="(item, index) in dialogErrors" :key="index">{{ item }}</li>
    </ul>
    <form method="dialog">
      <Button type="default" autofocus html-type="submit"> OK</Button>
    </form>
  </dialog>
</template>

<style scoped>
.search-form-container {
  display: flex;
  flex-direction: column;
  gap: 8px;

  padding: 16px;
  border-radius: 12px;

  background-color: var(--primary-color);
  color: var(--vt-c-text-dark-1);

  & h3,
  p {
    margin: 0;
  }

  & .search-form {
    display: flex;
    flex-direction: row;
    place-items: center;
    gap: 8px;

    & .button,
    .arrow {
      align-self: end;

      margin-bottom: 6px;
    }
    & .arrow {
      margin-bottom: 16px;
    }

    & .form-item {
      width: 100%;

      background-color: var(--color-background);
      padding: 6px 8px;
      border-radius: 6px;

      margin: 0;
    }
  }
}

.input-row-icon {
  display: flex;
  gap: 8px;
}

.dialog {
  background-color: var(--color-background);
  color: var(--color-text);
  border: none;
  border-radius: 12px;
  padding: 12px;
}

@media (prefers-color-scheme: dark) {
  .search-form-container {
    background-color: var(--primary-color-dark);
    color: var(--vt-c-text-dark-1);

    & .search-form {
      & .form-item {
        background-color: var(--color-background);
      }
    }
  }
}
</style>
