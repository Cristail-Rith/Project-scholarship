export interface CartProduct {
  id: number | string
  title: string
  name?: string
  category?: string
  price: number
  description?: string
  image?: string
  rating?: string
}

export interface CartItem extends CartProduct {
  quantity: number
}

export function useCart() {
  const items = useState<CartItem[]>('customer-cart', () => [])

  const addToCart = (product: CartProduct) => {
    const existing = items.value.find(item => item.id === product.id)

    if (existing) {
      existing.quantity += 1
      return
    }

    items.value.push({ ...product, quantity: 1 })
  }

  const updateQuantity = (id: CartItem['id'], quantity: number) => {
    const item = items.value.find(cartItem => cartItem.id === id)
    if (!item) return

    if (quantity <= 0) {
      removeFromCart(id)
      return
    }

    item.quantity = quantity
  }

  const removeFromCart = (id: CartItem['id']) => {
    items.value = items.value.filter(item => item.id !== id)
  }

  const totalItems = computed(() => items.value.reduce((total, item) => total + item.quantity, 0))
  const totalPrice = computed(() => items.value.reduce((total, item) => total + item.price * item.quantity, 0))

  return {
    items,
    addToCart,
    updateQuantity,
    removeFromCart,
    totalItems,
    totalPrice,
  }
}
