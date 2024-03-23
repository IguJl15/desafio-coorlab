export type Airport = { code: string; name: string }

export type Flight = {
  origin: Airport
  city_destination: Airport
  company_name: string
  price_comfort: number
  price_economic: number
  comfort_bed_location: string
  economic_seat_location: string
  duration: string
}
