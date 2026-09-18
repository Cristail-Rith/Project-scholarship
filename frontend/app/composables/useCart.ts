
import { computed } from 'vue'

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
  // Cart items
  const items = useState<CartItem[]>('customer-cart', () => [])

  // Shared cart sidebar state
  const isCartOpen = useState<boolean>('cart-open', () => false)

  // Cart icon animation
  const cartAnimating = useState<boolean>('cart-animating', () => false)

  // Toast notification
  const cartMessage = useState<string>('cart-message', () => '')

  // Add product to cart
  const addToCart = (product: CartProduct) => {
    const existing = items.value.find(
      item => item.id === product.id
    )

    if (existing) {
      existing.quantity += 1
    } else {
      items.value.push({
        ...product,
        quantity: 1
      })
    }

    // Start Navbar animation
    cartAnimating.value = false

    setTimeout(() => {
      cartAnimating.value = true
    }, 10)

    setTimeout(() => {
      cartAnimating.value = false
    }, 700)

    // Show toast
    cartMessage.value = `${product.title} added to your cart`

    setTimeout(() => {
      cartMessage.value = ''
    }, 2200)
  }

  // Update quantity
  const updateQuantity = (
    id: CartItem['id'],
    quantity: number
  ) => {
    const item = items.value.find(
      cartItem => cartItem.id === id
    )

    if (!item) return

    if (quantity <= 0) {
      removeFromCart(id)
      return
    }

    item.quantity = quantity
  }

  // Remove item
  const removeFromCart = (id: CartItem['id']) => {
    items.value = items.value.filter(
      item => item.id !== id
    )
  }

  // Clear cart
  const clearCart = () => {
    items.value = []
  }

  // Total number of items
  const totalItems = computed(() =>
    items.value.reduce(
      (total, item) => total + item.quantity,
      0
    )
  )

  // Total price
  const totalPrice = computed(() =>
    items.value.reduce(
      (total, item) => total + item.price * item.quantity,
      0
    )
  )

  return {
    items,
    isCartOpen,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
    totalItems,
    totalPrice,
    cartAnimating,
    cartMessage
  }
}
