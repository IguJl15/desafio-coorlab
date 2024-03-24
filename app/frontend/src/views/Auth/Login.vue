<script setup lang="ts">
import AuthService from '@/data/AuthService'
import { Form, FormItem, Input, InputPassword, Button } from 'ant-design-vue'
import { reactive, ref } from 'vue'
import { authState } from './AuthState'
import type { AppError } from '@/models/AppError'
import ErrorContainer from '@/views/components/ErrorContainer.vue'

if (authState.value.isLoggedIn) {
  redirectToHome()
}

interface FormState {
  username: string
  password: string
}

const formState = reactive<FormState>({
  username: '',
  password: ''
})

const error = ref<AppError | undefined>()

function redirectToHome() {
  window.location.hash = '/'
  console.log('Logged in. Redirecting to home')
}

async function onFinish(values: any) {
  try {
    error.value = undefined

    await AuthService.login(values.username, values.password)
    console.log('logou. Alterando estado de login do authstate')
    authState.value.loggedIn()
    redirectToHome()
  } catch (err) {
    console.log('error no login', err)
    error.value = err as AppError
  }
}

const onFinishFailed = (errorInfo: any) => {
  console.log('Failed:', errorInfo)
}
</script>

<template>
  <div class="login-container">
    <h1>Entrar</h1>
    <Form
      :model="formState"
      name="basic"
      :label-col="{ span: 6 }"
      :wrapper-col="{ span: 18 }"
      autocomplete="off"
      @finish="onFinish"
      @finishFailed="onFinishFailed"
    >
      <FormItem :hidden="!authState.isLoggedIn"
        >Você ja está autenticado. <a href="/">Prossiga para a tela inicial</a></FormItem
      >
      <FormItem
        label="Username"
        name="username"
        :rules="[{ required: true, message: 'Por favor, insira seu username' }]"
      >
        <Input v-model:value="formState.username" />
      </FormItem>

      <FormItem
        label="Senha"
        name="password"
        :rules="[{ required: true, message: 'Por favor, insira sua senha' }]"
      >
        <InputPassword v-model:value="formState.password" />
      </FormItem>

      <FormItem :wrapper-col="{ offset: 6, span: 18 }">
        <Button type="primary" html-type="submit">Entrar</Button>
      </FormItem>
      <FormItem v-if="error" :wrapper-col="{ span: 24 }">
        <ErrorContainer :error="error" />
      </FormItem>
    </Form>
  </div>
</template>

<style scoped>
h1 {
  margin-top: 0.5rem;
  text-align: center;
}
.login-container {
  background-color: var(--color-background);
  max-width: 600px;

  margin: 0 auto;

  display: flex;
  flex-direction: column;
  padding: 12px;
}
</style>
