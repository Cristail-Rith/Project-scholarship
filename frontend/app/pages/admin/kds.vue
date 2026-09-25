<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useAuth } from '~/composables/useAuth'

definePageMeta({ middleware: 'admin' })
const { apiBase } = useApiBase()
const { token } = useAuth()
const orders = ref<any[]>([])
const loading = ref(true)
const error = ref('')
let refreshTimer: ReturnType<typeof setInterval> | undefined
const kitchenOrders = computed(() => orders.value.filter(order => ['pending', 'preparing', 'ready'].includes(String(order.status || '').toLowerCase())))
async function loadOrders() {
  const authToken = token.value || (import.meta.client ? localStorage.getItem('access_token') : null)
  if (!authToken) { error.value = 'Please sign in again to view kitchen orders.'; loading.value = false; return }
  try {
    const result = await $fetch<any>('/orders', { baseURL: apiBase.value, headers: { Authorization: `Bearer ${authToken}` } })
    orders.value = Array.isArray(result) ? result : result?.orders || []
    error.value = ''
  } catch { error.value = 'Could not load kitchen orders. Please try again.' } finally { loading.value = false }
}
onMounted(() => { loadOrders(); refreshTimer = setInterval(loadOrders, 15000) })
onUnmounted(() => { if (refreshTimer) clearInterval(refreshTimer) })
</script>

<template>
  <main class="min-h-screen bg-stone-950 p-5 text-stone-100 sm:p-8">
    <header class="mx-auto flex max-w-7xl items-center justify-between gap-4">
      <div><p class="text-xs font-bold uppercase tracking-[.25em] text-amber-400">Kitchen Display System</p><h1 class="mt-2 font-serif text-3xl">Kitchen orders</h1></div>
      <div class="flex gap-3"><button class="rounded-lg border border-stone-700 px-4 py-2 text-sm" @click="loadOrders">Refresh</button><NuxtLink to="/admin" class="rounded-lg bg-amber-600 px-4 py-2 text-sm font-semibold">Admin home</NuxtLink></div>
    </header>
    <section class="mx-auto mt-8 grid max-w-7xl gap-5 sm:grid-cols-2 xl:grid-cols-3">
      <p v-if="loading" class="text-stone-400">Loading kitchen orders…</p><p v-else-if="error" class="text-rose-300">{{ error }}</p><p v-else-if="!kitchenOrders.length" class="text-stone-400">No active kitchen orders.</p>
      <article v-for="order in kitchenOrders" :key="order.id" class="rounded-2xl border border-stone-800 bg-stone-900 p-5">
        <div class="flex justify-between"><div><p class="text-xs font-bold text-amber-400">Order #{{ order.id }}</p><h2 class="mt-1 text-lg font-semibold">{{ order.customer_name || `Guest ${order.user_id || ""}` }}</h2><p class="text-sm text-stone-400">{{ order.table_number ? `Table ${order.table_number}` : (order.order_type || "Restaurant order") }}</p></div><span class="h-fit rounded-full bg-amber-900/60 px-3 py-1 text-xs capitalize text-amber-200">{{ order.status }}</span></div>
        <ul class="mt-5 space-y-3 border-t border-stone-800 pt-4"><li v-for="item in order.items || []" :key="item.id || item.product_id" class="text-sm">{{ item.quantity }} × {{ item.product_name || `Product #${item.product_id}` }}</li></ul>
        <p class="mt-5 text-xs text-stone-500">{{ order.created_at ? new Date(order.created_at).toLocaleTimeString() : "" }}</p>
      </article>
    </section>
  </main>
</template>

