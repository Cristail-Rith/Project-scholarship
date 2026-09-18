<script setup lang="ts">
import { ref, computed } from 'vue'
import Footer from '~/components/Footer.vue'
import Navbar from '~/components/Navbar.vue'

definePageMeta({ middleware: 'auth' })

interface User {
  id: number
  username: string
  email: string
  phone: string
  role: string
}

const { user, token } = useAuth()
const config = useRuntimeConfig()

const orderType = ref<'dine-in' | 'takeout' | 'delivery'>('dine-in')
const activeStep = ref<'details' | 'payment' | 'confirmation'>('details')
const placeSuccess = ref(false)

const { items, updateQuantity, clearCart } = useCart()

const customer = ref({
  fullName: '',
  phone: '',
  email: '',
  tableNumber: '',
  deliveryAddress: '',
  notes: ''
})

const paymentMethod = ref<'card' | 'qr' | 'cash'>('qr')
const orderId = ref<number | null>(null)
const confirmedTotal = ref(0)
const submitting = ref(false)

const subtotal = computed(() => items.value.reduce((sum, item) => sum + item.price * item.quantity, 0))
const deliveryFee = computed(() => (orderType.value === 'delivery' ? 5.00 : 0.00))
const total = computed(() => subtotal.value + deliveryFee.value)

const updateQty = (id: string | number, delta: number) => {
  const item = items.value.find(i => i.id === id)
  if (!item) return
  updateQuantity(id, item.quantity + delta)
}

const proceedToPayment = () => {
  if (!customer.value.phone) {
    alert('Please complete your phone number.')
    return
  }
  if (orderType.value === 'delivery' && !customer.value.deliveryAddress.trim()) {
    alert('Please enter a delivery address.')
    return
  }
  activeStep.value = 'payment'
}

const placeOrder = async () => {
  if (!items.value.length) {
    await navigateTo('/cart')
    return
  }
  if (!token.value) {
    await navigateTo({ path: '/login', query: { redirect: '/orders' } })
    return
  }

  submitting.value = true
  try {
    const response = await $fetch<{ order?: { id: number } }>('/orders', {
      baseURL: config.public.apiBase,
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token.value}`,
        'Content-Type': 'application/json',
      },
      body: {
        items: items.value.map(item => ({
          product_id: Number(item.id),
          quantity: item.quantity,
        })),
        order_type: orderType.value,
        payment_method: paymentMethod.value,
        notes: customer.value.notes,
        customer_name: customer.value.fullName,
        customer_email: customer.value.email || user.value?.email || '',
        customer_phone: customer.value.phone || user.value?.phone || '',
        table_number: customer.value.tableNumber,
        delivery_address: customer.value.deliveryAddress,
      },
    })

    orderId.value = response.order?.id ?? null
    confirmedTotal.value = total.value
    clearCart()
    activeStep.value = 'confirmation'
  } catch (error: any) {
    alert(error?.data?.message || 'Failed to place order. Please try again.')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <Navbar />
  <div class="relative min-h-screen py-12 px-4 overflow-hidden">
    <div class="absolute inset-0 -z-10">
      <img
        src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&q=80&w=2000"
        alt="Restaurant ambiance background"
        class="w-full h-full object-cover"
      />
      <div class="absolute inset-0 bg-[#48434379] backdrop-blur-none"></div>
    </div>

    <div class="max-w-6xl mx-auto space-y-10 relative z-10">

      <div class="text-center space-y-2">
        <span class="text-[#dddad8] text-xs font-semibold uppercase tracking-[0.2em]">Checkout</span>
        <h1 class="text-3xl font-serif font-semibold text-[#bbb4ad]">Complete your order</h1>
      </div>

      <div class="flex items-center justify-center bg-white/80 backdrop-blur-md border border-[#E6DFD3] rounded-[5px] p-1 max-w-md mx-auto shadow-sm">
        <div
          :class="activeStep === 'details' ? 'bg-amber-500 text-white' : 'text-[#8C8377]'"
          class="flex-1 text-center py-2 rounded-[5px] text-xs font-semibold tracking-wide transition-colors"
        >
          1. Details
        </div>
        <div
          :class="activeStep === 'payment' ? 'bg-amber-500 text-white' : 'text-[#8C8377]'"
          class="flex-1 text-center py-2 rounded-[5px] text-xs font-semibold tracking-wide transition-colors"
        >
          2. Payment
        </div>
        <div
          :class="activeStep === 'confirmation' ? 'bg-amber-500 text-white' : 'text-[#8C8377]'"
          class="flex-1 text-center py-2 rounded-[5px] text-xs font-semibold tracking-wide transition-colors"
        >
          3. Confirmed
        </div>
      </div>

      <div v-if="activeStep === 'confirmation'" class="bg-[#d4cfcf5b] backdrop-blur-sm border border-[#E6DFD3] rounded-2xl shadow-lg p-10 text-center space-y-6 max-w-xl mx-auto">
        <div class="w-14 h-14 rounded-[5px] bg-amber-100 text-amber-700 mx-auto flex items-center justify-center font-semibold text-xl">✓</div>
        <div class="space-y-2">
          <span class="text-xs font-medium uppercase text-[#f6f6f6] tracking-widest">Order received</span>
          <h2 class="text-2xl font-serif font-semibold text-[#3D3833]">Thank you, {{ customer.phone }}!</h2>
          <p class="text-xs text-[#c9c9c9]">Your order has been saved and sent directly to our kitchen.</p>
          <p v-if="orderId" class="text-xs font-mono text-[#f6f6f6]">Order reference: #{{ orderId }}</p>
        </div>
        <div class="border-t border-b border-[#E6DFD3] py-4 space-y-2 text-1/2xl text-[#e2e2e2]">
          <p><strong class="text-[#3D3833]">Order type:</strong> <span class="capitalize">{{ orderType }}</span></p>
          <p v-if="orderType === 'dine-in'"><strong class="text-[#3D3833]">Table number:</strong> {{ customer.tableNumber || 'Assigned at host desk' }}</p>
          <p><strong class="text-[#3D3833]">Total amount paid:</strong> ${{ confirmedTotal.toFixed(2) }}</p>
        </div>
        <button
            @click="navigateTo('/menu')"
            class="bg-amber-500 hover:bg-amber-600 text-white text-xs font-semibold px-8 py-3 rounded-xl tracking-wide transition-colors shadow-sm"
          >
            Back to menu
          </button>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">

        <div class="lg:col-span-7 space-y-8 bg-white/80 backdrop-blur-md p-6 sm:p-8 rounded-[5px] border border-[#E6DFD3] shadow-sm">

          <div class="space-y-3">
            <h2 class="text-xs font-semibold uppercase tracking-wide text-[#8C8377]">
              Select dining option
            </h2>
            <div class="grid grid-cols-3 gap-3">
              <button
                v-for="type in (['dine-in', 'takeout', 'delivery'] as const)"
                :key="type"
                @click="orderType = type"
                :class="orderType === type ? 'bg-amber-500 text-white border-amber-500 shadow-sm' : 'bg-white/90 text-[#5C5650] border-[#E6DFD3] hover:border-amber-500'"
                class="py-3 px-2 border rounded-[5px] text-xs font-semibold tracking-wide transition-all text-center capitalize"
              >
                {{ type.replace('-', ' ') }}
              </button>
            </div>
          </div>

          <div v-if="activeStep === 'details'" class="space-y-4">
            <h2 class="text-xs font-semibold uppercase tracking-wide text-[#8C8377]">
              Customer details
            </h2>
            <div class="grid grid-cols-1">
              

              <div class="space-y-1 ">
                <label class="text-[11px] font-medium text-[#8C8377]">Phone number *</label>
                <input
                  v-model="customer.phone"
                  type="tel"
                  placeholder="+1 (555) 000-0000"
                  class="w-full border border-[#E6DFD3] bg-[#FAF7F2]/60 rounded-[5px] p-3 text-xs text-[#3D3833] focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-100 focus:bg-white transition-colors"
                />
              </div>

              <div v-if="orderType === 'dine-in'" class="sm:col-span-2 space-y-1">
                <label class="text-[11px] font-medium text-[#8C8377]">Table number (optional)</label>
                <input
                  v-model="customer.tableNumber"
                  type="text"
                  placeholder="e.g. Table 12"
                  class="w-full border border-[#E6DFD3] bg-[#FAF7F2]/60 rounded-[5px] p-3 text-xs text-[#3D3833] focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-100 focus:bg-white transition-colors"
                />
              </div>

              <div v-if="orderType === 'delivery'" class="sm:col-span-2 space-y-1">
                <label class="text-[11px] font-medium text-[#8C8377]">Delivery address *</label>
                <input
                  v-model="customer.deliveryAddress"
                  type="text"
                  placeholder="Street name, building, apartment no."
                  class="w-full border border-[#E6DFD3] bg-[#FAF7F2]/60 rounded-[5px] p-3 text-xs text-[#3D3833] focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-100 focus:bg-white transition-colors"
                />
              </div>

              <div class="sm:col-span-2 space-y-1">
                <label class="text-[11px] font-medium text-[#8C8377]">Special notes for kitchen</label>
                <textarea
                  v-model="customer.notes"
                  rows="3"
                  placeholder="Allergies, door codes, or dietary requirements..."
                  class="w-full border border-[#E6DFD3] bg-[#FAF7F2]/60 rounded-[5px] p-3 text-xs text-[#3D3833] focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-100 focus:bg-white resize-none transition-colors"
                ></textarea>
              </div>
            </div>

            <button
              @click="proceedToPayment"
              class="w-full bg-amber-500 hover:bg-amber-600 text-white font-semibold text-xs py-3.5 rounded-[5px] tracking-wide transition-colors shadow-sm"
            >
              Continue to payment →
            </button>
          </div>

          <div v-if="activeStep === 'payment'" class="space-y-5">
            <h2 class="text-xs font-semibold uppercase tracking-wide text-[#8C8377]">
              Payment method
            </h2>

            <div class="grid grid-cols-3 gap-3">
              <button
                v-for="method in (['qr', 'card', 'cash'] as const)"
                :key="method"
                @click="paymentMethod = method"
                :class="paymentMethod === method ? 'bg-amber-500 text-white border-amber-500 shadow-sm' : 'bg-white/90 text-[#5C5650] border-[#E6DFD3] hover:border-amber-500'"
                class="py-3 px-2 border rounded-[5px] text-xs font-semibold tracking-wide transition-all text-center capitalize"
              >
                {{ method === 'qr' ? 'KHQR / QR code' : method }}
              </button>
            </div>

            <div v-if="paymentMethod === 'qr'" class="border border-[#E6DFD3] bg-white rounded-[5px] shadow-sm p-6 text-center space-y-4">
              <p class="text-xs font-medium text-[#5C5650]">Scan QR code to pay instantly</p>
              <div class="w-44 h-44 bg-[#FAF7F2] border border-[#E6DFD3] rounded-[5px] mx-auto flex items-center justify-center p-2 shadow-inner">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=RestaurantOrderPay" alt="Payment QR" class="w-full h-full" />
              </div>
              <p class="text-[11px] font-mono text-[#8C8377]">Amount due: ${{ total.toFixed(2) }}</p>
            </div>

            <div class="flex items-center gap-3">
              <button
                @click="activeStep = 'details'"
                class="w-1/3 border border-[#E6DFD3] bg-white hover:bg-[#F3EFE8] text-[#3D3833] font-semibold text-xs py-3.5 rounded-[5px] tracking-wide transition-colors"
              >
                ← Back
              </button>
              <button
                @click="placeOrder"
                class="w-2/3 bg-amber-500 hover:bg-amber-600 text-white font-semibold text-xs py-3.5 rounded-[5px] tracking-wide transition-colors shadow-sm"
              >
                Confirm & pay ${{ total.toFixed(2) }}
              </button>
            </div>
          </div>

        </div>

        <div class="lg:col-span-5 border border-[#E6DFD3] rounded-[5px] shadow-sm bg-white/80 backdrop-blur-md p-6 space-y-6">
          <div class="flex items-center justify-between border-b border-[#E6DFD3] pb-3">
            <h3 class="font-serif font-semibold text-lg text-[#3D3833]">Order summary</h3>
            <span class="text-xs font-semibold bg-amber-100 text-amber-800 px-2.5 py-1 rounded-[5px]">{{ items.length }} items</span>
          </div>

          <div class="space-y-4 divide-y divide-[#F0EBE1]">
            <div v-for="item in items" :key="item.id" class="pt-4 first:pt-0 space-y-2">
              <div class="flex justify-between items-start">
                <div>
                  <h4 class="text-xs font-semibold text-[#3D3833]">{{ item.name || item.title }}</h4>
                </div>
                <span class="text-xs font-mono font-semibold text-[#3D3833]">${{ (item.price * item.quantity).toFixed(2) }}</span>
              </div>

              <div class="flex items-center justify-between">
                <span class="text-[11px] font-mono text-[#8C8377]">${{ item.price.toFixed(2) }} each</span>
                <div class="flex items-center border border-[#E6DFD3] rounded-[5px] bg-[#FAF7F2]">
                  <button @click="updateQty(item.id, -1)" class="w-6 h-6 flex items-center justify-center text-xs font-semibold text-[#5C5650] hover:text-[#3D3833]">−</button>
                  <span class="w-6 text-center text-xs font-mono font-semibold text-[#3D3833]">{{ item.quantity }}</span>
                  <button @click="updateQty(item.id, 1)" class="w-6 h-6 flex items-center justify-center text-xs font-semibold text-[#5C5650] hover:text-[#3D3833]">+</button>
                </div>
              </div>
            </div>
          </div>

          <div class="border-t border-[#E6DFD3] pt-4 space-y-2 text-xs">
            <div class="flex justify-between text-[#8C8377]">
              <span>Subtotal</span>
              <span class="font-mono">${{ subtotal.toFixed(2) }}</span>
            </div>

            <div v-if="orderType === 'delivery'" class="flex justify-between text-[#8C8377]">
              <span>Delivery fee</span>
              <span class="font-mono">${{ deliveryFee.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between items-baseline text-[#3D3833] text-base font-serif font-semibold border-t border-[#E6DFD3] pt-3">
              <span>Total due</span>
              <span class="text-amber-600 font-mono">${{ total.toFixed(2) }}</span>
            </div>
          </div>

        </div>

      </div>

    </div>
  </div>
  <Footer/>
</template>
