<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '~/components/Navbar.vue'
import { useAuth } from '~/composables/useAuth'

const { apiBase } = useApiBase()

definePageMeta({
  middleware: 'auth'
})

interface ProfileUser {
  id: number
  username: string
  email: string
  phone: string
  avatar: string
  role: string
}

interface OrderItem {
  id: number
  product_id: number
  product_name?: string
  product_image?: string
  quantity: number
  price: number
}

interface Order {
  id: number
  user_id: number
  total_price: number
  status: string
  order_type?: string
  payment_method?: string
  delivery_fee?: number
  notes?: string
  customer_name?: string
  customer_email?: string
  customer_phone?: string
  table_number?: string
  delivery_address?: string
  created_at?: string
  items: OrderItem[]
}

interface Reservation {
  id: number
  guest_name: string | null
  guest_email: string | null
  guest_phone: string | null
  table_id: number | null
  date_time: string
  status: string
}

const { user, token, logout } = useAuth()
const router = useRouter()

const profileUser = ref<ProfileUser | null>(null)
const orders = ref<Order[]>([])
const reservations = ref<Reservation[]>([])

const loading = ref(true)
const error = ref('')

const isEditing = ref(false)
const isUploadingAvatar = ref(false)

const editForm = ref({
  username: '',
  email: '',
  phone: '',
  currentPassword: '',
  newPassword: '',
  confirmNewPassword: '',
  avatar: null as File | null
})

const editMessage = ref('')
const editSuccess = ref(false)
const reservationsLoading = ref(false)

/* ---------------------------------------
   COMPUTED
--------------------------------------- */

const totalOrders = computed(() => orders.value.length)

const totalSpent = computed(() =>
  orders.value.reduce((sum, order) => sum + Number(order.total_price || 0), 0)
)

const activeOrders = computed(() =>
  orders.value.filter(order =>
    ['pending', 'preparing', 'ready'].includes(
      order.status?.toLowerCase()
    )
  )
)

const currentOrder = computed(() => activeOrders.value[0] || null)

const loyaltyPoints = computed(() =>
  Math.floor(totalSpent.value * 10)
)

const loyaltyTier = computed(() => {
  const spent = totalSpent.value

  if (spent >= 2000) return 'Platinum VIP'
  if (spent >= 1000) return 'Gold VIP'
  if (spent >= 500) return 'Silver VIP'

  return 'Regular'
})

const nextTier = computed(() => {
  if (loyaltyTier.value === 'Regular') {
    return {
      name: 'Silver VIP',
      amount: Math.max(0, 500 - totalSpent.value)
    }
  }

  if (loyaltyTier.value === 'Silver VIP') {
    return {
      name: 'Gold VIP',
      amount: Math.max(0, 1000 - totalSpent.value)
    }
  }

  if (loyaltyTier.value === 'Gold VIP') {
    return {
      name: 'Platinum VIP',
      amount: Math.max(0, 2000 - totalSpent.value)
    }
  }

  return {
    name: 'Platinum VIP',
    amount: 0
  }
})

const loyaltyProgress = computed(() => {
  if (loyaltyTier.value === 'Regular') {
    return Math.min((totalSpent.value / 500) * 100, 100)
  }

  if (loyaltyTier.value === 'Silver VIP') {
    return Math.min(
      ((totalSpent.value - 500) / 500) * 100,
      100
    )
  }

  if (loyaltyTier.value === 'Gold VIP') {
    return Math.min(
      ((totalSpent.value - 1000) / 1000) * 100,
      100
    )
  }

  return 100
})

const profileCompleteness = computed(() => {
  if (!profileUser.value) return 0

  let score = 0

  if (profileUser.value.username) score += 25
  if (profileUser.value.email) score += 25
  if (profileUser.value.phone) score += 25
  if (profileUser.value.avatar) score += 25

  return score
})

const avatarUrl = computed(() => {
  if (!profileUser.value?.avatar) return ''

  const avatar = profileUser.value.avatar

  return avatar.startsWith('http')
    ? avatar
    : `${apiBase.value}${avatar}`
})

const previewAvatarUrl = ref('')

/* ---------------------------------------
   HELPERS
--------------------------------------- */

const resolveImageUrl = (imagePath?: string) => {
  if (!imagePath) return ''
  if (imagePath.startsWith('http')) return imagePath
  return `${apiBase.value}${imagePath}`
}

const formatCurrency = (amount: number) => {
  return `$${Number(amount || 0).toFixed(2)}`
}

const formatDate = (date?: string) => {
  if (!date) return 'Recently'

  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const formatDateTime = (date?: string) => {
  if (!date) return ''

  return new Date(date).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  })
}

const statusBadgeClass = (status: string) => {
  switch (status?.toLowerCase()) {
    case 'pending':
      return 'bg-amber-50 text-amber-700 border-amber-200'

    case 'preparing':
      return 'bg-blue-50 text-blue-700 border-blue-200'

    case 'ready':
      return 'bg-emerald-50 text-emerald-700 border-emerald-200'

    case 'delivered':
    case 'completed':
      return 'bg-stone-100 text-stone-600 border-stone-200'

    case 'cancelled':
      return 'bg-rose-50 text-rose-700 border-rose-200'

    default:
      return 'bg-stone-100 text-stone-600 border-stone-200'
  }
}

const tierBadgeClass = computed(() => {
  switch (loyaltyTier.value) {
    case 'Platinum VIP':
      return 'bg-stone-950 text-amber-300 border-stone-700'

    case 'Gold VIP':
      return 'bg-amber-50 text-amber-800 border-amber-300'

    case 'Silver VIP':
      return 'bg-stone-100 text-stone-700 border-stone-300'

    default:
      return 'bg-white/10 text-white border-white/20'
  }
})

const orderTypeLabel = (order: Order) => {
  if (!order.order_type) return 'Restaurant Order'

  return order.order_type.charAt(0).toUpperCase() +
    order.order_type.slice(1)
}

/* ---------------------------------------
   AVATAR
--------------------------------------- */

watch(
  () => editForm.value.avatar,
  file => {
    if (previewAvatarUrl.value) {
      URL.revokeObjectURL(previewAvatarUrl.value)
      previewAvatarUrl.value = ''
    }

    if (file) {
      previewAvatarUrl.value = URL.createObjectURL(file)
    }
  }
)

watch(isEditing, open => {
  if (!open && previewAvatarUrl.value) {
    URL.revokeObjectURL(previewAvatarUrl.value)
    previewAvatarUrl.value = ''
  }
})

/* ---------------------------------------
   FETCH PROFILE
--------------------------------------- */

async function fetchProfile() {
  if (!token.value) return

  try {
    const response = await $fetch<{ user: ProfileUser }>('/me', {
      baseURL: apiBase.value,
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })

    profileUser.value = response.user
  } catch {
    error.value = 'Failed to load profile'
  }
}

/* ---------------------------------------
   FETCH ORDERS
--------------------------------------- */

async function fetchOrders() {
  if (!token.value) return

  try {
    const response = await $fetch<Order[]>('/orders', {
      baseURL: apiBase.value,
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })

    orders.value = response || []
  } catch {
    error.value = 'Failed to load orders'
  } finally {
    loading.value = false
  }
}

/* ---------------------------------------
   FETCH RESERVATIONS
--------------------------------------- */

async function fetchReservations() {
  if (!token.value) return

  reservationsLoading.value = true

  try {
    const response = await $fetch<
      Reservation[] | { reservations?: Reservation[] }
    >('/reservations', {
      baseURL: apiBase.value,
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })

    reservations.value = (
      Array.isArray(response)
        ? response
        : response.reservations || []
    )
      .filter(item => item.status?.toLowerCase() !== 'cancelled')
      .slice(0, 3)
  } catch {
    reservations.value = []
  } finally {
    reservationsLoading.value = false
  }
}

/* ---------------------------------------
   EDIT PROFILE
--------------------------------------- */

function openEdit() {
  if (!profileUser.value) return

  editForm.value = {
    username: profileUser.value.username,
    email: profileUser.value.email,
    phone: profileUser.value.phone || '',
    currentPassword: '',
    newPassword: '',
    confirmNewPassword: '',
    avatar: null
  }

  editMessage.value = ''
  editSuccess.value = false
  isEditing.value = true
}

function onAvatarSelect(event: Event) {
  const target = event.target as HTMLInputElement

  if (target.files?.[0]) {
    editForm.value.avatar = target.files[0]
  }
}

async function saveProfile() {
  editMessage.value = ''
  editSuccess.value = false

  if (
    !editForm.value.username.trim() ||
    !editForm.value.email.trim()
  ) {
    editMessage.value = 'Username and email are required.'
    return
  }

  if (
    editForm.value.newPassword &&
    editForm.value.newPassword !== editForm.value.confirmNewPassword
  ) {
    editMessage.value = 'New passwords do not match.'
    return
  }

  if (
    editForm.value.newPassword &&
    editForm.value.newPassword.length < 6
  ) {
    editMessage.value =
      'New password must be at least 6 characters.'
    return
  }

  try {
    isUploadingAvatar.value = true

    const body: Record<string, string> = {
      username: editForm.value.username,
      email: editForm.value.email,
      phone: editForm.value.phone
    }

    if (
      editForm.value.currentPassword &&
      editForm.value.newPassword
    ) {
      body.currentPassword = editForm.value.currentPassword
      body.newPassword = editForm.value.newPassword
    }

    await $fetch('/me', {
      baseURL: apiBase.value,
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${token.value}`,
        'Content-Type': 'application/json'
      },
      body
    })

    if (editForm.value.avatar) {
      const formData = new FormData()

      formData.append(
        'avatar',
        editForm.value.avatar
      )

      await $fetch('/me/avatar', {
        baseURL: apiBase.value,
        method: 'PATCH',
        headers: {
          Authorization: `Bearer ${token.value}`
        },
        body: formData
      })
    }

    await fetchProfile()

    if (user.value && profileUser.value) {
      user.value.username = profileUser.value.username
      user.value.email = profileUser.value.email
      user.value.phone = profileUser.value.phone
      user.value.avatar = profileUser.value.avatar

      if (import.meta.client) {
        localStorage.setItem(
          'auth-user',
          JSON.stringify(profileUser.value)
        )
      }
    }

    isEditing.value = false
    editSuccess.value = true
    editMessage.value =
      'Profile updated successfully!'
  } catch (e: any) {
    editMessage.value =
      e?.data?.message ||
      'Failed to update profile.'

    editSuccess.value = false
  } finally {
    isUploadingAvatar.value = false
  }
}

/* ---------------------------------------
   LOGOUT
--------------------------------------- */

function handleLogout() {
  logout()
  router.push('/login')
}

/* ---------------------------------------
   MOUNT
--------------------------------------- */

onMounted(async () => {
  if (user.value) {
    await Promise.all([
      fetchProfile(),
      fetchOrders(),
      fetchReservations()
    ])
  } else {
    await navigateTo('/login')
  }
})
</script>

<template>
  <Navbar />

  <div
    class="min-h-screen bg-[#FDFBF7] text-stone-800 overflow-x-hidden"
  >

    <!-- =========================================
         HERO
    ========================================== -->
    <section
      class="relative overflow-hidden bg-stone-950 text-white"
    >
      <div class="absolute inset-0">
        <img
          src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=2000&q=80"
          alt="Restaurant"
          class="w-full h-full object-cover opacity-20"
        />

        <div
          class="absolute inset-0 bg-gradient-to-b from-stone-950/70 via-stone-950/80 to-stone-950"
        />
      </div>

      <div
        class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-28"
      >
        <div class="max-w-3xl">

          <p
            class="text-[11px] uppercase tracking-[0.35em] text-[#C59237] font-semibold mb-5"
          >
            FLAVORIA · Your Account
          </p>

          <h1
            class="font-serif text-4xl sm:text-5xl md:text-6xl font-normal tracking-wide"
          >
            Your dining journey.
          </h1>

          <p
            class="mt-5 max-w-xl text-stone-300 text-sm sm:text-base font-sans leading-relaxed"
          >
            Manage your profile, discover your rewards,
            track your orders and keep your reservations
            close at hand.
          </p>

        </div>
      </div>
    </section>


    <!-- =========================================
         MAIN CONTENT
    ========================================== -->
    <main
      class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-16 pb-20"
    >

      <!-- Loading -->
      <div
        v-if="loading"
        class="bg-white rounded-2xl border border-stone-200 shadow-xl p-20 text-center"
      >
        <div
          class="inline-block h-10 w-10 rounded-full border-2 border-stone-200 border-t-[#C59237] animate-spin"
        />

        <p class="mt-5 text-sm text-stone-500 font-sans">
          Preparing your profile...
        </p>
      </div>


      <!-- Error -->
      <div
        v-else-if="error"
        class="bg-white rounded-2xl border border-rose-200 shadow-xl p-12 text-center"
      >
        <div
          class="mx-auto w-14 h-14 rounded-full bg-rose-50 flex items-center justify-center text-rose-500"
        >
          !
        </div>

        <p class="mt-4 text-rose-600 font-sans">
          {{ error }}
        </p>
      </div>


      <!-- Profile -->
      <div
        v-else-if="profileUser"
        class="space-y-7"
      >

        <!-- =====================================
             PROFILE CARD
        ====================================== -->
        <section
          class="bg-white rounded-2xl border border-stone-200 shadow-xl overflow-hidden"
        >

          <div
            class="bg-stone-950 px-5 sm:px-8 py-7"
          >
            <div
              class="flex flex-col sm:flex-row sm:items-center gap-6"
            >

              <!-- Avatar -->
              <div class="relative shrink-0">

                <div
                  class="w-28 h-28 sm:w-32 sm:h-32 rounded-full overflow-hidden border-4 border-[#C59237] bg-[#C59237] flex items-center justify-center shadow-lg"
                >

                  <img
                    v-if="avatarUrl"
                    :src="avatarUrl"
                    alt="Profile"
                    class="w-full h-full object-cover"
                  />

                  <span
                    v-else
                    class="text-4xl sm:text-5xl font-serif font-bold text-white"
                  >
                    {{
                      profileUser.username
                        ?.charAt(0)
                        .toUpperCase() || 'U'
                    }}
                  </span>

                </div>

                <button
                  type="button"
                  @click="openEdit"
                  class="absolute bottom-0 right-0 w-9 h-9 rounded-full bg-[#C59237] hover:bg-[#b0802c] border-4 border-stone-950 text-white flex items-center justify-center transition"
                  title="Edit Profile"
                >
                  ✎
                </button>

              </div>


              <!-- Information -->
              <div class="flex-1">

                <div
                  class="flex flex-wrap items-center gap-3"
                >
                  <h2
                    class="text-2xl sm:text-3xl font-serif text-white"
                  >
                    {{ profileUser.username }}
                  </h2>

                  <span
                    :class="[
                      'px-3 py-1 rounded-full border text-[9px] font-bold uppercase tracking-wider',
                      tierBadgeClass
                    ]"
                  >
                    {{ loyaltyTier }}
                  </span>
                </div>

                <div
                  class="mt-3 flex flex-col sm:flex-row sm:flex-wrap gap-2 sm:gap-5 text-xs text-stone-400 font-sans"
                >
                  <span>
                    ✉ {{ profileUser.email }}
                  </span>

                  <span>
                    ☎ {{ profileUser.phone || 'Phone not provided' }}
                  </span>
                </div>

                <!-- Profile progress -->
                <div class="mt-6 max-w-md">

                  <div
                    class="flex items-center justify-between mb-2"
                  >
                    <span
                      class="text-[9px] uppercase tracking-widest text-stone-500 font-semibold"
                    >
                      Profile completeness
                    </span>

                    <span
                      class="text-[10px] text-[#C59237] font-bold"
                    >
                      {{ profileCompleteness }}%
                    </span>
                  </div>

                  <div
                    class="h-1.5 bg-stone-800 rounded-full overflow-hidden"
                  >
                    <div
                      class="h-full bg-[#C59237] transition-all"
                      :style="{
                        width: `${profileCompleteness}%`
                      }"
                    />
                  </div>

                </div>

              </div>


              <!-- Actions -->
              <div
                class="flex sm:flex-row gap-2"
              >
                <button
                  type="button"
                  @click="openEdit"
                  class="flex-1 sm:flex-none px-5 py-2.5 border border-stone-700 hover:border-[#C59237] text-stone-200 hover:text-[#C59237] rounded-lg text-[10px] font-bold uppercase tracking-wider transition"
                >
                  Edit Profile
                </button>

                <button
                  type="button"
                  @click="handleLogout"
                  class="hidden sm:inline-flex px-5 py-2.5 text-rose-400 hover:text-rose-300 rounded-lg text-[10px] font-bold uppercase tracking-wider transition"
                >
                  Logout
                </button>

                <button
                  type="button"
                  @click="handleLogout"
                  class="sm:hidden p-2 rounded-full bg-stone-800 hover:bg-stone-700 text-rose-400 hover:text-rose-300 transition"
                  aria-label="Logout"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 11-2 2v-1m0-11V5a2 2 0 1 1 2-2v1m0 0h.01M9 5a3 3 0 1 1 6 0v1H9z"></path>
                  </svg>
                </button>
              </div>

            </div>
          </div>

        </section>


        <!-- =====================================
             STATISTICS
        ====================================== -->
        <section
          class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4"
        >

          <div
            class="bg-white rounded-xl border border-stone-200 p-5 shadow-sm"
          >
            <p
              class="text-[9px] uppercase tracking-widest text-stone-400 font-bold"
            >
              Total Orders
            </p>

            <p
              class="mt-2 text-3xl font-serif text-stone-900"
            >
              {{ totalOrders }}
            </p>

            <p
              class="mt-1 text-xs text-stone-400 font-sans"
            >
              Lifetime orders
            </p>
          </div>


          <div
            class="bg-white rounded-xl border border-stone-200 p-5 shadow-sm"
          >
            <p
              class="text-[9px] uppercase tracking-widest text-stone-400 font-bold"
            >
              Total Spent
            </p>

            <p
              class="mt-2 text-3xl font-serif text-[#C59237]"
            >
              {{ formatCurrency(totalSpent) }}
            </p>

            <p
              class="mt-1 text-xs text-stone-400 font-sans"
            >
              Dining investment
            </p>
          </div>


          <div
            class="bg-white rounded-xl border border-stone-200 p-5 shadow-sm"
          >
            <p
              class="text-[9px] uppercase tracking-widest text-stone-400 font-bold"
            >
              Active Orders
            </p>

            <p
              class="mt-2 text-3xl font-serif text-stone-900"
            >
              {{ activeOrders.length }}
            </p>

            <p
              class="mt-1 text-xs text-stone-400 font-sans"
            >
              Currently in progress
            </p>
          </div>


          <div
            class="bg-stone-950 rounded-xl border border-stone-800 p-5 shadow-sm"
          >
            <p
              class="text-[9px] uppercase tracking-widest text-stone-500 font-bold"
            >
              Loyalty Points
            </p>

            <p
              class="mt-2 text-3xl font-serif text-[#C59237]"
            >
              {{ loyaltyPoints.toLocaleString() }}
            </p>

            <p
              class="mt-1 text-xs text-stone-500 font-sans"
            >
              Earn more with every order
            </p>
          </div>

        </section>


        <!-- =====================================
             LOYALTY + RESERVATIONS
        ====================================== -->
        <section
          class="grid grid-cols-1 lg:grid-cols-2 gap-6"
        >

          <!-- Loyalty -->
          <div
            class="relative overflow-hidden bg-gradient-to-br from-stone-950 to-stone-800 rounded-2xl p-7 text-white"
          >

            <div
              class="absolute -right-16 -top-16 w-40 h-40 rounded-full border border-[#C59237]/20"
            />

            <div
              class="absolute -right-10 -top-10 w-28 h-28 rounded-full border border-[#C59237]/10"
            />

            <div class="relative">

              <div
                class="flex items-center justify-between"
              >
                <div>
                  <p
                    class="text-[9px] uppercase tracking-[0.3em] text-[#C59237] font-bold"
                  >
                    FLAVORIA REWARDS
                  </p>

                  <h3
                    class="mt-2 text-2xl font-serif"
                  >
                    {{ loyaltyTier }}
                  </h3>
                </div>

                <div
                  class="w-12 h-12 rounded-full border border-[#C59237]/40 flex items-center justify-center text-[#C59237] text-xl"
                >
                  ✦
                </div>
              </div>


              <div class="mt-8">

                <div
                  class="flex items-end justify-between"
                >
                  <div>
                    <p
                      class="text-3xl font-serif text-[#C59237]"
                    >
                      {{ loyaltyPoints.toLocaleString() }}
                    </p>

                    <p
                      class="text-[9px] uppercase tracking-widest text-stone-500"
                    >
                      Points
                    </p>
                  </div>

                  <p
                    v-if="nextTier.amount > 0"
                    class="text-xs text-stone-400"
                  >
                    {{ formatCurrency(nextTier.amount) }}
                    to {{ nextTier.name }}
                  </p>

                  <p
                    v-else
                    class="text-xs text-[#C59237]"
                  >
                    Highest tier reached
                  </p>
                </div>


                <div class="mt-4">

                  <div
                    class="h-2 bg-white/10 rounded-full overflow-hidden"
                  >
                    <div
                      class="h-full bg-[#C59237] rounded-full transition-all"
                      :style="{
                        width: `${loyaltyProgress}%`
                      }"
                    />
                  </div>

                  <div
                    class="mt-2 flex justify-between text-[9px] uppercase tracking-wider text-stone-500"
                  >
                    <span>{{ loyaltyTier }}</span>
                    <span>{{ nextTier.name }}</span>
                  </div>

                </div>

              </div>

            </div>
          </div>


          <!-- Reservations -->
          <div
            class="bg-white rounded-2xl border border-stone-200 p-7"
          >

            <div
              class="flex items-start justify-between"
            >
              <div>
                <p
                  class="text-[9px] uppercase tracking-[0.3em] text-[#C59237] font-bold"
                >
                  YOUR TABLE
                </p>

                <h3
                  class="mt-2 text-2xl font-serif text-stone-900"
                >
                  Upcoming Reservations
                </h3>
              </div>

              <div
                class="w-10 h-10 rounded-full bg-[#C59237]/10 flex items-center justify-center text-[#C59237]"
              >
                ♢
              </div>
            </div>


            <div
              v-if="reservationsLoading"
              class="py-8 text-center text-xs text-stone-400"
            >
              Loading reservations...
            </div>


            <div
              v-else-if="reservations.length === 0"
              class="py-8"
            >
              <p
                class="text-sm text-stone-500 font-sans"
              >
                No upcoming reservations.
              </p>

              <NuxtLink
                to="/reservation"
                class="inline-block mt-4 text-[10px] uppercase tracking-widest font-bold text-[#C59237] hover:text-[#b0802c]"
              >
                Make a Reservation →
              </NuxtLink>
            </div>


            <div
              v-else
              class="mt-6 space-y-3"
            >

              <div
                v-for="reservation in reservations"
                :key="reservation.id"
                class="flex items-center gap-4 p-4 bg-[#FDFBF7] rounded-xl border border-stone-100"
              >

                <div
                  class="w-11 h-11 shrink-0 rounded-lg bg-stone-950 text-[#C59237] flex items-center justify-center"
                >
                  ♢
                </div>

                <div class="min-w-0 flex-1">

                  <p
                    class="text-sm font-semibold text-stone-900 font-sans"
                  >
                    {{ formatDateTime(reservation.date_time) }}
                  </p>

                  <p
                    class="mt-1 text-xs text-stone-400 font-sans"
                  >
                    Table
                    {{ reservation.table_id || 'TBA' }}
                  </p>

                </div>

                <span
                  class="px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-100 text-emerald-600 text-[8px] uppercase tracking-wider font-bold"
                >
                  {{ reservation.status }}
                </span>

              </div>

            </div>

          </div>

        </section>


        <!-- =====================================
             CURRENT ORDER
        ====================================== -->
        <section v-if="currentOrder">

          <div class="flex items-end justify-between mb-4">

            <div>
              <p
                class="text-[9px] uppercase tracking-[0.3em] text-[#C59237] font-bold"
              >
                LIVE ORDER
              </p>

              <h2
                class="mt-1 text-3xl font-serif text-stone-900"
              >
                Your current order
              </h2>
            </div>

          </div>


          <div
            class="bg-white rounded-2xl border border-stone-200 shadow-sm overflow-hidden"
          >

            <div
              class="bg-stone-950 px-6 py-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
            >

              <div
                class="flex items-center gap-3"
              >
                <span
                  class="font-mono text-xs text-stone-400"
                >
                  ORDER #{{ String(currentOrder.id).padStart(4, '0') }}
                </span>

                <span
                  :class="[
                    'px-3 py-1 rounded-full border text-[9px] font-bold uppercase tracking-wider',
                    statusBadgeClass(currentOrder.status)
                  ]"
                >
                  {{ currentOrder.status }}
                </span>
              </div>

              <span
                class="text-xl font-serif text-[#C59237]"
              >
                {{ formatCurrency(currentOrder.total_price) }}
              </span>

            </div>


            <div class="p-6">

              <div
                class="grid grid-cols-1 md:grid-cols-[1fr_auto] gap-6"
              >

                <div class="space-y-3">

                  <div
                    v-for="item in currentOrder.items"
                    :key="item.id"
                    class="flex items-center gap-4"
                  >

                    <div
                      class="w-12 h-12 rounded-lg overflow-hidden bg-stone-100 shrink-0"
                    >

                      <img
                        v-if="item.product_image"
                        :src="resolveImageUrl(item.product_image)"
                        :alt="item.product_name || 'Product'"
                        class="w-full h-full object-cover"
                      />

                      <div
                        v-else
                        class="w-full h-full flex items-center justify-center text-stone-400"
                      >
                        🍽
                      </div>

                    </div>

                    <div class="flex-1">

                      <p
                        class="text-sm font-semibold text-stone-800 font-sans"
                      >
                        {{ item.product_name || `Product #${item.product_id}` }}
                      </p>

                      <p
                        class="text-xs text-stone-400 mt-1 font-sans"
                      >
                        Quantity: {{ item.quantity }}
                      </p>

                    </div>

                    <span
                      class="text-sm font-mono text-stone-700"
                    >
                      {{ formatCurrency(item.price * item.quantity) }}
                    </span>

                  </div>

                </div>


                <div
                  class="md:text-right flex md:block items-center justify-between border-t md:border-t-0 md:border-l border-stone-100 pt-5 md:pt-0 md:pl-8"
                >

                  <div>
                    <p
                      class="text-[9px] uppercase tracking-widest text-stone-400 font-bold"
                    >
                      Order Type
                    </p>

                    <p
                      class="mt-1 text-sm text-stone-700 font-sans"
                    >
                      {{ orderTypeLabel(currentOrder) }}
                    </p>
                  </div>

                  <div class="mt-0 md:mt-5">
                    <p
                      class="text-[9px] uppercase tracking-widest text-stone-400 font-bold"
                    >
                      Ordered
                    </p>

                    <p
                      class="mt-1 text-sm text-stone-700 font-sans"
                    >
                      {{ formatDate(currentOrder.created_at) }}
                    </p>
                  </div>

                </div>

              </div>

            </div>

          </div>

        </section>


        <!-- =====================================
             ORDER HISTORY
        ====================================== -->
        <section>

          <div
            class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-3 mb-5"
          >

            <div>
              <p
                class="text-[9px] uppercase tracking-[0.3em] text-[#C59237] font-bold"
              >
                ORDER HISTORY
              </p>

              <h2
                class="mt-1 text-3xl font-serif text-stone-900"
              >
                Your Orders
              </h2>
            </div>

            <NuxtLink
              to="/menu"
              class="text-[10px] uppercase tracking-widest font-bold text-[#C59237] hover:text-[#b0802c]"
            >
              Browse Menu →
            </NuxtLink>

          </div>


          <!-- Empty -->
          <div
            v-if="orders.length === 0"
            class="bg-white rounded-2xl border border-stone-200 p-14 text-center"
          >

            <div
              class="mx-auto w-16 h-16 rounded-full bg-stone-100 flex items-center justify-center text-2xl"
            >
              🍽
            </div>

            <h3
              class="mt-5 text-xl font-serif text-stone-900"
            >
              Your table is waiting.
            </h3>

            <p
              class="mt-2 text-sm text-stone-500 font-sans"
            >
              You haven't placed any orders yet.
            </p>

            <NuxtLink
              to="/menu"
              class="inline-block mt-6 px-6 py-3 bg-[#C59237] hover:bg-[#b0802c] text-white rounded-lg text-[10px] uppercase tracking-widest font-bold transition"
            >
              Explore Our Menu
            </NuxtLink>

          </div>


          <!-- Orders -->
          <div
            v-else
            class="space-y-4"
          >

            <article
              v-for="order in orders"
              :key="order.id"
              class="bg-white rounded-2xl border border-stone-200 overflow-hidden hover:border-stone-300 transition"
            >

              <!-- Order Header -->
              <div
                class="px-5 sm:px-6 py-4 border-b border-stone-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3"
              >

                <div
                  class="flex flex-wrap items-center gap-3"
                >

                  <span
                    class="font-mono text-[11px] font-bold text-stone-500"
                  >
                    #{{ String(order.id).padStart(4, '0') }}
                  </span>

                  <span
                    :class="[
                      'px-2.5 py-1 rounded-full border text-[9px] font-bold uppercase tracking-wider',
                      statusBadgeClass(order.status)
                    ]"
                  >
                    {{ order.status }}
                  </span>

                  <span
                    v-if="order.order_type"
                    class="text-[10px] text-stone-400 font-sans"
                  >
                    {{ orderTypeLabel(order) }}
                  </span>

                </div>

                <div
                  class="flex items-center justify-between sm:justify-end gap-5"
                >

                  <span
                    class="text-xs text-stone-400 font-sans"
                  >
                    {{ formatDate(order.created_at) }}
                  </span>

                  <span
                    class="text-lg font-serif font-bold text-stone-900"
                  >
                    {{ formatCurrency(order.total_price) }}
                  </span>

                </div>

              </div>


              <!-- Items -->
              <div class="p-5 sm:p-6">

                <div class="space-y-3">

                  <div
                    v-for="item in order.items"
                    :key="item.id"
                    class="flex items-center gap-3"
                  >

                    <div
                      class="w-10 h-10 rounded-lg overflow-hidden bg-stone-100 shrink-0"
                    >

                      <img
                        v-if="item.product_image"
                        :src="resolveImageUrl(item.product_image)"
                        :alt="item.product_name || 'Product'"
                        class="w-full h-full object-cover"
                      />

                      <div
                        v-else
                        class="w-full h-full flex items-center justify-center text-stone-400 text-sm"
                      >
                        🍽
                      </div>

                    </div>

                    <div class="flex-1 min-w-0">

                      <p
                        class="text-sm text-stone-700 font-sans truncate"
                      >
                        {{ item.product_name || `Product #${item.product_id}` }}
                      </p>

                      <p
                        class="text-[11px] text-stone-400 font-sans"
                      >
                        Qty {{ item.quantity }}
                      </p>

                    </div>

                    <span
                      class="text-xs font-mono text-stone-600"
                    >
                      {{ formatCurrency(item.price * item.quantity) }}
                    </span>

                  </div>

                </div>


                <!-- Extra info -->
                <div
                  class="mt-5 pt-5 border-t border-stone-100 grid grid-cols-1 sm:grid-cols-3 gap-4"
                >

                  <div v-if="order.payment_method">

                    <p
                      class="text-[8px] uppercase tracking-widest text-stone-400 font-bold"
                    >
                      Payment
                    </p>

                    <p
                      class="mt-1 text-xs text-stone-600 font-sans"
                    >
                      {{ order.payment_method }}
                    </p>

                  </div>


                  <div v-if="order.table_number">

                    <p
                      class="text-[8px] uppercase tracking-widest text-stone-400 font-bold"
                    >
                      Table
                    </p>

                    <p
                      class="mt-1 text-xs text-stone-600 font-sans"
                    >
                      {{ order.table_number }}
                    </p>

                  </div>


                  <div v-if="order.delivery_address">

                    <p
                      class="text-[8px] uppercase tracking-widest text-stone-400 font-bold"
                    >
                      Delivery
                    </p>

                    <p
                      class="mt-1 text-xs text-stone-600 font-sans truncate"
                    >
                      {{ order.delivery_address }}
                    </p>

                  </div>

                </div>

              </div>

            </article>

          </div>

        </section>

      </div>

    </main>


    <!-- =========================================
         EDIT PROFILE MODAL
    ========================================== -->
    <div
      v-if="isEditing"
      class="fixed inset-0 z-50 flex items-center justify-center bg-stone-950/70 backdrop-blur-sm p-4"
      @click.self="isEditing = false"
    >

      <div
        class="bg-white w-full max-w-lg max-h-[90vh] overflow-y-auto rounded-2xl shadow-2xl"
      >

        <!-- Modal Header -->
        <div
          class="sticky top-0 z-10 bg-white border-b border-stone-100 px-6 py-5 flex items-center justify-between"
        >

          <div>
            <p
              class="text-[9px] uppercase tracking-[0.25em] text-[#C59237] font-bold"
            >
              MY ACCOUNT
            </p>

            <h3
              class="mt-1 text-xl font-serif text-stone-900"
            >
              Edit Profile
            </h3>
          </div>

          <button
            type="button"
            @click="isEditing = false"
            class="w-9 h-9 rounded-full hover:bg-stone-100 text-stone-400 hover:text-stone-800 transition"
          >
            ✕
          </button>

        </div>


        <form
          @submit.prevent="saveProfile"
          class="p-6 space-y-5"
        >

          <!-- Message -->
          <div
            v-if="editMessage"
            :class="[
              'px-4 py-3 rounded-lg text-xs font-sans text-center border',
              editSuccess
                ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                : 'bg-amber-50 text-amber-700 border-amber-200'
            ]"
          >
            {{ editMessage }}
          </div>


          <!-- Avatar -->
          <div class="flex justify-center">

            <div class="relative">

              <div
                class="w-24 h-24 rounded-full overflow-hidden bg-stone-100 border-2 border-[#C59237] flex items-center justify-center"
              >

                <img
                  v-if="editForm.avatar"
                  :src="previewAvatarUrl"
                  alt="Avatar preview"
                  class="w-full h-full object-cover"
                />

                <img
                  v-else-if="avatarUrl"
                  :src="avatarUrl"
                  alt="Avatar"
                  class="w-full h-full object-cover"
                />

                <span
                  v-else
                  class="text-3xl font-serif font-bold text-stone-500"
                >
                  {{
                    editForm.username
                      ?.charAt(0)
                      .toUpperCase() || 'U'
                  }}
                </span>

              </div>

              <label
                class="absolute bottom-0 right-0 w-8 h-8 rounded-full bg-[#C59237] hover:bg-[#b0802c] text-white flex items-center justify-center cursor-pointer border-4 border-white transition"
              >
                📷

                <input
                  type="file"
                  accept="image/jpeg,image/png,image/webp,image/gif"
                  @change="onAvatarSelect"
                  class="hidden"
                />
              </label>

            </div>

          </div>


          <!-- Username -->
          <div>

            <label
              class="block mb-2 text-[10px] uppercase tracking-widest font-bold text-stone-500"
            >
              Username
            </label>

            <input
              v-model="editForm.username"
              type="text"
              placeholder="Your username"
              required
              class="w-full rounded-lg border border-stone-200 bg-[#FDFBF7] px-4 py-3 text-sm text-stone-900 focus:border-[#C59237] focus:bg-white focus:outline-none transition"
            />

          </div>


          <!-- Email -->
          <div>

            <label
              class="block mb-2 text-[10px] uppercase tracking-widest font-bold text-stone-500"
            >
              Email Address
            </label>

            <input
              v-model="editForm.email"
              type="email"
              placeholder="your@email.com"
              required
              class="w-full rounded-lg border border-stone-200 bg-[#FDFBF7] px-4 py-3 text-sm text-stone-900 focus:border-[#C59237] focus:bg-white focus:outline-none transition"
            />

          </div>


          <!-- Phone -->
          <div>

            <label
              class="block mb-2 text-[10px] uppercase tracking-widest font-bold text-stone-500"
            >
              Phone Number
            </label>

            <input
              v-model="editForm.phone"
              type="tel"
              placeholder="+855 12 345 678"
              class="w-full rounded-lg border border-stone-200 bg-[#FDFBF7] px-4 py-3 text-sm text-stone-900 focus:border-[#C59237] focus:bg-white focus:outline-none transition"
            />

          </div>


          <!-- Password -->
          <div
            class="border-t border-stone-100 pt-5"
          >

            <p
              class="text-sm font-serif text-stone-900"
            >
              Change Password
            </p>

            <p
              class="mt-1 text-xs text-stone-400 font-sans"
            >
              Leave these fields empty if you don't want to change your password.
            </p>


            <div class="mt-4 space-y-3">

              <input
                v-model="editForm.currentPassword"
                type="password"
                placeholder="Current password"
                class="w-full rounded-lg border border-stone-200 bg-[#FDFBF7] px-4 py-3 text-sm focus:border-[#C59237] focus:bg-white focus:outline-none"
              />

              <input
                v-model="editForm.newPassword"
                type="password"
                placeholder="New password"
                class="w-full rounded-lg border border-stone-200 bg-[#FDFBF7] px-4 py-3 text-sm focus:border-[#C59237] focus:bg-white focus:outline-none"
              />

              <input
                v-model="editForm.confirmNewPassword"
                type="password"
                placeholder="Confirm new password"
                class="w-full rounded-lg border border-stone-200 bg-[#FDFBF7] px-4 py-3 text-sm focus:border-[#C59237] focus:bg-white focus:outline-none"
              />

            </div>

          </div>


          <!-- Buttons -->
          <div
            class="flex gap-3 pt-2"
          >

            <button
              type="button"
              @click="isEditing = false"
              class="flex-1 px-5 py-3 rounded-lg border border-stone-200 text-stone-600 hover:bg-stone-50 text-[10px] uppercase tracking-widest font-bold transition"
            >
              Cancel
            </button>

            <button
              type="submit"
              :disabled="isUploadingAvatar"
              class="flex-1 px-5 py-3 rounded-lg bg-[#C59237] hover:bg-[#b0802c] text-white text-[10px] uppercase tracking-widest font-bold transition disabled:opacity-50"
            >
              {{
                isUploadingAvatar
                  ? 'Saving...'
                  : 'Save Changes'
              }}
            </button>

          </div>

        </form>

      </div>

    </div>

  </div>
</template>