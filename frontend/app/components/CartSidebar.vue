<template>
  <div v-if="isCartOpen" class="fixed inset-0 z-50 bg-stone-950/60" @click.self="closeCart">
    <aside class="ml-auto flex h-full w-full max-w-md flex-col bg-white p-6 text-stone-900 shadow-2xl">
      <div class="flex items-center justify-between border-b-2 border-stone-900 pb-4">
        <div>
          <span class="text-[10px] font-black uppercase tracking-widest text-amber-700">Added to your order</span>
          <h2 class="font-serif text-2xl">Your Cart</h2>
        </div>
        <button type="button" class="text-2xl text-stone-400 hover:text-stone-900" aria-label="Close cart" @click="closeCart">&times;</button>
      </div>

      <div class="flex-1 overflow-y-auto py-5">
        <div v-if="!cartItems.length" class="py-12 text-center text-sm text-stone-500">Your cart is empty.</div>
        <div v-for="item in cartItems" :key="item.id" class="flex items-center gap-3 border-b border-stone-200 py-4">
          <img :src="item.image" :alt="item.title" class="h-16 w-16 object-cover" />
          <div class="min-w-0 flex-1">
            <button type="button" class="block truncate text-left font-serif hover:text-amber-700" @click="goToProduct(item)">{{ item.title }}</button>
            <p class="text-xs text-amber-700">${{ (item.price * item.quantity).toFixed(2) }}</p>
            <div class="mt-2 flex items-center gap-2">
              <button type="button" class="h-6 w-6 border border-stone-300" @click="updateCartQuantity(item.id, item.quantity - 1)">-</button>
              <span class="w-5 text-center text-xs">{{ item.quantity }}</span>
              <button type="button" class="h-6 w-6 border border-stone-300" @click="updateCartQuantity(item.id, item.quantity + 1)">+</button>
            </div>
          </div>
        </div>
      </div>

      <div class="border-t-2 border-stone-900 pt-4">
        <div class="flex justify-between font-bold"><span>Total</span><span>${{ totalPrice.toFixed(2) }}</span></div>
        <button
          type="button"
          class="mt-4 w-full bg-amber-600 py-3 text-xs font-bold uppercase tracking-widest text-white hover:bg-amber-700"
          @click="goToCart"
        >
          Go to order &amp; payment
        </button>
        <button type="button" class="mt-2 w-full border border-stone-300 py-3 text-xs font-bold uppercase tracking-widest text-stone-700 hover:border-stone-900 hover:text-stone-900" @click="closeCart">Continue shopping</button>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { useCart } from '~/composables/useCart'
import { useProducts } from '~/composables/useProducts'

const { items: cartItems, updateQuantity, totalPrice, isCartOpen } = useCart()
const { products } = useProducts()

const closeCart = () => {
  isCartOpen.value = false
}

const goToProduct = (item) => {
  navigateTo(`/product/${item.id}`)
}

const goToCart = () => {
  isCartOpen.value = false
  navigateTo('/cart')
}

const updateCartQuantity = (id, quantity) => {
  updateQuantity(id, quantity)
}
</script>