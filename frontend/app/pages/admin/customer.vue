<script setup lang="ts">
import { ref, computed } from 'vue'

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
}

// Available Tiers & Statuses
const tiers = ['Regular', 'Silver VIP', 'Gold VIP', 'Platinum VIP'] as const
const statuses = ['Active', 'Blocked'] as const

// Search & Filter State
const searchQuery = ref('')
const selectedTierFilter = ref('All')
const selectedStatusFilter = ref('All')

// Modal / Drawer Form State
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingCustomer = ref<Customer>({
  id: '',
  name: '',
  email: '',
  phone: '',
  avatar: '',
  tier: 'Regular',
  totalOrders: 0,
  totalSpent: 0,
  lastVisit: 'Today',
  status: 'Active'
})

// Customer Dataset
const customers = ref<Customer[]>([
  {
    id: 'CUST-801',
    name: 'Sophia Laurent',
    email: 'sophia.l@example.com',
    phone: '+1 (555) 234-5678',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150',
    tier: 'Platinum VIP',
    totalOrders: 42,
    totalSpent: 1850.50,
    lastVisit: '2 hours ago',
    status: 'Active'
  },
  {
    id: 'CUST-802',
    name: 'Alexander Wright',
    email: 'a.wright@example.com',
    phone: '+1 (555) 876-5432',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150',
    tier: 'Gold VIP',
    totalOrders: 28,
    totalSpent: 940.00,
    lastVisit: 'Yesterday',
    status: 'Active'
  },
  {
    id: 'CUST-803',
    name: 'Emily Watson',
    email: 'emily.w@example.com',
    phone: '+1 (555) 456-7890',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150',
    tier: 'Silver VIP',
    totalOrders: 14,
    totalSpent: 420.75,
    lastVisit: '3 days ago',
    status: 'Active'
  },
  {
    id: 'CUST-804',
    name: 'Michael Chang',
    email: 'm.chang@example.com',
    phone: '+1 (555) 321-6549',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150',
    tier: 'Regular',
    totalOrders: 5,
    totalSpent: 135.20,
    lastVisit: '1 week ago',
    status: 'Active'
  },
  {
    id: 'CUST-805',
    name: 'Jessica Taylor',
    email: 'j.taylor@example.com',
    phone: '+1 (555) 987-1234',
    avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150',
    tier: 'Gold VIP',
    totalOrders: 22,
    totalSpent: 810.00,
    lastVisit: '2 weeks ago',
    status: 'Blocked'
  }
])

// Computed Metrics
const totalCustomersCount = computed(() => customers.value.length)
const totalVIPsCount = computed(() => customers.value.filter(c => c.tier !== 'Regular').length)
const totalLifetimeRevenue = computed(() => 
  customers.value.reduce((sum, c) => sum + c.totalSpent, 0)
)
const averageSpentPerCustomer = computed(() => 
  totalCustomersCount.value ? (totalLifetimeRevenue.value / totalCustomersCount.value) : 0
)

// Filtered List
const filteredCustomers = computed(() => {
  return customers.value.filter(c => {
    const matchesSearch = c.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          c.email.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          c.phone.includes(searchQuery.value)
    const matchesTier = selectedTierFilter.value === 'All' || c.tier === selectedTierFilter.value
    const matchesStatus = selectedStatusFilter.value === 'All' || c.status === selectedStatusFilter.value

    return matchesSearch && matchesTier && matchesStatus
  })
})

// Quick Actions
const openAddModal = () => {
  isEditing.value = false
  editingCustomer.value = {
    id: `CUST-${Math.floor(800 + Math.random() * 200)}`,
    name: '',
    email: '',
    phone: '',
    avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150',
    tier: 'Regular',
    totalOrders: 0,
    totalSpent: 0.00,
    lastVisit: 'Just now',
    status: 'Active'
  }
  isModalOpen.value = true
}

const openEditModal = (cust: Customer) => {
  isEditing.value = true
  editingCustomer.value = { ...cust }
  isModalOpen.value = true
}

const toggleStatus = (cust: Customer) => {
  cust.status = cust.status === 'Active' ? 'Blocked' : 'Active'
}

const saveCustomer = () => {
  if (!editingCustomer.value.name.trim() || !editingCustomer.value.email.trim()) return

  if (isEditing.value) {
    const idx = customers.value.findIndex(c => c.id === editingCustomer.value.id)
    if (idx !== -1) customers.value[idx] = { ...editingCustomer.value }
  } else {
    customers.value.push({ ...editingCustomer.value })
  }
  isModalOpen.value = false
}

const deleteCustomer = (id: string) => {
  if (confirm('Are you sure you want to remove this customer record?')) {
    customers.value = customers.value.filter(c => c.id !== id)
  }
}

// Tier Styling Helper
const getTierBadgeClass = (tier: Customer['tier']) => {
  switch (tier) {
    case 'Platinum VIP': return 'bg-slate-900 text-amber-300 border-slate-700'
    case 'Gold VIP': return 'bg-amber-50 text-amber-800 border-amber-300'
    case 'Silver VIP': return 'bg-stone-100 text-stone-700 border-stone-300'
    default: return 'bg-stone-50 text-stone-500 border-stone-200'
  }
}
</script>

<template>
  <div class="min-h-screen bg-stone-100 text-stone-800 font-sans selection:bg-amber-100">
    <AdminSidebar />

    <main class="lg:ml-64 transition-all duration-300">
      
      <!-- Sticky Header -->
      <header class="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-stone-200 bg-white/90 px-6 backdrop-blur-md lg:px-8">
        <div>
          <h1 class="text-2xl font-bold text-stone-900 tracking-tight">Customer Management</h1>
          <p class="text-xs text-stone-500 font-normal">View guest history, order statistics, loyalty tiers, and status</p>
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
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
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
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
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
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
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
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
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

          <span class="text-xs text-stone-400 font-normal">Click status badge to toggle active/blocked</span>
        </section>

        <!-- Customer Data Table -->
        <section class="bg-white border border-stone-200 rounded-lg shadow-sm overflow-hidden">
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
                        :src="cust.avatar" 
                        :alt="cust.name" 
                        class="h-9 w-9 rounded-full object-cover border border-stone-200 shrink-0"
                      />
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
                      <p class="text-[11px] text-stone-400 font-mono">{{ cust.phone }}</p>
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
                        @click="openEditModal(cust)"
                        class="p-1.5 rounded-md text-stone-400 hover:text-amber-600 hover:bg-stone-100 transition-colors"
                        title="Edit Profile"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                      </button>

                      <button 
                        @click="deleteCustomer(cust.id)"
                        class="p-1.5 rounded-md text-stone-400 hover:text-rose-600 hover:bg-stone-100 transition-colors"
                        title="Delete Profile"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>

                <!-- Empty State -->
                <tr v-if="filteredCustomers.length === 0">
                  <td colspan="8" class="py-12 text-center text-stone-400 font-normal">
                    No customers found matching search filters.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

      </div>
    </main>

    <!-- Create / Edit Customer Modal -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4">
      <div class="bg-white border border-stone-200 rounded-lg max-w-lg w-full p-6 shadow-xl space-y-5 text-stone-800">
        
        <div class="flex items-center justify-between border-b border-stone-200 pb-4">
          <div>
            <span class="text-[10px] uppercase font-bold tracking-widest text-amber-600">Guest Database</span>
            <h3 class="text-xl font-bold text-stone-900">
              {{ isEditing ? 'Edit Customer Profile' : 'Add New Guest' }}
            </h3>
          </div>
          <button @click="isModalOpen = false" class="text-stone-400 hover:text-stone-700 text-base">✕</button>
        </div>

        <form @submit.prevent="saveCustomer" class="space-y-4 text-xs">
          
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