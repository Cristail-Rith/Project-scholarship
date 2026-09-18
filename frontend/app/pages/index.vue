<template>
  <Navbar/>
  <Caroursel/>
  <div class="min-h-screen bg-[#FDFBF7] text-neutral-800 font-serif">
    <!-- HERO SECTION -->
    

    <!-- OUR MENU CATEGORIES SECTION -->
    <section class="py-16 bg-[#FAF7F2] border-t border-b border-stone-200/50">
      <div class="max-w-7xl mx-auto px-6">
        <!-- Section Header -->
        <div class="text-center mb-12">
          <h2 class="text-2xl md:text-3xl font-serif text-neutral-900 tracking-wider uppercase font-normal">
            Our Menu Categories
          </h2>
          <!-- Crown Divider -->
          <div class="flex items-center justify-center gap-3 mt-3 text-[#C59237]">
            <span class="w-10 h-px bg-amber-600/40"></span>
            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M5 16L3 5l5.5 5L12 4l3.5 6L21 5l-2 11H5zm14 3c0 .6-.4 1-1 1H6c-.6 0-1-.4-1-1v-1h14v1z"/>
            </svg>
            <span class="w-10 h-px bg-amber-600/40"></span>
          </div>
        </div>

        <!-- Categories Grid -->
        <div v-if="categories.length" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-6 md:gap-8">
          <NuxtLink
            v-for="category in categories"
            :key="category.name"
            :to="'/menu?category=' + encodeURIComponent(category.name)"
            :aria-label="category.name"
            class="flex flex-col items-center group hover:text-[#C59237] transition-colors duration-300 focus:outline-none"
          >
            <!-- Circle Image Container -->
            <div class="w-28 h-28 sm:w-32 sm:h-32 md:w-36 md:h-36 rounded-full p-1.5 border-2 border-stone-200 group-hover:border-[#C59237] transition-all duration-300 shadow-sm bg-white overflow-hidden mb-4">
              <img
                :src="resolveCategoryImage(category)"
                :alt="category.name"
                class="w-full h-full object-cover rounded-full group-hover:scale-110 transition-transform duration-500"
              />
            </div>
            <!-- Category Title -->
            <span class="font-sans text-xs md:text-sm font-semibold tracking-wider text-neutral-800 group-hover:text-[#C59237] transition-colors">
              {{ category.name }}
            </span>
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- CHEF'S RECOMMENDATIONS SECTION -->
    <section class="py-16 max-w-7xl mx-auto px-6">
      <!-- Section Header -->
      <div class="text-center mb-10">
        <h2 class="text-2xl md:text-3xl font-serif text-neutral-900 tracking-wider uppercase font-normal">
          Chef's Recommendations
        </h2>
        <!-- Crown Divider -->
        <div class="flex items-center justify-center gap-3 mt-3 text-[#C59237]">
          <span class="w-10 h-px bg-amber-600/40"></span>
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24">
            <path d="M5 16L3 5l5.5 5L12 4l3.5 6L21 5l-2 11H5zm14 3c0 .6-.4 1-1 1H6c-.6 0-1-.4-1-1v-1h14v1z"/>
          </svg>
          <span class="w-10 h-px bg-amber-600/40"></span>
        </div>
      </div>

      <!-- Category Filter Tabs -->
      <div class="flex flex-wrap justify-center items-center gap-6 md:gap-10 font-sans text-xs font-semibold tracking-widest uppercase mb-12">
        <button
          v-for="tab in filterTabs"
          :key="tab"
          @click="selectedTab = tab"
          :class="[
            'pb-1 transition-all duration-300 relative',
            selectedTab === tab
              ? 'text-[#C59237] border-b-2 border-[#C59237]'
              : 'text-stone-600 hover:text-stone-900'
          ]"
        >
          {{ tab }}
        </button>
      </div>

      <!-- Recommendation Food Items Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div
          v-for="item in filteredItems"
          :key="item.id"
          class="cursor-pointer bg-white border border-stone-200/80 rounded-sm p-5 shadow-sm hover:shadow-md transition-shadow duration-300 flex flex-col justify-between group"
          @click="goToProduct(item)"
        >
          <div>
            <div class="relative overflow-hidden mb-4 rounded-sm h-48">
              <button type="button" class="block w-full h-full text-left" @click.stop="goToProduct(item)">
                <img
                  :src="item.image"
                  :alt="item.title"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
              </button>
              <span class="absolute top-3 right-3 bg-stone-900/80 text-amber-300 text-[10px] font-sans px-2.5 py-1 tracking-wider uppercase backdrop-blur-sm">
                ★ {{ item.rating }}
              </span>
            </div>

            <div class="flex justify-between items-start mb-2">
              <button type="button" class="font-serif text-left text-lg font-medium text-stone-900 group-hover:text-[#C59237] transition-colors" @click.stop="goToProduct(item)">
                {{ item.title }}
              </button>
              <span class="font-sans font-bold text-base text-[#C59237] ml-2">${{ item.price.toFixed(2) }}</span>
            </div>

            <p class="font-sans text-xs text-stone-500 font-light leading-relaxed mb-4">
              {{ item.description }}
            </p>
          </div>

          <button
            @click.stop="addItemToCart(item)"
            class="w-full py-2.5 bg-stone-100 hover:bg-[#C59237] hover:text-white text-stone-800 text-xs font-sans font-semibold tracking-wider uppercase transition-colors duration-300 rounded-sm"
          >
            Add To Order
          </button>
        </div>
      </div>
    </section>

    <CartSidebar/>
  </div>
  <Footer/>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useProducts } from '~/composables/useProducts'
import CartSidebar from '~/components/CartSidebar.vue'
const config = useRuntimeConfig()

const { products } = useProducts()

const {
  items: cartItems,
  addToCart,
  updateQuantity,
  totalPrice,
  isCartOpen
} = useCart()
const { data: categoryData } = useFetch('/categories', {
  baseURL: config.public.apiBase,
  default: () => []
})

const activeSlide = ref(0)
const selectedTab = ref('All Items')

const categoryFallbackImages = {
  Starters: 'https://images.unsplash.com/photo-1541544741938-0af808871cc0?auto=format&fit=crop&w=400&q=80',
  'Main Course': 'https://images.unsplash.com/photo-1621996346565-e3d5d6281273?auto=format&fit=crop&w=400&q=80',
  Desserts: 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=400&q=80',
  Beverages: 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=400&q=80',
  Pizza: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=400&q=80',
  'Chef Specials': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=400&q=80'
}

const categories = computed(() => (categoryData.value || []).filter(category => category.status !== 'Hidden'))

const resolveCategoryImage = (category) => {
  if (category.image) {
    return category.image.startsWith('http')
      ? category.image
      : `${config.public.apiBase}${category.image}`
  }
  return categoryFallbackImages[category.name] || categoryFallbackImages['Main Course']
}

// Filter Tabs
const filterTabs = computed(() => ['All Items', ...categories.value.map(category => category.name)])

// Recommendation Items
const items = products

const filteredItems = computed(() => {
  if (selectedTab.value === 'All Items') return items.value
  return items.value.filter(item => item.category === selectedTab.value)
})

const goToProduct = (item) => {
  navigateTo(`/product/${item.id}`)
}

const goToCart = () => {
  isCartOpen.value = false
  navigateTo('/cart')
}

const addItemToCart = (item) => {
  addToCart(item)
}

const updateCartQuantity = (id, quantity) => {
  updateQuantity(id, quantity)
}

</script>