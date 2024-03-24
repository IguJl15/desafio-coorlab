import env from '@/misc/env'

type AuthTokens = { refresh: string; access: string }

export default class AuthService {
  static async login(username: string, password: string) {
    const baseUrl = `${env.VITE_HOST}/api/token/`

    const result = await fetch(baseUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })

    if (!result.ok) {
      // TODO: Take this out of my sight
      throw result
    }

    localStorage.setItem('auth_tokens', await result.text())
  }

  private static getAuthTokens(): AuthTokens | null {
    const tokens = localStorage.getItem('auth_tokens')

    if (!tokens) return null

    return JSON.parse(tokens)
  }

  static getAuthorizationHeader(): Record<string, string> {
    const tokens = this.getAuthTokens()

    if (tokens) return { Authorization: 'Bearer ' + tokens.access }
    else return {}
  }
}
