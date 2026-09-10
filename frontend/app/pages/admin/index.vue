<script setup lang="ts">
import { ref, computed } from 'vue'

// Search & Filter Reactive States
const searchQuery = ref('')
const selectedStatusFilter = ref('All')
const revenuePeriod = ref('This Week')

// Operational Metrics
const stats = ref([
  {
    title: 'Total Revenue',
    value: '$12,450.00',
    change: '+12.5%',
    isPositive: true,
    icon: '💰'
  },
  {
    title: 'Total Orders',
    value: '1,248',
    change: '+8.2%',
    isPositive: true,
    icon: '🛒'
  },
  {
    title: 'Avg. Ticket Size',
    value: '$34.20',
    change: '-1.4%',
    isPositive: false,
    icon: '📊'
  },
  {
    title: 'Active Tables',
    value: '18 / 30',
    change: '60% Capacity',
    isPositive: true,
    icon: '🪑'
  }
])

// Orders Data Array
const orders = ref([
  {
    id: '#ORD-1001',
    customer: 'John Smith',
    item: 'Pepperoni Pizza x2',
    total: '$37.00',
    status: 'Completed',
    time: '10:30 AM',
    table: 'Table 04'
  },
  {
    id: '#ORD-1002',
    customer: 'Emma Watson',
    item: 'Chicken Burger Set',
    total: '$18.50',
    status: 'Preparing',
    time: '10:45 AM',
    table: 'Table 12'
  },
  {
    id: '#ORD-1003',
    customer: 'Michael Chen',
    item: 'Prime Beef Steak',
    total: '$45.00',
    status: 'Pending',
    time: '11:05 AM',
    table: 'Takeaway'
  },
  {
    id: '#ORD-1004',
    customer: 'Sophia Lee',
    item: 'Seafood Pasta & Wine',
    total: '$32.00',
    status: 'Completed',
    time: '11:20 AM',
    table: 'Table 02'
  }
])

// Popular Foods
const popularFoods = ref([
  {
    id: 1,
    name: 'Pepperoni Artisan Pizza',
    category: 'Italian • Pizza',
    price: '$18.50',
    orders: 245,
    growth: '+14%',
    image: 'https://images.unsplash.com/photo-1579751626657-72bc17010498?w=200'
  },
  {
    id: 2,
    name: 'Truffle Chicken Burger',
    category: 'Gourmet • Burger',
    price: '$14.00',
    orders: 198,
    growth: '+8%',
    image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=200'
  },
  {
    id: 3,
    name: 'Angus Beef Ribeye Steak',
    category: 'Steakhouse • Main',
    price: '$35.00',
    orders: 167,
    growth: '+22%',
    image: 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=200'
  }
])

// Kitchen Live Queue Bar
const kitchenQueue = ref([
  { id: '#ORD-1002', item: 'Chicken Burger Set', minsAgo: 12, urgent: false },
  { id: '#ORD-1005', item: 'Truffle Fries x3', minsAgo: 22, urgent: true },
  { id: '#ORD-1006', item: 'Grilled Salmon', minsAgo: 5, urgent: false }
])

// Live Status Toggles
const isAcceptingOrders = ref(true)

// Filter Computed Property
const filteredOrders = computed(() => {
  return orders.value.filter(order => {
    const matchesSearch = order.customer.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          order.id.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          order.item.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesStatus = selectedStatusFilter.value === 'All' || order.status === selectedStatusFilter.value
    
    return matchesSearch && matchesStatus
  })
})

const getStatusBadgeClass = (status: string) => {
  switch (status) {
    case 'Completed':
      return 'bg-emerald-50 text-emerald-700 border border-emerald-200/60'
    case 'Preparing':
      return 'bg-amber-50 text-amber-700 border border-amber-200/60'
    case 'Pending':
      return 'bg-rose-50 text-rose-700 border border-rose-200/60'
    default:
      return 'bg-stone-100 text-stone-600'
  }
}

const updateOrderStatus = (orderId: string, newStatus: string) => {
  const target = orders.value.find(o => o.id === orderId)
  if (target) target.status = newStatus
}
</script>

<template>
  <div class="min-h-screen bg-[#FBF9F5] text-stone-800 font-sans selection:bg-amber-100">
    <!-- Sidebar Placeholder -->
    <AdminSidebar />

    <!-- Main Content Container -->
    <main class="lg:ml-64 transition-all duration-300">
      
      <!-- Top Sticky Header -->
      <header class="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-stone-200/70 bg-white/80 px-6 backdrop-blur-md lg:px-8">
        <div>
          <h1 class="font-serif text-2xl font-bold text-stone-900">Executive Dashboard</h1>
          <p class="text-xs text-stone-500 font-light">Real-time restaurant operational overview</p>
        </div>

        <div class="flex items-center gap-4">
          <!-- Live Status Switcher -->
          <div class="hidden sm:flex items-center gap-2 bg-stone-100 px-3 py-1.5 rounded-full border border-stone-200/60">
            <span class="relative flex h-2.5 w-2.5">
              <span :class="isAcceptingOrders ? 'animate-ping bg-emerald-400' : 'bg-rose-400'" class="absolute inline-flex h-full w-full rounded-full opacity-75"></span>
              <span :class="isAcceptingOrders ? 'bg-emerald-500' : 'bg-rose-500'" class="relative inline-flex rounded-full h-2.5 w-2.5"></span>
            </span>
            <span class="text-xs font-medium text-stone-700">{{ isAcceptingOrders ? 'Accepting Orders' : 'Paused' }}</span>
            <button @click="isAcceptingOrders = !isAcceptingOrders" class="text-[10px] uppercase font-bold text-[#C59237] hover:underline ml-1">
              Toggle
            </button>
          </div>

          <!-- Global Search Input -->
          <div class="relative hidden md:block">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Search orders, dishes, clients..." 
              class="w-64 rounded-xl border border-stone-200 bg-stone-50/80 px-4 py-2 pl-9 text-xs text-stone-800 placeholder-stone-400 focus:border-[#C59237] focus:bg-white focus:outline-none transition-all"
            />
            <span class="absolute left-3 top-2.5 text-xs text-stone-400">🔍</span>
          </div>

          <!-- User Profile Brief -->
          <div class="flex items-center gap-3 border-l border-stone-200 pl-4">
            <img src="https://i.pravatar.cc/100?img=12" alt="Admin" class="h-10 w-10 rounded-full border-2 border-[#C59237] object-cover shadow-xs" />
            <div class="hidden xl:block">
              <h4 class="text-xs font-semibold text-stone-900">Chef Marco L.</h4>
              <p class="text-[10px] text-stone-400">General Manager</p>
            </div>
          </div>
        </div>
      </header>

      <!-- Dashboard Body -->
      <div class="p-6 lg:p-8 space-y-8">
        
        <!-- Welcome Hero Banner -->
        <section class="relative overflow-hidden rounded-2xl bg-stone-950 p-8 text-white shadow-xl">
          <div class="absolute -right-10 -top-10 h-64 w-64 rounded-full bg-[#C59237]/10 blur-3xl"></div>
          
          <div class="relative z-10 flex flex-col md:flex-row md:items-center md:justify-between gap-6">
            <div class="space-y-2">
              <span class="text-[10px] font-bold tracking-[0.25em] text-[#C59237] uppercase">Shift Overview</span>
              <h2 class="font-serif text-3xl font-normal text-stone-100">Good Evening, Executive Chef 👋</h2>
              <p class="text-xs text-stone-400 font-light max-w-lg leading-relaxed">
                Dinner service is running at <span class="text-amber-400 font-medium">60% table capacity</span>. 3 orders in the kitchen queue require immediate expedited prep.
              </p>
            </div>

            <div class="flex flex-wrap items-center gap-3">
              <button class="px-5 py-2.5 rounded-xl bg-[#C59237] hover:bg-[#b0802c] text-white text-xs font-semibold uppercase tracking-wider transition-all shadow-md">
                + New POS Order
              </button>
              <button class="px-5 py-2.5 rounded-xl bg-stone-800 hover:bg-stone-700 border border-stone-700 text-stone-200 text-xs font-semibold uppercase tracking-wider transition-all">
                Manage Floor Map
              </button>
            </div>
          </div>
        </section>

        <!-- Dynamic Metric Cards Grid -->
        <section class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">
          <div v-for="stat in stats" :key="stat.title" class="rounded-2xl border border-stone-200/80 bg-white p-5 shadow-xs hover:shadow-md transition-shadow">
            <div class="flex items-center justify-between">
              <div class="flex h-11 w-11 items-center justify-center rounded-xl bg-amber-50 text-xl border border-amber-100/50">
                {{ stat.icon }}
              </div>
              <span :class="stat.isPositive ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'" class="rounded-md px-2 py-1 text-[11px] font-semibold">
                {{ stat.change }}
              </span>
            </div>
            <div class="mt-4">
              <p class="text-xs font-medium uppercase tracking-wider text-stone-400">{{ stat.title }}</p>
              <h3 class="font-serif text-2xl font-bold text-stone-900 mt-1">{{ stat.value }}</h3>
            </div>
          </div>
        </section>

        <!-- Charts & Live Kitchen Split -->
        <section class="grid grid-cols-1 xl:grid-cols-3 gap-6">
          
          <!-- Revenue Visualizer -->
          <div class="xl:col-span-2 rounded-2xl border border-stone-200/80 bg-white p-6 shadow-xs">
            <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
              <div>
                <h3 class="font-serif text-lg font-bold text-stone-900">Revenue Analytics</h3>
                <p class="text-xs text-stone-400">Weekly monetary performance comparison</p>
              </div>
              <select v-model="revenuePeriod" class="rounded-xl border border-stone-200 bg-stone-50 px-3 py-1.5 text-xs text-stone-700 focus:outline-none">
                <option>This Week</option>
                <option>This Month</option>
                <option>This Year</option>
              </select>
            </div>

            <!-- Bar Chart Visual -->
            <div class="flex h-60 items-end justify-between gap-3 border-b border-stone-200 px-2 pb-2">
              <div v-for="(height, index) in [45, 65, 50, 85, 60, 95, 75]" :key="index" class="group flex flex-1 flex-col items-center justify-end">
                <div class="relative w-full max-w-[36px] rounded-t-lg bg-stone-800 transition-all group-hover:bg-[#C59237]" :style="{ height: `${height}%` }">
                  <span class="absolute -top-7 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity bg-stone-900 text-white text-[10px] px-1.5 py-0.5 rounded-xs">
                    ${{ height * 25 }}
                  </span>
                </div>
                <span class="mt-3 text-[11px] font-medium text-stone-400">
                  {{ ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][index] }}
                </span>
              </div>
            </div>
          </div>

          <!-- Live Kitchen Express Queue Widget -->
          <div class="rounded-2xl border border-stone-200/80 bg-white p-6 shadow-xs flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-serif text-lg font-bold text-stone-900">Kitchen Express Queue</h3>
                <span class="text-xs font-bold text-amber-600 bg-amber-50 px-2 py-0.5 rounded-md">Live Stream</span>
              </div>
              <p class="text-xs text-stone-400 mb-5">Current dishes pending chef pickup</p>

              <div class="space-y-3">
                <div v-for="item in kitchenQueue" :key="item.id" class="p-3 rounded-xl border border-stone-100 bg-stone-50/60 flex items-center justify-between">
                  <div>
                    <span class="text-[10px] font-bold text-stone-400">{{ item.id }}</span>
                    <h4 class="text-xs font-semibold text-stone-800">{{ item.item }}</h4>
                  </div>
                  <div class="text-right">
                    <span :class="item.urgent ? 'text-rose-600 font-bold' : 'text-stone-500'" class="text-[11px] block">
                      {{ item.minsAgo }} mins ago
                    </span>
                    <button class="text-[10px] font-bold text-[#C59237] hover:underline uppercase">Bump Order</button>
                  </div>
                </div>
              </div>
            </div>

            <button class="mt-6 w-full py-2.5 bg-stone-900 hover:bg-stone-800 text-white text-xs font-semibold rounded-xl transition-colors">
              Open Full KDS Display →
            </button>
          </div>
        </section>

        <!-- Orders Data Table Section -->
        <section class="rounded-2xl border border-stone-200/80 bg-white shadow-xs overflow-hidden">
          
          <!-- Table Controls Toolbar -->
          <div class="p-6 border-b border-stone-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 class="font-serif text-lg font-bold text-stone-900">Recent Guest Orders</h3>
              <p class="text-xs text-stone-400">Manage incoming and active table transactions</p>
            </div>

            <!-- Filter Status Chips -->
            <div class="flex items-center gap-1.5 overflow-x-auto no-scrollbar">
              <button 
                v-for="status in ['All', 'Pending', 'Preparing', 'Completed']" 
                :key="status"
                @click="selectedStatusFilter = status"
                :class="[
                  'px-3 py-1.5 rounded-xl text-xs font-semibold transition-all',
                  selectedStatusFilter === status ? 'bg-stone-900 text-white' : 'bg-stone-100 text-stone-600 hover:bg-stone-200'
                ]"
              >
                {{ status }}
              </button>
            </div>
          </div>

          <!-- Data Table -->
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="border-b border-stone-100 bg-stone-50/50 text-[11px] uppercase tracking-wider text-stone-400">
                  <th class="px-6 py-3.5 font-semibold">Order Ref</th>
                  <th class="px-6 py-3.5 font-semibold">Customer</th>
                  <th class="px-6 py-3.5 font-semibold">Items Ordered</th>
                  <th class="px-6 py-3.5 font-semibold">Table / Type</th>
                  <th class="px-6 py-3.5 font-semibold">Total Amount</th>
                  <th class="px-6 py-3.5 font-semibold">Status</th>
                  <th class="px-6 py-3.5 font-semibold text-right">Quick Action</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-stone-100 text-xs">
                <tr v-for="order in filteredOrders" :key="order.id" class="hover:bg-stone-50/60 transition-colors">
                  <td class="px-6 py-4 font-bold text-stone-900">{{ order.id }}</td>
                  <td class="px-6 py-4 font-medium text-stone-700">{{ order.customer }}</td>
                  <td class="px-6 py-4 text-stone-600">{{ order.item }}</td>
                  <td class="px-6 py-4 text-stone-500 font-light">{{ order.table }}</td>
                  <td class="px-6 py-4 font-bold text-stone-900">{{ order.total }}</td>
                  <td class="px-6 py-4">
                    <span :class="getStatusBadgeClass(order.status)" class="px-2.5 py-1 rounded-md text-[10px] font-bold">
                      {{ order.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-right">
                    <div class="inline-flex items-center gap-2">
                      <button @click="updateOrderStatus(order.id, 'Completed')" class="text-stone-400 hover:text-emerald-600 font-semibold text-[11px]">Mark Done</button>
                      <button class="text-[#C59237] hover:underline font-semibold text-[11px]">Details</button>
                    </div>
                  </td>
                </tr>
                <tr v-if="filteredOrders.length === 0">
                  <td colspan="7" class="px-6 py-8 text-center text-stone-400 italic">No orders found matching criteria.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Bottom Popular Menu & Store Quick Operations -->
        <section class="grid grid-cols-1 xl:grid-cols-2 gap-6">
          
          <!-- Best Sellers Widget -->
          <div class="rounded-2xl border border-stone-200/80 bg-white p-6 shadow-xs">
            <div class="flex items-center justify-between mb-6">
              <div>
                <h3 class="font-serif text-lg font-bold text-stone-900">Top Performing Dishes</h3>
                <p class="text-xs text-stone-400">Based on volume metrics this week</p>
              </div>
              <NuxtLink to="/admin/menu" class="text-xs font-semibold text-[#C59237] hover:underline">Full Menu →</NuxtLink>
            </div>

            <div class="space-y-4">
              <div v-for="food in popularFoods" :key="food.id" class="flex items-center justify-between p-2 rounded-xl hover:bg-stone-50 transition-colors">
                <div class="flex items-center gap-4">
                  <img :src="food.image" :alt="food.name" class="h-14 w-14 rounded-xl object-cover shadow-xs" />
                  <div>
                    <h4 class="text-xs font-bold text-stone-900">{{ food.name }}</h4>
                    <p class="text-[10px] text-stone-400">{{ food.category }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <span class="text-xs font-bold text-stone-900 block">{{ food.price }}</span>
                  <span class="text-[10px] text-emerald-600 font-semibold">{{ food.orders }} orders ({{ food.growth }})</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick System Controls -->
          <div class="rounded-2xl border border-stone-200/80 bg-white p-6 shadow-xs flex flex-col justify-between">
            <div>
              <h3 class="font-serif text-lg font-bold text-stone-900 mb-1">Staff & Service Control</h3>
              <p class="text-xs text-stone-400 mb-6">Live operational status switches</p>

              <div class="space-y-4">
                <div class="flex items-center justify-between p-4 rounded-xl bg-stone-50 border border-stone-100">
                  <div>
                    <h5 class="text-xs font-bold text-stone-800">Online Reservation Engine</h5>
                    <p class="text-[10px] text-stone-400">Allow table bookings via website</p>
                  </div>
                  <input type="checkbox" checked class="accent-[#C59237] h-4 w-4 rounded-xs cursor-pointer" />
                </div>

                <div class="flex items-center justify-between p-4 rounded-xl bg-stone-50 border border-stone-100">
                  <div>
                    <h5 class="text-xs font-bold text-stone-800">Kitchen Auto-Printing</h5>
                    <p class="text-[10px] text-stone-400">Direct print tickets to line cooks</p>
                  </div>
                  <input type="checkbox" checked class="accent-[#C59237] h-4 w-4 rounded-xs cursor-pointer" />
                </div>
              </div>
            </div>

            <div class="pt-6 border-t border-stone-100 flex items-center justify-between text-xs text-stone-500">
              <span>Shift active since 08:00 AM</span>
              <button class="text-rose-600 font-semibold hover:underline">Close Shift & Export</button>
            </div>
          </div>

        </section>

      </div>
    </main>
  </div>
</template>