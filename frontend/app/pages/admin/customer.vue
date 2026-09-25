<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuth } from '~/composables/useAuth'

definePageMeta({ middleware: 'admin' })

const { apiBase } = useApiBase()
const { logout, token } = useAuth()

interface Customer {
  id: string
  name: string
  email: string
  phone: string
  avatar: string
  tier: 'Regular' | 'Silver VIP' | 'Gold VIP' | 'Platinum VIP'
  totalOrders: number
  totalSpent: number
  lastVisit: string
  status: 'Active' | 'Blocked'
  dbId?: number
  bookings: Booking[]
  orders: OrderSummary[]
}

interface Booking {
  id: number
  type: 'dining' | 'private' | 'room'
  date: string
  time: string
  guests: number
  status: 'confirmed' | 'pending' | 'seated' | 'completed' | 'cancelled'
  location: string
  notes: string
  orderId?: number
  reservationId?: number
}

interface OrderSummary {
  id: number
  date: string
  total: number
  status: string
  orderType: string
  tableNumber: string
}

const tiers = ['Regular', 'Silver VIP', 'Gold VIP', 'Platinum VIP'] as const
const statuses = ['Active', 'Blocked'] as const

const searchQuery = ref('')
const selectedTierFilter = ref('All')
const selectedStatusFilter = ref('All')
const selectedBookingTypeFilter = ref('All')

const isModalOpen = ref(false)
const isEditing = ref(false)
const editingCustomer = ref<Customer>({
  id: '', name: '', email: '', phone: '', avatar: '', tier: 'Regular',
  totalOrders: 0, totalSpent: 0, lastVisit: 'Today', status: 'Active', dbId: undefined,
  bookings: [], orders: []
})
const avatarFile = ref<File | null>(null)
const avatarPreview = ref('')
const saveError = ref('')
const loading = ref(false)

const onAvatarSelect = (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (file) {
    avatarFile.value = file
    avatarPreview.value = URL.createObjectURL(file)
  }
}

const customers = ref<Customer[]>([])
const allOrders = ref<any[]>([])
const allReservations = ref<any[]>([])

function formatDate(dateStr: string | null): string {
  if (!dateStr) return '—'
  const d = new Date(dateStr)
  if (isNaN(d.getTime())) return '—'
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

function formatTime(dateStr: string | null): string {
  if (!dateStr) return '—'
  const d = new Date(dateStr)
  if (isNaN(d.getTime())) return '—'
  return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

function calculateTier(totalSpent: number): Customer['tier'] {
  if (totalSpent >= 5000) return 'Platinum VIP'
  if (totalSpent >= 2000) return 'Gold VIP'
  if (totalSpent >= 500) return 'Silver VIP'
  return 'Regular'
}

function getApiHeaders() {
  const authToken = token.value || (import.meta.client ? localStorage.getItem('access_token') : null)
  if (!authToken) {
    saveError.value = 'Not authenticated. Please log in again.'
    return null
  }
  return { Authorization: `Bearer ${authToken}` }
}

async function loadCustomers() {
  loading.value = true
  saveError.value = ''
  try {
    const headers = getApiHeaders()
    if (!headers) return

    const [usersRes, ordersRes, reservationsRes] = await Promise.all([
      $fetch(`${apiBase.value}/users`, { headers }),
      $fetch(`${apiBase.value}/orders`, { headers }),
      $fetch(`${apiBase.value}/reservations`, { headers }),
    ])

    const users = (usersRes as any)?.users || []
    allOrders.value = (ordersRes as any) || []
    allReservations.value = (reservationsRes as any) || []

    customers.value = users.map((u: any) => {
      const userOrders = allOrders.value.filter(o => o.user_id === u.id)
      const userReservations = allReservations.value.filter(r => r.userId === u.id || r.UserId === u.id)
      const totalSpent = userOrders.reduce((sum, o) => sum + (o.total_price || 0), 0)
      const totalOrders = userOrders.length
      const lastOrder = userOrders.sort((a, b) => {
        const da = new Date(a.created_at || '')
        const db = new Date(b.created_at || '')
        return db.getTime() - da.getTime()
      })[0]

      const customerOrders: OrderSummary[] = userOrders.map(o => ({
        id: o.id,
        date: formatDate(o.created_at),
        total: o.total_price || 0,
        status: o.status || 'pending',
        orderType: o.order_type || 'dine-in',
        tableNumber: o.table_number || '',
      }))

      // Build bookings from reservations and orders
      const bookings: Booking[] = []

      // Table reservations
      for (const r of userReservations) {
        const bookingType = r.bookingType || r.booking_type || 'dining'
        bookings.push({
          id: r.id,
          type: bookingType,
          date: formatDate(r.reservedFor || r.reserved_for),
          time: formatTime(r.reservedFor || r.reserved_for),
          guests: r.guests || r.guestCount || 0,
          status: r.status || 'pending',
          location: `Table ${r.tableNumber || r.table_number || '?'} (${r.zone || 'Main Dining'})`,
          notes: r.notes || r.guestNotes || '',
          reservationId: r.id,
        })
      }

      // Dine-in orders with table number
      for (const o of userOrders) {
        if (o.order_type === 'dine-in' && o.table_number) {
          const hasReservation = userReservations.some(r =>
            (r.reservedFor || r.reserved_for)?.slice(0, 10) === (o.created_at || '').slice(0, 10)
          )
          if (!hasReservation) {
            bookings.push({
              id: o.id + 10000,
              type: 'dining',
              date: formatDate(o.created_at),
              time: formatTime(o.created_at),
              guests: 0,
              status: o.status || 'completed',
              location: `Table ${o.table_number}`,
              notes: o.notes || '',
              orderId: o.id,
            })
          }
        }
      }

      bookings.sort((a, b) => {
        const da = new Date(a.date)
        const db = new Date(b.date)
        return db.getTime() - da.getTime()
      })

      return {
        id: `CUST-${u.id}`,
        name: u.username,
        email: u.email,
        phone: u.phone || '',
        avatar: u.avatar ? `${apiBase.value}${u.avatar}` : '',
        tier: calculateTier(totalSpent),
        totalOrders,
        totalSpent: Math.round(totalSpent * 100) / 100,
        lastVisit: lastOrder ? formatDate(lastOrder.created_at) : '—',
        status: u.status === 'blocked' ? 'Blocked' : 'Active',
        dbId: u.id,
        bookings,
        orders: customerOrders,
      }
    })
  } catch (err: any) {
    console.error('Failed to load customers:', err)
    saveError.value = err?.data?.message || err?.message || 'Failed to load customer data'
  } finally {
    loading.value = false
  }
}

onMounted(loadCustomers)

const totalCustomersCount = computed(() => customers.value.length)
const totalVIPsCount = computed(() => customers.value.filter(c => c.tier !== 'Regular').length)
const totalLifetimeRevenue = computed(() =>
  customers.value.reduce((sum, c) => sum + c.totalSpent, 0)
)
const averageSpentPerCustomer = computed(() =>
  totalCustomersCount.value ? (totalLifetimeRevenue.value / totalCustomersCount.value) : 0
)

// Booking type counts
const totalDiningBookings = computed(() =>
  customers.value.reduce((sum, c) => sum + c.bookings.filter(b => b.type === 'dining').length, 0)
)
const totalPrivateEventBookings = computed(() =>
  customers.value.reduce((sum, c) => sum + c.bookings.filter(b => b.type === 'private').length, 0)
)
const totalRoomBookings = computed(() =>
  customers.value.reduce((sum, c) => sum + c.bookings.filter(b => b.type === 'room').length, 0)
)

const filteredCustomers = computed(() => {
  return customers.value.filter(c => {
    const matchesSearch = c.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      c.email.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (c.phone || '').includes(searchQuery.value)
    const matchesTier = selectedTierFilter.value === 'All' || c.tier === selectedTierFilter.value
    const matchesStatus = selectedStatusFilter.value === 'All' || c.status === selectedStatusFilter.value
    const matchesBookingType = selectedBookingTypeFilter.value === 'All' ||
      c.bookings.some(b => b.type === selectedBookingTypeFilter.value)
    return matchesSearch && matchesTier && matchesStatus && matchesBookingType
  })
})

const openAddModal = () => {
  isEditing.value = false
  editingCustomer.value = {
    id: `CUST-${Math.floor(800 + Math.random() * 200)}`,
    name: '', email: '', phone: '', avatar: '', tier: 'Regular',
    totalOrders: 0, totalSpent: 0, lastVisit: 'Just now', status: 'Active', dbId: undefined,
    bookings: [], orders: []
  }
  avatarFile.value = null
  avatarPreview.value = ''
  isModalOpen.value = true
}

const openEditModal = (cust: Customer) => {
  isEditing.value = true
  editingCustomer.value = { ...cust }
  avatarFile.value = null
  avatarPreview.value = cust.avatar || ''
  isModalOpen.value = true
}

const toggleStatus = (cust: Customer) => {
  cust.status = cust.status === 'Active' ? 'Blocked' : 'Active'
}

const saveCustomer = async () => {
  if (!editingCustomer.value.name.trim() || !editingCustomer.value.email.trim()) return

  const headers = getApiHeaders()
  if (!headers) return

  if (isEditing.value && editingCustomer.value.dbId) {
    const formData = new FormData()
    formData.append('username', editingCustomer.value.name)
    formData.append('email', editingCustomer.value.email)
    formData.append('phone', editingCustomer.value.phone || '')
    formData.append('role', 'customer')
    if (avatarFile.value) {
      formData.append('avatar', avatarFile.value)
    }
    try {
      saveError.value = ''
      const res = await $fetch(`/users/${editingCustomer.value.dbId}`, {
        baseURL: apiBase.value,
        method: 'PUT',
        body: formData,
        headers,
      })
      console.log('Customer updated:', res)
    } catch (e: any) {
      saveError.value = e?.data?.message || e?.message || String(e)
    }
  } else if (!isEditing.value) {
    const formData = new FormData()
    formData.append('username', editingCustomer.value.name)
    formData.append('email', editingCustomer.value.email)
    formData.append('phone', editingCustomer.value.phone || '')
    formData.append('password', 'password123')
    formData.append('role', 'customer')
    if (avatarFile.value) {
      formData.append('avatar', avatarFile.value)
    }
    try {
      saveError.value = ''
      await $fetch('/users', {
        baseURL: apiBase.value,
        method: 'POST',
        body: formData,
        headers,
      })
      await loadCustomers()
    } catch (e: any) {
      saveError.value = e?.data?.message || e?.message || String(e)
    }
  }

  isModalOpen.value = false
}

const deleteCustomer = (id: string) => {
  if (confirm('Are you sure you want to remove this customer record?')) {
    customers.value = customers.value.filter(c => c.id !== id)
  }
}

const getTierBadgeClass = (tier: Customer['tier']) => {
  switch (tier) {
    case 'Platinum VIP': return 'bg-slate-900 text-amber-300 border-slate-700'
    case 'Gold VIP': return 'bg-amber-50 text-amber-800 border-amber-300'
    case 'Silver VIP': return 'bg-stone-100 text-stone-700 border-stone-300'
    default: return 'bg-stone-50 text-stone-500 border-stone-200'
  }
}

const getBookingTypeBadge = (type: Booking['type']) => {
  switch (type) {
    case 'private': return 'bg-purple-50 text-purple-800 border-purple-300'
    case 'room': return 'bg-blue-50 text-blue-800 border-blue-300'
    default: return 'bg-emerald-50 text-emerald-800 border-emerald-300'
  }
}

const getBookingTypeLabel = (type: Booking['type']) => {
  switch (type) {
    case 'private': return 'Private Event'
    case 'room': return 'Room Booking'
    default: return 'Dining'
  }
}

const selectedCustomer = ref<Customer | null>(null)
const showBookingsModal = ref(false)
const selectedBooking = ref<Booking | null>(null)
const showBookingDetailModal = ref(false)

function viewCustomerBookings(cust: Customer) {
  selectedCustomer.value = cust
  showBookingsModal.value = true
}

function viewBookingDetail(booking: Booking) {
  selectedBooking.value = booking
  showBookingDetailModal.value = true
}

const activeDetailTab = ref<'profile' | 'bookings' | 'orders'>('profile')
</script>

<template>
  <div class="min-h-screen bg-stone-100 text-stone-800 font-sans selection:bg-amber-100">
    <AdminSidebar />

    <main class="lg:ml-64 transition-all duration-300">
      
      <!-- Sticky Header -->
      <header class="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-stone-200 bg-white/90 px-6 backdrop-blur-md lg:px-8">
        <div>
          <h1 class="text-2xl font-bold text-stone-900 tracking-tight">Customer Management</h1>
          <p class="text-xs text-stone-500 font-normal">View guest history, order statistics, loyalty tiers, bookings, and status</p>
        </div>

        <div class="flex items-center gap-3">
          <div class="relative hidden sm:block">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Search name, email, or phone..." 
              class="w-72 rounded-lg border border-stone-300 bg-stone-50 px-4 py-2 pl-9 text-xs text-stone-800 placeholder-stone-400 focus:border-amber-600 focus:bg-white focus:outline-none transition-all"
            />
            <svg class="absolute left-3 top-2.5 h-4 w-4 text-stone-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0 1 14 0z"/>
            </svg>
          </div>

          <button 
            @click="openAddModal"
            class="px-4 py-2 rounded-lg bg-amber-600 hover:bg-amber-700 text-white text-xs font-semibold uppercase tracking-wider transition-all shadow-sm flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Add Customer
          </button>
        </div>
      </header>

      <div class="p-6 lg:p-8 space-y-6">

        <!-- Metrics Overview Section -->
        <section class="grid grid-cols-1 sm:grid-cols-4 gap-5">
          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-stone-400">Total Customers</span>
              <p class="text-2xl font-bold text-stone-900 mt-1">{{ totalCustomersCount }} Guests</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-50 text-amber-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 0 1 5.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 0 1 9.288 0M15 7a3 3 0 11-6 0 3 3 0 0 1 6 0z"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-amber-600">VIP Members</span>
              <p class="text-2xl font-bold text-amber-700 mt-1">{{ totalVIPsCount }} VIPs</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-50 text-amber-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-emerald-600">Lifetime Revenue</span>
              <p class="text-2xl font-bold text-emerald-700 mt-1">${{ totalLifetimeRevenue.toFixed(2) }}</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 0 0 1 18 0z"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-stone-400">Avg Spend / Guest</span>
              <p class="text-2xl font-bold text-stone-900 mt-1">${{ averageSpentPerCustomer.toFixed(2) }}</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-stone-100 text-stone-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2zm0 0V9a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v10m-6 0a2 2 0 0 0 2 2h2a2 2 0 0 1 2-2m0 0V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </div>
          </div>
        </section>

        <!-- Booking Metrics Section -->
        <section class="grid grid-cols-1 sm:grid-cols-3 gap-5">
          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-emerald-600">Dining Bookings</span>
              <p class="text-2xl font-bold text-emerald-700 mt-1">{{ totalDiningBookings }} Tables</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 0 0 2 2h1l3-4h5l3 4h1a2 2 0 0 0 2-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2z"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-purple-600">Private Events</span>
              <p class="text-2xl font-bold text-purple-700 mt-1">{{ totalPrivateEventBookings }} Bookings</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-50 text-purple-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 9h10a2 2 0 0 1 2 2v2a2 2 0 01-2 2H7a2 2 0 01-2-2v-2a2 2 0 0 1 2-2z"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-blue-600">Room Bookings</span>
              <p class="text-2xl font-bold text-blue-700 mt-1">{{ totalRoomBookings }} Rooms</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-50 text-blue-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2z"/>
              </svg>
            </div>
          </div>
        </section>

        <!-- Filter Bar -->
        <section class="bg-white p-4 rounded-lg border border-stone-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
          <div class="flex items-center gap-4 w-full md:w-auto">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-stone-400 uppercase tracking-wider">Tier:</span>
              <select 
                v-model="selectedTierFilter"
                class="rounded-md border border-stone-300 bg-stone-50 px-3 py-1.5 text-xs text-stone-800 focus:border-amber-600 focus:outline-none"
              >
                <option value="All">All Tiers</option>
                <option v-for="t in tiers" :key="t" :value="t">{{ t }}</option>
              </select>
            </div>

            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-stone-400 uppercase tracking-wider">Status:</span>
              <select 
                v-model="selectedStatusFilter"
                class="rounded-md border border-stone-300 bg-stone-50 px-3 py-1.5 text-xs text-stone-800 focus:border-amber-600 focus:outline-none"
              >
                <option value="All">All Statuses</option>
                <option value="Active">Active</option>
                <option value="Blocked">Blocked</option>
              </select>
            </div>
          </div>

          <span class="text-xs text-stone-400 font-normal">Click status badge to toggle active/blocked. Click "View Bookings" to see customer booking history.</span>
        </section>

        <!-- Loading state -->
        <div v-if="loading" class="bg-white border border-stone-200 rounded-lg shadow-sm p-8 text-center text-stone-400">
          Loading customer data...
        </div>

        <!-- Error state -->
        <div v-else-if="saveError" class="bg-rose-50 border border-rose-200 rounded-lg shadow-sm p-4 text-rose-800 text-sm">
          {{ saveError }}
        </div>

        <!-- Customer Data Table -->
        <section v-else class="bg-white border border-stone-200 rounded-lg shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs text-stone-700">
              <thead>
                <tr class="bg-stone-50 border-b border-stone-200 text-[10px] font-bold uppercase tracking-wider text-stone-400">
                  <th scope="col" class="py-3.5 px-4">Customer Name</th>
                  <th scope="col" class="py-3.5 px-4">Contact Info</th>
                  <th scope="col" class="py-3.5 px-4">Loyalty Tier</th>
                  <th scope="col" class="py-3.5 px-4 text-center">Total Orders</th>
                  <th scope="col" class="py-3.5 px-4 text-right">Total Spent</th>
                  <th scope="col" class="py-3.5 px-4">Last Visit</th>
                  <th scope="col" class="py-3.5 px-4 text-center">Bookings</th>
                  <th scope="col" class="py-3.5 px-4 text-center">Booking Types</th>
                  <th scope="col" class="py-3.5 px-4 text-center">Status</th>
                  <th scope="col" class="py-3.5 px-4 text-right pr-6">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-stone-100">
                <tr 
                  v-for="cust in filteredCustomers" 
                  :key="cust.id" 
                  class="hover:bg-stone-50/80 transition-colors group"
                >
                  <!-- Customer Avatar & Name -->
                  <td class="py-3.5 px-4">
                    <div class="flex items-center gap-3">
                      <img 
                        v-if="cust.avatar"
                        :src="cust.avatar" 
                        :alt="cust.name" 
                        class="h-10 w-10 rounded-full object-cover border-2 border-[#C59237] shrink-0"
                      />
                      <div
                        v-else
                        class="h-10 w-10 rounded-full bg-[#C59237] flex items-center justify-center text-white text-sm font-bold shrink-0"
                      >
                        {{ cust.name?.charAt(0).toUpperCase() || '?' }}
                      </div>
                      <div>
                        <span class="font-bold text-stone-900 text-sm block">{{ cust.name }}</span>
                        <span class="text-[10px] font-mono text-stone-400">{{ cust.id }}</span>
                      </div>
                    </div>
                  </td>

                  <!-- Contact Info -->
                  <td class="py-3.5 px-4 whitespace-nowrap">
                    <div class="space-y-0.5">
                      <p class="text-stone-800 font-medium">{{ cust.email }}</p>
                      <p class="text-[11px] text-stone-400 font-mono">{{ cust.phone || '—' }}</p>
                    </div>
                  </td>

                  <!-- Tier -->
                  <td class="py-3.5 px-4 whitespace-nowrap">
                    <span 
                      :class="getTierBadgeClass(cust.tier)"
                      class="px-2.5 py-0.5 rounded border text-[10px] font-bold tracking-wide"
                    >
                      {{ cust.tier }}
                    </span>
                  </td>

                  <!-- Orders -->
                  <td class="py-3.5 px-4 text-center whitespace-nowrap">
                    <span class="font-bold text-stone-800 bg-stone-100 px-2 py-0.5 rounded border border-stone-200">
                      {{ cust.totalOrders }} Orders
                    </span>
                  </td>

                  <!-- Total Spent -->
                  <td class="py-3.5 px-4 text-right font-bold text-stone-900 whitespace-nowrap">
                    ${{ cust.totalSpent.toFixed(2) }}
                  </td>

                  <!-- Last Visit -->
                  <td class="py-3.5 px-4 text-stone-500 whitespace-nowrap">
                    {{ cust.lastVisit }}
                  </td>

                  <!-- Bookings Count -->
                  <td class="py-3.5 px-4 text-center whitespace-nowrap">
                    <span class="font-bold text-stone-800 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                      {{ cust.bookings.length }} Bookings
                    </span>
                  </td>

                  <!-- Booking Type Breakdown -->
                  <td class="py-3.5 px-4 text-center whitespace-nowrap">
                    <div class="flex flex-col gap-1">
                      <span v-if="cust.bookings.filter(b => b.type === 'dining').length > 0" class="px-1.5 py-0.5 rounded text-[10px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                        Dining {{ cust.bookings.filter(b => b.type === 'dining').length }}
                      </span>
                      <span v-if="cust.bookings.filter(b => b.type === 'private').length > 0" class="px-1.5 py-0.5 rounded text-[10px] font-medium bg-purple-50 text-purple-700 border border-purple-200">
                        Private {{ cust.bookings.filter(b => b.type === 'private').length }}
                      </span>
                      <span v-if="cust.bookings.filter(b => b.type === 'room').length > 0" class="px-1.5 py-0.5 rounded text-[10px] font-medium bg-blue-50 text-blue-700 border border-blue-200">
                        Room {{ cust.bookings.filter(b => b.type === 'room').length }}
                      </span>
                    </div>
                  </td>

                  <!-- Status Toggle -->
                  <td class="py-3.5 px-4 text-center whitespace-nowrap">
                    <button 
                      @click="toggleStatus(cust)"
                      :class="cust.status === 'Active' ? 'bg-emerald-50 text-emerald-700 border-emerald-300' : 'bg-rose-50 text-rose-700 border-rose-300'"
                      class="px-2.5 py-1 rounded text-[10px] font-bold border transition-all cursor-pointer hover:opacity-80"
                    >
                      {{ cust.status }}
                    </button>
                  </td>

                  <!-- Actions -->
                  <td class="py-3.5 px-4 text-right pr-6 whitespace-nowrap">
                    <div class="flex items-center justify-end gap-1">
                      <button 
                        @click="viewCustomerBookings(cust)"
                        class="p-1.5 rounded-md text-stone-400 hover:text-amber-600 hover:bg-stone-100 transition-colors"
                        title="View Bookings"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12H9m12 0l-4 4m4-4l-4-4"/>
                        </svg>
                      </button>
                      <button 
                        @click="openEditModal(cust)"
                        class="p-1.5 rounded-md text-stone-400 hover:text-amber-600 hover:bg-stone-100 transition-colors"
                        title="Edit Profile"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2v-5m-1.414-9.414a2 2 0 1 1 2.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                      </button>
                      <button 
                        @click="deleteCustomer(cust.id)"
                        class="p-1.5 rounded-md text-stone-400 hover:text-rose-600 hover:bg-stone-100 transition-colors"
                        title="Delete Profile"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0 1 16.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>

                <!-- Empty State -->
                <tr v-if="filteredCustomers.length === 0">
                  <td colspan="10" class="py-12 text-center text-stone-400 font-normal">
                    No customers found matching search filters.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

      </div>
    </main>

    <!-- Customer Detail Modal -->
    <div 
      v-if="showBookingsModal && selectedCustomer" 
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4"
    >
      <div class="bg-white border border-stone-200 rounded-lg max-w-5xl w-full shadow-xl text-stone-800">
        <div class="flex items-center justify-between border-b border-stone-200 px-6 py-4">
          <div class="flex items-center gap-4">
            <img
              v-if="selectedCustomer.avatar"
              :src="selectedCustomer.avatar"
              :alt="selectedCustomer.name"
              class="h-14 w-14 rounded-full object-cover border-2 border-[#C59237]"
            />
            <div
              v-else
              class="h-14 w-14 rounded-full bg-[#C59237] flex items-center justify-center text-white text-2xl font-bold"
            >
              {{ selectedCustomer.name?.charAt(0).toUpperCase() || '?' }}
            </div>
            <div>
              <h3 class="text-xl font-bold text-stone-900">{{ selectedCustomer.name }}</h3>
              <div class="flex items-center gap-4 text-xs text-stone-500">
                <span>{{ selectedCustomer.email }}</span>
                <span>{{ selectedCustomer.phone || '—' }}</span>
                <span>ID: {{ selectedCustomer.id }}</span>
              </div>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button 
              @click="showBookingsModal = false"
              class="text-stone-400 hover:text-stone-700 text-xl"
            >
              ✕
            </button>
          </div>
        </div>

        <!-- Tabs -->
        <div class="flex border-b border-stone-200 bg-stone-50/50">
          <button
            v-for="tab in [
              { key: 'profile', label: 'Customer Profile' },
              { key: 'bookings', label: 'Booking History' },
              { key: 'orders', label: 'Order History' }
            ]"
            :key="tab.key"
            @click="activeDetailTab = tab.key"
            :class="[
              'px-6 py-3 text-sm font-medium transition-all',
              activeDetailTab === tab.key
                ? 'text-amber-700 border-b-2 border-amber-600 bg-white'
                : 'text-stone-600 hover:text-stone-900 hover:bg-stone-100'
            ]"
          >
            {{ tab.label }}
          </button>
        </div>

        <div class="p-6">
          <!-- Profile Tab -->
          <div v-if="activeDetailTab === 'profile'" class="space-y-6">
            <!-- Stats Grid -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div class="bg-stone-50 p-4 rounded-lg border border-stone-200">
                <span class="text-[10px] font-bold uppercase text-stone-400">Loyalty Tier</span>
                <div class="mt-2">
                  <span 
                    :class="getTierBadgeClass(selectedCustomer.tier)"
                    class="px-3 py-1 rounded border text-sm font-bold"
                  >
                    {{ selectedCustomer.tier }}
                  </span>
                </div>
              </div>

              <div class="bg-stone-50 p-4 rounded-lg border border-stone-200">
                <span class="text-[10px] font-bold uppercase text-stone-400">Total Orders</span>
                <p class="text-2xl font-bold text-stone-900 mt-1">{{ selectedCustomer.totalOrders }} Orders</p>
              </div>

              <div class="bg-stone-50 p-4 rounded-lg border border-stone-200">
                <span class="text-[10px] font-bold uppercase text-emerald-600">Lifetime Spent</span>
                <p class="text-2xl font-bold text-emerald-700 mt-1">${{ selectedCustomer.totalSpent.toFixed(2) }}</p>
              </div>

              <div class="bg-stone-50 p-4 rounded-lg border border-stone-200">
                <span class="text-[10px] font-bold uppercase text-stone-400">Last Visit</span>
                <p class="text-2xl font-bold text-stone-900 mt-1">{{ selectedCustomer.lastVisit }}</p>
              </div>
            </div>

            <!-- Booking Type Summary -->
            <div class="grid grid-cols-3 gap-4">
              <div class="bg-emerald-50 p-4 rounded-lg border border-emerald-100 text-center">
                <span class="text-[10px] font-bold uppercase text-emerald-600">Dining Bookings</span>
                <p class="text-xl font-bold text-emerald-700 mt-1">{{ selectedCustomer.bookings.filter(b => b.type === 'dining').length }}</p>
              </div>
              <div class="bg-purple-50 p-4 rounded-lg border border-purple-100 text-center">
                <span class="text-[10px] font-bold uppercase text-purple-600">Private Events</span>
                <p class="text-xl font-bold text-purple-700 mt-1">{{ selectedCustomer.bookings.filter(b => b.type === 'private').length }}</p>
              </div>
              <div class="bg-blue-50 p-4 rounded-lg border border-blue-100 text-center">
                <span class="text-[10px] font-bold uppercase text-blue-600">Room Bookings</span>
                <p class="text-xl font-bold text-blue-700 mt-1">{{ selectedCustomer.bookings.filter(b => b.type === 'room').length }}</p>
              </div>
            </div>

            <!-- Contact Info -->
            <div class="border-t border-stone-200 pt-4">
              <h4 class="text-sm font-bold text-stone-700 mb-3">Contact Information</h4>
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="font-medium text-stone-500">Full Name:</span>
                  <span class="text-stone-900 ml-2">{{ selectedCustomer.name }}</span>
                </div>
                <div>
                  <span class="font-medium text-stone-500">Email:</span>
                  <span class="text-stone-900 ml-2">{{ selectedCustomer.email }}</span>
                </div>
                <div>
                  <span class="font-medium text-stone-500">Phone:</span>
                  <span class="text-stone-900 ml-2">{{ selectedCustomer.phone || '—' }}</span>
                </div>
                <div>
                  <span class="font-medium text-stone-500">Account Status:</span>
                  <span 
                    :class="selectedCustomer.status === 'Active' ? 'text-emerald-700' : 'text-rose-700'"
                    class="font-bold"
                  >
                    {{ selectedCustomer.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Bookings Tab -->
          <div v-else-if="activeDetailTab === 'bookings'" class="space-y-3">
            <div v-if="selectedCustomer.bookings.length === 0" class="py-8 text-center text-stone-400">
              No bookings found for this customer.
            </div>
            <div 
              v-else
              v-for="booking in selectedCustomer.bookings" 
              :key="booking.id"
              class="border border-stone-200 rounded-lg p-4 hover:bg-stone-50 transition-colors"
            >
              <div class="flex items-start justify-between gap-4">
                <div class="flex items-start gap-3">
                  <span 
                    :class="getBookingTypeBadge(booking.type)"
                    class="px-2.5 py-1 rounded border text-[10px] font-bold tracking-wide whitespace-nowrap"
                  >
                    {{ getBookingTypeLabel(booking.type) }}
                  </span>
                  <div class="flex-1">
                    <p class="font-bold text-stone-900 text-sm">{{ booking.location }}</p>
                    <div class="grid grid-cols-2 gap-x-4 gap-y-1 mt-1 text-[11px] text-stone-500">
                      <div><span class="font-medium">Date:</span> {{ booking.date }}</div>
                      <div><span class="font-medium">Time:</span> {{ booking.time }}</div>
                      <div><span class="font-medium">Guests:</span> {{ booking.guests || '—' }}</div>
                      <div>
                        <span class="font-medium">Status:</span>
                        <span 
                          :class="booking.status === 'confirmed' ? 'text-emerald-700' : 
                                 booking.status === 'pending' ? 'text-amber-700' : 
                                 booking.status === 'cancelled' ? 'text-rose-700' : 'text-stone-700'"
                          class="font-medium"
                        >
                          {{ booking.status }}
                        </span>
                      </div>
                    </div>
                    <p v-if="booking.notes" class="text-[11px] text-stone-500 mt-1">{{ booking.notes }}</p>
                  </div>
                </div>
                <div class="flex flex-col items-end gap-1">
                  <span class="text-[10px] text-stone-300 font-mono">ID: {{ booking.id }}</span>
                  <span v-if="booking.reservationId" class="text-[10px] text-stone-400">Reservation #{{ booking.reservationId }}</span>
                  <span v-else-if="booking.orderId" class="text-[10px] text-stone-400">Order #{{ booking.orderId }}</span>
                  <button 
                    @click="viewBookingDetail(booking)"
                    class="mt-2 px-2 py-1 rounded-md bg-amber-50 text-amber-700 text-[9px] font-semibold hover:bg-amber-100 transition-colors"
                    title="View booking details"
                  >
                    View Details
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Orders Tab -->
          <div v-else-if="activeDetailTab === 'orders'" class="space-y-3">
            <div v-if="selectedCustomer.orders.length === 0" class="py-8 text-center text-stone-400">
              No orders found for this customer.
            </div>
            <div 
              v-else
              v-for="order in selectedCustomer.orders" 
              :key="order.id"
              class="border border-stone-200 rounded-lg p-4 hover:bg-stone-50 transition-colors"
            >
              <div class="flex items-start justify-between gap-4">
                <div class="flex-1">
                  <p class="font-bold text-stone-900 text-sm">Order #{{ order.id }}</p>
                  <div class="grid grid-cols-2 gap-x-4 gap-y-1 mt-1 text-[11px] text-stone-500">
                    <div><span class="font-medium">Date:</span> {{ order.date }}</div>
                    <div><span class="font-medium">Total:</span> ${{ order.total.toFixed(2) }}</div>
                    <div><span class="font-medium">Type:</span> {{ order.orderType }}</div>
                    <div><span class="font-medium">Table:</span> {{ order.tableNumber || '—' }}</div>
                  </div>
                </div>
                <div class="flex flex-col items-end">
                  <span 
                    :class="order.status === 'completed' || order.status === 'delivered' ? 'text-emerald-700' : 
                           order.status === 'cancelled' ? 'text-rose-700' : 
                           order.status === 'pending' ? 'text-amber-700' : 'text-stone-700'"
                    class="text-[10px] font-bold uppercase"
                  >
                    {{ order.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="border-t border-stone-200 px-6 py-4 flex items-center justify-end">
          <button 
            @click="showBookingsModal = false"
            class="px-5 py-2.5 rounded-lg border border-stone-300 text-stone-700 font-semibold hover:bg-stone-100 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- Booking Detail Modal -->
    <div 
      v-if="showBookingDetailModal && selectedBooking" 
      class="fixed inset-0 z-[60] flex items-center justify-center bg-black/50 backdrop-blur-xs p-4"
    >
      <div class="bg-white border border-stone-200 rounded-lg max-w-3xl w-full shadow-xl text-stone-800">
        <div class="border-b border-stone-200 px-6 py-4 flex items-center justify-between">
          <div>
            <h3 class="text-xl font-bold text-stone-900">Booking Details</h3>
            <p class="text-sm text-stone-500">
              <span class="font-medium">{{ getBookingTypeLabel(selectedBooking.type) }}</span>
              • {{ selectedBooking.location }}
            </p>
          </div>
          <button 
            @click="showBookingDetailModal = false"
            class="text-stone-400 hover:text-stone-700 text-xl"
          >
            ✕
          </button>
        </div>

        <div class="p-6 space-y-4">
          <!-- Booking Type Badge -->
          <div>
            <span 
              :class="getBookingTypeBadge(selectedBooking.type)"
              class="px-3 py-1 rounded border text-sm font-bold"
            >
              {{ getBookingTypeLabel(selectedBooking.type) }}
            </span>
          </div>

          <!-- Detail Grid -->
          <div class="grid grid-cols-2 gap-x-6 gap-y-3 text-sm">
            <div>
              <span class="font-medium text-stone-500">Booking ID:</span>
              <span class="text-stone-900 ml-2">{{ selectedBooking.id }}</span>
            </div>
            <div>
              <span class="font-medium text-stone-500">Booking Date:</span>
              <span class="text-stone-900 ml-2">{{ selectedBooking.date }}</span>
            </div>
            <div>
              <span class="font-medium text-stone-500">Booking Time:</span>
              <span class="text-stone-900 ml-2">{{ selectedBooking.time }}</span>
            </div>
            <div>
              <span class="font-medium text-stone-500">Number of Guests:</span>
              <span class="text-stone-900 ml-2">{{ selectedBooking.guests || '—' }}</span>
            </div>
            <div>
              <span class="font-medium text-stone-500">Location:</span>
              <span class="text-stone-900 ml-2">{{ selectedBooking.location }}</span>
            </div>
            <div>
              <span class="font-medium text-stone-500">Status:</span>
              <span 
                :class="selectedBooking.status === 'confirmed' ? 'text-emerald-700' : 
                       selectedBooking.status === 'pending' ? 'text-amber-700' : 
                       selectedBooking.status === 'cancelled' ? 'text-rose-700' : 'text-stone-700'"
                class="font-bold"
              >
                {{ selectedBooking.status }}
              </span>
            </div>
            <div v-if="selectedBooking.reservationId">
              <span class="font-medium text-stone-500">Reservation #:</span>
              <span class="text-stone-900 ml-2">{{ selectedBooking.reservationId }}</span>
            </div>
            <div v-else-if="selectedBooking.orderId">
              <span class="font-medium text-stone-500">Order #:</span>
              <span class="text-stone-900 ml-2">{{ selectedBooking.orderId }}</span>
            </div>
            <div v-if="selectedBooking.notes" class="col-span-2">
              <span class="font-medium text-stone-500">Notes:</span>
              <p class="text-stone-900 mt-1 whitespace-pre-wrap">{{ selectedBooking.notes }}</p>
            </div>
          </div>
        </div>

        <div class="border-t border-stone-200 px-6 py-4 flex items-center justify-end gap-3">
          <button 
            @click="showBookingDetailModal = false"
            class="px-5 py-2.5 rounded-lg border border-stone-300 text-stone-700 font-semibold hover:bg-stone-100 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- Create / Edit Customer Modal -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4">
      <div class="bg-white border border-stone-200 rounded-lg max-w-lg w-full p-6 shadow-xl space-y-5 text-stone-800">
        
        <div class="flex items-center justify-between border-b border-stone-200 pb-4">
          <div class="flex items-center gap-4">
            <img
              v-if="avatarPreview"
              :src="avatarPreview"
              alt="Customer logo"
              class="h-14 w-14 rounded-full object-cover border border-stone-200"
            />
            <div>
              <span class="text-[10px] uppercase font-bold tracking-widest text-amber-600">Guest Database</span>
              <h3 class="text-xl font-bold text-stone-900">
                {{ isEditing ? 'Edit Customer Profile' : 'Add New Guest' }}
              </h3>
            </div>
          </div>
          <button @click="isModalOpen = false" class="text-stone-400 hover:text-stone-700 text-base">✕</button>
        </div>

        <form @submit.prevent="saveCustomer" class="space-y-4 text-xs">
          
          <div>
            <label class="font-bold text-stone-700 block mb-1">Customer Logo / Avatar</label>
            <div class="flex items-center gap-3">
              <input
                type="file"
                accept="image/*"
                @change="onAvatarSelect"
                class="text-xs text-stone-600 file:mr-3 file:py-1.5 file:px-3 file:rounded-md file:border-0 file:bg-amber-50 file:text-amber-700 file:text-xs file:font-semibold hover:file:bg-amber-100 cursor-pointer"
              />
            </div>
            <p v-if="saveError" class="mt-2 text-xs text-rose-600 font-semibold">{{ saveError }}</p>
          </div>

          <div>
            <label class="font-bold text-stone-700 block mb-1">Full Name</label>
            <input 
              v-model="editingCustomer.name" 
              type="text" 
              placeholder="e.g. Sophia Laurent"
              required
              class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-900 focus:border-amber-600 focus:bg-white focus:outline-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="font-bold text-stone-700 block mb-1">Email Address</label>
              <input 
                v-model="editingCustomer.email" 
                type="email" 
                placeholder="sophia@example.com"
                required
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
              />
            </div>

            <div>
              <label class="font-bold text-stone-700 block mb-1">Phone Number</label>
              <input 
                v-model="editingCustomer.phone" 
                type="text" 
                placeholder="+1 (555) 000-0000"
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="font-bold text-stone-700 block mb-1">Loyalty Tier</label>
              <select 
                v-model="editingCustomer.tier"
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
              >
                <option v-for="t in tiers" :key="t" :value="t">{{ t }}</option>
              </select>
            </div>

            <div>
              <label class="font-bold text-stone-700 block mb-1">Account Status</label>
              <select 
                v-model="editingCustomer.status"
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
              >
                <option value="Active">Active</option>
                <option value="Blocked">Blocked</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="font-bold text-stone-700 block mb-1">Total Orders</label>
              <input 
                v-model.number="editingCustomer.totalOrders" 
                type="number" 
                min="0"
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
              />
            </div>

            <div>
              <label class="font-bold text-stone-700 block mb-1">Lifetime Spent ($)</label>
              <input 
                v-model.number="editingCustomer.totalSpent" 
                type="number" 
                step="0.01" 
                min="0"
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
              />
            </div>
          </div>

          <div class="pt-4 border-t border-stone-200 flex items-center justify-end gap-3">
            <button 
              type="button" 
              @click="isModalOpen = false" 
              class="px-5 py-2.5 rounded-lg border border-stone-300 text-stone-700 font-semibold hover:bg-stone-100 transition-colors"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              class="px-5 py-2.5 rounded-lg bg-amber-600 hover:bg-amber-700 text-white font-semibold transition-colors shadow-sm"
            >
              {{ isEditing ? 'Update Guest' : 'Save Guest' }}
            </button>
          </div>

        </form>

      </div>
    </div>
  </div>
</template>
