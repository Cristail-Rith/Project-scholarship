<script setup lang="ts">
import { ref, computed } from 'vue'

const { items, updateQuantity, removeFromCart, totalItems, totalPrice } = useCart()

// Free shipping threshold logic
const FREE_SHIPPING_THRESHOLD = 50
const amountUntilFreeShipping = computed(() => Math.max(0, FREE_SHIPPING_THRESHOLD - totalPrice.value))
const shippingProgress = computed(() => Math.min(100, (totalPrice.value / FREE_SHIPPING_THRESHOLD) * 100))

// Checkout state
const couponCode = ref('')
const couponApplied = ref(false)
const orderNote = ref('')
const showNoteInput = ref(false)

const applyCoupon = () => {
  if (couponCode.value.trim().toUpperCase() === 'WELCOME10') {
    couponApplied.value = true
  }
}

const placeOrder = () => {
  if (!items.value.length) return
  navigateTo('/orders')
}
</script>

<template>
  <div class="min-h-screen bg-[#FDFBF7] text-stone-900 font-sans antialiased border-t-4 border-amber-500">
    <Navbar />

    <main class="max-w-6xl mx-auto px-4 sm:px-6 py-12 sm:py-16">
      <!-- Header -->
      <header class="flex flex-col sm:flex-row sm:items-end justify-between gap-4 border-b-1 border-gray-700 pb-6 mb-8">
        <div>
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-amber-500"></span>
            <span class="text-xs font-bold uppercase tracking-[0.25em] text-amber-600">Your selection</span>
          </div>
          <h1 class="mt-1 text-4xl sm:text-5xl font-serif tracking-tight text-stone-800">Shopping Cart</h1>
        </div>
        <div v-if="totalItems" class="flex items-center gap-3">
          <span class="inline-flex items-center rounded-none bg-amber-500/10 border border-amber-500/30 px-3 py-1 text-xs font-semibold text-amber-700">
            {{ totalItems }} {{ totalItems === 1 ? 'item' : 'items' }}
          </span>
        </div>
      </header>

      <!-- Main Content Layout -->
      <div v-if="items.length" class="grid gap-12 lg:grid-cols-[1fr_360px] items-start">
        <!-- Left: Cart Items List -->
        <section class="space-y-6">
          <!-- Free Shipping Banner -->
          <div class="rounded-[5px] border border-stone-300 bg-white p-5 shadow-xs">
            <div class="flex justify-between text-xs font-bold uppercase tracking-wider mb-2">
              <span v-if="amountUntilFreeShipping > 0" class="text-stone-700">
                Add <strong class="text-amber-600 font-extrabold">${{ amountUntilFreeShipping.toFixed(2) }}</strong> more for free shipping
              </span>
              <span v-else class="text-emerald-700 font-bold flex items-center gap-1">
                <span>✓</span> You've unlocked free standard shipping!
              </span>
              <span class="text-stone-500 font-mono">${{ totalPrice.toFixed(2) }} /${{ FREE_SHIPPING_THRESHOLD }}</span>
            </div>
            <div class="h-2 w-full bg-stone-100 overflow-hidden border border-stone-200">
              <div 
                class="h-full bg-amber-500 transition-all duration-500 ease-out" 
                :style="{ width: `${shippingProgress}%` }"
              />
            </div>
          </div>

          <!-- Items Stack -->
          <div class="divide-y divide-stone-200 border-t border-b border-stone-200">
            <TransitionGroup name="cart-item">
              <article 
                v-for="item in items" 
                :key="item.id" 
                class="group flex flex-col sm:flex-row gap-4 sm:gap-6 py-6 transition-all"
              >
                <!-- Thumbnail -->
                <NuxtLink :to="`/product/${item.id}`" class="relative h-28 w-28 shrink-0 overflow-hidden bg-stone-100 border border-stone-200 group-hover:border-amber-500 transition-colors">
                  <img 
                    :src="item.image" 
                    :alt="item.title" 
                    class="h-full w-full object-cover object-center transition-transform duration-500 group-hover:scale-105" 
                  />
                </NuxtLink>

                <!-- Item Details -->
                <div class="flex flex-1 flex-col justify-between">
                  <div>
                    <div class="flex justify-between items-start gap-4">
                      <NuxtLink 
                        :to="`/product/${item.id}`" 
                        class="font-serif text-xl text-stone-900 hover:text-amber-600 transition-colors line-clamp-1"
                      >
                        {{ item.title }}
                      </NuxtLink>
                      <span class="font-serif text-lg font-bold whitespace-nowrap text-stone-900">
                        ${{ (item.price * item.quantity).toFixed(2) }}
                      </span>
                    </div>
                    <p class="mt-1 text-sm text-stone-500 font-mono">${{ item.price.toFixed(2) }} each</p>
                  </div>

                  <!-- Controls Row -->
                  <div class="mt-4 flex items-center justify-between">
                    <!-- Quantity Controls -->
                    <div class="inline-flex items-center border border-stone-300 bg-white">
                      <button 
                        type="button" 
                        class="h-8 w-8 flex items-center justify-center text-stone-600 hover:bg-amber-500 hover:text-white transition-colors disabled:opacity-30 disabled:hover:bg-transparent disabled:hover:text-stone-600" 
                        :disabled="item.quantity <= 1"
                        @click="updateQuantity(item.id, item.quantity - 1)"
                        aria-label="Decrease quantity"
                      >
                        &#8722;
                      </button>
                      <span class="w-8 text-center text-sm font-bold text-stone-900 font-mono">
                        {{ item.quantity }}
                      </span>
                      <button 
                        type="button" 
                        class="h-8 w-8 flex items-center justify-center text-stone-600 hover:bg-amber-500 hover:text-white transition-colors" 
                        @click="updateQuantity(item.id, item.quantity + 1)"
                        aria-label="Increase quantity"
                      >
                        &#43;
                      </button>
                    </div>

                    <!-- Remove Action -->
                    <button 
                      type="button" 
                      class="text-xs font-bold uppercase tracking-widest text-stone-400 hover:text-rose-700 transition-colors underline-offset-4 hover:underline" 
                      @click="removeFromCart(item.id)"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              </article>
            </TransitionGroup>
          </div>

          <!-- Order Notes Accordion -->
          <div class="pt-2">
            <button 
              type="button" 
              class="text-xs font-bold uppercase tracking-wider text-stone-700 hover:text-amber-600 flex items-center gap-2 transition-colors"
              @click="showNoteInput = !showNoteInput"
            >
              <span class="text-amber-500 font-bold text-sm">{{ showNoteInput ? '−' : '+' }}</span>
              <span>Add special instructions or gift note</span>
            </button>
            <div v-if="showNoteInput" class="mt-3">
              <textarea 
                v-model="orderNote" 
                rows="3" 
                placeholder="Include delivery instructions, gift messaging, or packaging preferences..." 
                class="w-full border border-stone-300 bg-white p-3 text-sm focus:border-amber-500 focus:outline-none rounded-none placeholder:text-stone-400"
              />
            </div>
          </div>
        </section>

        <!-- Right: Summary Drawer -->
        <aside class="sticky top-8 border border-gray-300 rounded-[7px] bg-white p-6 shadow-[4px_4px_0px_0px_rgba(245,158,11,1)]">
          <h2 class="font-serif text-2xl pb-4 border-b border-stone-200 font-bold uppercase tracking-wide">Order Summary</h2>

          <!-- Promo Code Input -->
          <div class="mt-6">
            <label for="promo" class="block text-xs font-bold uppercase tracking-wider text-stone-600 mb-2">
              Promo Code
            </label>
            <div class="flex gap-2">
              <input 
                id="promo"
                v-model="couponCode" 
                type="text" 
                placeholder="e.g. WELCOME10" 
                class="min-w-0 flex-1 border border-stone-400 px-3 py-2 text-sm uppercase focus:border-amber-500 focus:outline-none rounded-[5px] font-mono"
              />
              <button 
                type="button" 
                class="bg-gray-700 px-4 py-2 text-xs font-bold rounded-[5px] uppercase tracking-wider text-white hover:bg-amber-500 transition-colors"
                @click="applyCoupon"
              >
                Apply
              </button>
            </div>
            <p v-if="couponApplied" class="mt-2 text-xs text-emerald-700 font-semibold flex items-center gap-1">
              <span>✓</span> Promo applied: 10% discount included
            </p>
          </div>

          <!-- Price Calculation Breakdown -->
          <dl class="mt-6 space-y-3 border-t border-stone-200 pt-4 text-sm">
            <div class="flex justify-between text-stone-600">
              <dt>Subtotal</dt>
              <dd class="font-bold text-stone-900 font-mono">${{ totalPrice.toFixed(2) }}</dd>
            </div>
            <div class="flex justify-between text-stone-600">
              <dt>Estimated Shipping</dt>
              <dd class="font-semibold text-stone-900">
                <span v-if="amountUntilFreeShipping === 0" class="text-emerald-700 uppercase text-xs font-extrabold">Free</span>
                <span v-else class="font-mono">$5.00</span>
              </dd>
            </div>
            <div class="flex justify-between text-stone-600">
              <dt>Estimated Tax</dt>
              <dd class="text-stone-400 text-xs italic">Calculated at checkout</dd>
            </div>
            <div class="flex justify-between border-t border-stone-900 pt-4 font-serif text-xl font-bold text-stone-900">
              <dt>Total</dt>
              <dd class="text-amber-600 font-mono">${{ (totalPrice + (amountUntilFreeShipping === 0 ? 0 : 5)).toFixed(2) }}</dd>
            </div>
          </dl>

          <!-- Action Buttons -->
          <button 
            type="button" 
            class="mt-6 w-full border-none  bg-red-600 py-3.5 text-xs font-bold uppercase tracking-[0.2em] text-white hover:bg-amber-800 hover:border-amber-800 transition-colors shadow-xs rounded-[5px]" 
            @click="placeOrder"
          >
            Proceed to Checkout
          </button>

          <!-- Security Badges / Guarantees -->
          <div class="mt-6 flex items-center justify-center gap-2 border-t border-stone-100 pt-4 text-stone-400">
            <span class="text-[10px] uppercase font-bold tracking-widest text-stone-500 flex items-center gap-1">
              🔒 256-Bit SSL Encrypted
            </span>
          </div>
        </aside>
      </div>

      <!-- Empty State -->
      <div v-else class="border-2 border-dashed border-stone-300 py-24 px-6 text-center bg-white">
        <div class="mx-auto h-14 w-14 text-amber-500 mb-4 flex items-center justify-center rounded-none bg-amber-500/10 border border-amber-500/20 text-2xl">
          🛍️
        </div>
        <h2 class="font-serif text-3xl text-stone-900 font-bold">Your shopping cart is empty</h2>
        <p class="mt-2 text-stone-500 max-w-sm mx-auto text-sm">
          It looks like you haven't added anything to your cart yet. Explore our curated selection to get started.
        </p>
        <NuxtLink 
          to="/menu" 
          class="mt-8 inline-block border-2 border-amber-500 bg-amber-500 px-8 py-3.5 text-xs font-bold uppercase tracking-[0.2em] text-white hover:bg-amber-600 hover:border-amber-600 transition-colors rounded-none shadow-xs"
        >
          Browse the Collection
        </NuxtLink>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* Smooth animated removal of cart items */
.cart-item-enter-active,
.cart-item-leave-active {
  transition: all 0.3s ease;
}
.cart-item-enter-from,
.cart-item-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>