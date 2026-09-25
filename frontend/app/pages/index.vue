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
    <section v-if="false" class="py-16 max-w-7xl mx-auto px-6">
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
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        <div
          v-for="item in filteredItems"
          :key="item.id"
          class="cursor-pointer bg-white border border-gray-300 rounded-[5px] border-sm overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col group"
          @click="goToProduct(item)"
        >
          <!-- Image with Badges -->
          <div class="relative overflow-hidden h-64">
            <img
              :src="item.image"
              :alt="item.title"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

            <!-- Rating Badge -->
            <div
              v-if="item.rating && parseFloat(item.rating) > 0"
              class="absolute top-3 right-3 bg-white/95 backdrop-blur-sm text-amber-600 text-xs font-sans px-2 py-1 rounded-full shadow border border-amber-200 flex items-center gap-0.5"
            >
              <svg class="w-3.5 h-3.5 fill-amber-400" viewBox="0 0 24 24">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7.91 15.14 4 9.27 10.91 8.26z"/>
              </svg>
              {{ parseFloat(item.rating).toFixed(1) }}
            </div>

            <!-- Sale Badge -->
            <div
              v-if="item.previousPrice && item.previousPrice > item.price"
              class="absolute top-3 left-3 bg-rose-500 text-white text-[10px] font-sans font-bold px-2.5 py-1 rounded-full shadow"
            >
              SALE
            </div>

            <!-- Quick Add overlay button -->
            <button
              v-if="item.stockQuantity > 0"
              @click.stop="addItemToCart(item)"
              class="absolute bottom-3 right-3 w-10 h-10 bg-white/95 hover:bg-amber-600 hover:text-white rounded-full shadow-lg flex items-center justify-center transition-all duration-200 opacity-0 translate-y-2 group-hover:opacity-100 group-hover:translate-y-0"
              aria-label="Add to cart"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.89 2M7 13h10.1l-.95 4.55L7 13z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V3a4 4 0 00-8 0v8m8 7H8a2 2 0 1 0 0 4h8a2 2 0 1 0 0-4z"/>
              </svg>
            </button>
          </div>

          <!-- Content -->
          <div class="p-5 flex-1 flex flex-col">
            <div class="flex-1">
              <h3
                class="font-serif text-xl font-bold text-stone-900 group-hover:text-[#C59237] transition-colors line-clamp-1 "
              >
                {{ item.title }}
              </h3>

              <!-- Price -->
              <div class="mt-2 flex items-center gap-2">
                <span class="font-sans font-bold text-xl text-[#C59237]">
                  ${{ item.price.toFixed(2) }}
                </span>
                <span
                  v-if="item.previousPrice && item.previousPrice > item.price"
                  class="font-sans text-sm text-stone-400 line-through"
                >
                  ${{ item.previousPrice.toFixed(2) }}
                </span>
              </div>

              <!-- Short Description -->
              <p
                v-if="item.description"
                class="mt-3 font-sans text-xs text-stone-500 line-clamp-2 leading-relaxed"
              >
                {{ item.description }}
              </p>
            </div>

            <!-- Action Button -->
            <button
              @click.stop="addItemToCart(item)"
              class="mt-4 w-full py-2.5 bg-amber-600 hover:bg-amber-700 text-white text-xs font-sans font-semibold tracking-wider uppercase rounded-[5px] transition-colors duration-200 shadow-sm hover:shadow-md"
            >
              Add To Order
            </button>
          </div>
        </div>

        <!-- Empty State -->
        <div
          v-if="filteredItems.length === 0"
          class="col-span-full text-center py-16 text-stone-400"
        >
          <svg class="w-16 h-16 mx-auto mb-4 text-stone-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 3h2l.89 2M7 13h10.1l-.95 4.55L7 13z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V3a4 4 0 00-8 0v8m8 7H8a2 2 0 1 0 0 4h8a2 2 0 1 0 0-4z"/>
          </svg>
          <p class="text-lg font-medium">No items found</p>
          <p class="text-sm mt-1">Try adjusting your search or filter criteria</p>
        </div>
      </div>
    </section>

    <section class="max-w-7xl mx-auto px-6 py-16">
      <header class="mb-9 text-center"><p class="font-sans text-xs uppercase tracking-[0.25em] text-amber-700">Picked for you</p><h2 class="mt-2 font-serif text-3xl md:text-4xl">Hot from our kitchen</h2><p class="mt-3 font-sans text-stone-500">Guest favorites, freshly prepared every day.</p></header>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <article v-for="item in hotProducts" :key="item.id" class="overflow-hidden rounded-2xl bg-white border border-stone-200 shadow-sm hover:shadow-lg transition-shadow">
          <button class="relative block w-full h-56 text-left" @click="goToProduct(item)"><img :src="item.image" :alt="item.title" class="w-full h-full object-cover" /><span class="absolute top-4 left-4 rounded-full bg-amber-700 px-3 py-1 text-xs font-sans font-bold uppercase text-white">🔥 Hot pick</span></button>
          <div class="p-5"><div class="flex justify-between gap-3"><h3 class="font-serif text-xl font-semibold">{{ item.title }}</h3><span class="font-sans font-bold text-amber-700">${{ Number(item.price).toFixed(2) }}</span></div><p class="mt-2 min-h-10 text-sm text-stone-500 font-sans line-clamp-2">{{ item.description }}</p><button @click="addItemToCart(item)" class="mt-4 w-full rounded-lg bg-neutral-900 py-3 text-xs font-sans font-semibold uppercase tracking-widest text-white hover:bg-amber-700">Add to order</button></div>
        </article>
      </div>
      <div class="mt-8 text-center"><NuxtLink to="/menu" class="inline-flex rounded-full border border-stone-300 px-6 py-3 font-sans text-sm hover:border-amber-600 hover:text-amber-700">Explore full menu →</NuxtLink></div>
    </section>

    <section v-if="offerProducts.length" class="bg-[#211d19] py-16 text-white">
      <div class="max-w-7xl mx-auto px-6"><div class="mb-8"><p class="font-sans text-xs uppercase tracking-[0.25em] text-amber-400">Limited time</p><h2 class="mt-2 font-serif text-3xl md:text-4xl">Special offers</h2></div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5"><article v-for="item in offerProducts" :key="item.id" class="flex overflow-hidden rounded-xl bg-white/10 ring-1 ring-white/10"><img :src="item.image" :alt="item.title" class="h-36 w-32 object-cover"/><div class="flex min-w-0 flex-1 flex-col justify-center p-4"><span class="font-sans text-[10px] font-bold uppercase tracking-widest text-amber-400">Save {{ discountPercent(item) }}%</span><h3 class="mt-1 truncate font-serif text-lg">{{ item.title }}</h3><div class="mt-2 flex gap-2 font-sans"><span class="font-bold text-amber-300">${{ Number(item.price).toFixed(2) }}</span><del class="text-sm text-stone-400">${{ Number(item.previousPrice).toFixed(2) }}</del></div><button @click="addItemToCart(item)" class="mt-3 self-start text-xs font-sans font-semibold uppercase text-white underline decoration-amber-400 underline-offset-4">Add to order</button></div></article></div>
      </div>
    </section>

    <section class="bg-[#FAF7F2] py-16"><div class="max-w-7xl mx-auto px-6"><header class="mb-8 flex items-end justify-between"><div><p class="font-sans text-xs uppercase tracking-[0.25em] text-amber-700">Just added</p><h2 class="mt-2 font-serif text-3xl md:text-4xl">New to the menu</h2></div><NuxtLink to="/menu" class="font-sans text-sm text-amber-800 hover:underline">See full menu →</NuxtLink></header>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4"><button v-for="item in newProducts" :key="item.id" @click="goToProduct(item)" class="group overflow-hidden rounded-xl bg-white text-left shadow-sm hover:shadow-md"><div class="relative h-40 sm:h-48"><img :src="item.image" :alt="item.title" class="h-full w-full object-cover transition-transform group-hover:scale-105"/><span class="absolute left-3 top-3 rounded-full bg-white px-3 py-1 font-sans text-[10px] font-bold uppercase text-amber-800">New</span></div><div class="p-4"><h3 class="truncate font-serif text-lg">{{ item.title }}</h3><p class="mt-1 font-sans font-semibold text-amber-700">${{ Number(item.price).toFixed(2) }}</p></div></button></div>
    </div></section>

    <section v-if="setProducts.length" class="max-w-7xl mx-auto px-6 py-16"><header class="mb-8 text-center"><p class="font-sans text-xs uppercase tracking-[0.25em] text-amber-700">Made to share</p><h2 class="mt-2 font-serif text-3xl md:text-4xl">Dinner sets & bundles</h2><p class="mt-3 font-sans text-stone-500">Thoughtful combinations for date night and the whole table.</p></header>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6"><article v-for="item in setProducts" :key="item.id" class="flex overflow-hidden rounded-2xl border border-stone-200 bg-white shadow-sm"><img :src="item.image" :alt="item.title" class="w-2/5 min-h-48 object-cover"/><div class="flex flex-1 flex-col justify-center p-5"><span class="font-sans text-[10px] font-bold uppercase tracking-widest text-amber-700">Chef's set</span><h3 class="mt-1 font-serif text-xl">{{ item.title }}</h3><p class="mt-2 text-sm text-stone-500 font-sans line-clamp-2">{{ item.description }}</p><div class="mt-4 flex items-center justify-between gap-3"><span class="font-sans text-lg font-bold text-amber-700">${{ Number(item.price).toFixed(2) }}</span><button @click="addItemToCart(item)" class="rounded-lg bg-amber-700 px-4 py-2.5 font-sans text-xs font-semibold uppercase text-white hover:bg-amber-800">Add set</button></div></div></article></div>
    </section>

    <CartSidebar/>
  </div>
  <Footer/>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useProducts } from '~/composables/useProducts'
import CartSidebar from '~/components/CartSidebar.vue'

const { apiBase } = useApiBase()

const { products } = useProducts()

const {
  items: cartItems,
  addToCart,
  updateQuantity,
  totalPrice,
  isCartOpen
} = useCart()
const { data: categoryData } = useFetch('/categories', {
  baseURL: apiBase.value,
  default: () => []
})

const activeSlide = ref(0)

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
      : `${apiBase.value}${category.image}`
  }
  return categoryFallbackImages[category.name] || categoryFallbackImages['Main Course']
}

const hotSkus = ['SEED-004', 'SEED-014', 'SEED-017', 'SEED-024', 'SEED-029', 'SEED-030']
const hotProducts = computed(() => {
  const selected = hotSkus.map(sku => products.value.find(item => item.sku === sku)).filter(item => item && item.status !== 'Out of Stock')
  return (selected.length ? selected : [...products.value].sort((a, b) => Number(b.rating || 0) - Number(a.rating || 0))).slice(0, 6)
})
const offerProducts = computed(() => products.value.filter(item => Number(item.previousPrice) > Number(item.price)).slice(0, 3))
const newProducts = computed(() => [...products.value].sort((a, b) => Number(b.id) - Number(a.id)).slice(0, 4))
const setProducts = computed(() => products.value.filter(item => /\b(set|bundle|feast|for two)\b/i.test(item.title)).slice(-5))
const discountPercent = item => Math.round((1 - Number(item.price) / Number(item.previousPrice)) * 100)

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
