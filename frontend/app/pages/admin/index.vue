<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminSidebar from '~/components/AdminSidebar.vue'
import Chart from '~/components/Chart.vue'
import { useAuth } from '~/composables/useAuth'
import { useAdminTheme } from '~/composables/useAdminTheme'

const { apiBase } = useApiBase()

definePageMeta({ middleware: 'admin' })

const { user, token } = useAuth()
const { isDark } = useAdminTheme()
const adminAvatar = ref('')
// Computed property to construct full avatar URL
const avatarUrl = computed(() => {
  if (!adminAvatar.value) return ''
  if (adminAvatar.value.startsWith('http')) return adminAvatar.value
  return apiBase.value + adminAvatar.value
})


const searchQuery = ref('')
const selectedStatusFilter = ref('All')
const loading = ref(false)
const orders = ref<any[]>([])
const categories = ref<any[]>([])
const tables = ref<any[]>([])
const products = ref<any[]>([])
const reservations = ref<any[]>([])
const pendingReservationCount = computed(() => reservations.value.filter(item => item.status === 'pending').length)
const eventInquiries = ref<any[]>([])
const newEventInquiryCount = computed(() => eventInquiries.value.filter(item => item.status === 'new').length)
const contactMessages = ref<any[]>([])
const newContactMessageCount = computed(() => contactMessages.value.filter(item => item.status === 'new').length)

onMounted(async () => {
  loading.value = true
  try {
    if (token.value) {
      try {
        const res = await $fetch('/me', {
          baseURL: apiBase.value,
          headers: {
            Authorization: `Bearer ${token.value}`,
          },
        })
        adminAvatar.value = (res as any).user?.avatar || ''
      } catch {
        adminAvatar.value = ''
      }
    }
    const authToken = token.value || (import.meta.client ? localStorage.getItem('access_token') : null)
    if (authToken) {
      const headers = { Authorization: `Bearer ${authToken}` }
      try {
        const ordersRes = await $fetch('/orders', {
          baseURL: apiBase.value,
          headers,
        })
        const statusMap: Record<string, string> = {
          pending: 'Pending', preparing: 'Preparing', ready: 'Ready',
          delivered: 'Delivered', cancelled: 'Cancelled', completed: 'Completed',
        }
orders.value = (Array.isArray(ordersRes) ? ordersRes : (ordersRes as any)?.orders || []).map((o: any, i: number) => {
          const rawPrice = o.total_price || 0
          const orderDate = o.created_at ? new Date(o.created_at) : new Date()
          return {
            id: `#ORD-${o.id}`,
            customer: o.customer_name || `User ${o.user_id}`,
            item: (o.items || []).map((it: any) => `${it.quantity}x ${it.product_name || ('Product #' + it.product_id)}`).join(', ') || '—',
            total: `$${rawPrice.toFixed(2)}`,
            rawTotal: rawPrice,
            date: orderDate.toISOString().slice(0, 10),
            day: ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][orderDate.getDay()],
            time: orderDate.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
            status: statusMap[(o.status || 'pending').toLowerCase()] || 'Pending',
            table: o.table_number || `Table ${(i % 12) + 1}`,
          }
        })
      } catch {}
      try {
        const catsRes = await $fetch('/categories', {
          baseURL: apiBase.value,
          headers,
        })
        categories.value = (Array.isArray(catsRes) ? catsRes : (catsRes as any)?.categories || [])
      } catch {}
      try {
        const tablesRes = await $fetch('/tables', {
          baseURL: apiBase.value,
          headers,
        })
        tables.value = (Array.isArray(tablesRes) ? tablesRes : (tablesRes as any)?.tables || [])
      } catch {}
      try {
        const prodRes = await $fetch('/products', {
          baseURL: apiBase.value,
          headers,
        })
        products.value = (Array.isArray(prodRes) ? prodRes : (prodRes as any)?.products || [])
      } catch {}
      try {
        const resRes = await $fetch('/reservations', {
          baseURL: apiBase.value,
          headers,
        })
        reservations.value = (Array.isArray(resRes) ? resRes : (resRes as any)?.reservations || [])
      } catch {}
      try {
        eventInquiries.value = await $fetch('/event-inquiries', { baseURL: apiBase.value, headers })
      } catch {}
      try {
        contactMessages.value = await $fetch('/contact-messages', { baseURL: apiBase.value, headers })
      } catch {}
    }
  } catch {}
  loading.value = false
})

const totalTables = computed(() => tables.value.length || 30)
const occupiedTables = computed(() => tables.value.filter(t => t.status === 'Occupied' || t.status === 'Reserved').length || 18)
const totalCategories = computed(() => categories.value.length)
const totalProducts = computed(() => products.value.length)
const totalReservations = computed(() => reservations.value.length)
const availableTables = computed(() => tables.value.filter(t => t.status === 'Available').length)
const tableCapacity = computed(() => Math.round((occupiedTables.value / totalTables.value) * 100))

const revenueTotal = computed(() => orders.value.reduce((sum, order) => sum + Number(order.total.replace('$', '')), 0))
const averageTicket = computed(() => orders.value.length ? revenueTotal.value / orders.value.length : 0)

// Daily revenue chart data based on orders from this week
const dailyRevenue = computed(() => {
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
  const today = new Date()
  const last7 = Array.from({ length: 7 }, (_, i) => {
    const d = new Date(today)
    d.setDate(today.getDate() - 6 + i)
    return { date: d.toISOString().slice(0, 10), day: days[d.getDay()] }
  })

  const data = last7.map(({ date, day }) => {
    const dayOrders = orders.value.filter(o => o.date === date)
    const revenue = dayOrders.reduce((sum, o) => sum + (o.rawTotal || 0), 0)
    return { day, revenue, count: dayOrders.length }
  })
  
  return data
})

const weeklyRevenue = computed(() => dailyRevenue.value.reduce((sum, day) => sum + day.revenue, 0))
const weeklyOrderCount = computed(() => dailyRevenue.value.reduce((sum, day) => sum + day.count, 0))

const maxRevenue = computed(() => {
  const max = Math.max(...dailyRevenue.value.map(d => d.revenue), 1)
  return max
})

// Chart.js data for Revenue Analytics line chart
const revenueChartData = computed(() => ({
  labels: dailyRevenue.value.map(d => d.day),
  datasets: [{
    label: 'Revenue',
    data: dailyRevenue.value.map(d => d.revenue),
    borderColor: 'rgb(197 146 55)',
    backgroundColor: isDark.value ? 'rgb(197 146 55 / 0.2)' : 'rgb(197 146 55 / 0.14)',
    borderWidth: 3.5,
    pointBackgroundColor: '#C59237',
    pointBorderColor: '#ffffff',
    pointBorderWidth: 2,
    pointRadius: 4.5,
    pointHoverRadius: 7,
    pointHoverBackgroundColor: '#C59237',
    pointHoverBorderColor: '#C59237',
    pointHoverBorderWidth: 3,
    tension: 0.4,
    fill: true,
  }]
}))

const revenueChartOptions = computed(() => {
  const chartText = isDark.value ? '#c8bba8' : '#647489'
  const chartMuted = isDark.value ? '#a99b87' : '#475569'
  const chartSurface = isDark.value ? 'rgba(35, 31, 26, 0.97)' : 'rgba(255, 255, 255, 0.95)'
  return {
  animation: {
    duration: 2500,
    easing: 'easeOutQuart',
  },
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      backgroundColor: chartSurface,
      titleColor: isDark.value ? '#f3e5ce' : '#263344',
      titleFont: { size: 13, weight: 700, family: 'Georgia, serif' },
      bodyColor: chartMuted,
      bodyFont: { size: 12 },
      borderColor: 'rgb(197 146 55 / 0.3)',
      borderWidth: 2,
      padding: { top: 10, bottom: 10, left: 14, right: 14 },
      cornerRadius: 12,
      boxShadow: '0 25px 50px -12px rgb(0 0 0 / 0.25), 0 0 0 1px rgba(0, 0, 0, 0.05)',
      backdropFilter: 'blur(10px)',
      callbacks: {
        title: () => 'Revenue Details',
        label: (ctx) => {
          const dayData = dailyRevenue.value[ctx.dataIndex]
          return `$${ctx.parsed.y.toFixed(2)} (${dayData.count} ${dayData.count === 1 ? 'order' : 'orders'})`
        },
        labelColor: () => chartText,
        labelFontSize: () => 12,
        labelFontWeight: () => 600,
      },
    },
    datalabels: {
      display: true,
      color: chartMuted,
      font: { size: 11, weight: 600 },
      anchor: 'end',
      align: 'top',
      formatter: (val) => `$${val.toFixed(0)}`,
    },
  },
  scales: {
    y: {
      grid: {
        color: isDark.value ? 'rgb(191 161 116 / 0.18)' : 'rgb(226 232 240 / 0.5)',
        borderColor: 'rgb(197 146 55 / 0.2)',
        borderWidth: 1,
        drawBorder: false,
      },
      ticks: {
        color: chartText,
        font: { size: 11, weight: 500 },
        padding: 8,
        callback: (val) => '$' + val,
      },
      beginAtZero: true,
      border: { dash: [4, 4], color: 'rgb(197 146 55 / 0.15)' },
      position: 'left',
    },
    x: {
      grid: { display: false },
      ticks: {
        color: chartText,
        font: { size: 12, weight: 600 },
        padding: 6,
      },
      border: { color: 'rgb(197 146 55 / 0.2)', width: 1 },
    },
  },
  barPercentage: 0.65,
  categoryPercentage: 0.8,
  maintainAspectRatio: false,
  }
})

const totalRevenue = computed(() => revenueTotal.value)

const stats = computed(() => [
  {
    title: 'Total Revenue',
    value: `$${revenueTotal.value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
    change: '+12.5%',
    isPositive: true,
    icon: 'revenue'
  },
  {
    title: 'Total Orders',
    value: orders.value.length.toLocaleString('en-US'),
    change: '+8.2%',
    isPositive: true,
    icon: 'orders'
  },
  {
    title: 'Avg. Ticket Size',
    value: `$${averageTicket.value.toFixed(2)}`,
    change: '-1.4%',
    isPositive: false,
    icon: 'average'
  },
  {
    title: 'Active Tables',
    value: `${occupiedTables.value} / ${totalTables.value}`,
    change: `${tableCapacity.value}% Capacity`,
    isPositive: true,
    icon: 'tables'
  }
])

const popularFoods = computed(() => {
  return products.value
    .sort((a, b) => (b.stockQuantity || 0) - (a.stockQuantity || 0))
    .slice(0, 3)
    .map((p: any, i: number) => ({
      id: p.id,
      name: p.title || p.name,
      category: `${p.category || 'Menu'}`,
      price: `$${(p.price || 0).toFixed(2)}`,
      orders: Math.floor(Math.random() * 300) + 50,
      growth: `+${Math.floor(Math.random() * 25)}%`,
      image: p.image && (p.image.startsWith('http') || p.image.startsWith('blob:')) ? p.image : (p.image ? `${apiBase.value}${p.image}` : 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=200'),
    }))
})

const kitchenQueue = computed(() => {
  return reservations.value
    .filter(r => r.status === 'confirmed' || r.status === 'pending')
    .sort((a, b) => new Date(a.reservedFor).getTime() - new Date(b.reservedFor).getTime())
    .slice(0, 5)
    .map((r: any) => ({
      id: `T${r.tableNumber || r.tableId || '?'}`,
      item: `${r.guestName || 'Guest'} - ${r.guests || 2} guests`,
      minsAgo: Math.max(1, Math.floor(Math.random() * 30)),
      urgent: (r.guests || 0) > 4,
    }))
})

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
  <div class="admin-dashboard min-h-screen bg-[#FBF9F5] text-stone-800 font-sans selection:bg-amber-100">
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
            <NuxtLink to="admin/profile" class="block">
              <img :src="avatarUrl" alt="Admin" class="h-10 w-10 rounded-full border-2 border-[#C59237] object-cover shadow-xs cursor-pointer hover:opacity-80 transition-opacity" />
            </NuxtLink>
          </div>
        </div>
        </header>


      <!-- Dashboard Body -->
      <div class="p-6 lg:p-8 space-y-8">

        <NuxtLink v-if="pendingReservationCount" to="/admin/reservations" class="dashboard-notice dashboard-notice--reservation flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-violet-200 bg-violet-50 px-5 py-4 text-violet-950 transition hover:bg-violet-100">
          <span class="dashboard-notice__copy"><strong>{{ pendingReservationCount }} table reservation request{{ pendingReservationCount === 1 ? '' : 's' }}</strong><span class="ml-2 text-sm text-violet-800">Review the guest’s room, table, and special requests.</span></span>
          <span class="dashboard-notice__action rounded-lg bg-violet-800 px-4 py-2 text-xs font-bold text-white">Review bookings →</span>
        </NuxtLink>

        <NuxtLink v-if="newEventInquiryCount" to="/admin/event-inquiries" class="dashboard-notice dashboard-notice--event flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-amber-200 bg-amber-50 px-5 py-4 text-amber-950 transition hover:bg-amber-100">
          <span class="dashboard-notice__copy"><strong>{{ newEventInquiryCount }} new event booking request{{ newEventInquiryCount === 1 ? '' : 's' }}</strong><span class="ml-2 text-sm text-amber-800">Open the event inbox to review guest messages.</span></span>
          <span class="dashboard-notice__action rounded-lg bg-amber-700 px-4 py-2 text-xs font-bold text-white">View requests →</span>
        </NuxtLink>
        <NuxtLink v-if="newContactMessageCount" to="/admin/contact-messages" class="dashboard-notice dashboard-notice--contact flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-sky-200 bg-sky-50 px-5 py-4 text-sky-950 transition hover:bg-sky-100">
          <span class="dashboard-notice__copy"><strong>{{ newContactMessageCount }} new contact request{{ newContactMessageCount === 1 ? '' : 's' }}</strong><span class="ml-2 text-sm text-sky-800">Guest reservation requests and questions are waiting.</span></span>
          <span class="dashboard-notice__action rounded-lg bg-sky-800 px-4 py-2 text-xs font-bold text-white">Open messages →</span>
        </NuxtLink>
        
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
              <NuxtLink to="/admin/orders" class="px-5 py-2.5 rounded-xl bg-[#C59237] hover:bg-[#b0802c] text-white text-xs font-semibold uppercase tracking-wider transition-all shadow-md">
                + New POS Order
              </NuxtLink>
              <NuxtLink to="/admin/tables" class="px-5 py-2.5 rounded-xl bg-stone-800 hover:bg-stone-700 border border-stone-700 text-stone-200 text-xs font-semibold uppercase tracking-wider transition-all">
                Manage Floor Map
              </NuxtLink>
            </div>
          </div>
        </section>

        <!-- Dynamic Metric Cards Grid -->
        <section class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">
          <div v-for="stat in stats" :key="stat.title" class="rounded-2xl border border-stone-200/80 bg-white p-5 shadow-xs hover:shadow-md transition-shadow">
            <div class="flex items-center justify-between">
              <div class="flex h-11 w-11 items-center justify-center rounded-xl bg-amber-50 text-amber-700 border border-amber-100/50">
                <svg v-if="stat.icon === 'revenue'" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 3v18m4-14.5c-.7-.7-1.8-1.2-3.3-1.2-2.1 0-3.7 1.1-3.7 2.8 0 4.1 7 2.1 7 6.1 0 1.8-1.5 2.9-3.8 2.9-1.6 0-2.9-.5-3.8-1.5" />
                </svg>
                <svg v-else-if="stat.icon === 'orders'" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M3 4h2l1.5 10.5a2 2 0 0 0 2 1.5h7.8a2 2 0 0 0 1.9-1.4L20 8H6m3 12h.01M17 20h.01" />
                </svg>
                <svg v-else-if="stat.icon === 'average'" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4 19V5m0 14h16M8 16v-3m4 3V8m4 8v-6" />
                </svg>
                <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M5 20V9m7 11V4m7 16v-7" />
                </svg>
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
          <div class="chart-panel xl:col-span-2 rounded-2xl border border-stone-200/80 bg-white p-6 shadow-xs">
            <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
              <div>
                <h3 class="font-serif text-lg font-bold text-stone-900 border-b-2 border-[#C59237] pb-1.5 mb-1">Revenue Analytics</h3>
                <p class="text-xs text-stone-400">Daily sales performance this week</p>
              </div>
              <div class="flex items-center gap-4">
                <div class="hidden sm:block text-right">
                  <span class="block text-[9px] font-bold uppercase tracking-[0.16em] text-stone-400">Weekly revenue</span>
                  <strong class="font-serif text-lg text-stone-900">${{ weeklyRevenue.toFixed(2) }}</strong>
                  <span class="ml-2 text-[10px] text-stone-400">{{ weeklyOrderCount }} orders</span>
                </div>
                <span class="rounded-xl border border-amber-200 bg-amber-50 px-3 py-2 text-xs font-semibold text-amber-700">This Week</span>
              </div>
            </div>

            <!-- Bar Chart Visual -->
            <div class="chart-well">
              <Chart type="line" :data="revenueChartData" :options="revenueChartOptions" :height="260" />
            </div>
          </div>

          <!-- Live Kitchen Express Queue Widget -->
          <div class="rounded-2xl border border-stone-200/80 bg-white p-6 shadow-xs flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-serif text-lg font-bold text-stone-900 border-b-2 border-[#C59237] pb-1.5 mb-1">Kitchen Express Queue</h3>
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

            <NuxtLink to="/admin/kds" class="mt-6 block w-full py-2.5 bg-stone-900 hover:bg-stone-800 text-white text-xs font-semibold rounded-xl transition-colors text-center">
              Open Full KDS Display →
            </NuxtLink>
          </div>
        </section>

        <!-- Orders Data Table Section -->
        <section class="rounded-2xl border border-stone-200/80 bg-white shadow-xs overflow-hidden">
          
          <!-- Table Controls Toolbar -->
          <div class="p-6 border-b border-stone-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 class="font-serif text-lg font-bold text-stone-900 border-b-2 border-[#C59237] pb-1.5 mb-1">Recent Guest Orders</h3>
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
                <h3 class="font-serif text-lg font-bold text-stone-900  border-b-2 border-[#C59237] pb-1.5 mb-1">Top Performing Dishes</h3>
                <p class="text-xs text-stone-400">Based on volume metrics this week</p>
              </div>
              <NuxtLink to="/menu" class="text-xs font-semibold text-[#C59237] hover:underline">Full Menu →</NuxtLink>
            </div>

            <div class="space-y-4">
              <div v-for="food in popularFoods" :key="food.id" class="flex items-center justify-between p-2 rounded-xl  hover:bg-stone-800  transition-colors">
                <div class="flex items-center gap-4">
                  <img :src="food.image" :alt="food.name" class="h-14 w-14 rounded-xl object-cover shadow-xs" />
                  <div>
                    <h4 class="text-xs font-bold  text-[#828181]">{{ food.name }}</h4>
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
              <h3 class="font-serif text-lg font-bold text-stone-900 mb-1 border-b-2 border-[#C59237] pb-1.5">Staff & Service Control</h3>
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


