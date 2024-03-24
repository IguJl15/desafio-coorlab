import AuthService from '@/data/AuthService'
import env from '@/misc/env'
import { Flight, type Airport, type GenericFlight } from '@/models/Flight'

import airports from '@/data/airports.json'

export type FlightsResponse = {
  comfort: GenericFlight[]
  economic: GenericFlight[]
  others: GenericFlight[]
}

export type FlightsData = {
  comfort: Flight[]
  economic: Flight[]
  others: Flight[]
}

export default class FlightService {
  static async searchFlights(destination: Airport, date: Date): Promise<FlightsData> {
    const baseUrl = `${env.VITE_HOST}/api/flights/`

    const params = new URLSearchParams()
    params.append('city', destination.name)
    params.append('date', typeof date == 'string' ? date : this.formatDate(date))

    const url = new URL(baseUrl)
    url.search = params.toString()

    const requestData: RequestInit = {
      headers: { ...AuthService.getAuthorizationHeader() }
    }

    const result = await fetch(url, requestData)

    if (result.ok) {
      const json: FlightsResponse = await result.json()

      const comfort = json.comfort.map((a) => Flight.comfort(a))
      const economic = json.economic.map((a) => Flight.economic(a))

      // For each flight, create both economic and comfort items to better
      // visualization on the page
      const others = json.comfort.reduce<Flight[]>((flightsList, currentData) => {
        flightsList.push(Flight.comfort(currentData))
        flightsList.push(Flight.economic(currentData))
        return flightsList
      }, [])

      return {
        comfort,
        economic,
        others
      }
    } else {
      // TODO: Handle 401 (access token expired)
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
