export type Airport = { code: string; name: string }

export type Flight = {
  origin: Airport
  destination: Airport
  companyName: string
  price: number
  seatLocation: string
  estimateTime: string
}
