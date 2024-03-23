import type { Airport } from '@/models/Flight'

export function formatVerboseDestination(dest: Airport) {
  return `${dest.code} - ${dest.name}`
}
