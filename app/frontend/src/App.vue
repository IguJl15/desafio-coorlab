<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'
import { ref, onMounted } from 'vue'

const flightsEventData = ref({
  isLoading: true,
  error: '',
  data: []
})

const formData = ref({
  destination: '',
  date: Date.now()
})

onMounted(() => {
  console.log(`Alo, onmounted! Counter is ${flightsEventData.value}`)
})
</script>

<template>
  <div class="search-form-container">
    <h2>Encontre sua viagem dos sonhos</h2>
    <p>Insira abaixo as informações da viagem que você planeja</p>
    <form action="" method="get">
      <input type="text" v-model="formData.destination" />
      <input type="date" v-model="formData.date" />
    </form>
  </div>

  <main>
    <TheWelcome />
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

    & input {

    }
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
