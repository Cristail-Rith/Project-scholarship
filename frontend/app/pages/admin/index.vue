<script setup lang="ts">
const stats = [
  {
    title: 'Total Revenue',
    value: '$12,450',
    change: '+12.5%',
    icon: '💰'
  },
  {
    title: 'Total Orders',
    value: '1,248',
    change: '+8.2%',
    icon: '🛒'
  },
  {
    title: 'Customers',
    value: '856',
    change: '+6.4%',
    icon: '👥'
  },
  {
    title: 'Menu Items',
    value: '64',
    change: '+4 New',
    icon: '🍽️'
  }
]

const orders = [
  {
    id: '#ORD-1001',
    customer: 'John Smith',
    item: 'Pepperoni Pizza',
    total: '$18.50',
    status: 'Completed',
    time: '10:30 AM'
  },
  {
    id: '#ORD-1002',
    customer: 'Emma Watson',
    item: 'Chicken Burger',
    total: '$12.00',
    status: 'Preparing',
    time: '10:45 AM'
  },
  {
    id: '#ORD-1003',
    customer: 'Michael Chen',
    item: 'Beef Steak',
    total: '$25.00',
    status: 'Pending',
    time: '11:05 AM'
  },
  {
    id: '#ORD-1004',
    customer: 'Sophia Lee',
    item: 'Seafood Pasta',
    total: '$20.00',
    status: 'Completed',
    time: '11:20 AM'
  }
]

const popularFoods = [
  {
    id: 1,
    name: 'Pepperoni Pizza',
    category: 'Pizza',
    price: '$18.50',
    orders: 245,
    image:
      'https://images.unsplash.com/photo-1579751626657-72bc17010498?w=200'
  },
  {
    id: 2,
    name: 'Chicken Burger',
    category: 'Burger',
    price: '$12.00',
    orders: 198,
    image:
      'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=200'
  },
  {
    id: 3,
    name: 'Beef Steak',
    category: 'Main Course',
    price: '$25.00',
    orders: 167,
    image:
      'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=200'
  }
]

const getStatusClass = (status: string) => {
  if (status === 'Completed') {
    return 'bg-green-100 text-green-700'
  }

  if (status === 'Preparing') {
    return 'bg-orange-100 text-orange-700'
  }

  return 'bg-yellow-100 text-yellow-700'
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Sidebar -->
    <AdminSidebar/>

    <!-- Main -->
    <main class="lg:ml-64">
      <!-- Header -->
      <header
        class="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-gray-200 bg-white px-5 lg:px-8"
      >
        <div>
          <h2 class="text-xl font-bold text-gray-900 lg:text-2xl">
            Dashboard
          </h2>

        </div>

        <div class="flex items-center gap-3">
          <!-- Search -->
          <div
            class="hidden items-center rounded-xl bg-gray-100 px-4 py-2.5 md:flex"
          >
            <span class="mr-2">🔍</span>

            <input
              type="text"
              placeholder="Search"
              class="w-40 bg-transparent text-sm outline-none"
            />
          </div>

          <!-- Profile -->
          <div class="flex items-center gap-3">
            <img
              src="https://i.pravatar.cc/100?img=12"
              alt="Admin"
              class="h-11 w-11 rounded-xl object-cover"
            />

            <div class="hidden sm:block">
              <h4 class="text-sm font-semibold text-gray-900">
                Admin
              </h4>

              <p class="text-xs text-gray-400">
                Restaurant Manager
              </p>
            </div>
          </div>
        </div>
      </header>

      <!-- Content -->
      <div class="p-5 lg:p-8">
        <!-- Welcome -->
        <section
          class="mb-7 flex flex-col justify-between gap-5 rounded-3xl bg-linear-to-r from-black to-orange-700 p-7 text-orange-500 md:flex-row md:items-center"
        >
          <div>

            <h1 class="text-2xl font-bold md:text-3xl">
              Good evening, Admin 👋
            </h1>

            <button
              class="mt-5 rounded-xl bg-black border-2 border-orange-400 px-5 py-2.5 text-sm font-semibold text-orange-500 transition hover:bg-orange-50"
            >
              View Orders
            </button>
          </div>

          <div
            class="hidden text-8xl opacity-90 md:block"
          >
            
          </div>
        </section>

        <!-- Stats -->
        <section
          class="mb-7 grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4"
        >
          <div
            v-for="stat in stats"
            :key="stat.title"
            class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm"
          >
            <div class="flex items-start justify-between">
              <div
                class="flex h-12 w-12 items-center justify-center rounded-xl bg-orange-50 text-2xl"
              >
                {{ stat.icon }}
              </div>

              <span
                class="rounded-lg bg-green-50 px-2 py-1 text-xs font-medium text-green-600"
              >
                {{ stat.change }}
              </span>
            </div>

            <p class="mt-5 text-sm text-gray-400">
              {{ stat.title }}
            </p>

            <h3 class="mt-1 text-2xl font-bold text-gray-900">
              {{ stat.value }}
            </h3>
          </div>
        </section>

        <!-- Order Overview -->
        <section
          class="mb-7 grid grid-cols-1 gap-6 xl:grid-cols-3"
        >
          <!-- Sales chart -->
          <div
            class="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm xl:col-span-2"
          >
            <div class="mb-6 flex items-center justify-between">
              <div>
                <h3 class="text-lg font-bold text-gray-900">
                  Revenue Overview
                </h3>

                <p class="text-sm text-gray-400">
                  Restaurant revenue this week
                </p>
              </div>

              <select
                class="rounded-xl border border-gray-200 px-3 py-2 text-sm outline-none"
              >
                <option>This Week</option>
                <option>This Month</option>
                <option>This Year</option>
              </select>
            </div>

            <!-- Fake chart -->
            <div
              class="flex h-64 items-end justify-between gap-3 border-b border-l border-gray-200 px-4 pb-2"
            >
              <div
                v-for="(height, index) in [40, 65, 45, 80, 55, 95, 70]"
                :key="index"
                class="flex flex-1 flex-col items-center justify-end"
              >
                <div
                  class="w-full max-w-10 rounded-t-xl bg-orange-400 transition hover:bg-orange-500"
                  :style="{ height: `${height}%` }"
                ></div>

                <span
                  class="mt-3 text-xs text-gray-400"
                >
                  {{
                    ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][index]
                  }}
                </span>
              </div>
            </div>
          </div>

          <!-- Order summary -->
          <div
            class="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm"
          >
            <h3 class="text-lg font-bold text-gray-900">
              Order Summary
            </h3>

            <p class="mb-6 text-sm text-gray-400">
              Today's orders
            </p>

            <div class="space-y-5">
              <div>
                <div class="mb-2 flex justify-between">
                  <span class="text-sm text-gray-600">
                    Completed
                  </span>

                  <span class="font-semibold text-gray-900">
                    82
                  </span>
                </div>

                <div class="h-2 rounded-full bg-gray-100">
                  <div
                    class="h-2 w-[80%] rounded-full bg-green-500"
                  ></div>
                </div>
              </div>

              <div>
                <div class="mb-2 flex justify-between">
                  <span class="text-sm text-gray-600">
                    Preparing
                  </span>

                  <span class="font-semibold text-gray-900">
                    24
                  </span>
                </div>

                <div class="h-2 rounded-full bg-gray-100">
                  <div
                    class="h-2 w-[55%] rounded-full bg-orange-500"
                  ></div>
                </div>
              </div>

              <div>
                <div class="mb-2 flex justify-between">
                  <span class="text-sm text-gray-600">
                    Pending
                  </span>

                  <span class="font-semibold text-gray-900">
                    14
                  </span>
                </div>

                <div class="h-2 rounded-full bg-gray-100">
                  <div
                    class="h-2 w-[35%] rounded-full bg-yellow-400"
                  ></div>
                </div>
              </div>

              <div>
                <div class="mb-2 flex justify-between">
                  <span class="text-sm text-gray-600">
                    Cancelled
                  </span>

                  <span class="font-semibold text-gray-900">
                    8
                  </span>
                </div>

                <div class="h-2 rounded-full bg-gray-100">
                  <div
                    class="h-2 w-[20%] rounded-full bg-red-400"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Recent Orders -->
        <section
          class="mb-7 overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-sm"
        >
          <div
            class="flex items-center justify-between border-b border-gray-100 p-6"
          >
            <div>
              <h3 class="text-lg font-bold text-gray-900">
                Recent Orders
              </h3>

              <p class="text-sm text-gray-400">
                Latest customer orders
              </p>
            </div>

            <NuxtLink
              to="/admin/orders"
              class="text-sm font-semibold text-orange-500 hover:text-orange-600"
            >
              View All →
            </NuxtLink>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full min-w-200 text-left">
              <thead class="bg-gray-50">
                <tr class="text-sm text-gray-500">
                  <th class="px-6 py-4 font-medium">
                    Order ID
                  </th>

                  <th class="px-6 py-4 font-medium">
                    Customer
                  </th>

                  <th class="px-6 py-4 font-medium">
                    Order
                  </th>

                  <th class="px-6 py-4 font-medium">
                    Total
                  </th>

                  <th class="px-6 py-4 font-medium">
                    Time
                  </th>

                  <th class="px-6 py-4 font-medium">
                    Status
                  </th>

                  <th class="px-6 py-4 font-medium">
                    Action
                  </th>
                </tr>
              </thead>

              <tbody>
                <tr
                  v-for="order in orders"
                  :key="order.id"
                  class="border-t border-gray-100 text-sm"
                >
                  <td class="px-6 py-5 font-semibold text-gray-900">
                    {{ order.id }}
                  </td>

                  <td class="px-6 py-5 text-gray-600">
                    {{ order.customer }}
                  </td>

                  <td class="px-6 py-5 text-gray-600">
                    {{ order.item }}
                  </td>

                  <td class="px-6 py-5 font-semibold text-gray-900">
                    {{ order.total }}
                  </td>

                  <td class="px-6 py-5 text-gray-500">
                    {{ order.time }}
                  </td>

                  <td class="px-6 py-5">
                    <span
                      :class="getStatusClass(order.status)"
                      class="rounded-full px-3 py-1 text-xs font-medium"
                    >
                      {{ order.status }}
                    </span>
                  </td>

                  <td class="px-6 py-5">
                    <button
                      class="rounded-lg px-3 py-1.5 text-orange-500 hover:bg-orange-50"
                    >
                      View
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Bottom Section -->
        <section
          class="grid grid-cols-1 gap-6 xl:grid-cols-2"
        >
          <!-- Popular Foods -->
          <div
            class="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm"
          >
            <div class="mb-6 flex items-center justify-between">
              <div>
                <h3 class="text-lg font-bold text-gray-900">
                  Popular Menu
                </h3>

                <p class="text-sm text-gray-400">
                  Best selling dishes
                </p>
              </div>

              <NuxtLink
                to="/admin/menu"
                class="text-sm font-medium text-orange-500"
              >
                View Menu
              </NuxtLink>
            </div>

            <div class="space-y-5">
              <div
                v-for="food in popularFoods"
                :key="food.id"
                class="flex items-center"
              >
                <img
                  :src="food.image"
                  :alt="food.name"
                  class="h-16 w-16 rounded-xl object-cover"
                />

                <div class="ml-4 flex-1">
                  <h4 class="font-semibold text-gray-900">
                    {{ food.name }}
                  </h4>

                  <p class="text-xs text-gray-400">
                    {{ food.category }}
                  </p>
                </div>

                <div class="text-right">
                  <p class="font-bold text-gray-900">
                    {{ food.price }}
                  </p>

                  <p class="text-xs text-gray-400">
                    {{ food.orders }} orders
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Restaurant Status -->
          <div
            class="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm"
          >
            <h3 class="text-lg font-bold text-gray-900">
              Restaurant Status
            </h3>

            <p class="mb-6 text-sm text-gray-400">
              Live restaurant information
            </p>

            <div
              class="mb-4 flex items-center justify-between rounded-2xl bg-green-50 p-4"
            >
              <div class="flex items-center gap-3">
                <div
                  class="flex h-11 w-11 items-center justify-center rounded-xl bg-green-100"
                >
                  🟢
                </div>

                <div>
                  <p class="font-semibold text-gray-900">
                    Restaurant
                  </p>

                  <p class="text-xs text-gray-500">
                    Currently accepting orders
                  </p>
                </div>
              </div>

              <span class="font-semibold text-green-600">
                Open
              </span>
            </div>

            <div
              class="mb-4 flex items-center justify-between rounded-2xl bg-gray-50 p-4"
            >
              <div>
                <p class="text-sm text-gray-500">
                  Available Tables
                </p>

                <h4 class="text-xl font-bold text-gray-900">
                  18 / 30
                </h4>
              </div>

              <span class="text-3xl">🪑</span>
            </div>

            <div
              class="flex items-center justify-between rounded-2xl bg-gray-50 p-4"
            >
              <div>
                <p class="text-sm text-gray-500">
                  Staff Online
                </p>

                <h4 class="text-xl font-bold text-gray-900">
                  14 / 18
                </h4>
              </div>

              <span class="text-3xl">👨‍🍳</span>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>