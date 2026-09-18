
import { computed } from 'vue'

interface Product {
  id: number
  title: string
  name?: string
  category: string
  price: number
  rating: string
  description: string
  image: string
  images?: string[]
}

export function useProducts() {
  const config = useRuntimeConfig()

  const { data, pending, error, refresh } = useFetch<Product[]>('/products', {
    baseURL: config.public.apiBase,
    default: () => [],
  })

  const products = computed(() =>
    (data.value ?? []).map((product) => ({
      ...product,
      image:
        product.image && !product.image.startsWith('http')
          ? `${config.public.apiBase}${product.image}`
          : product.image,
    })),
  )

  const searchQuery = useState('product-search-query', () => '')

  const filteredProducts = computed(() => {
    const query = searchQuery.value.trim().toLowerCase()

    if (!query) return []

    return products.value.filter((product) =>
      [product.title, product.name, product.category]
        .filter(Boolean)
        .some((value) => value!.toLowerCase().includes(query)),
    )
  })

  return {
    products,
    searchQuery,
    filteredProducts,
    pending,
    error,
    refresh,
  }
}

