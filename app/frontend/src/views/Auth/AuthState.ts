import AuthService from '@/data/AuthService'
import { ref } from 'vue'

export const authState = ref({
  isLoggedIn: AuthService.hasAuthTokens(),

  loggedIn() {
    this.isLoggedIn = true
  },
  loggedOut() {
    this.isLoggedIn = false
  }
})
