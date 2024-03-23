import type { Airport, Flight } from '@/models/Flight'
import env from '@/misc/env'
import AuthService from '@/data/AuthService'

export type FlightsResponse = {
  comfort: Flight[]
  economic: Flight[]
  others: Flight[]
}

export default class FlightService {
  static async searchFlights(destination: Airport, date: Date): Promise<FlightsResponse> {
    const baseUrl = `${env.VITE_HOST}/api/flights/`

    const params = new URLSearchParams()
    params.append('city', destination.name)
    params.append('date', this.formatDate(date))

    const url = new URL(baseUrl)
    url.search = params.toString()

    const requestData: RequestInit = {
      headers: { ...AuthService.getAuthorizationHeader() }
    }

    const result = await fetch(url, requestData)

    if (result.ok) {
      const json = await result.json()
      console.log(json)
      return json
    } else {
      // TODO: Take this out of my sight
      throw {
        response: result,
        requestData: requestData,
        title: 'Ocorreu um erro ao buscar os voos disponíveis',
        ...(await result.json())
      }
    }
  }

  private static formatDate(date: Date) {
    return date.toLocaleDateString('en-US')
  }
}
