<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuth } from '~/composables/useAuth'

const { apiBase } = useApiBase()

definePageMeta({ middleware: 'admin' })

interface User {
  id: number
  username: string
  email: string
  phone: string
  avatar: string
  role: string
}

interface ApiUser {
  id: number
  username: string
  email: string
  phone: string
  avatar: string
  role: string
}

const { user, token } = useAuth()

const users = ref<User[]>([])
const loading = ref(true)
const error = ref('')
const avatarFile = ref<File | null>(null)
const avatarPreview = ref('')

onMounted(fetchUsers)

const searchQuery = ref('')
const selectedRoleFilter = ref('All')

const isModalOpen = ref(false)
const isEditing = ref(false)
const editingUser = ref<ApiUser>({
  id: 0,
  username: '',
  email: '',
  phone: '',
  role: 'customer'
})

const totalUsers = computed(() => users.value.length)
const activeUsersCount = computed(() => users.value.filter(u => u.role !== 'admin').length)

const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const matchesSearch = user.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          user.email.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesRole = selectedRoleFilter.value === 'All' || user.role === selectedRoleFilter.value.toLowerCase()
    return matchesSearch && matchesRole
  })
})

const getRoleBadgeClass = (role: string) => {
  switch (role) {
    case 'admin': return 'bg-purple-50 text-purple-700 border-purple-200'
    default: return 'bg-amber-50 text-amber-700 border-amber-200'
  }
}

const getRoleLabel = (role: string) => role === 'online_customer'
  ? 'Online Customer'
  : role.charAt(0).toUpperCase() + role.slice(1)

const toggleStatus = (user: User) => {
  // No status in user model, remove status cycling
}

async function fetchUsers() {
  const authToken = token.value || (import.meta.client ? localStorage.getItem('access_token') : null)
  if (!authToken) {
    error.value = 'Not authenticated. Please log in again.'
    loading.value = false
    return
  }
  try {
    const response = await $fetch<{ users: ApiUser[] }>('/users', {
      baseURL: apiBase.value,
      headers: {
        Authorization: `Bearer ${authToken}`
      }
    })
    users.value = (response.users || []).map(u => ({
      id: u.id,
      username: u.username,
      email: u.email,
      phone: u.phone || '',
      avatar: u.avatar || '',
      role: u.role,
    }))
  } catch (e) {
    error.value = (e as Error).message || 'Failed to load users'
  } finally {
    loading.value = false
  }
}

const openAddModal = () => {
  isEditing.value = false
  editingUser.value = {
    id: 0, username: '', email: '', phone: '', role: 'customer'
  }
  avatarFile.value = null
  avatarPreview.value = ''
  isModalOpen.value = true
}

const openEditModal = (user: User) => {
  isEditing.value = true
  editingUser.value = { ...user }
  avatarFile.value = null
  avatarPreview.value = user.avatar
    ? (user.avatar.startsWith('http') ? user.avatar : apiBase.value + user.avatar)
    : ''
  isModalOpen.value = true
}

const onAvatarSelect = (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (file) {
    avatarFile.value = file
    avatarPreview.value = URL.createObjectURL(file)
  }
}

const saveUser = async () => {
  if (!editingUser.value.username.trim() || !editingUser.value.email.trim()) return
  const authToken = token.value || (import.meta.client ? localStorage.getItem('access_token') : null)
  if (!authToken) {
    error.value = 'Not authenticated. Please log in again.'
    return
  }
  const formData = new FormData()
  formData.append('username', editingUser.value.username)
  formData.append('email', editingUser.value.email)
  formData.append('phone', editingUser.value.phone || '')
  formData.append('role', editingUser.value.role.toLowerCase())
  if (avatarFile.value) {
    formData.append('avatar', avatarFile.value)
  }
  try {
    if (isEditing.value && editingUser.value.id) {
      await $fetch(`/users/${editingUser.value.id}`, {
        baseURL: apiBase.value,
        method: 'PUT',
        body: formData,
        headers: { Authorization: `Bearer ${authToken}` },
      })
    } else {
      await $fetch('/users', {
        baseURL: apiBase.value,
        method: 'POST',
        body: formData,
        headers: { Authorization: `Bearer ${authToken}` },
      })
    }
    await fetchUsers()
    isModalOpen.value = false
  } catch (e) {
    error.value = (e as Error).message || 'Failed to save user'
  }
}

const deleteUser = async (id: number) => {
  if (!confirm('Are you sure you want to remove this user?')) return
  const authToken = token.value || (import.meta.client ? localStorage.getItem('access_token') : null)
  if (!authToken) {
    error.value = 'Not authenticated. Please log in again.'
    return
  }
  try {
    await $fetch(`/users/${id}`, {
      baseURL: apiBase.value,
      method: 'DELETE',
      headers: { Authorization: `Bearer ${authToken}` },
    })
    await fetchUsers()
  } catch (e) {
    error.value = (e as Error).message || 'Failed to delete user'
  }
}
</script>

<template>
  <div class="min-h-screen bg-stone-100 text-stone-800 font-sans selection:bg-amber-100">
    <AdminSidebar />

    <main class="lg:ml-64 transition-all duration-300">

      <header class="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-stone-200 bg-white/90 px-6 backdrop-blur-md lg:px-8">
        <div>
          <h1 class="text-2xl font-bold text-stone-900 tracking-tight">Users</h1>
          <p class="text-xs text-stone-500 font-normal">Manage registered customer accounts</p>
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
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0 1 14 0z"/>
            </svg>
          </div>
        </div>
      </header>

      <div class="p-6 lg:p-8 space-y-6">

        <section class="grid grid-cols-1 sm:grid-cols-3 gap-5">
          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-stone-400">Total Users</span>
              <p class="text-2xl font-bold text-stone-900 mt-1">{{ totalUsers }} Users</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-50 text-amber-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 43a8 8 0 1 0 0-16 8 8 0 0 0 0 16zM21 20a6 6 0 1 0 0-12 6 6 0 0 0 0 12zM3 20a6 6 0 1 0 0-12 6 6 0 0 0 0 12z"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-emerald-600">Customers</span>
              <p class="text-2xl font-bold text-emerald-700 mt-1">{{ activeUsersCount }} Users</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0 1 18 0z"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-stone-400">Administrators</span>
              <p class="text-2xl font-bold text-stone-900 mt-1">{{ users.filter(u => u.role === 'admin').length }} Admins</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-stone-100 text-stone-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 0 1 8 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
            </div>
          </div>
        </section>

        <section class="bg-white p-4 rounded-lg border border-stone-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
          <div class="flex items-center gap-3 w-full md:w-auto">
            <div class="flex items-center gap-1">
              <span class="text-xs font-bold text-stone-400 uppercase tracking-wider mr-2">Role:</span>
              <select
                v-model="selectedRoleFilter"
                class="rounded-md border border-stone-300 bg-stone-50 px-3 py-1.5 text-xs text-stone-800 focus:border-amber-600 focus:outline-none"
              >
                <option value="All">All Roles</option>
                 <option value="admin">Admin</option>
                 <option value="customer">Customer</option>
                 <option value="online_customer">Online Customer</option>
              </select>
            </div>
          </div>
        </section>

        <section class="bg-white border border-stone-200 rounded-lg shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs text-stone-700">
              <thead>
                <tr class="bg-stone-50 border-b border-stone-200 text-[10px] font-bold uppercase tracking-wider text-stone-400">
                  <th scope="col" class="py-3.5 px-4">Profile</th>
                  <th scope="col" class="py-3.5 px-4">Role</th>
                  <th scope="col" class="py-3.5 px-4">Email</th>
                  <th scope="col" class="py-3.5 px-4">Phone</th>
                  <th scope="col" class="py-3.5 px-4 text-right pr-6">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-stone-100">
                <tr
                  v-for="user in filteredUsers"
                  :key="user.id"
                  class="hover:bg-stone-50/80 transition-colors group"
                >
                  <td class="py-3.5 px-4">
                    <div class="flex items-center gap-3">
                      <img
                        v-if="user.avatar"
                        :src="user.avatar.startsWith('http') ? user.avatar : apiBase + user.avatar"
                        :alt="user.username"
                        class="h-12 w-12 rounded-full object-cover border-2 border-[#C59237] shadow-sm"
                      />
                      <div
                        v-else
                        class="h-12 w-12 rounded-full bg-[#C59237] flex items-center justify-center text-white text-base font-bold shadow-sm"
                      >
                        {{ user.username?.charAt(0).toUpperCase() || '?' }}
                      </div>
                      <div>
                        <span class="font-bold text-stone-900 text-sm block">{{ user.username }}</span>
                          <span class="text-[10px] text-stone-400 font-mono">#{{ user.id }} · {{ getRoleLabel(user.role) }}</span>
                      </div>
                    </div>
                  </td>

                  <td class="py-3.5 px-4">
                    <span
                      :class="getRoleBadgeClass(user.role)"
                      class="px-2.5 py-0.5 rounded border text-[10px] font-bold tracking-wide"
                    >
                       {{ getRoleLabel(user.role) }}
                    </span>
                  </td>

                  <td class="py-3.5 px-4 text-stone-600 whitespace-nowrap">
                    {{ user.email }}
                  </td>

                  <td class="py-3.5 px-4 text-stone-600 whitespace-nowrap">
                    {{ user.phone || '—' }}
                  </td>

                  <td class="py-3.5 px-4 text-right pr-6 whitespace-nowrap">
                    <div class="flex items-center justify-end gap-1">
                      <button
                        @click="openEditModal(user)"
                        class="p-1.5 rounded-md text-stone-400 hover:text-amber-600 hover:bg-stone-100 transition-colors"
                        title="Edit User"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2v-5m-1.414-9.414a2 2 0 1 1 2.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                      </button>

                      <button
                        @click="deleteUser(user.id)"
                        class="p-1.5 rounded-md text-stone-400 hover:text-rose-600 hover:bg-stone-100 transition-colors"
                        title="Delete User"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0 1 16.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>

                <tr v-if="filteredUsers.length === 0">
                  <td colspan="5" class="py-12 text-center text-stone-400 font-normal">
                    No users found.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <div v-if="loading && users.length === 0" class="text-center py-20">
          <div class="inline-block animate-spin rounded-full h-10 w-10 border-b-2 border-amber-500"></div>
          <p class="mt-4 text-stone-500">Loading users...</p>
        </div>

        <div v-if="error" class="text-center py-10 bg-rose-50 border border-rose-200 rounded-lg text-rose-700">
          {{ error }}
        </div>

      </div>
    </main>

    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4">
      <div class="bg-white border border-stone-200 rounded-lg max-w-lg w-full p-6 shadow-xl space-y-5 text-stone-800">

        <div class="flex items-center justify-between border-b border-stone-200 pb-4">
          <div>
            <span class="text-[10px] uppercase font-bold tracking-widest text-amber-600">User Management</span>
            <h3 class="text-xl font-bold text-stone-900">
              {{ isEditing ? 'Edit User' : 'Add New User' }}
            </h3>
          </div>
          <button @click="isModalOpen = false" class="text-stone-400 hover:text-stone-700 text-base">✕</button>
        </div>

        <form @submit.prevent="saveUser" class="space-y-4 text-xs">

          <div>
            <label class="font-bold text-stone-700 block mb-1">Username</label>
            <input
              v-model="editingUser.username"
              type="text"
              placeholder="e.g. John Doe"
              required
              class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-900 focus:border-amber-600 focus:bg-white focus:outline-none"
            />
          </div>

          <div>
            <label class="font-bold text-stone-700 block mb-1">Email Address</label>
            <input
              v-model="editingUser.email"
              type="email"
              placeholder="john@example.com"
              required
              class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
            />
          </div>

          <div>
            <label class="font-bold text-stone-700 block mb-1">Phone Number</label>
            <input
              v-model="editingUser.phone"
              type="tel"
              placeholder="+1 (555) 000-0000"
              class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="font-bold text-stone-700 block mb-1">Avatar Image</label>
              <div class="flex items-center gap-3">
                <img
                  v-if="avatarPreview"
                  :src="avatarPreview"
                  alt="Avatar preview"
                  class="h-10 w-10 rounded-full object-cover border border-stone-200 shrink-0"
                />
                <div
                  v-else
                  class="h-10 w-10 rounded-full bg-stone-200 flex items-center justify-center text-stone-500 text-xs font-bold"
                >
                  {{ editingUser.username?.charAt(0)?.toUpperCase() || '?' }}
                </div>
                <input
                  type="file"
                  accept="image/*"
                  @change="onAvatarSelect"
                  class="text-xs text-stone-600 file:mr-3 file:py-1.5 file:px-3 file:rounded-md file:border-0 file:bg-amber-50 file:text-amber-700 file:text-xs file:font-semibold hover:file:bg-amber-100 cursor-pointer"
                />
              </div>
            </div>

            <div>
              <label class="font-bold text-stone-700 block mb-1">Role</label>
              <select
                v-model="editingUser.role"
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
              >
                <option value="customer">Customer</option>
                <option value="online_customer">Online Customer</option>
                <option value="admin">Admin</option>
              </select>
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
              {{ isEditing ? 'Update User' : 'Create User' }}
            </button>
          </div>

        </form>

      </div>
    </div>
  </div>
</template>
