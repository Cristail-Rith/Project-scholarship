<script setup lang="ts">
import { ref, computed } from 'vue'

interface User {
  id: string
  name: string
  email: string
  avatar: string
  role: 'Admin' | 'Manager' | 'Kitchen Staff' | 'Waitstaff' | 'Barist'
  station: 'Kitchen Grill' | 'Pizza Oven' | 'Bar & Drinks' | 'Pastry & Cold' | 'Main Line' | 'All'
  status: 'Active' | 'On Leave' | 'Inactive'
  lastActive: string
}

// Available Options for Forms
const roles = ['Admin', 'Manager', 'Kitchen Staff', 'Waitstaff', 'Barist'] as const
const stations = ['All', 'Kitchen Grill', 'Pizza Oven', 'Main Line', 'Pastry & Cold', 'Bar & Drinks'] as const

// Search & Filter State
const searchQuery = ref('')
const selectedRoleFilter = ref('All')
const selectedStatusFilter = ref('All')

// Modal Form State
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingUser = ref<User>({
  id: '',
  name: '',
  email: '',
  avatar: '',
  role: 'Kitchen Staff',
  station: 'Main Line',
  status: 'Active',
  lastActive: 'Just now'
})

// Users Dataset
const users = ref<User[]>([
  {
    id: 'USR-101',
    name: 'Marcus Vance',
    email: 'm.vance@restaurant.com',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150',
    role: 'Admin',
    station: 'All',
    status: 'Active',
    lastActive: '2 mins ago'
  },
  {
    id: 'USR-102',
    name: 'Elena Rostova',
    email: 'e.rostova@restaurant.com',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150',
    role: 'Manager',
    station: 'All',
    status: 'Active',
    lastActive: '15 mins ago'
  },
  {
    id: 'USR-103',
    name: 'David Chen',
    email: 'd.chen@restaurant.com',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150',
    role: 'Kitchen Staff',
    station: 'Kitchen Grill',
    status: 'Active',
    lastActive: '1 hour ago'
  },
  {
    id: 'USR-104',
    name: 'Sophia Martinez',
    email: 's.martinez@restaurant.com',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150',
    role: 'Barist',
    station: 'Bar & Drinks',
    status: 'Active',
    lastActive: '3 hours ago'
  },
  {
    id: 'USR-105',
    name: 'Liam O\'Connor',
    email: 'l.oconnor@restaurant.com',
    avatar: 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150',
    role: 'Kitchen Staff',
    station: 'Pizza Oven',
    status: 'On Leave',
    lastActive: '2 days ago'
  },
  {
    id: 'USR-106',
    name: 'Chloe Bennett',
    email: 'c.bennett@restaurant.com',
    avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150',
    role: 'Waitstaff',
    station: 'Main Line',
    status: 'Inactive',
    lastActive: '1 week ago'
  }
])

// Computed Metrics
const totalUsers = computed(() => users.value.length)
const activeUsersCount = computed(() => users.value.filter(u => u.status === 'Active').length)
const kitchenStaffCount = computed(() => users.value.filter(u => u.role === 'Kitchen Staff').length)

// Filter Computed Property
const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const matchesSearch = user.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          user.email.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesRole = selectedRoleFilter.value === 'All' || user.role === selectedRoleFilter.value
    const matchesStatus = selectedStatusFilter.value === 'All' || user.status === selectedStatusFilter.value
    
    return matchesSearch && matchesRole && matchesStatus
  })
})

// Quick Actions
const openAddModal = () => {
  isEditing.value = false
  editingUser.value = {
    id: `USR-${Math.floor(100 + Math.random() * 900)}`,
    name: '',
    email: '',
    avatar: `https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150`,
    role: 'Kitchen Staff',
    station: 'Main Line',
    status: 'Active',
    lastActive: 'Just now'
  }
  isModalOpen.value = true
}

const openEditModal = (user: User) => {
  isEditing.value = true
  editingUser.value = { ...user }
  isModalOpen.value = true
}

const toggleStatus = (user: User) => {
  if (user.status === 'Active') user.status = 'On Leave'
  else if (user.status === 'On Leave') user.status = 'Inactive'
  else user.status = 'Active'
}

const saveUser = () => {
  if (!editingUser.value.name.trim() || !editingUser.value.email.trim()) return

  if (isEditing.value) {
    const idx = users.value.findIndex(u => u.id === editingUser.value.id)
    if (idx !== -1) users.value[idx] = { ...editingUser.value }
  } else {
    users.value.push({ ...editingUser.value })
  }
  isModalOpen.value = false
}

const deleteUser = (id: string) => {
  if (confirm('Are you sure you want to remove this staff member?')) {
    users.value = users.value.filter(u => u.id !== id)
  }
}

const getRoleBadgeClass = (role: User['role']) => {
  switch (role) {
    case 'Admin': return 'bg-purple-50 text-purple-700 border-purple-200'
    case 'Manager': return 'bg-blue-50 text-blue-700 border-blue-200'
    case 'Kitchen Staff': return 'bg-amber-50 text-amber-700 border-amber-200'
    case 'Barist': return 'bg-rose-50 text-rose-700 border-rose-200'
    default: return 'bg-stone-100 text-stone-700 border-stone-200'
  }
}
</script>

<template>
  <div class="min-h-screen bg-stone-100 text-stone-800 font-sans selection:bg-amber-100">
    <AdminSidebar />

    <main class="lg:ml-64 transition-all duration-300">
      
      <!-- Top Sticky Header -->
      <header class="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-stone-200 bg-white/90 px-6 backdrop-blur-md lg:px-8">
        <div>
          <h1 class="text-2xl font-bold text-stone-900 tracking-tight">Staff & Users</h1>
          <p class="text-xs text-stone-500 font-normal">Manage team accounts, station assignments, and access roles</p>
        </div>

        <div class="flex items-center gap-3">
          <div class="relative hidden sm:block">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Search user or email..." 
              class="w-64 rounded-lg border border-stone-300 bg-stone-50 px-4 py-2 pl-9 text-xs text-stone-800 placeholder-stone-400 focus:border-amber-600 focus:bg-white focus:outline-none transition-all"
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
            Add Staff Member
          </button>
        </div>
      </header>

      <div class="p-6 lg:p-8 space-y-6">

        <!-- Metrics Overview -->
        <section class="grid grid-cols-1 sm:grid-cols-3 gap-5">
          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-stone-400">Total Accounts</span>
              <p class="text-2xl font-bold text-stone-900 mt-1">{{ totalUsers }} Staff</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-50 text-amber-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 43a8 8 0 100-16 8 8 0 000 16zM21 20a6 6 0 100-12 6 6 0 000 12zM3 20a6 6 0 100-12 6 6 0 000 12z"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-emerald-600">Active On Duty</span>
              <p class="text-2xl font-bold text-emerald-700 mt-1">{{ activeUsersCount }} Online</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-stone-400">Kitchen & Line Crew</span>
              <p class="text-2xl font-bold text-stone-900 mt-1">{{ kitchenStaffCount }} Chefs</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-stone-100 text-stone-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
            </div>
          </div>
        </section>

        <!-- Filter Bar -->
        <section class="bg-white p-4 rounded-lg border border-stone-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
          <div class="flex items-center gap-3 w-full md:w-auto">
            <div class="flex items-center gap-1">
              <span class="text-xs font-bold text-stone-400 uppercase tracking-wider mr-2">Role:</span>
              <select 
                v-model="selectedRoleFilter"
                class="rounded-md border border-stone-300 bg-stone-50 px-3 py-1.5 text-xs text-stone-800 focus:border-amber-600 focus:outline-none"
              >
                <option value="All">All Roles</option>
                <option v-for="r in roles" :key="r" :value="r">{{ r }}</option>
              </select>
            </div>

            <div class="flex items-center gap-1">
              <span class="text-xs font-bold text-stone-400 uppercase tracking-wider mr-2">Status:</span>
              <select 
                v-model="selectedStatusFilter"
                class="rounded-md border border-stone-300 bg-stone-50 px-3 py-1.5 text-xs text-stone-800 focus:border-amber-600 focus:outline-none"
              >
                <option value="All">All Statuses</option>
                <option value="Active">Active</option>
                <option value="On Leave">On Leave</option>
                <option value="Inactive">Inactive</option>
              </select>
            </div>
          </div>

          <span class="text-xs text-stone-400 font-normal">Click status pill to cycle states</span>
        </section>

        <!-- Users Table -->
        <section class="bg-white border border-stone-200 rounded-lg shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs text-stone-700">
              <thead>
                <tr class="bg-stone-50 border-b border-stone-200 text-[10px] font-bold uppercase tracking-wider text-stone-400">
                  <th scope="col" class="py-3.5 px-4">User</th>
                  <th scope="col" class="py-3.5 px-4">Role</th>
                  <th scope="col" class="py-3.5 px-4">Station</th>
                  <th scope="col" class="py-3.5 px-4 text-center">Status</th>
                  <th scope="col" class="py-3.5 px-4">Last Activity</th>
                  <th scope="col" class="py-3.5 px-4 text-right pr-6">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-stone-100">
                <tr 
                  v-for="user in filteredUsers" 
                  :key="user.id" 
                  class="hover:bg-stone-50/80 transition-colors group"
                >
                  <!-- Avatar + User Profile -->
                  <td class="py-3.5 px-4">
                    <div class="flex items-center gap-3">
                      <img 
                        :src="user.avatar" 
                        :alt="user.name" 
                        class="h-9 w-9 rounded-full object-cover border border-stone-200"
                      />
                      <div>
                        <span class="font-bold text-stone-900 text-sm block">{{ user.name }}</span>
                        <span class="text-[11px] text-stone-400 font-mono">{{ user.email }}</span>
                      </div>
                    </div>
                  </td>

                  <!-- Access Role -->
                  <td class="py-3.5 px-4">
                    <span 
                      :class="getRoleBadgeClass(user.role)"
                      class="px-2.5 py-0.5 rounded border text-[10px] font-bold tracking-wide"
                    >
                      {{ user.role }}
                    </span>
                  </td>

                  <!-- Assigned Station -->
                  <td class="py-3.5 px-4 font-semibold text-stone-800 whitespace-nowrap">
                    <span class="inline-flex items-center gap-1.5">
                      <svg class="w-3.5 h-3.5 text-stone-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                      </svg>
                      {{ user.station }}
                    </span>
                  </td>

                  <!-- Status -->
                  <td class="py-3.5 px-4 text-center whitespace-nowrap">
                    <button 
                      @click="toggleStatus(user)"
                      :class="[
                        'px-2.5 py-1 rounded text-[10px] font-bold border transition-all cursor-pointer hover:opacity-80',
                        user.status === 'Active' ? 'bg-emerald-50 text-emerald-700 border-emerald-300' :
                        user.status === 'On Leave' ? 'bg-amber-50 text-amber-700 border-amber-300' : 
                        'bg-stone-100 text-stone-500 border-stone-300'
                      ]"
                    >
                      {{ user.status }}
                    </button>
                  </td>

                  <!-- Last Activity -->
                  <td class="py-3.5 px-4 text-stone-500 whitespace-nowrap">
                    {{ user.lastActive }}
                  </td>

                  <!-- Actions -->
                  <td class="py-3.5 px-4 text-right pr-6 whitespace-nowrap">
                    <div class="flex items-center justify-end gap-1">
                      <button 
                        @click="openEditModal(user)"
                        class="p-1.5 rounded-md text-stone-400 hover:text-amber-600 hover:bg-stone-100 transition-colors"
                        title="Edit User"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                      </button>

                      <button 
                        @click="deleteUser(user.id)"
                        class="p-1.5 rounded-md text-stone-400 hover:text-rose-600 hover:bg-stone-100 transition-colors"
                        title="Delete User"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>

                <!-- Empty State -->
                <tr v-if="filteredUsers.length === 0">
                  <td colspan="6" class="py-12 text-center text-stone-400 font-normal">
                    No staff members match the selected criteria.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

      </div>
    </main>

    <!-- Create / Edit User Modal -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4">
      <div class="bg-white border border-stone-200 rounded-lg max-w-lg w-full p-6 shadow-xl space-y-5 text-stone-800">
        
        <div class="flex items-center justify-between border-b border-stone-200 pb-4">
          <div>
            <span class="text-[10px] uppercase font-bold tracking-widest text-amber-600">Account Management</span>
            <h3 class="text-xl font-bold text-stone-900">
              {{ isEditing ? 'Edit Staff Profile' : 'Add New Staff Member' }}
            </h3>
          </div>
          <button @click="isModalOpen = false" class="text-stone-400 hover:text-stone-700 text-base">✕</button>
        </div>

        <form @submit.prevent="saveUser" class="space-y-4 text-xs">
          
          <div>
            <label class="font-bold text-stone-700 block mb-1">Full Name</label>
            <input 
              v-model="editingUser.name" 
              type="text" 
              placeholder="e.g. Alex Turner"
              required
              class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-900 focus:border-amber-600 focus:bg-white focus:outline-none"
            />
          </div>

          <div>
            <label class="font-bold text-stone-700 block mb-1">Email Address</label>
            <input 
              v-model="editingUser.email" 
              type="email" 
              placeholder="alex.turner@restaurant.com"
              required
              class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="font-bold text-stone-700 block mb-1">Role / Access Level</label>
              <select 
                v-model="editingUser.role"
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
              >
                <option v-for="r in roles" :key="r" :value="r">{{ r }}</option>
              </select>
            </div>

            <div>
              <label class="font-bold text-stone-700 block mb-1">Assigned Station</label>
              <select 
                v-model="editingUser.station"
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
              >
                <option v-for="s in stations" :key="s" :value="s">{{ s }}</option>
              </select>
            </div>
          </div>

          <div>
            <label class="font-bold text-stone-700 block mb-1">Account Status</label>
            <select 
              v-model="editingUser.status"
              class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
            >
              <option value="Active">Active</option>
              <option value="On Leave">On Leave</option>
              <option value="Inactive">Inactive</option>
            </select>
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
              {{ isEditing ? 'Update User' : 'Create User' }}
            </button>
          </div>

        </form>

      </div>
    </div>
  </div>
</template>