import type { Airport, Flight } from '@/models/Flight'

type FlightsResponse = {
  comfortFlights: Flight[]
  economicFlights: Flight[]
  othersFlights: Flight[]
}

class FlightService {
  private host = 'localhost:3000'

  async searchFlights(destination: Airport, date: Date): Promise<FlightsResponse> {
    const baseUrl = `${this.host}/api/flights`

    const params = new URLSearchParams()
    params.append('city', destination.name)
    params.append('date', this.formatDate(date))

    const url = new URL(baseUrl)
    url.search = params.toString()

    const result = await fetch(url)

    return await result.json()
  }

  private formatDate(date: Date) {
    return date.toLocaleDateString('en-US')
  }
}
