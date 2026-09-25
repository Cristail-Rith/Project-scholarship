
import { computed } from 'vue'

interface Product {
  id: number
  title: string
  name?: string
  category: string
  price: number
  previousPrice?: number | null
  rating: string
  description: string
  image: string
  images?: string[]
  sku?: string
  status?: string
  stockQuantity?: number
}

export function useProducts() {
  const { apiBase } = useApiBase()

  const { data, pending, error, refresh } = useFetch<Product[]>('/products', {
    baseURL: apiBase.value,
    default: () => [],
  })

  const products = computed(() =>
    (data.value ?? []).map((product) => ({
      ...product,
      image:
        product.image && !product.image.startsWith('http')
          ? `${apiBase.value}${product.image}`
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

