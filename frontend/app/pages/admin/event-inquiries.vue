<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import AdminSidebar from '~/components/AdminSidebar.vue'
import { useAuth } from '~/composables/useAuth'

definePageMeta({ middleware: 'admin' })
const { apiBase } = useApiBase()
const { token } = useAuth()
const inquiries = ref<any[]>([])
const loading = ref(true)
const error = ref('')
const savingId = ref<number | null>(null)
const newCount = computed(() => inquiries.value.filter(item => item.status === 'new').length)

async function loadInquiries() {
  loading.value = true
  error.value = ''
  try {
    const authToken = token.value || (import.meta.client ? localStorage.getItem('access_token') : null)
    inquiries.value = await $fetch<any[]>('/event-inquiries', {
      baseURL: apiBase.value,
      headers: authToken ? { Authorization: `Bearer ${authToken}` } : {},
    })
  } catch (err: any) {
    error.value = err?.data?.message || 'Could not load event inquiries.'
  } finally {
    loading.value = false
  }
}

async function updateStatus(inquiry: any, status: string) {
  savingId.value = inquiry.id
  try {
    const authToken = token.value || (import.meta.client ? localStorage.getItem('access_token') : null)
    const result = await $fetch<{ inquiry: any }>(`/event-inquiries/${inquiry.id}`, {
      baseURL: apiBase.value,
      method: 'PATCH',
      headers: authToken ? { Authorization: `Bearer ${authToken}` } : {},
      body: { status },
    })
    const index = inquiries.value.findIndex(item => item.id === inquiry.id)
    if (index !== -1) inquiries.value[index] = result.inquiry
  } catch (err: any) {
    error.value = err?.data?.message || 'Could not update this inquiry.'
  } finally {
    savingId.value = null
  }
}

onMounted(loadInquiries)
</script>

<template>
  <div class="min-h-screen bg-stone-100 text-stone-800">
    <AdminSidebar />
    <main class="px-5 py-8 transition-all lg:ml-64 lg:px-8">
      <header class="mb-7 flex flex-wrap items-end justify-between gap-4">
        <div>
          <p class="text-xs font-bold uppercase tracking-[.2em] text-amber-700">Messages</p>
          <h1 class="mt-1 font-serif text-3xl font-bold text-stone-900">Event inquiries</h1>
          <p class="mt-2 text-sm text-stone-500">Review booking requests and follow up with guests.</p>
        </div>
        <button class="rounded-lg border border-stone-300 bg-white px-4 py-2 text-sm font-semibold hover:bg-stone-50" @click="loadInquiries">Refresh</button>
      </header>

      <div v-if="newCount" class="mb-6 flex items-center gap-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-amber-900">
        <span class="flex h-9 w-9 items-center justify-center rounded-full bg-amber-200 font-bold">{{ newCount }}</span>
        <p class="text-sm"><strong>New event request{{ newCount === 1 ? '' : 's' }}</strong> waiting for your review.</p>
      </div>
      <p v-if="error" role="alert" class="mb-5 rounded-lg border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">{{ error }}</p>
      <p v-if="loading" class="py-12 text-center text-stone-500">Loading requests…</p>
      <div v-else-if="!inquiries.length" class="rounded-2xl border border-stone-200 bg-white p-10 text-center text-stone-500">No event requests yet.</div>

      <section v-else class="space-y-4">
        <article v-for="item in inquiries" :key="item.id" class="rounded-2xl border bg-white p-5 shadow-sm" :class="item.status === 'new' ? 'border-amber-300 ring-1 ring-amber-100' : 'border-stone-200'">
          <div class="flex flex-wrap items-start justify-between gap-4">
            <div>
              <div class="flex flex-wrap items-center gap-2">
                <h2 class="text-lg font-bold text-stone-900">{{ item.name }}</h2>
                <span class="rounded-full px-2.5 py-1 text-[10px] font-bold uppercase tracking-wide" :class="item.status === 'new' ? 'bg-amber-100 text-amber-800' : 'bg-stone-100 text-stone-600'">{{ item.status }}</span>
              </div>
              <p class="mt-1 text-xs text-stone-500">Request #{{ item.id }} · received {{ item.createdAt ? new Date(item.createdAt).toLocaleString() : '' }}</p>
            </div>
            <div class="flex flex-wrap gap-2">
              <a class="rounded-lg border border-stone-400 hover:bg-stone-500 hover:text-white px-3 py-2 text-xs font-semibold" :href="`mailto:${item.email}`">Email guest</a>
              <a class="rounded-lg border border-stone-400 hover:bg-stone-500 hover:text-white px-3 py-2 text-xs font-semibold" :href="`tel:${item.phone}`">Call guest</a>
              <select :value="item.status" :disabled="savingId === item.id" class="rounded-lg border border-stone-300 bg-white px-3 py-2 text-xs" @change="updateStatus(item, ($event.target as HTMLSelectElement).value)">
                <option value="new">New</option><option value="contacted">Contacted</option><option value="confirmed">Confirmed</option><option value="declined">Declined</option>
              </select> 
            </div>
          </div>
          <dl class="mt-5 grid gap-4 border-t border-stone-100 pt-4 sm:grid-cols-2 lg:grid-cols-4">
            <div><dt class="text-[10px] font-bold uppercase tracking-wide text-stone-400">Event</dt><dd class="mt-1 text-sm font-semibold">{{ item.eventType }}</dd></div>
            <div><dt class="text-[10px] font-bold uppercase tracking-wide text-stone-400">Date & guests</dt><dd class="mt-1 text-sm font-semibold">{{ item.eventDate }} · {{ item.guests }} guests</dd></div>
            <div><dt class="text-[10px] font-bold uppercase tracking-wide text-stone-400">Preferred space</dt><dd class="mt-1 text-sm font-semibold">{{ item.preferredSpace }}</dd></div>
            <div><dt class="text-[10px] font-bold uppercase tracking-wide text-stone-400">Contact</dt><dd class="mt-1 break-all text-sm">{{ item.email }}<br>{{ item.phone }}</dd></div>
          </dl>
          <div v-if="item.notes" class="mt-4 rounded-lg bg-stone-50 p-4">
            <p class="text-[10px] font-bold uppercase tracking-wide text-stone-400">Guest message</p>
            <p class="mt-1 whitespace-pre-wrap text-sm text-stone-700">{{ item.notes }}</p>
          </div>
        </article>
      </section>
    </main>
  </div>
</template>
