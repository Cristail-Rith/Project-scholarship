<script setup lang="ts">
import { ref, computed } from 'vue'

definePageMeta({ middleware: 'admin' })

interface Product {
  id: number
  sku: string
  name: string
  category: string
  category_id: number
  description?: string
  image?: string
  price: number
  previousPrice?: number | null
  costPrice: number
  sellingPrice: number
  stockQuantity: number
  reorderLevel: number
  status: 'In Stock' | 'Low Stock' | 'Out of Stock' | 'Archived'
  updatedAt: string
}

// Filter States
const searchQuery = ref('')
const selectedCategoryFilter = ref('All')
const selectedStatusFilter = ref('All')

// Modal & Form State
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingProduct = ref<Product>({
  id: 0,
  sku: '',
  name: '',
  category: 'Main Course',
  category_id: 0,
  price: 0,
  costPrice: 0,
  sellingPrice: 0,
  stockQuantity: 0,
  reorderLevel: 5,
  status: 'In Stock',
  updatedAt: 'Just now'
})

const products = ref<Product[]>([])
const categories = ref<{ id: number; name: string }[]>([])
const saveError = ref('')
const loadError = ref('')
const isSaving = ref(false)
const selectedImageFile = ref<File | null>(null)
const imagePreview = ref('')
const { apiBase } = useApiBase()
const { token } = useAuth()

const getApiError = (error: any, fallback: string) =>
  error?.data?.message || error?.data?.msg || error?.message || fallback

const isExpiredTokenError = (error: any) =>
  error?.status === 401 || error?.statusCode === 401 || error?.response?.status === 401

const api = <T>(path: string, options: Record<string, any> = {}) => {
  const storedToken = import.meta.client
    ? localStorage.getItem('access_token')
    : null
  const authToken = token.value || storedToken

  return $fetch<T>(path, {
    baseURL: apiBase.value,
    ...options,
    headers: {
      ...(options.headers || {}),
      ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
    },
  })
}

const resolveImage = (image: string | undefined) => {
  if (!image) return ''
  return image.startsWith('http') ? image : `${apiBase.value}${image}`
}

const selectImage = (event: Event) => {
  const input = event.target as HTMLInputElement
  selectedImageFile.value = input.files?.[0] || null
  imagePreview.value = selectedImageFile.value
    ? URL.createObjectURL(selectedImageFile.value)
    : ''
}

onMounted(async () => {
  try {
    const [productData, categoryData] = await Promise.all([
      api<Product[]>('/products'),
      api<{ id: number; name: string }[]>('/categories'),
    ])
    categories.value = categoryData
    products.value = productData.map((product) => ({
      ...product,
      sku: product.sku || `PRD-${product.id}`,
      costPrice: product.costPrice ?? 0,
      sellingPrice: product.price,
      stockQuantity: product.stockQuantity ?? 0,
      reorderLevel: product.reorderLevel ?? 5,
      status: product.status || 'Out of Stock',
      updatedAt: 'Just now',
    }))
  } catch (error: any) {
    loadError.value = getApiError(error, 'Could not load products from the database.')
  }
})

// Metrics Computations
const totalProductsCount = computed(() => products.value.length)
const lowStockCount = computed(() => products.value.filter(p => p.stockQuantity <= p.reorderLevel && p.stockQuantity > 0).length)
const outOfStockCount = computed(() => products.value.filter(p => p.stockQuantity === 0).length)
const totalInventoryValue = computed(() => 
  products.value.reduce((sum, p) => sum + (p.costPrice * p.stockQuantity), 0)
)

// Filtered List
const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          product.sku.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          String(product.id).includes(searchQuery.value.toLowerCase())
    const matchesCategory = selectedCategoryFilter.value === 'All' || product.category === selectedCategoryFilter.value
    const matchesStatus = selectedStatusFilter.value === 'All' || product.status === selectedStatusFilter.value

    return matchesSearch && matchesCategory && matchesStatus
  })
})

// Auto Status Determination
const determineStatus = (stock: number, reorder: number): Product['status'] => {
  if (stock === 0) return 'Out of Stock'
  if (stock <= reorder) return 'Low Stock'
  return 'In Stock'
}

// Modal Handlers
const openAddModal = () => {
  isEditing.value = false
  saveError.value = ''
  selectedImageFile.value = null
  imagePreview.value = ''
  editingProduct.value = {
    id: 0,
    sku: `SKU-${Math.floor(1000 + Math.random() * 9000)}`,
    name: '',
    category: categories.value[0]?.name || 'Main Course',
    category_id: categories.value[0]?.id || 0,
    price: 0,
    costPrice: 0,
    sellingPrice: 0,
    stockQuantity: 10,
    reorderLevel: 5,
    status: 'In Stock',
    updatedAt: 'Just now'
  }
  isModalOpen.value = true
}

const openEditModal = (product: Product) => {
  isEditing.value = true
  saveError.value = ''
  selectedImageFile.value = null
  editingProduct.value = JSON.parse(JSON.stringify(product))
  imagePreview.value = resolveImage(product.image)
  isModalOpen.value = true
}

const saveProduct = async () => {
  saveError.value = ''
  if (!editingProduct.value.name.trim()) {
    saveError.value = 'Product name is required.'
    return
  }
  if (!editingProduct.value.sellingPrice || editingProduct.value.sellingPrice <= 0) {
    saveError.value = 'Selling price must be greater than 0.'
    return
  }

  // Automatically update status based on inventory logic
  editingProduct.value.status = determineStatus(
    editingProduct.value.stockQuantity, 
    editingProduct.value.reorderLevel
  )

  const category = categories.value.find((item) => item.name === editingProduct.value.category)
  if (!category) {
    saveError.value = 'Please select a valid category.'
    return
  }
  const payload = new FormData()
  payload.append('name', editingProduct.value.name)
  payload.append('description', editingProduct.value.description || '')
  payload.append('price', String(editingProduct.value.sellingPrice))
  payload.append('category_id', String(category.id))
  payload.append('sku', editingProduct.value.sku)
  payload.append('cost_price', String(editingProduct.value.costPrice))
  payload.append('stock_quantity', String(editingProduct.value.stockQuantity))
  payload.append('reorder_level', String(editingProduct.value.reorderLevel))
  payload.append('status', editingProduct.value.status)
  if (selectedImageFile.value) payload.append('image', selectedImageFile.value)
  isSaving.value = true
  try {
    const response = isEditing.value
      ? await api<{ product: any }>(`/products/${editingProduct.value.id}`, { method: 'PUT', body: payload })
      : await api<{ product: any }>('/products', { method: 'POST', body: payload })
    const product = response.product
    const savedProduct = { ...editingProduct.value, ...product, category: product.category, sellingPrice: product.price, category_id: product.category_id }
    if (isEditing.value) {
      const index = products.value.findIndex((item) => item.id === savedProduct.id)
      if (index !== -1) products.value[index] = savedProduct
    } else {
      products.value.unshift({ ...savedProduct, sku: `PRD-${savedProduct.id}` })
    }
    isModalOpen.value = false
  } catch (error: any) {
    if (isExpiredTokenError(error)) {
      const { logout } = useAuth()
      logout()
      await navigateTo('/login')
      return
    }
    saveError.value = getApiError(error, 'Could not save product.')
  } finally {
    isSaving.value = false
  }
}

const deleteProduct = async (id: number) => {
  if (confirm('Are you sure you want to delete this product item?')) {
    try {
      await api(`/products/${id}`, { method: 'DELETE' })
      products.value = products.value.filter(p => p.id !== id)
    } catch (error: any) {
      saveError.value = getApiError(error, 'Could not delete product.')
    }
  }
}

// Dynamic Style Badges
const getStatusBadgeClass = (status: Product['status']) => {
  switch (status) {
    case 'In Stock': return 'bg-emerald-50 text-emerald-700 border-emerald-300'
    case 'Low Stock': return 'bg-amber-50 text-amber-700 border-amber-300'
    case 'Out of Stock': return 'bg-rose-50 text-rose-700 border-rose-300'
    case 'Archived': return 'bg-stone-100 text-stone-600 border-stone-300'
  }
}

const getProfitMargin = (cost: number, price: number) => {
  if (!price || price === 0) return 0
  return (((price - cost) / price) * 100).toFixed(1)
}
</script>

<template>
  <div class="min-h-screen bg-stone-100 text-stone-800 font-sans selection:bg-amber-100">
    <AdminSidebar />

    <main class="lg:ml-64 transition-all duration-300">
      
      <!-- Top Header -->
      <header class="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-stone-200 bg-white/90 px-6 backdrop-blur-md lg:px-8">
        <div>
          <h1 class="text-2xl font-bold text-stone-900 tracking-tight">Product Catalog & Inventory</h1>
          <p class="text-xs text-stone-500 font-normal">Manage dishes, pricing margins, SKU codes, and stock levels</p>
        </div>

        <div class="flex items-center gap-3">
          <div class="relative hidden sm:block">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Search product name, SKU..." 
              class="w-72 rounded-lg border border-stone-300 bg-stone-50 px-4 py-2 pl-9 text-xs text-stone-800 placeholder-stone-400 focus:border-amber-600 focus:bg-white focus:outline-none transition-all"
            />
            <svg class="absolute left-3 top-2.5 h-4 w-4 text-stone-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0 1 14 0z"/>
            </svg>
          </div>

          <button 
            @click="openAddModal"
            class="px-4 py-2 rounded-lg bg-amber-600 hover:bg-amber-700 text-white text-xs font-semibold uppercase tracking-wider transition-all shadow-sm flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            Add New Product
          </button>
        </div>
      </header>

      <div class="p-6 lg:p-8 space-y-6">

        <!-- Load Error -->
        <div v-if="loadError" class="mb-4 p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-lg text-xs">
          {{ loadError }}
        </div>

        <!-- Top Metrics Overview -->
        <section class="grid grid-cols-1 sm:grid-cols-4 gap-5">
          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-stone-400">Total Catalog Items</span>
              <p class="text-2xl font-bold text-stone-900 mt-1">{{ totalProductsCount }} Items</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-stone-100 text-stone-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-amber-600">Low Stock Warning</span>
              <p class="text-2xl font-bold text-amber-700 mt-1">{{ lowStockCount }} Items</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-50 text-amber-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-rose-600">Out of Stock</span>
              <p class="text-2xl font-bold text-rose-700 mt-1">{{ outOfStockCount }} Items</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-rose-50 text-rose-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 0 0 5.636 5.636m12.728 12.728A9 9 0 0 1 5.636 5.636m12.728 12.728L5.636 5.636"/>
              </svg>
            </div>
          </div>

          <div class="bg-white p-5 rounded-lg border border-stone-200 shadow-sm flex items-center justify-between">
            <div>
              <span class="text-[10px] font-bold tracking-wider uppercase text-emerald-600">Inventory Valuation</span>
              <p class="text-2xl font-bold text-emerald-700 mt-1">${{ totalInventoryValue.toFixed(2) }}</p>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-50 text-emerald-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0 1 18 0z"/>
              </svg>
            </div>
          </div>
        </section>

        <!-- Filter Bar -->
        <section class="bg-white p-4 rounded-lg border border-stone-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
          <div class="flex items-center gap-4 w-full md:w-auto">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-stone-400 uppercase tracking-wider">Category:</span>
              <select 
                v-model="selectedCategoryFilter"
                class="rounded-md border border-stone-300 bg-stone-50 px-3 py-1.5 text-xs text-stone-800 focus:border-amber-600 focus:outline-none"
              >
                <option value="All">All Categories</option>
                <option v-for="category in categories" :key="category.id" :value="category.name">
                  {{ category.name }}
                </option>
              </select>
            </div>

            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-stone-400 uppercase tracking-wider">Stock Status:</span>
              <select 
                v-model="selectedStatusFilter"
                class="rounded-md border border-stone-300 bg-stone-50 px-3 py-1.5 text-xs text-stone-800 focus:border-amber-600 focus:outline-none"
              >
                <option value="All">All Statuses</option>
                <option value="In Stock">In Stock</option>
                <option value="Low Stock">Low Stock</option>
                <option value="Out of Stock">Out of Stock</option>
              </select>
            </div>
          </div>

          <span class="text-xs text-stone-400 font-normal">Real-time Margin & Stock Calculations</span>
        </section>

        <!-- Product Table -->
        <section class="bg-white border border-stone-200 rounded-lg shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs text-stone-700">
              <thead>
                <tr class="bg-stone-50 border-b border-stone-200 text-[10px] font-bold uppercase tracking-wider text-stone-400">
                  <th scope="col" class="py-3.5 px-4">Image</th>
                  <th scope="col" class="py-3.5 px-4">Item & SKU</th>
                  <th scope="col" class="py-3.5 px-4">Category</th>
                  <th scope="col" class="py-3.5 px-4 text-right">Cost Price</th>
                  <th scope="col" class="py-3.5 px-4 text-right">Selling Price</th>
                  <th scope="col" class="py-3.5 px-4 text-right">Previous Price</th>
                  <th scope="col" class="py-3.5 px-4 text-right">Margin</th>
                  <!-- <th scope="col" class="py-3.5 px-4 text-center">In Stock</th>
                  <th scope="col" class="py-3.5 px-4 text-center">Status</th> -->
                  <th scope="col" class="py-3.5 px-4 text-right pr-6">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-stone-100">
                <tr 
                  v-for="product in filteredProducts" 
                  :key="product.id" 
                  class="hover:bg-stone-50/80 transition-colors group"
                >
                  <!-- Product Image -->
                  <td class="py-3.5 px-4">
                    <img
                      v-if="product.image"
                      :src="resolveImage(product.image)"
                      :alt="product.name"
                      class="h-12 w-12 rounded-md border border-stone-200 object-cover"
                    />
                    <div
                      v-else
                      class="flex h-12 w-12 items-center justify-center rounded-md border border-dashed border-stone-300 bg-stone-50 text-[9px] font-semibold uppercase text-stone-400"
                    >
                      No image
                    </div>
                  </td>

                  <!-- Name & SKU -->
                  <td class="py-3.5 px-4">
                    <div>
                      <span class="font-bold text-stone-900 text-sm block">{{ product.name }}</span>
                      <span class="text-stone-400 font-mono text-[10px]">{{ product.sku }} | {{ product.id }}</span>
                    </div>
                  </td>

                  <!-- Category -->
                  <td class="py-3.5 px-4 whitespace-nowrap font-semibold text-stone-700">
                    {{ product.category }}
                  </td>

                  <!-- Cost Price -->
                  <td class="py-3.5 px-4 text-right font-mono text-stone-500 whitespace-nowrap">
                    ${{ product.costPrice.toFixed(2) }}
                  </td>

                  <!-- Selling Price -->
                  <td class="py-3.5 px-4 text-right font-mono font-bold text-stone-900 whitespace-nowrap">
                    ${{ product.sellingPrice.toFixed(2) }}
                  </td>

                  <!-- Previous Selling Price -->
                  <td class="py-3.5 px-4 text-right font-mono text-stone-500 whitespace-nowrap">
                    <span v-if="product.previousPrice != null">
                      ${{ product.previousPrice.toFixed(2) }}
                    </span>
                    <!-- <span v-else class="text-stone-300">--</span> -->
                  </td>

                  <!-- Margin -->
                  <td class="py-3.5 px-4 text-right whitespace-nowrap">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                      {{ getProfitMargin(product.costPrice, product.sellingPrice) }}%
                    </span>
                  </td>

                  <!-- Quantity -->
                  <!-- <td class="py-3.5 px-4 text-center font-bold text-stone-800 font-mono">
                    {{ product.stockQuantity }}
                    <span class="text-[10px] font-normal text-stone-400 block">(Min: {{ product.reorderLevel }})</span>
                  </td>

                  Status -->
                  <!-- <td class="py-3.5 px-4 text-center whitespace-nowrap">
                    <span 
                      :class="getStatusBadgeClass(product.status)"
                      class="px-2.5 py-1 rounded text-[10px] font-bold border block w-max mx-auto"
                    >
                      {{ product.status }}
                    </span>
                  </td> -->

                  <!-- Actions -->
                  <td class="py-3.5 px-4 text-right pr-6 whitespace-nowrap">
                    <div class="flex items-center justify-end gap-1">
                      <button 
                        @click="openEditModal(product)"
                        class="p-1.5 rounded-md text-stone-400 hover:text-amber-600 hover:bg-stone-100 transition-colors"
                        title="Edit Product"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2v-5m-1.414-9.414a2 2 0 1 1 2.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                      </button>

                      <button 
                        @click="deleteProduct(product.id)"
                        class="p-1.5 rounded-md text-stone-400 hover:text-rose-600 hover:bg-stone-100 transition-colors"
                        title="Delete Product"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0 1 16.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>

                <!-- Empty State -->
                <tr v-if="filteredProducts.length === 0">
                  <td colspan="10" class="py-12 text-center text-stone-400 font-normal">
                    No products match your search or filter parameters.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

      </div>
    </main>

    <!-- Modal Form -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4 overflow-y-auto">
      <div class="bg-white border border-stone-200 rounded-lg max-w-lg w-full p-6 shadow-xl space-y-5 text-stone-800 my-8">
        
        <div class="flex items-center justify-between border-b border-stone-200 pb-4">
          <div>
            <span class="text-[10px] uppercase font-bold tracking-widest text-amber-600">Inventory Management</span>
            <h3 class="text-xl font-bold text-stone-900">
              {{ isEditing ? 'Edit Product Item' : 'Add New Product' }}
            </h3>
          </div>
          <button @click="isModalOpen = false" class="text-stone-400 hover:text-stone-700 text-base">✕</button>
        </div>

        <form @submit.prevent="saveProduct" class="space-y-4 text-xs">
          
          <div>
            <label class="font-bold text-stone-700 block mb-1">Product Name</label>
            <input 
              v-model="editingProduct.name" 
              type="text" 
              placeholder="e.g. Woodfired Margherita Pizza"
              required
              class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-900 focus:border-amber-600 focus:bg-white focus:outline-none"
            />
          </div>

          <div>
            <label class="font-bold text-stone-700 block mb-1">Product Image</label>
            <label class="group relative flex cursor-pointer items-center gap-4 rounded-xl border-2 border-dashed border-amber-300 bg-amber-50/60 p-4 transition hover:border-amber-500 hover:bg-amber-50 focus-within:ring-2 focus-within:ring-amber-400">
              <span class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-white text-amber-700 shadow-sm">
                <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4 16.5V19a1 1 0 001 1h14a1 1 0 001-1v-2.5M12 15V4m0 0L8 8m4-4l4 4" /></svg>
              </span>
              <span class="min-w-0 flex-1">
                <span class="block truncate text-sm font-semibold text-stone-800">{{ selectedImageFile?.name || (isEditing && imagePreview ? 'Current image kept — choose a replacement' : 'Choose a product picture') }}</span>
                <span class="mt-1 block text-xs font-normal text-stone-500">JPG, PNG, WEBP or GIF · up to 5 MB</span>
              </span>
              <span class="rounded-lg border border-amber-200 bg-white px-3 py-2 text-xs font-bold text-amber-800 shadow-sm group-hover:border-amber-300">Browse</span>
              <input
                type="file"
                accept=".jpg,.jpeg,.png,.webp,.gif,image/jpeg,image/png,image/webp,image/gif"
                @change="selectImage"
                class="absolute inset-0 cursor-pointer opacity-0"
              />
            </label>
            <img
              v-if="imagePreview"
              :src="imagePreview"
              alt="Product preview"
              class="mt-3 h-36 w-full rounded-xl object-cover border border-stone-200 shadow-sm"
            />
          </div>

          <div>
            <label class="font-bold text-stone-700 block mb-1">Description</label>
            <textarea
              v-model="editingProduct.description"
              rows="3"
              placeholder="Describe the ingredients, flavor, or serving details..."
              class="w-full resize-y rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-900 focus:border-amber-600 focus:bg-white focus:outline-none"
            ></textarea>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="font-bold text-stone-700 block mb-1">SKU Code</label>
              <input 
                v-model="editingProduct.sku" 
                type="text" 
                placeholder="e.g. PIZ-MAR-01"
                required
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:outline-none"
              />
            </div>

            <div>
              <label class="font-bold text-stone-700 block mb-1">Category</label>
              <select 
                v-model="editingProduct.category"
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:outline-none"
              >
                <option v-for="category in categories" :key="category.id" :value="category.name">
                  {{ category.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="font-bold text-stone-700 block mb-1">Cost Price ($)</label>
              <input 
                v-model.number="editingProduct.costPrice" 
                type="number" 
                step="0.01" 
                required
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:outline-none"
              />
            </div>

            <div>
              <label class="font-bold text-stone-700 block mb-1">Selling Price ($)</label>
              <input 
                v-model.number="editingProduct.sellingPrice" 
                type="number" 
                step="0.01" 
                required
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:outline-none"
              />
            </div>
          </div>

          <!-- <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="font-bold text-stone-700 block mb-1">Initial Stock Qty</label>
              <input 
                v-model.number="editingProduct.stockQuantity" 
                type="number" 
                min="0"
                required
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:outline-none"
              />
            </div>

            <div>
              <label class="font-bold text-stone-700 block mb-1">Reorder Warning Level</label>
              <input 
                v-model.number="editingProduct.reorderLevel" 
                type="number" 
                min="1"
                required
                class="w-full rounded-lg border border-stone-300 bg-stone-50 p-2.5 text-stone-800 focus:border-amber-600 focus:outline-none"
              />
            </div>
          </div> -->

          <div class="pt-4 border-t border-stone-200 flex items-center justify-end gap-3">
            <p v-if="saveError" class="mr-auto text-xs text-rose-600">
              {{ saveError }}
            </p>
            <button 
              type="button" 
              @click="isModalOpen = false" 
              class="px-5 py-2.5 rounded-lg border border-stone-300 text-stone-700 font-semibold hover:bg-stone-100 transition-colors"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              :disabled="isSaving"
              :class="isSaving ? 'cursor-wait opacity-60' : ''"
              class="px-5 py-2.5 rounded-lg bg-amber-600 hover:bg-amber-700 text-white font-semibold transition-colors shadow-sm"
            >
              {{ isSaving ? 'Saving...' : (isEditing ? 'Save Changes' : 'Create Product') }}
            </button>
          </div>

        </form>

      </div>
    </div>
  </div>
</template>
