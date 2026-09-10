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
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-6 md:gap-8">
          <div
            v-for="category in categories"
            :key="category.name"
            class="flex flex-col items-center group cursor-pointer"
          >
            <!-- Circle Image Container -->
            <div class="w-28 h-28 sm:w-32 sm:h-32 md:w-36 md:h-36 rounded-full p-1.5 border-2 border-stone-200 group-hover:border-[#C59237] transition-all duration-300 shadow-sm bg-white overflow-hidden mb-4">
              <img
                :src="category.image"
                :alt="category.name"
                class="w-full h-full object-cover rounded-full group-hover:scale-110 transition-transform duration-500"
              />
            </div>
            <!-- Category Title -->
            <span class="font-sans text-xs md:text-sm font-semibold tracking-wider text-neutral-800 group-hover:text-[#C59237] transition-colors">
              {{ category.name }}
            </span>
          </div>
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

    <!-- Cart sidebar -->
    <div v-if="isCartOpen" class="fixed inset-0 z-50 bg-stone-950/60" @click.self="isCartOpen = false">
      <aside class="ml-auto flex h-full w-full max-w-md flex-col bg-white p-6 text-stone-900 shadow-2xl">
        <div class="flex items-center justify-between border-b-2 border-stone-900 pb-4">
          <div>
            <span class="text-[10px] font-black uppercase tracking-widest text-amber-700">Added to your order</span>
            <h2 class="font-serif text-2xl">Your Cart</h2>
          </div>
          <button type="button" class="text-2xl text-stone-400 hover:text-stone-900" aria-label="Close cart" @click="isCartOpen = false">&times;</button>
        </div>

        <div class="flex-1 overflow-y-auto py-5">
          <div v-if="!cartItems.length" class="py-12 text-center text-sm text-stone-500">Your cart is empty.</div>
          <div v-for="item in cartItems" :key="item.id" class="flex items-center gap-3 border-b border-stone-200 py-4">
            <img :src="item.image" :alt="item.title" class="h-16 w-16 object-cover" />
            <div class="min-w-0 flex-1">
              <button type="button" class="block truncate text-left font-serif hover:text-amber-700" @click="goToProduct(item)">{{ item.title }}</button>
              <p class="text-xs text-amber-700">${{ (item.price * item.quantity).toFixed(2) }}</p>
              <div class="mt-2 flex items-center gap-2">
                <button type="button" class="h-6 w-6 border border-stone-300" @click="updateCartQuantity(item.id, item.quantity - 1)">-</button>
                <span class="w-5 text-center text-xs">{{ item.quantity }}</span>
                <button type="button" class="h-6 w-6 border border-stone-300" @click="updateCartQuantity(item.id, item.quantity + 1)">+</button>
              </div>
            </div>
          </div>
        </div>

        <div class="border-t-2 border-stone-900 pt-4">
          <div class="flex justify-between font-bold"><span>Total</span><span>${{ totalPrice.toFixed(2) }}</span></div>
          <button type="button" class="mt-4 w-full bg-amber-600 py-3 text-xs font-bold uppercase tracking-widest text-white hover:bg-amber-700" @click="isCartOpen = false">Continue shopping</button>
        </div>
      </aside>
    </div>
  </div>
  <Footer/>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useProducts } from '~/composables/useProducts'

const { products } = useProducts()
const { items: cartItems, addToCart, updateQuantity, totalPrice } = useCart()

const activeSlide = ref(0)
const selectedTab = ref('All Items')
const isCartOpen = ref(false)

const categories = [
  {
    name: 'Starters',
    image: 'https://images.unsplash.com/photo-1541544741938-0af808871cc0?auto=format&fit=crop&w=400&q=80'
  },
  {
    name: 'Main Course',
    image: 'https://images.unsplash.com/photo-1621996346565-e3d5d6281273?auto=format&fit=crop&w=400&q=80'
  },
  {
    name: 'Desserts',
    image: 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=400&q=80'
  },
  {
    name: 'Beverages',
    image: 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=400&q=80'
  },
  {
    name: 'Pizza',
    image: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=400&q=80'
  },
  {
    name: 'Chef Specials',
    image: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=400&q=80'
  }
]

// Filter Tabs
const filterTabs = ['All Items', 'Starters', 'Main Course', 'Desserts', 'Beverages']

// Recommendation Items
const items = products

const filteredItems = computed(() => {
  if (selectedTab.value === 'All Items') return items.value
  return items.value.filter(item => item.category === selectedTab.value)
})

const goToProduct = (item) => {
  navigateTo(`/product/${item.id}`)
}

const addItemToCart = (item) => {
  addToCart(item)
  isCartOpen.value = true
}

const updateCartQuantity = (id, quantity) => {
  updateQuantity(id, quantity)
}

</script>