import allAirports from '@/data/airports.json'

export type Airport = { code: string; name: string }
export type FlightType = 'comfort' | 'economic'
export type GenericFlight = {
  city_from: string
  city_destination: string

  company_name: string

  price_comfort: number
  price_economic: number

  comfort_bed_location: string
  economic_seat_location: string

  duration: string
}

export class Flight {
  constructor(
    public origin: Airport,
    public destination: Airport,
    public company_name: string,
    public price: number,
    public seat: string,
    public duration: string
  ) {}

  static comfort(data: GenericFlight) {
    return new Flight(
      this.getAirportFromCity(data.city_from),
      this.getAirportFromCity(data.city_destination),

      data.company_name,
      data.price_comfort,
      data.comfort_bed_location,

      data.duration
    )
  }

  static economic(data: GenericFlight) {
    return new Flight(
      this.getAirportFromCity(data.city_from),
      this.getAirportFromCity(data.city_destination),
      data.company_name,

      data.price_economic,
      data.economic_seat_location,

      data.duration
    )
  }

  private static getAirportFromCity(city: string): Airport {
    const candidates = allAirports.filter((airport) => airport.name == city)

    if (candidates.length > 0) return candidates[0]
    else if (city && city != '') return { code: 'DSC', name: city }
    else return this.mockOrigin()
  }

  private static mockOrigin(): Airport {
    return { code: 'THE', name: 'Teresina' }
  }
}
