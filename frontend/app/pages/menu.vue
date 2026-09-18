<script setup lang="ts">
import { ref, computed } from 'vue'
import Caroursel from '~/components/Caroursel.vue'
import Footer from '~/components/Footer.vue'
import Navbar from '~/components/Navbar.vue'
import CartSidebar from '~/components/CartSidebar.vue'
import { useProducts } from '~/composables/useProducts'
import { useCart } from '~/composables/useCart'

const activeCategory = ref('All')
const searchQuery = ref('')
const route = useRoute()

const { products } = useProducts()
const { items: cart, addToCart, updateQuantity, totalItems: totalCartItems, totalPrice: totalCartPrice, isCartOpen } = useCart()
const { data: categoryData } = useFetch<any[]>('/categories', {
  baseURL: useRuntimeConfig().public.apiBase,
  default: () => []
})

if (route.query.category) {
  activeCategory.value = String(route.query.category)
}

const menuCategories = computed(() => [
  'All',
  ...(categoryData.value || [])
    .filter((category: any) => category.status !== 'Hidden')
    .map((category: any) => category.name)
])

const filteredMenu = computed(() => {
  return products.value.filter(item => {
    const matchesCategory = activeCategory.value === 'All' || item.category === activeCategory.value
    const displayName = item.name || item.title
    const matchesSearch = displayName.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          item.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesCategory && matchesSearch
  })
})

const goToProduct = (item) => {
  navigateTo(`/product/${item.id}`)
}

const addToMenuItem = (item) => {
  addToCart(item)
}

const updateCartQuantity = (id: string | number, delta: number) => {
  const item = cart.value.find(c => c.id === id)
  if (!item) return
  updateQuantity(id, item.quantity + delta)
}
</script>

<template>
  <Navbar/>
  <section class="bg-stone-50 text-stone-800 font-sans selection:bg-amber-600 selection:text-white py-16 px-4 sm:px-6 lg:px-8 relative">
    
    <div class="max-w-7xl mx-auto space-y-12">
      
      <!-- Editorial Section Header -->
      <div class="text-center space-y-3 max-w-3xl mx-auto">
        <div class="flex items-center justify-center gap-3">
          <span class="h-px w-10 bg-amber-600/60"></span>
          <span class="text-amber-700 text-xs font-bold uppercase tracking-[0.2em]">Culinary Excellence</span>
          <span class="h-px w-10 bg-amber-600/60"></span>
        </div>
        <h2 class="text-3xl sm:text-4xl font-serif font-bold text-stone-800 tracking-tight">Our Menu</h2>
        <p class="text-stone-600 text-xs sm:text-sm leading-relaxed max-w-xl mx-auto font-medium">
          Fresh ingredients, artisanal recipes, and woodfired perfection crafted daily for an unmatched dining experience.
        </p>
      </div>

      <!-- Controls Bar: Category Navigation & Search Bar -->
      <div class="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4 border-b border-stone-200 pb-5">
        
        <!-- Category Buttons -->
        <div class="flex items-center gap-2 overflow-x-auto pb-2 md:pb-0 scrollbar-none">
          <button 
            v-for="cat in menuCategories"
            :key="cat"
            @click="activeCategory = cat"
            :class="activeCategory === cat 
              ? 'bg-amber-600 text-white border-amber-600 font-semibold shadow-xs'
              : 'bg-white text-stone-600 border-stone-200 hover:border-amber-500 hover:text-stone-800 font-medium'"
            class="px-4 py-2 rounded-md text-xs whitespace-nowrap border transition-colors duration-200 uppercase tracking-wider"
          >
            {{ cat }}
          </button>
        </div>

        <!-- Search Input -->
        <div class="relative w-full md:w-72">
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Search menu items..." 
            class="w-full bg-white border border-stone-200 text-stone-800 placeholder-stone-400 text-xs rounded-md py-2 pl-9 pr-4 focus:outline-none focus:border-amber-600 transition-colors font-medium"
          />
          <svg class="w-4 h-4 text-stone-400 absolute left-3 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>
      </div>

        <!-- Item Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="item in filteredMenu" 
          :key="item.id"
          class="bg-white border border-stone-200 rounded-lg overflow-hidden hover:border-amber-500/50 transition-all duration-300 flex flex-col justify-between group shadow-xs hover:shadow-md cursor-pointer"
          @click="goToProduct(item)"
        >
          <!-- Image Section -->
          <div class="relative h-52 w-full overflow-hidden bg-stone-100">
            <img 
              :src="item.image" 
              :alt="item.name || item.title"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 ease-out"
            />
            <!-- Badges -->
            <div class="absolute top-3 left-3 flex flex-wrap gap-1.5">
              <span class="bg-stone-900/80 backdrop-blur-xs text-white text-[10px] font-semibold px-2 py-0.5 rounded-md uppercase tracking-wider">
                ★ {{ item.rating }}
              </span>
            </div>

            <!-- Floating Price Badge -->
            <div class="absolute bottom-3 right-3 bg-white/95 backdrop-blur-xs border border-stone-200 px-2.5 py-1 rounded-md shadow-xs">
              <span class="font-serif font-bold text-stone-800 text-sm">${{ item.price.toFixed(2) }}</span>
            </div>
          </div>

          <!-- Content Section -->
          <div class="p-5 flex-1 flex flex-col justify-between space-y-5">
            <div class="space-y-1.5">
              <h3 class="text-lg font-bold text-stone-800 group-hover:text-amber-700 transition-colors font-serif leading-tight">
                {{ item.name || item.title }}
              </h3>
              <p class="text-stone-500 text-xs leading-relaxed line-clamp-2 font-normal">
                {{ item.description }}
              </p>
            </div>

            <!-- Action Button -->
            <button 
              @click="addToMenuItem(item); $event.stopPropagation()"
              class="w-full bg-stone-800 hover:bg-amber-600 text-white font-semibold text-xs py-2.5 rounded-md transition-colors duration-200 flex items-center justify-center gap-2 uppercase tracking-wider active:bg-amber-700"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
              </svg>
              Add To Order
            </button>
          </div>
        </div>
      </div>

      <!-- Filter Empty State -->
      <div v-if="filteredMenu.length === 0" class="text-center py-16 border border-dashed border-stone-300 rounded-lg space-y-3">
        <p class="text-stone-500 text-xs font-semibold uppercase tracking-wider">No matching dishes found</p>
        <button 
          @click="searchQuery = ''; activeCategory = 'All'" 
          class="bg-stone-800 text-white text-xs font-semibold px-4 py-2 rounded-md uppercase tracking-wider hover:bg-amber-600 transition-colors"
        >
          Reset Search Filters
        </button>
      </div>

    </div>

    <!-- Floating Order Drawer Button -->
    <div v-if="totalCartItems > 0" class="fixed bottom-6 right-6 z-40">
      <button 
        @click="isCartOpen = true"
        class="bg-stone-900 hover:bg-amber-600 text-white font-bold px-5 py-3.5 rounded-lg shadow-lg flex items-center gap-3 transition-colors duration-200"
      >
        <span class="bg-amber-600 text-white text-xs px-2 py-0.5 rounded font-mono font-semibold">{{ totalCartItems }}</span>
        <span class="text-xs uppercase tracking-wider">Your Order</span>
        <span class="font-serif font-bold text-stone-200 border-l border-stone-700 pl-3">${{ totalCartPrice.toFixed(2) }}</span>
      </button>
    </div>

<!-- Order Side Drawer -->
    <CartSidebar/>
  </section>
  <Footer/>
</template>

<style scoped>
</style>