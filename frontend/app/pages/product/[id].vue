<script setup lang="ts">
import { ref, computed } from 'vue'
import CartSidebar from '~/components/CartSidebar.vue'

const route = useRoute()
const { products, pending, error } = useProducts()
const { addToCart } = useCart()

const product = computed(() => products.value.find(item => String(item.id) === String(route.params.id)))

// State Management
const quantity = ref(1)
const addedToast = ref(false)
const activeAccordion = ref<string | null>('details')
const activeImageIndex = ref(0)
const isFavorite = ref(false)

// Gallery images array fallback
const galleryImages = computed(() => {
  if (!product.value) return []
  return product.value.images && product.value.images.length > 0 
    ? product.value.images 
    : [product.value.image]
})

const currentImage = computed(() => galleryImages.value[activeImageIndex.value] || product.value?.image)

const increaseQty = () => quantity.value++
const decreaseQty = () => {
  if (quantity.value > 1) quantity.value--
}

const addProductToCart = () => {
  if (!product.value) return

  for (let i = 0; i < quantity.value; i++) {
    addToCart(product.value)
  }
  addedToast.value = true
  setTimeout(() => {
    addedToast.value = false
  }, 3200)
}

const toggleAccordion = (section: string) => {
  activeAccordion.value = activeAccordion.value === section ? null : section
}
</script>

<template>
  <div class="relative min-h-screen bg-[#ECE8E1] text-[#221F1D] font-sans antialiased selection:bg-[#F59E0B] selection:text-white">
    <!-- Ambient Blur Highlight Blobs -->
    <div class="fixed top-12 left-1/4 z-0 h-96 w-96 rounded-full bg-amber-500/10 blur-[120px] pointer-events-none" />
    <div class="fixed bottom-10 right-10 z-0 h-80 w-80 rounded-full bg-orange-600/10 blur-[100px] pointer-events-none" />

    <!-- Background Image with Soft Desaturated Overlay -->
    <div 
      class="fixed inset-0 bg-cover bg-center bg-no-repeat opacity-20 grayscale-40 pointer-events-none"
      style="background-image: url('https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?q=80&w=1600&auto=format&fit=crop');"
    />
    <div class="fixed inset-0 bg-[#F4F1EA]/85 backdrop-blur-xs pointer-events-none" />

    <div class="relative z-10">
      <Navbar />

      <main class="mx-auto max-w-5xl px-4 sm:px-6 py-8 sm:py-14 pb-28 sm:pb-16">
        <!-- Navigation Trail -->
        <nav class="flex items-center gap-2 text-[11px] font-semibold uppercase tracking-[0.2em] text-[#7A746E] mb-8">
          <NuxtLink to="/menu" class="hover:text-amber-600 transition-colors">Shop</NuxtLink>
          <span class="text-amber-500/60">&bull;</span>
          <span class="text-[#8C857E] truncate max-w-55">{{ product?.title || 'Collection' }}</span>
        </nav>

        <!-- Skeleton Loading State -->
        <div v-if="pending" class="grid gap-10 md:grid-cols-2 animate-pulse bg-[#F7F5F0] p-8 border border-[#E0D9CE] rounded-xl shadow-sm">
          <div class="h-115 bg-[#EBE6DC] rounded-lg" />
          <div class="space-y-4 py-6">
            <div class="h-3 w-20 bg-[#EBE6DC] rounded" />
            <div class="h-8 w-3/4 bg-[#EBE6DC] rounded" />
            <div class="h-5 w-16 bg-[#EBE6DC] rounded" />
            <div class="h-20 w-full bg-[#EBE6DC] rounded" />
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error || !product" class="py-20 text-center border border-[#D8D1C5] bg-[#F7F5F0]/90 rounded-2xl shadow-sm p-8">
          <p class="font-serif text-2xl text-[#221F1D]">Item Unavailable</p>
          <p class="mt-2 text-xs text-[#7A746E]">The product you are looking for is currently out of stock or removed.</p>
          <NuxtLink 
            to="/menu" 
            class="mt-6 inline-block rounded-lg border border-amber-600 bg-amber-600 px-6 py-3 text-[11px] font-bold uppercase tracking-[0.2em] text-white hover:bg-amber-700 transition-all shadow-md shadow-amber-600/20"
          >
            Back to Collection
          </NuxtLink>
        </div>

        <!-- Main Editorial Product Frame -->
        <article 
          v-else 
          class="border border-[#D8D1C5]/80 bg-[#F7F5F0]/90 backdrop-blur-md p-6 sm:p-10 rounded-2xl shadow-[0_15px_35px_rgba(0,0,0,0.04)] grid gap-10 md:gap-12 md:grid-cols-2 items-start"
        >
          <!-- Left: Product Image Gallery -->
          <div class="space-y-4">
            <div class="relative overflow-hidden rounded-xl border border-[#E2DBD0] bg-[#EFECE6] group">
              <img 
                :src="currentImage" 
                :alt="product.title" 
                class="h-100 sm:h-115 w-full object-cover object-center filter saturate-95 transition-all duration-700 hover:scale-105"
              />
              
              <!-- Highlight Stock Badge -->
              <span class="absolute top-4 left-4 bg-amber-500 text-white font-semibold text-[10px] uppercase tracking-widest px-3 py-1 rounded-full shadow-sm">
                In Stock &bull; Handcrafted
              </span>

              <!-- Wishlist Toggle Button -->
              <button 
                type="button" 
                @click="isFavorite = !isFavorite"
                class="absolute top-4 right-4 h-9 w-9 flex items-center justify-center rounded-full bg-[#F7F5F0]/80 backdrop-blur-md border border-[#D8D1C5] text-[#221F1D] hover:text-amber-600 transition-colors shadow-sm"
                aria-label="Save item"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" :class="{ 'fill-amber-500 stroke-amber-500': isFavorite, 'fill-none stroke-current': !isFavorite }" viewBox="0 0 24 24" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 0 0 0 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </button>
            </div>

            <!-- Thumbnail Selector List -->
            <div v-if="galleryImages.length > 1" class="flex gap-3 overflow-x-auto pb-1">
              <button 
                v-for="(img, idx) in galleryImages" 
                :key="idx" 
                @click="activeImageIndex = idx"
                class="relative h-16 w-16 shrink-0 overflow-hidden rounded-lg border-2 transition-all"
                :class="activeImageIndex === idx ? 'border-amber-600 scale-95 shadow-sm' : 'border-transparent opacity-70 hover:opacity-100'"
              >
                <img :src="img" :alt="product.title" class="h-full w-full object-cover" />
              </button>
            </div>
          </div>

          <!-- Right: Product Details Column -->
          <div class="flex flex-col">
            <div class="flex items-center justify-between">
              <!-- Category Tag with Accent Highlight -->
              <span class="inline-flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-[0.25em] text-amber-700 bg-amber-500/10 px-2.5 py-1 rounded-md">
                <span class="h-1.5 w-1.5 rounded-full bg-amber-500"></span>
                {{ product.category || 'Limited Batch' }}
              </span>

              <!-- Star Rating Indicator -->
              <div class="flex items-center gap-1 text-xs text-amber-600 font-semibold">
                <span>★</span>
                <span>4.9</span>
                <span class="text-[#8C857E] font-normal">(28)</span>
              </div>
            </div>

            <!-- Title -->
            <h1 class="mt-3 font-serif text-3xl sm:text-4xl text-[#221F1D] tracking-tight leading-snug">
              {{ product.title }}
            </h1>

            <!-- Price & Highlight Line -->
            <div class="mt-4 flex items-baseline gap-3 border-b border-[#E2DBD0] pb-5">
              <span class="font-serif text-3xl font-bold text-[#221F1D]">${{ product.price.toFixed(2) }}</span>
              <span class="text-xs text-amber-700 font-medium bg-amber-100/60 px-2 py-0.5 rounded">Free Express Shipping</span>
            </div>

            <!-- Description -->
            <p class="mt-5 text-xs sm:text-sm leading-relaxed text-[#5A544E]">
              {{ product.description }}
            </p>

            <!-- Quantity & Purchasing Panel -->
            <div class="mt-8 space-y-4 border-b border-[#E2DBD0] pb-7">
              <label class="block text-[10px] font-bold uppercase tracking-widest text-[#7A746E]">Select Quantity</label>
              
              <div class="flex gap-3">
                <!-- Stepper -->
                <div class="inline-flex items-center border border-[#C8C1B4] bg-[#FDFBF7] rounded-lg">
                  <button 
                    type="button" 
                    class="h-11 w-11 flex items-center justify-center text-[#5A544E] hover:text-amber-600 hover:bg-[#EAE5DC] transition-colors disabled:opacity-30 rounded-l-lg" 
                    :disabled="quantity <= 1"
                    @click="decreaseQty"
                    aria-label="Decrease quantity"
                  >
                    &#8722;
                  </button>
                  <span class="w-9 text-center font-bold text-xs text-[#221F1D]">
                    {{ quantity }}
                  </span>
                  <button 
                    type="button" 
                    class="h-11 w-11 flex items-center justify-center text-[#5A544E] hover:text-amber-600 hover:bg-[#EAE5DC] transition-colors rounded-r-lg" 
                    @click="increaseQty"
                    aria-label="Increase quantity"
                  >
                    &#43;
                  </button>
                </div>

                <!-- Add to Cart CTA with Amber Accent -->
                <button 
                  type="button" 
                  class="flex-1 rounded-lg border border-amber-600 bg-amber-600 py-3 text-[11px] font-bold uppercase tracking-[0.2em] text-white hover:bg-amber-700 active:scale-[0.99] transition-all shadow-md shadow-amber-600/20" 
                  @click="addProductToCart"
                >
                  Add To Cart &bull; ${{ (product.price * quantity).toFixed(2) }}
                </button>
              </div>

              <!-- Toast Feedback Banner -->
              <Transition name="fade">
                <div v-if="addedToast" class="flex items-center justify-between border border-amber-300/80 bg-amber-500/10 rounded-lg p-3 text-xs text-[#3D3834]">
                  <span class="flex items-center gap-2">
                    <span class="flex h-2 w-2 rounded-full bg-amber-500"></span>
                    Added <strong>{{ quantity }}x {{ product.title }}</strong> to bag.
                  </span>
                  <NuxtLink to="/cart" class="font-bold uppercase tracking-wider text-amber-700 underline hover:text-amber-800">
                    View Bag
                  </NuxtLink>
                </div>
              </Transition>
            </div>

            <!-- Accordion Details -->
            <div class="divide-y divide-[#E2DBD0] border-b border-[#E2DBD0]">
              <!-- Product Info Drawer -->
              <div>
                <button 
                  type="button" 
                  class="w-full py-3.5 flex items-center justify-between text-[11px] font-bold uppercase tracking-widest text-[#3D3834] text-left hover:text-amber-700 transition-colors"
                  @click="toggleAccordion('details')"
                >
                  <span>Materials & Craftsmanship</span>
                  <span class="text-xs font-bold text-amber-600">{{ activeAccordion === 'details' ? '−' : '+' }}</span>
                </button>
                <div v-if="activeAccordion === 'details'" class="pb-4 text-xs text-[#5A544E] leading-relaxed space-y-1.5">
                  <p>&bull; Sustainably crafted with organic, tactile materials.</p>
                  <p>&bull; Designed to age gracefully with daily use.</p>
                  <p>&bull; Inspected individually for quality and nuance.</p>
                </div>
              </div>

              <!-- Delivery Drawer -->
              <div>
                <button 
                  type="button" 
                  class="w-full py-3.5 flex items-center justify-between text-[11px] font-bold uppercase tracking-widest text-[#3D3834] text-left hover:text-amber-700 transition-colors"
                  @click="toggleAccordion('shipping')"
                >
                  <span>Shipping & Returns</span>
                  <span class="text-xs font-bold text-amber-600">{{ activeAccordion === 'shipping' ? '−' : '+' }}</span>
                </button>
                <div v-if="activeAccordion === 'shipping'" class="pb-4 text-xs text-[#5A544E] leading-relaxed space-y-1.5">
                  <p>&bull; Standard delivery takes 3–5 business days.</p>
                  <p>&bull; Complimentary shipping on orders over $50.</p>
                  <p>&bull; 30-day hassle-free return guarantee.</p>
                </div>
              </div>
            </div>

          </div>
        </article>
      </main>

      <!-- Sticky Mobile Quick-Buy Bar -->
      <div v-if="product" class="fixed bottom-0 inset-x-0 bg-[#F7F5F0]/95 backdrop-blur-md border-t border-[#D8D1C5] p-3 sm:hidden z-40 flex items-center justify-between gap-3 shadow-lg">
        <div>
          <p class="text-[10px] uppercase font-bold text-[#7A746E] truncate max-w-32.5">{{ product.title }}</p>
          <p class="font-serif text-base font-bold text-[#221F1D]">${{ (product.price * quantity).toFixed(2) }}</p>
        </div>
        <button 
          type="button" 
          @click="addProductToCart"
          class="flex-1 rounded-lg bg-amber-600 py-2.5 text-[10px] font-bold uppercase tracking-widest text-white shadow-md shadow-amber-600/20"
        >
          Add to Bag
        </button>
      </div>
    </div>
  </div>
  <CartSidebar/>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>