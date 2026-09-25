import { computed } from 'vue'

export function useApiBase() {
  const config = useRuntimeConfig()

  const apiBase = computed(() => {
    if (import.meta.client) {
      const { hostname, protocol } = window.location
      return `${protocol}//${hostname}:5000`
    }
    return config.public.apiBase || 'http://localhost:5000'
  })

  return { apiBase }
}
