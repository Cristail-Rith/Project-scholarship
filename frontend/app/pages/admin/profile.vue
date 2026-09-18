<script setup lang="ts">
import { ref, computed, onMounted } from "vue"

import AdminSidebar from "~/components/AdminSidebar.vue"
import { useAuth } from "~/composables/useAuth"
import { useRuntimeConfig } from "#imports"

interface AdminUser {
  name: string
  role: string
  email: string
  phone: string
  avatar: string
  joinedDate: string
  permissions: string[]
}

// Tab navigation state
const activeTab = ref<"overview" | "settings" | "security">("overview")

const { user, token } = useAuth()
const config = useRuntimeConfig()

// Password form state
const currentPassword = ref("")
const newPassword = ref("")
const confirmPassword = ref("")

// Profile state
const admin = ref<AdminUser>({
  name: "",
  role: "",
  email: "",
  phone: "",
  avatar: "",
  joinedDate: "January 2025",
  permissions: [
    "Menu & Pricing Management",
    "POS System Override",
    "Financial Reports & Sales Data",
    "Staff Access & User Roles",
  ],
})

// Metrics Overview
const stats = ref([
  { label: "Today's Revenue", value: "$2,450.00", change: "+12.5%" },
  { label: "Total Orders", value: "148", change: "+8.2%" },
  { label: "Active Tables", value: "18 / 24", change: "75% Capacity" },
  { label: "Pending Orders", value: "6", change: "Normal Traffic" },
])

// System Activity Logs
const activityLogs = ref([
  {
    action: "Updated Menu Price",
    detail: "Prime Angus Ribeye changed to $42.00",
    time: "10 mins ago",
  },
  {
    action: "System Backup",
    detail: "Database backup completed successfully",
    time: "1 hour ago",
  },
  {
    action: "Staff Role Modified",
    detail: "Granted POS access to Shift Supervisor",
    time: "3 hours ago",
  },
])

// Computed property to construct full avatar URL
const avatarUrl = computed(() => {
  if (!admin.value.avatar) return ""

  if (admin.value.avatar.startsWith("http")) {
    return admin.value.avatar
  }

  return config.public.apiBase + admin.value.avatar
})

// Load user data on client side
onMounted(async () => {
  if (user.value) {
    admin.value.name = user.value.username || ""
    admin.value.role =
      user.value.role === "admin"
        ? "Store Owner & General Manager"
        : "Admin"
    admin.value.email = user.value.email || ""
    admin.value.phone = user.value.phone || ""
    admin.value.avatar = user.value.avatar || ""
  }

  try {
    const res = await $fetch<{ user: any }>("/me", {
      baseURL: config.public.apiBase,
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    })

    if (res.user) {
      admin.value.name = res.user.username || admin.value.name
      admin.value.email = res.user.email || admin.value.email
      admin.value.phone = res.user.phone || admin.value.phone
      admin.value.avatar = res.user.avatar || admin.value.avatar
      admin.value.role =
        res.user.role === "admin"
          ? "Store Owner & General Manager"
          : "Admin"
    }
  } catch (e) {
    console.error("Failed to fetch user data", e)
  }
})

// Upload avatar
const handleAvatarUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]

  if (!file) return

  const allowedTypes = [
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/gif",
  ]

  if (!allowedTypes.includes(file.type)) {
    alert("Please upload a JPG, PNG, WEBP, or GIF image under 5 MB")
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    alert("Image must be under 5 MB")
    return
  }

  try {
    const formData = new FormData()
    formData.append("avatar", file)

    const res = await $fetch<{ user: any }>("/me/avatar", {
      baseURL: config.public.apiBase,
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
      body: formData,
    })

    if (res.user) {
      admin.value.avatar = res.user.avatar
      alert("Profile picture updated successfully!")
    }
  } catch (error: any) {
    console.error("Avatar upload failed:", error)
    alert(
      error.data?.message ||
        "Failed to upload avatar. Please try again.",
    )
  }
}

// Save profile
const handleSave = async () => {
  try {
    const updateData = {
      username: admin.value.name,
      email: admin.value.email,
      phone: admin.value.phone,
    }

    const res = await $fetch<{ user: any }>("/me", {
      baseURL: config.public.apiBase,
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
      body: updateData,
    })

    if (res.user) {
      admin.value.name = res.user.username || admin.value.name
      admin.value.email = res.user.email || admin.value.email
      admin.value.phone = res.user.phone || admin.value.phone

      alert("Profile updated successfully!")
    }
  } catch (error: any) {
    console.error("Profile update failed:", error)

    alert(
      error.data?.message ||
        "Failed to update profile. Please try again.",
    )
  }
}

// Update password
const updatePassword = async () => {
  if (
    !currentPassword.value ||
    !newPassword.value ||
    !confirmPassword.value
  ) {
    alert("Please fill in all password fields")
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    alert("New passwords do not match")
    return
  }

  if (newPassword.value.length < 6) {
    alert("New password must be at least 6 characters")
    return
  }

  try {
    const res = await $fetch<{ user: any }>("/me", {
      baseURL: config.public.apiBase,
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
      body: {
        currentPassword: currentPassword.value,
        newPassword: newPassword.value,
      },
    })

    if (res.user) {
      currentPassword.value = ""
      newPassword.value = ""
      confirmPassword.value = ""

      alert("Password updated successfully!")
    }
  } catch (error: any) {
    console.error("Password update failed:", error)

    alert(
      error.data?.message ||
        "Failed to update password. Please try again.",
    )
  }
}
</script>

<template>
  <div class="flex min-h-screen bg-stone-50 relative">
    <!-- Fixed Custom Sidebar -->
    <AdminSidebar />

    <!-- Main Content Area -->
    <main class="flex-1 text-stone-800 font-sans py-10 ml-64  px-6 sm:px-8 lg:px-10 border-t-4 border-amber-500 overflow-y-auto scrollbar-thin scrollbar-thumb-stone-300 scrollbar-track-stone-100">
      <div class="max-w-6xl space-y-8">

        <!-- Header Section -->
        <div class="flex flex-col md:flex-row md:items-end justify-between border-b border-stone-200 pb-6 gap-4">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-amber-500"></span>
              <span class="text-amber-500 text-xs font-bold uppercase tracking-widest">System Administration</span>
            </div>
            <h1 class="text-3xl font-serif font-bold text-stone-900 uppercase tracking-tight">Admin Profile</h1>
          </div>

          <!-- Tab Controls -->
          <div class="flex items-center gap-2">
            <button 
              v-for="tab in (['overview', 'settings', 'security'] as const)" 
              :key="tab"
              @click="activeTab = tab"
              :class="activeTab === tab 
                ? 'bg-amber-500 text-white border-amber-500 shadow-xs' 
                : 'bg-white text-stone-600 border-stone-200 hover:border-amber-500 hover:text-amber-600'"
              class="px-5 py-2 border text-xs font-bold uppercase tracking-wider transition-all rounded-none"
            >
              {{ tab }}
            </button>
          </div>
        </div>

        <!-- System Metrics Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div 
            v-for="(stat, idx) in stats" 
            :key="idx"
            class="border border-stone-200 p-5 bg-white space-y-2 rounded-none hover:border-amber-500 transition-colors"
          >
            <span class="text-[10px] font-bold uppercase tracking-widest text-stone-400">{{ stat.label }}</span>
            <p class="text-2xl font-serif font-bold text-stone-900">{{ stat.value }}</p>
            <span class="inline-block bg-amber-500/10 text-amber-600 text-[10px] font-mono font-bold px-2 py-0.5 border border-amber-500/20">
              {{ stat.change }}
            </span>
          </div>
        </div>

        <!-- Layout Content Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

          <!-- Left Column: Admin Info Card (4 Cols) -->
          <div class="lg:col-span-4 space-y-6">
            
            <div class="border border-stone-200 bg-white p-6 space-y-6 text-center rounded-none">
              <div class="relative w-28 h-28 mx-auto border-2 border-stone-200 group">
                <label for="avatar-upload" class="cursor-pointer block w-full h-full">
                  <img :src="avatarUrl" :alt="admin.name" class="w-full h-full object-cover rounded-full" />
                  <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity rounded-full flex items-center justify-center">
                    <span class="text-white text-[10px] font-bold uppercase">Change</span>
                  </div>
                </label>
                <input 
                  id="avatar-upload"
                  type="file" 
                  accept="image/*" 
                  @change="handleAvatarUpload" 
                  class="hidden" 
                />
                <div class="absolute -bottom-2 -right-2 bg-amber-500 text-white text-[9px] font-black uppercase px-2 py-0.5 shadow-xs">
                  Active
                </div>
              </div>

              <div class="space-y-1">
                <h2 class="text-xl font-serif font-bold text-stone-900 uppercase tracking-wide">{{ admin.name }}</h2>
                <p class="text-xs font-bold text-amber-500 uppercase tracking-wider">{{ admin.role }}</p>
                <p class="text-[10px] text-stone-400 font-mono">Joined {{ admin.joinedDate }}</p>
              </div>

              <div class="border-t border-stone-100 pt-4 text-left space-y-2 text-xs text-stone-600">
                <p><strong class="uppercase text-[10px] text-stone-400 block font-sans">Email:</strong> {{ admin.email }}</p>
                <p><strong class="uppercase text-[10px] text-stone-400 block font-sans">Phone:</strong> {{ admin.phone }}</p>
              </div>
            </div>

            <!-- Granted Permissions -->
            <div class="border border-stone-200 bg-white p-6 space-y-3 rounded-none">
              <h3 class="text-xs font-bold uppercase tracking-widest text-stone-700 border-b border-stone-100 pb-2 flex items-center justify-between">
                <span>System Access</span>
                <span class="w-1.5 h-1.5 bg-amber-500"></span>
              </h3>
              <ul class="space-y-2">
                <li 
                  v-for="(perm, idx) in admin.permissions" 
                  :key="idx"
                  class="flex items-center gap-2 text-xs text-stone-600 font-medium"
                >
                  <span class="text-amber-500 font-bold">✓</span> {{ perm }}
                </li>
              </ul>
            </div>

          </div>

          <!-- Right Column: Workspace Tabs (8 Cols) -->
          <div class="lg:col-span-8 space-y-6">

            <!-- TAB 1: OVERVIEW -->
            <div v-if="activeTab === 'overview'" class="space-y-6">
              <div class="border border-stone-200 bg-white p-6 space-y-4 rounded-none">
                <h3 class="text-xs font-bold uppercase tracking-widest text-stone-700 border-b border-stone-100 pb-2">
                  Recent Activity Log
                </h3>

                <div class="divide-y divide-stone-100">
                  <div v-for="(log, idx) in activityLogs" :key="idx" class="py-3 flex justify-between items-start">
                    <div class="space-y-0.5">
                      <h4 class="text-xs font-bold uppercase text-stone-900">{{ log.action }}</h4>
                      <p class="text-xs text-stone-500">{{ log.detail }}</p>
                    </div>
                    <span class="text-[10px] font-mono text-stone-400 bg-stone-50 px-2 py-0.5 border border-stone-200">
                      {{ log.time }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Quick Operations -->
              <div class="border border-stone-200 bg-white p-6 space-y-3 rounded-none">
                <h3 class="text-xs font-bold uppercase tracking-widest text-stone-700 border-b border-stone-100 pb-2">
                  Quick Operations
                </h3>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <button class="p-3 border border-stone-200 bg-stone-50 hover:bg-amber-500 hover:text-white hover:border-amber-500 text-stone-700 text-xs font-bold uppercase tracking-wider text-left transition-colors rounded-none">
                    + Add Menu Item
                  </button>
                  <button class="p-3 border border-stone-200 bg-stone-50 hover:bg-amber-500 hover:text-white hover:border-amber-500 text-stone-700 text-xs font-bold uppercase tracking-wider text-left transition-colors rounded-none">
                    View Reports
                  </button>
                  <button class="p-3 border border-stone-200 bg-stone-50 hover:bg-amber-500 hover:text-white hover:border-amber-500 text-stone-700 text-xs font-bold uppercase tracking-wider text-left transition-colors rounded-none">
                    Manage Staff
                  </button>
                </div>
              </div>
            </div>

            <!-- TAB 2: SETTINGS -->
            <div v-if="activeTab === 'settings'" class="border border-stone-200 bg-white p-6 space-y-6 rounded-none">
              <h3 class="text-xs font-bold uppercase tracking-widest text-stone-700 border-b border-stone-100 pb-2">
                Edit Administrator Profile
              </h3>

              <form @submit.prevent="handleSave" class="space-y-4">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div class="space-y-1">
                    <label class="text-[10px] font-bold uppercase tracking-wider text-stone-400">Full Name</label>
                    <input 
                      v-model="admin.name" 
                      type="text" 
                      class="w-full border border-stone-200 bg-stone-50 p-2.5 text-xs text-stone-900 focus:outline-none focus:border-amber-500 focus:bg-white rounded-none transition-colors"
                    />
                  </div>

                  <div class="space-y-1">
                    <label class="text-[10px] font-bold uppercase tracking-wider text-stone-400">Role Title</label>
                    <input 
                      v-model="admin.role" 
                      type="text" 
                      class="w-full border border-stone-200 bg-stone-50 p-2.5 text-xs text-stone-900 focus:outline-none focus:border-amber-500 focus:bg-white rounded-none transition-colors"
                    />
                  </div>

                  <div class="space-y-1">
                    <label class="text-[10px] font-bold uppercase tracking-wider text-stone-400">Email Address</label>
                    <input 
                      v-model="admin.email" 
                      type="email" 
                      class="w-full border border-stone-200 bg-stone-50 p-2.5 text-xs text-stone-900 focus:outline-none focus:border-amber-500 focus:bg-white rounded-none transition-colors"
                    />
                  </div>

                  <div class="space-y-1">
                    <label class="text-[10px] font-bold uppercase tracking-wider text-stone-400">Phone Number</label>
                    <input 
                      v-model="admin.phone" 
                      type="text" 
                      class="w-full border border-stone-200 bg-stone-50 p-2.5 text-xs text-stone-900 focus:outline-none focus:border-amber-500 focus:bg-white rounded-none transition-colors"
                    />
                  </div>
                </div>

                <button 
                  type="submit" 
                  class="bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs px-6 py-3 uppercase tracking-widest transition-colors rounded-none shadow-xs"
                >
                  Save Changes
                </button>
              </form>
            </div>

            <!-- TAB 3: SECURITY -->
            <div v-if="activeTab === 'security'" class="border border-stone-200 bg-white p-6 space-y-6 rounded-none">
              <h3 class="text-xs font-bold uppercase tracking-widest text-stone-700 border-b border-stone-100 pb-2">
                Security & Credentials
              </h3>

              <form @submit.prevent="updatePassword" class="space-y-4">
                <div class="space-y-1">
                  <label class="text-[10px] font-bold uppercase tracking-wider text-stone-400">Current Password</label>
                  <input 
                    type="password" 
                    placeholder="••••••••••••" v-model="currentPassword"
                    class="w-full border border-stone-200 bg-stone-50 p-2.5 text-xs text-stone-900 focus:outline-none focus:border-amber-500 focus:bg-white rounded-none"
                  />
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div class="space-y-1">
                    <label class="text-[10px] font-bold uppercase tracking-wider text-stone-400">New Password</label>
                    <input 
                      type="password" 
                      placeholder="Enter new password" v-model="newPassword"
                      class="w-full border border-stone-200 bg-stone-50 p-2.5 text-xs text-stone-900 focus:outline-none focus:border-amber-500 focus:bg-white rounded-none"
                    />
                  </div>

                  <div class="space-y-1">
                    <label class="text-[10px] font-bold uppercase tracking-wider text-stone-400">Confirm Password</label>
                    <input 
                      type="password" 
                      placeholder="Confirm new password" v-model="confirmPassword"
                      class="w-full border border-stone-200 bg-stone-50 p-2.5 text-xs text-stone-900 focus:outline-none focus:border-amber-500 focus:bg-white rounded-none"
                    />
                  </div>
                </div>

                <button 
                  type="submit" 
                  class="bg-stone-900 hover:bg-amber-500 text-white font-bold text-xs px-6 py-3 uppercase tracking-widest transition-colors rounded-none"
                >
                  Update Password
                </button>
              </form>
            </div>

          </div>

        </div>

      </div>
    </main>
  </div>
</template>