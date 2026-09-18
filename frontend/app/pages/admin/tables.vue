<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuth } from '~/composables/useAuth'
import { useRuntimeConfig } from '#imports'

definePageMeta({ middleware: 'admin' })

interface Table {
  id: string
  number: number
  capacity: number
  zone: 'Main Dining' | 'VIP Lounge' | 'Terrace' | 'Bar'
  status: 'Available' | 'Occupied' | 'Reserved' | 'Cleaning'
  shape: 'round' | 'square' | 'long'
  bgImage: string
  currentGuest?: string
  guestImage?: string
  partySize?: number
  timeSeated?: string
  server?: string
}

interface ApiTable {
  id: number
  number: number
  capacity: number
  status: Table['status']
  zone: Table['zone']
  shape: Table['shape']
  bgImage: string
  reservation?: {
    guestName: string
    guests: number
    reservedFor: string
  } | null
}

// Filters & State
const activeZone = ref('All')
const searchQuery = ref('')
const selectedTable = ref<Table | null>(null)
const isDetailsModalOpen = ref(false)
const isAddTableModalOpen = ref(false)
const config = useRuntimeConfig()
const tableError = ref('')

// Background image presets for tables/zones
const tableBgPresets = [
  'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=800&auto=format&fit=crop',
  'https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?q=80&w=800&auto=format&fit=crop',
  'https://images.unsplash.com/photo-1544161515-4ab6ce6db874?q=80&w=800&auto=format&fit=crop',
  'https://images.unsplash.com/photo-1559339352-11d035aa65de?q=80&w=800&auto=format&fit=crop'
]

// Floor Plan Tables Data
const tables = ref<Table[]>([
  {
    id: 'T1',
    number: 1,
    capacity: 2,
    zone: 'Main Dining',
    status: 'Available',
    shape: 'round',
    bgImage: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=800&auto=format&fit=crop'
  },
  {
    id: 'T2',
    number: 2,
    capacity: 4,
    zone: 'Main Dining',
    status: 'Occupied',
    shape: 'square',
    currentGuest: 'John Smith',
    guestImage: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150',
    partySize: 3,
    timeSeated: '6:45 PM',
    server: 'Alex M.',
    bgImage: 'https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?q=80&w=800&auto=format&fit=crop'
  },
  {
    id: 'T3',
    number: 3,
    capacity: 4,
    zone: 'Main Dining',
    status: 'Occupied',
    shape: 'square',
    currentGuest: 'Emma Watson',
    guestImage: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150',
    partySize: 4,
    timeSeated: '7:15 PM',
    server: 'Sarah K.',
    bgImage: 'https://images.unsplash.com/photo-1559339352-11d035aa65de?q=80&w=800&auto=format&fit=crop'
  },
  {
    id: 'T4',
    number: 4,
    capacity: 6,
    zone: 'Main Dining',
    status: 'Reserved',
    shape: 'long',
    currentGuest: 'Michael Chen (8:00 PM)',
    guestImage: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150',
    partySize: 5,
    bgImage: 'https://images.unsplash.com/photo-1544161515-4ab6ce6db874?q=80&w=800&auto=format&fit=crop'
  },
  {
    id: 'T5',
    number: 5,
    capacity: 2,
    zone: 'Main Dining',
    status: 'Cleaning',
    shape: 'round',
    bgImage: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=800&auto=format&fit=crop'
  },
  {
    id: 'VIP1',
    number: 101,
    capacity: 8,
    zone: 'VIP Lounge',
    status: 'Reserved',
    shape: 'long',
    currentGuest: 'Ambassador Party (8:30 PM)',
    guestImage: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150',
    partySize: 8,
    bgImage: 'https://images.unsplash.com/photo-1578474846511-04ba529f0b88?q=80&w=800&auto=format&fit=crop'
  },
  {
    id: 'VIP2',
    number: 102,
    capacity: 12,
    zone: 'VIP Lounge',
    status: 'Occupied',
    shape: 'long',
    currentGuest: 'Vance Group',
    guestImage: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150',
    partySize: 10,
    timeSeated: '6:30 PM',
    server: 'David R.',
    bgImage: 'https://images.unsplash.com/photo-1578474846511-04ba529f0b88?q=80&w=800&auto=format&fit=crop'
  },
  {
    id: 'TR1',
    number: 201,
    capacity: 4,
    zone: 'Terrace',
    status: 'Available',
    shape: 'square',
    bgImage: 'https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?q=80&w=800&auto=format&fit=crop'
  },
  {
    id: 'TR2',
    number: 202,
    capacity: 4,
    zone: 'Terrace',
    status: 'Available',
    shape: 'square',
    bgImage: 'https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?q=80&w=800&auto=format&fit=crop'
  },
  {
    id: 'B1',
    number: 301,
    capacity: 2,
    zone: 'Bar',
    status: 'Available',
    shape: 'round',
    bgImage: 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?q=80&w=800&auto=format&fit=crop'
  }
])

// Form state for creating a new table
const newTableForm = ref<Partial<Table>>({
  number: undefined,
  capacity: 4,
  zone: 'Main Dining',
  status: 'Available',
  shape: 'square',
  bgImage: tableBgPresets[0]
})

// Metrics
const totalTables = computed(() => tables.value.length)
const availableCount = computed(() => tables.value.filter(t => t.status === 'Available').length)
const occupiedCount = computed(() => tables.value.filter(t => t.status === 'Occupied').length)
const reservedCount = computed(() => tables.value.filter(t => t.status === 'Reserved').length)

// Filtered List
const filteredTables = computed(() => {
  return tables.value.filter(t => {
    const matchesZone = activeZone.value === 'All' || t.zone === activeZone.value
    const matchesSearch = t.number.toString().includes(searchQuery.value) || 
                          (t.currentGuest && t.currentGuest.toLowerCase().includes(searchQuery.value.toLowerCase()))
    return matchesZone && matchesSearch
  })
})

// Visual Helpers
const getStatusBadge = (status: Table['status']) => {
  switch (status) {
    case 'Available': return 'bg-emerald-600 text-white'
    case 'Occupied': return 'bg-rose-600 text-white'
    case 'Reserved': return 'bg-amber-600 text-white'
    case 'Cleaning': return 'bg-gray-600 text-white'
  }
}

const getStatusBorder = (status: Table['status']) => {
  switch (status) {
    case 'Available': return 'border-emerald-200'
    case 'Occupied': return 'border-rose-200'
    case 'Reserved': return 'border-amber-200'
    case 'Cleaning': return 'border-gray-200'
  }
}

const getOccupancy = (table: Table) => {
  if (!table.partySize) return 0
  return Math.min(Math.round((table.partySize / table.capacity) * 100), 100)
}

const upcomingTables = computed(() => {
  return tables.value.filter((t) => t.currentGuest)
})

const loadReservedTables = async () => {
  const apiTables = await $fetch<ApiTable[]>('/tables', {
    baseURL: config.public.apiBase,
  })

  tables.value = apiTables.map(apiTable => ({
    id: String(apiTable.id),
    number: apiTable.number,
    capacity: apiTable.capacity,
    zone: apiTable.zone,
    shape: apiTable.shape,
    status: apiTable.status,
    bgImage: apiTable.bgImage || tableBgPresets[0] || '',
    currentGuest: apiTable.reservation?.guestName,
    partySize: apiTable.reservation?.guests,
    timeSeated: apiTable.reservation
      ? new Date(apiTable.reservation.reservedFor).toLocaleTimeString([], {
          hour: 'numeric',
          minute: '2-digit',
        })
      : undefined,
  }))
}

onMounted(() => {
  loadReservedTables().catch(() => {
    // Keep the floor plan visible if the table service is unavailable.
  })
})

// Handlers
const openTableDetails = (table: Table) => {
  selectedTable.value = { ...table }
  isDetailsModalOpen.value = true
}

const updateTableStatus = async (newStatus: Table['status']) => {
  if (!selectedTable.value) return
  try {
    await $fetch(`/tables/${selectedTable.value.id}`, {
      baseURL: config.public.apiBase,
      method: 'PATCH',
      body: { status: newStatus },
    })
    await loadReservedTables()
    isDetailsModalOpen.value = false
  } catch (error: any) {
    tableError.value = error?.data?.message || 'Could not update table.'
  }
}

const handleCreateTable = async () => {
  if (!newTableForm.value.number) return
  tableError.value = ''
  try {
    await $fetch('/tables', {
      baseURL: config.public.apiBase,
      method: 'POST',
      body: {
        number: newTableForm.value.number,
        capacity: newTableForm.value.capacity || 4,
        zone: newTableForm.value.zone || 'Main Dining',
        status: (newTableForm.value.status || 'Available').toLowerCase(),
        shape: newTableForm.value.shape || 'square',
        bgImage: newTableForm.value.bgImage || '',
      },
    })
    await loadReservedTables()
    isAddTableModalOpen.value = false
  } catch (error: any) {
    tableError.value = error?.data?.message || 'Could not save table.'
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-100 text-gray-800 font-sans">
    <AdminSidebar />

    <main class="lg:ml-64 transition-all duration-300">
      
      <!-- Sticky Top Navigation / Header -->
      <header class="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-gray-200 bg-white px-6 shadow-sm lg:px-8">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 tracking-wide">Floor Plan & Live Seating</h1>
          <p class="text-xs text-gray-500">Interactive visual floor layout and table reservation hub</p>
        </div>

        <div class="flex items-center gap-3">
          <div class="relative hidden sm:block">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Search Table # or Guest..." 
              class="w-60 rounded-lg border border-gray-300 bg-gray-50 px-4 py-2 pl-9 text-xs text-gray-800 placeholder-gray-400 focus:border-amber-500 focus:bg-white focus:outline-none transition-all"
            />
            <span class="absolute left-3 top-2.5 text-xs text-gray-400">🔍</span>
          </div>

          <button 
            @click="isAddTableModalOpen = true"
            class="px-4 py-2 rounded-lg bg-amber-600 hover:bg-amber-700 text-white text-xs font-semibold uppercase tracking-wider transition-all shadow flex items-center gap-1.5"
          >
            <span>+</span> Add Table
          </button>
        </div>
      </header>

      <div class="p-6 lg:p-8 space-y-6">

        <!-- Live Status Metric Counters -->
        <section class="grid md:grid-cols-2 lg:grid-cols-4 gap-5">
          <div class="bg-white p-5 rounded-lg border border-gray-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-gray-500">Total Seating Capacity</span>
              <p class="text-2xl font-bold text-gray-900 mt-1">{{ totalTables }} Tables</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-gray-100 text-gray-600 text-lg">🍽️</div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-gray-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-emerald-600">Available Now</span>
              <p class="text-2xl font-bold text-emerald-600 mt-1">{{ availableCount }}</p>
            </div>
            <span class="h-3 w-3 rounded-full bg-emerald-500 shadow-sm"></span>
          </div>

          <div class="bg-white p-5 rounded-lg border border-gray-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-rose-600">Occupied</span>
              <p class="text-2xl font-bold text-rose-600 mt-1">{{ occupiedCount }}</p>
            </div>
            <span class="h-3 w-3 rounded-full bg-rose-500 shadow-sm"></span>
          </div>

          <div class="bg-white p-5 rounded-lg border border-gray-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-amber-600">Reserved</span>
              <p class="text-2xl font-bold text-amber-600 mt-1">{{ reservedCount }}</p>
            </div>
            <span class="h-3 w-3 rounded-full bg-amber-500 shadow-sm"></span>
          </div>
        </section>

        <!-- Floor Plan Filter Bar & Legend -->
        <section class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
          <!-- Zone Filter Tabs -->
          <div class="flex items-center gap-2 overflow-x-auto w-full md:w-auto no-scrollbar">
            <button 
              v-for="zone in ['All', 'Main Dining', 'VIP Lounge', 'Terrace', 'Bar']" 
              :key="zone"
              @click="activeZone = zone"
              :class="[
                'px-4 py-2 rounded-lg text-xs font-semibold whitespace-nowrap transition-all border',
                activeZone === zone 
                  ? 'bg-amber-600 border-amber-600 text-white shadow-sm' 
                  : 'bg-gray-50 border-gray-200 text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              ]"
            >
              {{ zone }}
            </button>
          </div>

          <!-- Status Legend -->
          <div class="flex items-center gap-4 text-xs text-gray-600 font-medium">
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Available</span>
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span> Occupied</span>
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span> Reserved</span>
            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-gray-500"></span> Cleaning</span>
          </div>
        </section>

        <!-- Visual Table Cards Grid -->
        <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div 
            v-for="table in filteredTables" 
            :key="table.id"
            @click="openTableDetails(table)"
            :class="[
              'relative overflow-hidden rounded-lg border-2 bg-white cursor-pointer shadow-sm',
              getStatusBorder(table.status)
            ]"
          >
            <!-- Visual Table Backdrop -->
            <div class="relative h-48 w-full overflow-hidden">
              <img 
                :src="table.bgImage" 
                :alt="`Table ${table.number} Background`"
                class="h-full w-full object-cover" 
              />
              <div class="absolute inset-0 bg-linear-to-t from-gray-900/90 via-gray-900/40 to-transparent"></div>

              <!-- Top Badges -->
              <div class="absolute top-3 left-3 right-3 flex items-center justify-between">
                <span class="px-2.5 py-1 rounded bg-white/90 backdrop-blur-md text-[10px] font-bold uppercase tracking-wider text-gray-800 shadow-sm">
                  {{ table.zone }}
                </span>
                <span :class="getStatusBadge(table.status)" class="px-2.5 py-1 rounded text-[10px] font-bold uppercase tracking-wider shadow-sm">
                  {{ table.status }}
                </span>
              </div>

              <!-- Visual Seating Graphic -->
              <div class="absolute inset-0 flex items-center justify-center pt-2">
                <div class="relative flex items-center justify-center">
                  
                  <!-- Circular Table Graphic -->
                  <div 
                    v-if="table.shape === 'round'"
                    class="h-16 w-16 rounded-full border-2 border-white/40 bg-gray-900/80 backdrop-blur-md flex items-center justify-center font-serif text-xl font-bold text-amber-400 shadow-md"
                  >
                    T{{ table.number }}
                  </div>

                  <!-- Square Table Graphic -->
                  <div 
                    v-else-if="table.shape === 'square'"
                    class="h-16 w-16 rounded-lg border-2 border-white/40 bg-gray-900/80 backdrop-blur-md flex items-center justify-center font-serif text-xl font-bold text-amber-400 shadow-md"
                  >
                    T{{ table.number }}
                  </div>

                  <!-- Long Dining Table Graphic -->
                  <div 
                    v-else
                    class="h-14 w-28 rounded-lg border-2 border-white/40 bg-gray-900/80 backdrop-blur-md flex items-center justify-center font-serif text-xl font-bold text-amber-400 shadow-md"
                  >
                    T{{ table.number }}
                  </div>

                  <!-- Seats indicator dots -->
                  <div class="absolute -inset-3 flex items-center justify-between pointer-events-none">
                    <span class="h-2.5 w-2.5 rounded-full bg-white/80 border border-gray-800 shadow-sm"></span>
                    <span class="h-2.5 w-2.5 rounded-full bg-white/80 border border-gray-800 shadow-sm"></span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Table Guest Details -->
            <div class="p-4 space-y-3 bg-white">
              <div class="min-h-12">
                <div v-if="table.currentGuest" class="flex items-start justify-between gap-2">
                  <div class="flex min-w-0 items-center gap-2">
                    <img
                      v-if="table.guestImage"
                      :src="table.guestImage"
                      :alt="table.currentGuest"
                      class="h-9 w-9 shrink-0 rounded-full object-cover border border-gray-200"
                    />
                    <div class="min-w-0">
                    <p class="text-sm font-bold text-gray-900 truncate">{{ table.currentGuest }}</p>
                    <p class="text-[11px] text-gray-500 mt-0.5">
                      {{ table.timeSeated ? `Seated at ${table.timeSeated}` : 'Upcoming Reservation' }}
                    </p>
                    </div>
                  </div>
                  <span class="px-2 py-0.5 rounded bg-gray-100 text-gray-700 font-bold text-[10px] shrink-0 border border-gray-200">
                    {{ table.partySize }}/{{ table.capacity }} Guests
                  </span>
                </div>
                <div v-else class="flex items-center justify-between py-1">
                  <span class="text-xs font-semibold text-gray-500">Ready for Walk-ins</span>
                  <span class="text-[10px] font-bold text-emerald-600 uppercase tracking-wider">Open</span>
                </div>
              </div>

              <!-- Occupancy Bar -->
              <div class="space-y-1">
                <div class="flex justify-between text-[10px] font-bold uppercase tracking-wider text-gray-500">
                  <span>Capacity</span>
                  <span>{{ table.capacity }} Seats</span>
                </div>
                <div class="h-1.5 w-full bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    class="h-full bg-amber-500 rounded-full" 
                    :style="{ width: `${getOccupancy(table)}%` }"
                  ></div>
                </div>
              </div>

              <div class="pt-3 border-t border-gray-100 flex items-center justify-between text-xs text-gray-500">
                <span>{{ table.server ? `Server: ${table.server}` : 'Unassigned' }}</span>
                <span class="text-amber-600 font-semibold">
                  Manage &rarr;
                </span>
              </div>
            </div>

          </div>
        </section>

        <!-- Upcoming Reservations List -->
        <section class="bg-white border border-stone-200 rounded-lg shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs text-stone-700">
              <thead>
                <tr class="bg-stone-50 border-b border-stone-200 text-[10px] font-bold uppercase tracking-wider text-stone-400">
                  <th scope="col" class="py-3.5 px-4">Table</th>
                  <th scope="col" class="py-3.5 px-4">Guest</th>
                  <th scope="col" class="py-3.5 px-4">Party</th>
                  <th scope="col" class="py-3.5 px-4">Reserved For</th>
                  <th scope="col" class="py-3.5 px-4">Status</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-stone-100">
                <tr
                  v-for="table in upcomingTables"
                  :key="table.id"
                  class="hover:bg-stone-50/80 transition-colors"
                >
                  <td class="py-3.5 px-4 font-bold">Table {{ table.number }}</td>
                  <td class="py-3.5 px-4">{{ table.currentGuest }}</td>
                  <td class="py-3.5 px-4">{{ table.partySize }}/{{ table.capacity }} Guests</td>
                  <td class="py-3.5 px-4">{{ table.timeSeated || '—' }}</td>
                  <td class="py-3.5 px-4">
                    <span class="px-2 py-0.5 rounded bg-amber-100 text-amber-700 font-bold text-[10px] uppercase">{{ table.status }}</span>
                  </td>
                </tr>
                <tr v-if="upcomingTables.length === 0">
                  <td colspan="5" class="py-8 text-center text-stone-400">No upcoming reservations.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

      </div>
    </main>

    <!-- Modal 1: Table Management Details -->
    <div v-if="isDetailsModalOpen && selectedTable" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div class="bg-white border border-gray-200 rounded-lg max-w-md w-full p-6 shadow-xl space-y-6 text-gray-800">
        
        <div class="flex items-center justify-between border-b border-gray-200 pb-4">
          <div>
            <span class="text-[10px] uppercase font-bold tracking-widest text-amber-600">{{ selectedTable.zone }}</span>
            <h3 class="text-2xl font-bold text-gray-900">Table {{ selectedTable.number }} Status</h3>
          </div>
          <button @click="isDetailsModalOpen = false" class="text-gray-400 hover:text-gray-600 text-lg">✕</button>
        </div>

        <div class="space-y-4 text-xs">
          <div class="grid grid-cols-2 gap-3 bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div>
              <span class="text-gray-500 block">Total Capacity</span>
              <span class="font-bold text-gray-800 text-sm">{{ selectedTable.capacity }} Persons</span>
            </div>
            <div>
              <span class="text-gray-500 block">Current Status</span>
              <span :class="getStatusBadge(selectedTable.status)" class="px-2 py-0.5 rounded font-bold inline-block mt-1">
                {{ selectedTable.status }}
              </span>
            </div>
          </div>

          <div v-if="selectedTable.currentGuest" class="space-y-2">
            <h4 class="font-bold text-gray-900">Guest Information</h4>
            <div class="space-y-1.5 text-gray-700 bg-gray-50 p-3.5 rounded-lg border border-gray-200">
              <img
                v-if="selectedTable.guestImage"
                :src="selectedTable.guestImage"
                :alt="selectedTable.currentGuest"
                class="h-14 w-14 rounded-full object-cover border border-gray-200"
              />
              <p><strong>Name:</strong> {{ selectedTable.currentGuest }}</p>
              <p><strong>Party Size:</strong> {{ selectedTable.partySize }} Guests</p>
              <p v-if="selectedTable.server"><strong>Server:</strong> {{ selectedTable.server }}</p>
            </div>
          </div>

          <div class="space-y-2 pt-2">
            <label class="font-bold text-gray-900 block">Quick Action Update</label>
            <div class="grid grid-cols-2 gap-2">
              <button 
                @click="updateTableStatus('Available')"
                class="py-2.5 rounded-lg border border-emerald-300 bg-emerald-50 text-emerald-700 font-bold hover:bg-emerald-100 transition-colors"
              >
                Mark Available
              </button>
              <button 
                @click="updateTableStatus('Occupied')"
                class="py-2.5 rounded-lg border border-rose-300 bg-rose-50 text-rose-700 font-bold hover:bg-rose-100 transition-colors"
              >
                Seat Guests
              </button>
              <button 
                @click="updateTableStatus('Reserved')"
                class="py-2.5 rounded-lg border border-amber-300 bg-amber-50 text-amber-700 font-bold hover:bg-amber-100 transition-colors"
              >
                Reserve Table
              </button>
              <button 
                @click="updateTableStatus('Cleaning')"
                class="py-2.5 rounded-lg border border-gray-300 bg-gray-100 text-gray-700 font-bold hover:bg-gray-200 transition-colors"
              >
                Set Cleaning
              </button>
            </div>
          </div>
        </div>

        <div class="pt-4 border-t border-gray-200 flex justify-end">
          <button @click="isDetailsModalOpen = false" class="px-5 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold text-xs rounded-lg">
            Close
          </button>
        </div>

      </div>
    </div>

    <!-- Modal 2: Add New Table -->
    <div v-if="isAddTableModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div class="bg-white border border-gray-200 rounded-lg max-w-md w-full p-6 shadow-xl space-y-5 text-gray-800">
        
        <div class="flex items-center justify-between border-b border-gray-200 pb-4">
          <div>
            <span class="text-[10px] uppercase font-bold tracking-widest text-amber-600">Floor Layout Editor</span>
            <h3 class="text-2xl font-bold text-gray-900">Add New Table</h3>
          </div>
          <button @click="isAddTableModalOpen = false" class="text-gray-400 hover:text-gray-600 text-lg">✕</button>
        </div>

        <form @submit.prevent="handleCreateTable" class="space-y-4 text-xs">
          
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="font-bold text-gray-700 block mb-1">Table Number #</label>
              <input 
                v-model.number="newTableForm.number" 
                type="number" 
                placeholder="e.g. 12"
                required
                class="w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-800 focus:border-amber-500 focus:bg-white focus:outline-none"
              />
            </div>
            <div>
              <label class="font-bold text-gray-700 block mb-1">Capacity (Seats)</label>
              <input 
                v-model.number="newTableForm.capacity" 
                type="number" 
                min="1"
                required
                class="w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-800 focus:border-amber-500 focus:bg-white focus:outline-none"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="font-bold text-gray-700 block mb-1">Floor Zone</label>
              <select 
                v-model="newTableForm.zone" 
                class="w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-800 focus:border-amber-500 focus:bg-white focus:outline-none"
              >
                <option>Main Dining</option>
                <option>VIP Lounge</option>
                <option>Terrace</option>
                <option>Bar</option>
              </select>
            </div>
            <div>
              <label class="font-bold text-gray-700 block mb-1">Table Shape</label>
              <select 
                v-model="newTableForm.shape" 
                class="w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-800 focus:border-amber-500 focus:bg-white focus:outline-none"
              >
                <option value="round">Round Table</option>
                <option value="square">Square Table</option>
                <option value="long">Long Banquet Table</option>
              </select>
            </div>
          </div>

          <div>
            <label class="font-bold text-gray-700 block mb-1">Select Card Background Image</label>
            <div class="grid grid-cols-4 gap-2">
              <img 
                v-for="(img, idx) in tableBgPresets" 
                :key="idx"
                :src="img"
                @click="newTableForm.bgImage = img"
                :class="[
                  'h-14 w-full rounded-lg object-cover cursor-pointer border-2 transition-all',
                  newTableForm.bgImage === img ? 'border-amber-600 ring-2 ring-amber-300' : 'border-gray-200 opacity-70'
                ]"
              />
            </div>
          </div>

          <div class="pt-4 border-t border-gray-200 flex items-center justify-end gap-3">
            <button 
              type="button" 
              @click="isAddTableModalOpen = false" 
              class="px-5 py-2.5 rounded-lg border border-gray-300 text-gray-700 font-semibold hover:bg-gray-100 transition-colors"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              class="px-5 py-2.5 rounded-lg bg-amber-600 hover:bg-amber-700 text-white font-semibold transition-colors shadow"
            >
              Create Table
            </button>
          </div>

        </form>

      </div>
    </div>

  </div>
</template>