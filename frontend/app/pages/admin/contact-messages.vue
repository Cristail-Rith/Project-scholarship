<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import AdminSidebar from '~/components/AdminSidebar.vue'
import { useAuth } from '~/composables/useAuth'

definePageMeta({ middleware: 'admin' })
const { apiBase } = useApiBase()
const { token } = useAuth()
const messages = ref<any[]>([])
const loading = ref(true)
const error = ref('')
const savingId = ref<number | null>(null)
const newCount = computed(() => messages.value.filter(item => item.status === 'new').length)

async function loadMessages() {
  loading.value = true
  error.value = ''
  try {
    const authToken = token.value || (import.meta.client ? localStorage.getItem('access_token') : null)
    messages.value = await $fetch<any[]>('/contact-messages', {
      baseURL: apiBase.value,
      headers: authToken ? { Authorization: `Bearer ${authToken}` } : {},
    })
  } catch (err: any) {
    error.value = err?.data?.message || 'Could not load contact messages.'
  } finally {
    loading.value = false
  }
}

async function updateStatus(message: any, status: string) {
  savingId.value = message.id
  try {
    const authToken = token.value || (import.meta.client ? localStorage.getItem('access_token') : null)
    const result = await $fetch<{ contactMessage: any }>(`/contact-messages/${message.id}`, {
      baseURL: apiBase.value,
      method: 'PATCH',
      headers: authToken ? { Authorization: `Bearer ${authToken}` } : {},
      body: { status },
    })
    const index = messages.value.findIndex(item => item.id === message.id)
    if (index !== -1) messages.value[index] = result.contactMessage
  } catch (err: any) {
    error.value = err?.data?.message || 'Could not update this message.'
  } finally {
    savingId.value = null
  }
}

onMounted(loadMessages)
</script>

<template>
  <div class="min-h-screen bg-stone-100 text-stone-800">
    <AdminSidebar />
    <main class="px-5 py-8 lg:ml-64 lg:px-8">
      <header class="mb-7 flex flex-wrap items-end justify-between gap-4">
        <div>
          <p class="text-xs font-bold uppercase tracking-[.2em] text-amber-700">Guest messages</p>
          <h1 class="mt-1 font-serif text-3xl font-bold text-stone-900">Contact requests</h1>
          <p class="mt-2 text-sm text-stone-500">Table requests and questions sent through the contact form.</p>
        </div>
        <button class="rounded-lg border border-stone-300 bg-white px-4 py-2 text-sm font-semibold hover:bg-stone-50" @click="loadMessages">Refresh</button>
      </header>
      <div v-if="newCount" class="mb-6 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900"><strong>{{ newCount }} new contact request{{ newCount === 1 ? '' : 's' }}</strong> waiting for review.</div>
      <p v-if="error" role="alert" class="mb-5 rounded-lg border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">{{ error }}</p>
      <p v-if="loading" class="py-12 text-center text-stone-500">Loading messages…</p>
      <div v-else-if="!messages.length" class="rounded-2xl border border-stone-200 bg-white p-10 text-center text-stone-500">No contact requests yet.</div>
      <section v-else class="space-y-4">
        <article v-for="item in messages" :key="item.id" class="rounded-2xl border bg-white p-5 shadow-sm" :class="item.status === 'new' ? 'border-amber-300 ring-1 ring-amber-100' : 'border-stone-200'">
          <div class="flex flex-wrap items-start justify-between gap-4">
            <div>
              <div class="flex items-center gap-2"><h2 class="text-lg font-bold text-stone-900">{{ item.name }}</h2><span class="rounded-full px-2.5 py-1 text-[10px] font-bold uppercase" :class="item.status === 'new' ? 'bg-amber-100 text-amber-800' : 'bg-stone-100 text-stone-600'">{{ item.status }}</span></div>
              <p class="mt-1 text-xs text-stone-500">Message #{{ item.id }} · {{ item.createdAt ? new Date(item.createdAt).toLocaleString() : '' }}</p>
            </div>
            <div class="flex flex-wrap gap-2">
              <a class="rounded-lg border border-stone-300 px-3 py-2 text-xs font-semibold" :href="`mailto:${item.email}`">Email</a>
              <a class="rounded-lg border border-stone-300 px-3 py-2 text-xs font-semibold" :href="`tel:${item.phone}`">Call</a>
              <select :value="item.status" :disabled="savingId === item.id" class="rounded-lg border border-stone-300 bg-white px-3 py-2 text-xs" @change="updateStatus(item, ($event.target as HTMLSelectElement).value)"><option value="new">New</option><option value="contacted">Contacted</option><option value="resolved">Resolved</option></select>
            </div>
          </div>
          <dl class="mt-5 grid gap-4 border-t border-stone-100 pt-4 sm:grid-cols-3">
            <div><dt class="text-[10px] font-bold uppercase tracking-wide text-stone-400">Email</dt><dd class="mt-1 break-all text-sm">{{ item.email }}</dd></div>
            <div><dt class="text-[10px] font-bold uppercase tracking-wide text-stone-400">Preferred date</dt><dd class="mt-1 text-sm">{{ item.preferredDate || 'Flexible' }}</dd></div>
            <div><dt class="text-[10px] font-bold uppercase tracking-wide text-stone-400">Guests</dt><dd class="mt-1 text-sm">{{ item.guests }}{{ item.guests === 6 ? '+' : '' }}</dd></div>
          </dl>
          <div v-if="item.message" class="mt-4 rounded-lg bg-stone-50 p-4"><p class="text-[10px] font-bold uppercase tracking-wide text-stone-400">Guest message</p><p class="mt-1 whitespace-pre-wrap text-sm text-stone-700">{{ item.message }}</p></div>
        </article>
      </section>
    </main>
  </div>
</template>
