<script setup lang="ts">
import { ref, computed } from 'vue'

interface OrderItem {
  name: string
  quantity: number
  price: number
  notes?: string
}

interface Order {
  id: string
  customerName: string
  orderType: 'Dine-In' | 'Takeout' | 'Delivery'
  tableNumber?: string
  station: 'Kitchen Grill' | 'Pizza Oven' | 'Bar & Drinks' | 'Pastry & Cold' | 'Main Line'
  items: OrderItem[]
  totalAmount: number
  status: 'Pending' | 'Preparing' | 'Ready' | 'Delivered' | 'Cancelled'
  createdAt: string
}

// Filter States
const searchQuery = ref('')
const selectedStatusFilter = ref('All')
const selectedTypeFilter = ref('All')

// Modal & Form State
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingOrder = ref<Order>({
  id: '',
  customerName: '',
  orderType: 'Dine-In',
  tableNumber: 'Table 1',
  station: 'Main Line',
  items: [{ name: '', quantity: 1, price: 0 }],
  totalAmount: 0,
  status: 'Pending',
  createdAt: 'Just now'
})

// Orders Reactive Dataset
const orders = ref<Order[]>([
  {
    id: 'ORD-9001',
    customerName: 'Sophia Laurent',
    orderType: 'Dine-In',
    tableNumber: 'Table 04',
    station: 'Pizza Oven',
    items: [
      { name: 'Margherita Woodfired Pizza', quantity: 2, price: 18.50 },
      { name: 'Aperol Spritz', quantity: 2, price: 12.00 }
    ],
    totalAmount: 61.00,
    status: 'Preparing',
    createdAt: '5 mins ago'
  },
  {
    id: 'ORD-9002',
    customerName: 'Marcus Vance',
    orderType: 'Takeout',
    station: 'Kitchen Grill',
    items: [
      { name: 'Prime Angus Ribeye Steak', quantity: 1, price: 42.00 },
      { name: 'Truffle Parmesan Fries', quantity: 1, price: 9.50 }
    ],
    totalAmount: 51.50,
    status: 'Pending',
    createdAt: '12 mins ago'
  },
  {
    id: 'ORD-9003',
    customerName: 'David Chen',
    orderType: 'Dine-In',
    tableNumber: 'Table 12',
    station: 'Bar & Drinks',
    items: [
      { name: 'Smoked Old Fashioned', quantity: 3, price: 15.00 },
      { name: 'Artisan Cheese Board', quantity: 1, price: 24.00 }
    ],
    totalAmount: 69.00,
    status: 'Ready',
    createdAt: '25 mins ago'
  },
  {
    id: 'ORD-9004',
    customerName: 'Emily Watson',
    orderType: 'Delivery',
    station: 'Pastry & Cold',
    items: [
      { name: 'House-made Tiramisu', quantity: 2, price: 8.50 },
      { name: 'Iced Vanilla Latte', quantity: 2, price: 5.50 }
    ],
    totalAmount: 28.00,
    status: 'Delivered',
    createdAt: '1 hour ago'
  },
  {
    id: 'ORD-9005',
    customerName: 'Alexander Wright',
    orderType: 'Dine-In',
    tableNumber: 'Table 02',
    station: 'Kitchen Grill',
    items: [
      { name: 'Gourmet Wagyu Burger', quantity: 1, price: 22.00 }
    ],
    totalAmount: 22.00,
    status: 'Cancelled',
    createdAt: '2 hours ago'
  }
])

// Metrics Computations
const totalOrdersCount = computed(() => orders.value.length)
const pendingCount = computed(() => orders.value.filter(o => o.status === 'Pending').length)
const preparingCount = computed(() => orders.value.filter(o => o.status === 'Preparing').length)
const totalSalesVolume = computed(() => 
  orders.value
    .filter(o => o.status !== 'Cancelled')
    .reduce((sum, o) => sum + o.totalAmount, 0)
)

// Computed Filtered List
const filteredOrders = computed(() => {
  return orders.value.filter(order => {
    const matchesSearch = order.id.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          order.customerName.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          (order.tableNumber && order.tableNumber.toLowerCase().includes(searchQuery.value.toLowerCase()))
    const matchesStatus = selectedStatusFilter.value === 'All' || order.status === selectedStatusFilter.value
    const matchesType = selectedTypeFilter.value === 'All' || order.orderType === selectedTypeFilter.value

    return matchesSearch && matchesStatus && matchesType
  })
})

// Quick Actions & Status Cycling
const cycleStatus = (order: Order) => {
  const statusFlow: Order['status'][] = ['Pending', 'Preparing', 'Ready', 'Delivered', 'Cancelled']
  const currentIndex = statusFlow.indexOf(order.status)
  order.status = statusFlow[(currentIndex + 1) % statusFlow.length]
}

const openAddModal = () => {
  isEditing.value = false
  editingOrder.value = {
    id: `ORD-${Math.floor(9000 + Math.random() * 1000)}`,
    customerName: '',
    orderType: 'Dine-In',
    tableNumber: 'Table 1',
    station: 'Main Line',
    items: [{ name: '', quantity: 1, price: 0 }],
    totalAmount: 0,
    status: 'Pending',
    createdAt: 'Just now'
  }
  isModalOpen.value = true
}

const openEditModal = (order: Order) => {
  isEditing.value = true
  editingOrder.value = JSON.parse(JSON.stringify(order))
  isModalOpen.value = true
}

const addItemToOrder = () => {
  editingOrder.value.items.push({ name: '', quantity: 1, price: 0 })
}

const removeItemFromOrder = (index: number) => {
  if (editingOrder.value.items.length > 1) {
    editingOrder.value.items.splice(index, 1)
  }
}

const saveOrder = () => {
  if (!editingOrder.value.customerName.trim()) return

  // Recalculate Total
  editingOrder.value.totalAmount = editingOrder.value.items.reduce((sum, item) => sum + (item.price * item.quantity), 0)

  if (isEditing.value) {
    const idx = orders.value.findIndex(o => o.id === editingOrder.value.id)
    if (idx !== -1) orders.value[idx] = { ...editingOrder.value }
  } else {
    orders.value.unshift({ ...editingOrder.value })
  }
  isModalOpen.value = false
}

const deleteOrder = (id: string) => {
  if (confirm('Are you sure you want to cancel and remove this ticket?')) {
    orders.value = orders.value.filter(o => o.id !== id)
  }
}

// Dynamic Style Badges
const getStatusBadgeClass = (status: Order['status']) => {
  switch (status) {
    case 'Pending': return 'bg-amber-50 text-amber-700 border-amber-300'
    case 'Preparing': return 'bg-blue-50 text-blue-700 border-blue-300'
    case 'Ready': return 'bg-emerald-50 text-emerald-700 border-emerald-300'
    case 'Delivered': return 'bg-stone-100 text-stone-600 border-stone-300'
    case 'Cancelled': return 'bg-rose-50 text-rose-700 border-rose-300'
  }
}

const getTypeBadgeClass = (type: Order['orderType']) => {
  switch (type) {
    case 'Dine-In': return 'bg-purple-50 text-purple-700 border-purple-200'
    case 'Takeout': return 'bg-sky-50 text-sky-700 border-sky-200'
    case 'Delivery': return 'bg-indigo-50 text-indigo-700 border-indigo-200'
  }
}
</script>

<template>
  <div class="min-h-screen bg-stone-100 text-stone-800 font-sans selection:bg-amber-100">
    <AdminSidebar />

    <main class="lg:ml-64 transition-all duration-300">
      
      <!-- Top Header -->
      <header class="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-stone-200 bg-white/90 px-6 backdrop-blur-md lg:px-8">
        <div>
          <h1 class="text-2xl font-bold text-stone-900 tracking-tight">Order Tickets & KDS</h1>
          <p class="text-xs text-stone-500 font-normal">Monitor incoming kitchen tickets, table fulfillment, and order states</p>
        </div>

        <div class="flex items-center gap-3">
          <div class="relative hidden sm:block">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Search Ticket #, Guest, Table..." 
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
            Create Order Ticket
          </button>
        </div>
      </header>

      <div class="p-6 lg:p-8 space-y-6">

        <!-- Top Metrics Overview -->
        <section class="grid grid-cols-1 sm:grid-cols-4 gap-5">
          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-stone-400">Total Active Tickets</span>
              <p class="text-2xl font-bold text-stone-900 mt-1">{{ totalOrdersCount }} Tickets</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-50 text-amber-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-amber-600">Kitchen Preparing</span>
              <p class="text-2xl font-bold text-amber-700 mt-1">{{ preparingCount }} In Progress</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-50 text-amber-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-blue-600">Pending Approval</span>
              <p class="text-2xl font-bold text-blue-700 mt-1">{{ pendingCount }} Queued</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-50 text-blue-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-emerald-600">Total Order Sales</span>
              <p class="text-2xl font-bold text-emerald-700 mt-1">${{ totalSalesVolume.toFixed(2) }}</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
          </div>
        </section>

        <!-- Filter Bar -->
        <section class="bg-white p-4 rounded-lg border border-stone-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
          <div class="flex items-center gap-4 w-full md:w-auto">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-stone-400 uppercase tracking-wider">Status:</span>
              <select 
                v-model="selectedStatusFilter"
                class="rounded-md border border-stone-300 bg-stone-50 px-3 py-1.5 text-xs text-stone-800 focus:border-amber-600 focus:outline-none"
              >
                <option value="All">All Statuses</option>
                <option value="Pending">Pending</option>
                <option value="Preparing">Preparing</option>
                <option value="Ready">Ready</option>
                <option value="Delivered">Delivered</option>
                <option value="Cancelled">Cancelled</option>
              </select>
            </div>

            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-stone-400 uppercase tracking-wider">Type:</span>
              <select 
                v-model="selectedTypeFilter"
                class="rounded-md border border-stone-300 bg-stone-50 px-3 py-1.5 text-xs text-stone-800 focus:border-amber-600 focus:outline-none"
              >
                <option value="All">All Types</option>
                <option value="Dine-In">Dine-In</option>
                <option value="Takeout">Takeout</option>
                <option value="Delivery">Delivery</option>
              </select>
            </div>
          </div>

          <span class="text-xs text-stone-400 font-normal">Click status badge to advance ticket state</span>
        </section>

        <!-- Orders Table -->
        <section class="bg-white border border-stone-200 rounded-lg shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs text-stone-700">
              <thead>
                <tr class="bg-stone-50 border-b border-stone-200 text-[10px] font-bold uppercase tracking-wider text-stone-400">
                  <th scope="col" class="py-3.5 px-4">Ticket / Guest</th>
                  <th scope="col" class="py-3.5 px-4">Type & Location</th>
                  <th scope="col" class="py-3.5 px-4">Station</th>
                  <th scope="col" class="py-3.5 px-4">Ordered Items Summary</th>
                  <th scope="col" class="py-3.5 px-4 text-right">Total</th>
                  <th scope="col" class="py-3.5 px-4 text-center">Status</th>
                  <th scope="col" class="py-3.5 px-4 text-right pr-6">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-stone-100">
                <tr 
                  v-for="order in filteredOrders" 
                  :key="order.id" 
                  class="hover:bg-stone-50/80 transition-colors group"
                >
                  <!-- ID & Guest -->
                  <td class="py-3.5 px-4">
                    <div>
                      <span class="font-bold text-stone-900 text-sm font-mono block">{{ order.id }}</span>
                      <span class="text-stone-600 font-semibold">{{ order.customerName }}</span>
                      <span class="text-[10px] text-stone-400 block">{{ order.createdAt }}</span>
                    </div>
                  </td>

                  <!-- Type & Location -->
                  <td class="py-3.5 px-4 whitespace-nowrap">
                    <div class="space-y-1">
                      <span 
                        :class="getTypeBadgeClass(order.orderType)"
                        class="px-2 py-0.5 rounded border text-[10px] font-bold tracking-wide block w-max"
                      >
                        {{ order.orderType }}
                      </span>
                      <span v-if="order.tableNumber" class="text-stone-500 font-mono text-[11px] block">
                        {{ order.tableNumber }}
                      </span>
                    </div>
                  </td>

                  <!-- Station -->
                  <td class="py-3.5 px-4 whitespace-nowrap font-semibold text-stone-800">
                    {{ order.station }}
                  </td>

                  <!-- Items Summary -->
                  <td class="py-3.5 px-4">
                    <div class="space-y-0.5 max-w-xs">
                      <p 
                        v-for="(item, idx) in order.items" 
                        :key="idx"
                        class="text-stone-700 font-medium text-[11px]"
                      >
                        <span class="font-bold text-amber-700">{{ item.quantity }}x</span> {{ item.name }}
                      </p>
                    </div>
                  </td>

                  <!-- Total -->
                  <td class="py-3.5 px-4 text-right font-bold text-stone-900 text-sm whitespace-nowrap">
                    ${{ order.totalAmount.toFixed(2) }}
                  </td>

                  <!-- Status (Interactive) -->
                  <td class="py-3.5 px-4 text-center whitespace-nowrap">
                    <button 
                      @click="cycleStatus(order)"
                      :class="getStatusBadgeClass(order.status)"
                      class="px-2.5 py-1 rounded text-[10px] font-bold border transition-all cursor-pointer hover:opacity-80"
                    >
                      {{ order.status }}
                    </button>
                  </td>

                  <!-- Actions -->
                  <td class="py-3.5 px-4 text-right pr-6 whitespace-nowrap">
                    <div class="flex items-center justify-end gap-1">
                      <button 
                        @click="openEditModal(order)"
                        class="p-1.5 rounded-md text-stone-400 hover:text-amber-600 hover:bg-stone-100 transition-colors"
                        title="Edit Ticket"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                      </button>

                      <button 
                        @click="deleteOrder(order.id)"
                        class="p-1.5 rounded-md text-stone-400 hover:text-rose-600 hover:bg-stone-100 transition-colors"
                        title="Delete Ticket"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>

                <!-- Empty State -->
                <tr v-if="filteredOrders.length === 0">
                  <td colspan="7" class="py-12 text-center text-stone-400 font-normal">
                    No active kitchen orders match your selected filters.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

      </div>
    </main>

    <!-- Create / Edit Order Modal -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4 overflow-y-auto">
      <div class="bg-white border border-stone-200 rounded-lg max-w-lg w-full p-6 shadow-xl space-y-5 text-stone-800 my-8">
        
        <div class="flex items-center justify-between border-b border-stone-200 pb-4">
          <div>
            <span class="text-[10px] uppercase font-bold tracking-widest text-amber-600">POS Ticket System</span>
            <h3 class="text-xl font-bold text-stone-900">
              {{ isEditing ? 'Edit Order Ticket' : 'Create New Ticket' }}
            </h3>
          </div>
          <button @click="isModalOpen = false" class="text-stone-400 hover:text-stone-700 text-base">✕</button>
        </div>

        <form @submit.prevent="saveOrder" class="space-y-4 text-xs">
          
          <div>
            <label class="font-bold text-stone-700 block mb-1">Customer / Guest Name</label>
            <input 
              v-model="editingOrder.customerName" 
              type="text" 
              placeholder="e.g. Sophia Laurent"
              required
              class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-900 focus:border-amber-600 focus:bg-white focus:outline-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="font-bold text-stone-700 block mb-1">Order Type</label>
              <select 
                v-model="editingOrder.orderType"
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:outline-none"
              >
                <option value="Dine-In">Dine-In</option>
                <option value="Takeout">Takeout</option>
                <option value="Delivery">Delivery</option>
              </select>
            </div>

            <div>
              <label class="font-bold text-stone-700 block mb-1">Table # (if Dine-In)</label>
              <input 
                v-model="editingOrder.tableNumber" 
                type="text" 
                placeholder="e.g. Table 04"
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:outline-none"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="font-bold text-stone-700 block mb-1">Target Station</label>
              <select 
                v-model="editingOrder.station"
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:outline-none"
              >
                <option>Main Line</option>
                <option>Kitchen Grill</option>
                <option>Pizza Oven</option>
                <option>Pastry & Cold</option>
                <option>Bar & Drinks</option>
              </select>
            </div>

            <div>
              <label class="font-bold text-stone-700 block mb-1">Order Status</label>
              <select 
                v-model="editingOrder.status"
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:outline-none"
              >
                <option value="Pending">Pending</option>
                <option value="Preparing">Preparing</option>
                <option value="Ready">Ready</option>
                <option value="Delivered">Delivered</option>
                <option value="Cancelled">Cancelled</option>
              </select>
            </div>
          </div>

          <!-- Dynamic Items Builder -->
          <div class="border-t border-stone-200 pt-3">
            <div class="flex items-center justify-between mb-2">
              <label class="font-bold text-stone-700">Order Items</label>
              <button 
                type="button" 
                @click="addItemToOrder" 
                class="text-amber-600 hover:text-amber-700 font-semibold text-[11px]"
              >
                + Add Dish Item
              </button>
            </div>

            <div class="space-y-2">
              <div 
                v-for="(item, idx) in editingOrder.items" 
                :key="idx" 
                class="flex items-center gap-2"
              >
                <input 
                  v-model="item.name" 
                  type="text" 
                  placeholder="Item name"
                  required
                  class="flex-grow rounded-lg border border-stone-300 bg-stone-50 p-2 text-stone-800 focus:outline-none"
                />
                <input 
                  v-model.number="item.quantity" 
                  type="number" 
                  min="1" 
                  placeholder="Qty"
                  class="w-16 rounded-lg border border-stone-300 bg-stone-50 p-2 text-stone-800 focus:outline-none"
                />
                <input 
                  v-model.number="item.price" 
                  type="number" 
                  step="0.01" 
                  placeholder="Price"
                  class="w-20 rounded-lg border border-stone-300 bg-stone-50 p-2 text-stone-800 focus:outline-none"
                />
                <button 
                  type="button" 
                  @click="removeItemFromOrder(idx)"
                  class="text-stone-400 hover:text-rose-600 p-1"
                >
                  ✕
                </button>
              </div>
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
              {{ isEditing ? 'Update Ticket' : 'Submit Ticket' }}
            </button>
          </div>

        </form>

      </div>
    </div>
  </div>
</template>