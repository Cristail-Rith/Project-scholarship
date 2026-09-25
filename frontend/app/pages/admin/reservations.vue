<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import AdminSidebar from '~/components/AdminSidebar.vue'
import { useAuth } from '~/composables/useAuth'

definePageMeta({ middleware: 'admin' })
const { apiBase } = useApiBase()
const { token } = useAuth()
const reservations = ref<any[]>([])
const loading = ref(true)
const error = ref('')
const savingId = ref<number | null>(null)
const pendingCount = computed(() => reservations.value.filter(item => item.status === 'pending').length)
const roomImages: Record<string, string> = {
  'Main Dining Room': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=700&q=80',
  'Garden Terrace': 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=700&q=80',
  "Chef's Counter": 'https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=700&q=80',
  'Private Dining': 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=700&q=80',
  'VIP Suite': 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=700&q=80',
}
const getRoomImage = (areaName: string) => roomImages[areaName] || roomImages['Main Dining Room']

async function loadReservations() {
  loading.value = true
  error.value = ''
  try {
    const authToken = token.value || (import.meta.client ? localStorage.getItem('access_token') : null)
    reservations.value = await $fetch<any[]>('/reservations', {
      baseURL: apiBase.value,
      headers: authToken ? { Authorization: `Bearer ${authToken}` } : {},
    })
  } catch (err: any) {
    error.value = err?.data?.message || 'Could not load reservation requests.'
  } finally {
    loading.value = false
  }
}

async function updateStatus(reservation: any, status: string) {
  savingId.value = reservation.id
  try {
    const authToken = token.value || (import.meta.client ? localStorage.getItem('access_token') : null)
    const result = await $fetch<{ reservation: any }>(`/reservations/${reservation.id}`, {
      baseURL: apiBase.value,
      method: 'PATCH',
      headers: authToken ? { Authorization: `Bearer ${authToken}` } : {},
      body: { status },
    })
    const index = reservations.value.findIndex(item => item.id === reservation.id)
    if (index !== -1) reservations.value[index] = result.reservation
  } catch (err: any) {
    error.value = err?.data?.message || 'Could not update this reservation.'
  } finally {
    savingId.value = null
  }
}

onMounted(loadReservations)
</script>

<template>
  <div class="min-h-screen bg-stone-100 text-stone-800">
    <AdminSidebar />
    <main class="px-5 py-8 lg:ml-64 lg:px-8">
      <header class="mb-7 flex flex-wrap items-end justify-between gap-4">
        <div><p class="text-xs font-bold uppercase tracking-[.2em] text-amber-700">Floor & guest management</p><h1 class="mt-1 font-serif text-3xl font-bold text-stone-900">Table reservation requests</h1><p class="mt-2 text-sm text-stone-500">Review the customer’s room, table, occasion, and dietary choices.</p></div>
        <button class="rounded-lg border border-stone-300 bg-white px-4 py-2 text-sm font-semibold hover:bg-stone-50" @click="loadReservations">Refresh</button>
      </header>
      <div v-if="pendingCount" class="mb-6 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900"><strong>{{ pendingCount }} reservation request{{ pendingCount === 1 ? '' : 's' }}</strong> waiting for confirmation.</div>
      <p v-if="error" role="alert" class="mb-5 rounded-lg border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">{{ error }}</p>
      <p v-if="loading" class="py-12 text-center text-stone-500">Loading reservations…</p>
      <div v-else-if="!reservations.length" class="rounded-2xl border border-stone-200 bg-white p-10 text-center text-stone-500">No reservation requests yet.</div>
      <section v-else class="space-y-4">
        <article v-for="item in reservations" :key="item.id" class="rounded-2xl border bg-white p-5 shadow-sm" :class="item.status === 'pending' ? 'border-amber-300 ring-1 ring-amber-100' : 'border-stone-200'">
          <div class="flex flex-wrap items-start justify-between gap-4">
            <div class="flex items-center gap-4">
              <img :src="getRoomImage(item.areaName)" :alt="`${item.areaName} room`" class="h-20 w-28 shrink-0 rounded-xl object-cover shadow-sm" />
              <div><p class="text-[10px] font-bold uppercase tracking-wide text-amber-700">{{ item.areaName }}</p><div class="mt-1 flex flex-wrap items-center gap-2"><h2 class="text-lg font-bold text-stone-900">{{ item.guestName }}</h2><span class="rounded-full px-2.5 py-1 text-[10px] font-bold uppercase" :class="item.status === 'pending' ? 'bg-amber-100 text-amber-800' : 'bg-stone-100 text-stone-600'">{{ item.status }}</span></div><p class="mt-1 text-xs text-stone-500">Request #{{ item.id }} · {{ item.reservedFor ? new Date(item.reservedFor).toLocaleString() : '' }}</p></div>
            </div>
            <div class="flex flex-wrap gap-2"><a class="rounded-lg border border-stone-300 px-3 py-2 text-xs font-semibold" :href="`mailto:${item.guestEmail}`">Email guest</a><a class="rounded-lg border border-stone-300 px-3 py-2 text-xs font-semibold" :href="`tel:${item.guestPhone}`">Call guest</a><select :value="item.status" :disabled="savingId === item.id" class="rounded-lg border border-stone-300 bg-white px-3 py-2 text-xs" @change="updateStatus(item, ($event.target as HTMLSelectElement).value)"><option value="pending">Pending</option><option value="confirmed">Confirmed</option><option value="cancelled">Cancelled</option><option value="completed">Completed</option></select></div>
          </div>
          <dl class="mt-5 grid gap-4 border-t border-stone-100 pt-4 sm:grid-cols-2 lg:grid-cols-4">
            <div><dt class="text-[10px] font-bold uppercase tracking-wide text-stone-400">Room / atmosphere</dt><dd class="mt-1 text-sm font-semibold">{{ item.areaName }} <span class="font-normal text-stone-500">· {{ item.tableNumber ? `Table ${item.tableNumber}` : 'Table to be assigned' }}</span></dd></div>
            <div><dt class="text-[10px] font-bold uppercase tracking-wide text-stone-400">Party</dt><dd class="mt-1 text-sm">{{ item.guests }} guests · {{ item.bookingType }}</dd></div>
            <div><dt class="text-[10px] font-bold uppercase tracking-wide text-stone-400">Occasion</dt><dd class="mt-1 text-sm">{{ item.occasion }}</dd></div>
            <div><dt class="text-[10px] font-bold uppercase tracking-wide text-stone-400">Contact</dt><dd class="mt-1 break-all text-sm">{{ item.guestEmail }}<br>{{ item.guestPhone }}</dd></div>
          </dl>
          <div v-if="item.dietary?.length" class="mt-4"><p class="text-[10px] font-bold uppercase tracking-wide text-stone-400">Dietary preferences</p><div class="mt-2 flex flex-wrap gap-2"><span v-for="diet in item.dietary" :key="diet" class="rounded-full bg-amber-50 px-3 py-1 text-xs text-amber-900">{{ diet }}</span></div></div>
          <div v-if="item.notes" class="mt-4 rounded-lg bg-stone-50 p-4"><p class="text-[10px] font-bold uppercase tracking-wide text-stone-400">Guest notes</p><p class="mt-1 whitespace-pre-wrap text-sm text-stone-700">{{ item.notes }}</p></div>
        </article>
      </section>
    </main>
  </div>
</template>
