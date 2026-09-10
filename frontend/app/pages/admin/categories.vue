<script setup lang="ts">
import { ref, computed } from 'vue'

interface Category {
  id: string
  name: string
  slug: string
  description: string
  itemCount: number
  icon: string // Storing icon key/identifier instead of emoji
  station: 'Kitchen Grill' | 'Pizza Oven' | 'Bar & Drinks' | 'Pastry & Cold' | 'Main Line'
  status: 'Active' | 'Hidden'
  displayOrder: number
}

// Available Icon Options for Selection
const availableIcons = [
  { id: 'utensils', label: 'Utensils' },
  { id: 'pizza', label: 'Pizza' },
  { id: 'burger', label: 'Burger' },
  { id: 'steak', label: 'Steak / Grill' },
  { id: 'drink', label: 'Cocktail / Bar' },
  { id: 'pasta', label: 'Pasta' },
  { id: 'cake', label: 'Dessert' },
  { id: 'salad', label: 'Salad / Cold' }
]

// Search & Filter State
const searchQuery = ref('')
const selectedStationFilter = ref('All')

// Drawer / Modal Form State
const isDrawerOpen = ref(false)
const isEditing = ref(false)
const editingCategory = ref<Category>({
  id: '',
  name: '',
  slug: '',
  description: '',
  itemCount: 0,
  icon: 'utensils',
  station: 'Main Line',
  status: 'Active',
  displayOrder: 1
})

// Categories Reactive Dataset
const categories = ref<Category[]>([
  {
    id: 'CAT-101',
    name: 'Artisan Pizzas',
    slug: 'artisan-pizzas',
    description: 'Wood-fired sourdough pizzas crafted with organic flour and imported mozzarella.',
    itemCount: 12,
    icon: 'pizza',
    station: 'Pizza Oven',
    status: 'Active',
    displayOrder: 1
  },
  {
    id: 'CAT-102',
    name: 'Gourmet Burgers',
    slug: 'gourmet-burgers',
    description: 'Prime Angus beef burgers served on toasted brioche buns with signature sauces.',
    itemCount: 8,
    icon: 'burger',
    station: 'Kitchen Grill',
    status: 'Active',
    displayOrder: 2
  },
  {
    id: 'CAT-103',
    name: 'Prime Steaks & Grills',
    slug: 'prime-steaks',
    description: 'Dry-aged steaks grilled over charcoal with house herb butter.',
    itemCount: 6,
    icon: 'steak',
    station: 'Kitchen Grill',
    status: 'Active',
    displayOrder: 3
  },
  {
    id: 'CAT-104',
    name: 'Craft Cocktails & Wines',
    slug: 'cocktails-wines',
    description: 'Signature mixologist cocktails, vintage wines, and craft draft beers.',
    itemCount: 24,
    icon: 'drink',
    station: 'Bar & Drinks',
    status: 'Active',
    displayOrder: 4
  },
  {
    id: 'CAT-105',
    name: 'Pastas & Risottos',
    slug: 'pastas-risottos',
    description: 'Handmade fresh egg pastas and slow-cooked Arborio rice dishes.',
    itemCount: 10,
    icon: 'pasta',
    station: 'Main Line',
    status: 'Active',
    displayOrder: 5
  },
  {
    id: 'CAT-106',
    name: 'Desserts & Sweets',
    slug: 'desserts',
    description: 'House-made gelatos, soufflés, and artisanal pastry creations.',
    itemCount: 9,
    icon: 'cake',
    station: 'Pastry & Cold',
    status: 'Active',
    displayOrder: 6
  },
  {
    id: 'CAT-107',
    name: 'Seasonal Appetizers',
    slug: 'seasonal-appetizers',
    description: 'Light starters, fresh oysters, and shared tapas plates.',
    itemCount: 14,
    icon: 'salad',
    station: 'Pastry & Cold',
    status: 'Hidden',
    displayOrder: 7
  }
])

// Computed Metrics
const totalCategories = computed(() => categories.value.length)
const activeCategoriesCount = computed(() => categories.value.filter(c => c.status === 'Active').length)
const totalItemsInCategories = computed(() => categories.value.reduce((acc, c) => acc + c.itemCount, 0))

// Filter Computed Property
const filteredCategories = computed(() => {
  return categories.value
    .filter(cat => {
      const matchesSearch = cat.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                            cat.description.toLowerCase().includes(searchQuery.value.toLowerCase())
      const matchesStation = selectedStationFilter.value === 'All' || cat.station === selectedStationFilter.value
      return matchesSearch && matchesStation
    })
    .sort((a, b) => a.displayOrder - b.displayOrder)
})

// Quick Actions
const openAddModal = () => {
  isEditing.value = false
  editingCategory.value = {
    id: `CAT-${Math.floor(100 + Math.random() * 900)}`,
    name: '',
    slug: '',
    description: '',
    itemCount: 0,
    icon: 'utensils',
    station: 'Main Line',
    status: 'Active',
    displayOrder: categories.value.length + 1
  }
  isDrawerOpen.value = true
}

const openEditModal = (cat: Category) => {
  isEditing.value = true
  editingCategory.value = { ...cat }
  isDrawerOpen.value = true
}

const toggleStatus = (cat: Category) => {
  cat.status = cat.status === 'Active' ? 'Hidden' : 'Active'
}

const saveCategory = () => {
  if (!editingCategory.value.name.trim()) return

  // Auto-generate slug if empty
  if (!editingCategory.value.slug) {
    editingCategory.value.slug = editingCategory.value.name.toLowerCase().replace(/\s+/g, '-')
  }

  if (isEditing.value) {
    const idx = categories.value.findIndex(c => c.id === editingCategory.value.id)
    if (idx !== -1) categories.value[idx] = { ...editingCategory.value }
  } else {
    categories.value.push({ ...editingCategory.value })
  }
  isDrawerOpen.value = false
}

const deleteCategory = (id: string) => {
  if (confirm('Are you sure you want to delete this category? Menu items assigned to it may need re-assigning.')) {
    categories.value = categories.value.filter(c => c.id !== id)
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
          <h1 class="text-2xl font-bold text-stone-900 tracking-tight">Menu Categories</h1>
          <p class="text-xs text-stone-500 font-normal">Organize your dishes, kitchen routing stations, and catalog hierarchy</p>
        </div>

        <div class="flex items-center gap-3">
          <div class="relative hidden sm:block">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Search category or station..." 
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
            Add Category
          </button>
        </div>
      </header>

      <div class="p-6 lg:p-8 space-y-6">

        <!-- Top Overview Stats -->
        <section class="grid grid-cols-1 sm:grid-cols-3 gap-5">
          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-stone-400">Total Categories</span>
              <p class="text-2xl font-bold text-stone-900 mt-1">{{ totalCategories }} Groups</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-50 text-amber-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-emerald-600">Active Live Categories</span>
              <p class="text-2xl font-bold text-emerald-700 mt-1">{{ activeCategoriesCount }} Visible</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-stone-400">Total Catalog Items</span>
              <p class="text-2xl font-bold text-stone-900 mt-1">{{ totalItemsInCategories }} Dishes</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-stone-100 text-stone-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
              </svg>
            </div>
          </div>
        </section>

        <!-- Kitchen Station Filter Bar -->
        <section class="bg-white p-4 rounded-lg border border-stone-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
          <div class="flex items-center gap-1.5 overflow-x-auto w-full md:w-auto no-scrollbar">
            <span class="text-xs font-bold text-stone-400 uppercase mr-2 tracking-wider">Station Filter:</span>
            <button 
              v-for="station in ['All', 'Kitchen Grill', 'Pizza Oven', 'Main Line', 'Pastry & Cold', 'Bar & Drinks']" 
              :key="station"
              @click="selectedStationFilter = station"
              :class="[
                'px-3.5 py-1.5 rounded-md text-xs font-semibold whitespace-nowrap transition-all border',
                selectedStationFilter === station 
                  ? 'bg-stone-900 border-stone-900 text-white shadow-xs' 
                  : 'bg-stone-50 border-stone-200 text-stone-600 hover:bg-stone-100'
              ]"
            >
              {{ station }}
            </button>
          </div>

          <span class="text-xs text-stone-400 font-normal">Re-order items or adjust status to change guest visibility</span>
        </section>

        <!-- Table View Categories -->
        <section class="bg-white border border-stone-200 rounded-lg shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs text-stone-700">
              <thead>
                <tr class="bg-stone-50 border-b border-stone-200 text-[10px] font-bold uppercase tracking-wider text-stone-400">
                  <th scope="col" class="py-3.5 px-4 text-center w-12">Order</th>
                  <th scope="col" class="py-3.5 px-4">Category Name</th>
                  <th scope="col" class="py-3.5 px-4">Station</th>
                  <th scope="col" class="py-3.5 px-4 text-center">Items</th>
                  <th scope="col" class="py-3.5 px-4 text-center">Status</th>
                  <th scope="col" class="py-3.5 px-4 text-right pr-6">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-stone-100">
                <tr 
                  v-for="cat in filteredCategories" 
                  :key="cat.id" 
                  class="hover:bg-stone-50/80 transition-colors group"
                >
                  <!-- Display Priority Order -->
                  <td class="py-3.5 px-4 text-center font-bold text-stone-400">
                    #{{ cat.displayOrder }}
                  </td>

                  <!-- Category Info (Icon, Name, Slug, Description) -->
                  <td class="py-3.5 px-4">
                    <div class="flex items-center gap-3">
                      <!-- Vector Icon Display -->
                      <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-stone-100 border border-stone-200 text-stone-700 shrink-0">
                        <svg v-if="cat.icon === 'pizza'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 2L2 22h20L12 2zM12 6l5 10H7l5-10z"/>
                        </svg>
                        <svg v-else-if="cat.icon === 'burger'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4 11a8 8 0 0116 0H4zm0 4h16m-14 3h12a2 2 0 002-2v-1H4v1a2 2 0 002 2z"/>
                        </svg>
                        <svg v-else-if="cat.icon === 'steak'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0 0-2 4 1.5 5.5s6.5-.5 7.157 3.157z"/>
                        </svg>
                        <svg v-else-if="cat.icon === 'drink'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M19.5 4.5l-15 0l7.5 8.5l0 6.5l-3 0l0 2l10 0l0 -2l-3 0l0 -6.5l7.5 -8.5z"/>
                        </svg>
                        <svg v-else-if="cat.icon === 'pasta'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4 10h16M4 14h16M4 18h16M12 4v16"/>
                        </svg>
                        <svg v-else-if="cat.icon === 'cake'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M20 21v-8a2 2 0 00-2-2H6a2 2 0 00-2 2v8m16 0H4m16 0a2 2 0 002-2V9a2 2 0 00-2-2h-3a1 1 0 01-1-1V5a2 2 0 00-2-2h-2a2 2 0 00-2 2v1a1 1 0 01-1 1H4a2 2 0 00-2 2v10a2 2 0 002 2"/>
                        </svg>
                        <svg v-else-if="cat.icon === 'salad'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 3v18m9-9H3"/>
                        </svg>
                        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
                        </svg>
                      </div>

                      <div>
                        <div class="flex items-center gap-2">
                          <span class="font-bold text-stone-900 text-sm">{{ cat.name }}</span>
                          <span class="text-[10px] font-mono text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200/60">
                            /{{ cat.slug }}
                          </span>
                        </div>
                        <p class="text-[11px] text-stone-500 line-clamp-1 max-w-md font-normal mt-0.5">
                          {{ cat.description }}
                        </p>
                      </div>
                    </div>
                  </td>

                  <!-- Kitchen Station -->
                  <td class="py-3.5 px-4 font-semibold text-stone-800 whitespace-nowrap">
                    <span class="inline-flex items-center gap-1.5">
                      <svg class="w-3.5 h-3.5 text-stone-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                      </svg>
                      {{ cat.station }}
                    </span>
                  </td>

                  <!-- Total Items -->
                  <td class="py-3.5 px-4 text-center whitespace-nowrap">
                    <span class="text-xs font-bold text-stone-700 bg-stone-100 px-2 py-0.5 rounded border border-stone-200">
                      {{ cat.itemCount }} Items
                    </span>
                  </td>

                  <!-- Status -->
                  <td class="py-3.5 px-4 text-center whitespace-nowrap">
                    <button 
                      @click="toggleStatus(cat)" 
                      :class="cat.status === 'Active' ? 'bg-emerald-50 text-emerald-700 border-emerald-300' : 'bg-stone-100 text-stone-500 border-stone-300'"
                      class="px-2.5 py-1 rounded text-[10px] font-bold border transition-all cursor-pointer hover:opacity-80"
                    >
                      {{ cat.status }}
                    </button>
                  </td>

                  <!-- Actions -->
                  <td class="py-3.5 px-4 text-right pr-6 whitespace-nowrap">
                    <div class="flex items-center justify-end gap-1">
                      <button 
                        @click="openEditModal(cat)"
                        class="p-1.5 rounded-md text-stone-400 hover:text-amber-600 hover:bg-stone-100 transition-colors"
                        title="Edit Category"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                      </button>

                      <button 
                        @click="deleteCategory(cat.id)"
                        class="p-1.5 rounded-md text-stone-400 hover:text-rose-600 hover:bg-stone-100 transition-colors"
                        title="Delete Category"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>

                <!-- Empty State -->
                <tr v-if="filteredCategories.length === 0">
                  <td colspan="6" class="py-12 text-center text-stone-400 font-normal">
                    No menu categories match your search filter criteria.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

      </div>
    </main>

    <!-- Create / Edit Drawer Modal -->
    <div v-if="isDrawerOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4">
      <div class="bg-white border border-stone-200 rounded-lg max-w-lg w-full p-6 shadow-xl space-y-5 text-stone-800">
        
        <div class="flex items-center justify-between border-b border-stone-200 pb-4">
          <div>
            <span class="text-[10px] uppercase font-bold tracking-widest text-amber-600">Catalog Manager</span>
            <h3 class="text-xl font-bold text-stone-900">
              {{ isEditing ? 'Edit Category' : 'Create New Category' }}
            </h3>
          </div>
          <button @click="isDrawerOpen = false" class="text-stone-400 hover:text-stone-700 text-base">✕</button>
        </div>

        <form @submit.prevent="saveCategory" class="space-y-4 text-xs">
          
          <div>
            <label class="font-bold text-stone-700 block mb-1">Select Vector Icon</label>
            <div class="grid grid-cols-4 gap-2">
              <button
                v-for="iconItem in availableIcons"
                :key="iconItem.id"
                type="button"
                @click="editingCategory.icon = iconItem.id"
                :class="[
                  'p-2.5 rounded-lg border text-xs font-semibold flex flex-col items-center gap-1 transition-all',
                  editingCategory.icon === iconItem.id 
                    ? 'border-amber-600 bg-amber-50 text-amber-700 ring-1 ring-amber-600' 
                    : 'border-stone-200 bg-stone-50 text-stone-600 hover:bg-stone-100'
                ]"
              >
                <!-- Simplified Icon Previews -->
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
                </svg>
                <span>{{ iconItem.label }}</span>
              </button>
            </div>
          </div>

          <div>
            <label class="font-bold text-stone-700 block mb-1">Category Title</label>
            <input 
              v-model="editingCategory.name" 
              type="text" 
              placeholder="e.g. Woodfired Pizzas"
              required
              class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-900 focus:border-amber-600 focus:bg-white focus:outline-none"
            />
          </div>

          <div>
            <label class="font-bold text-stone-700 block mb-1">URL Slug (Optional)</label>
            <input 
              v-model="editingCategory.slug" 
              type="text" 
              placeholder="woodfired-pizzas"
              class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 font-mono text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="font-bold text-stone-700 block mb-1">Kitchen Ticket Station</label>
              <select 
                v-model="editingCategory.station"
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
              >
                <option>Main Line</option>
                <option>Kitchen Grill</option>
                <option>Pizza Oven</option>
                <option>Pastry & Cold</option>
                <option>Bar & Drinks</option>
              </select>
            </div>

            <div>
              <label class="font-bold text-stone-700 block mb-1">Display Priority Order</label>
              <input 
                v-model.number="editingCategory.displayOrder" 
                type="number" 
                min="1"
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label class="font-bold text-stone-700 block mb-1">Short Description</label>
            <textarea 
              v-model="editingCategory.description" 
              rows="3"
              placeholder="Brief overview displayed on digital menu..."
              class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:bg-white focus:outline-none"
            ></textarea>
          </div>

          <div class="pt-4 border-t border-stone-200 flex items-center justify-end gap-3">
            <button 
              type="button" 
              @click="isDrawerOpen = false" 
              class="px-5 py-2.5 rounded-lg border border-stone-300 text-stone-700 font-semibold hover:bg-stone-100 transition-colors"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              class="px-5 py-2.5 rounded-lg bg-amber-600 hover:bg-amber-700 text-white font-semibold transition-colors shadow-sm"
            >
              {{ isEditing ? 'Update Category' : 'Save Category' }}
            </button>
          </div>

        </form>

      </div>
    </div>
  </div>
</template>