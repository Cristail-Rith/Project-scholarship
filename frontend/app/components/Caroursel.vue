<template>
  <div class="min-h-screen bg-[#FDFBF7] text-neutral-800 font-serif selection:bg-amber-200 selection:text-amber-900 overflow-x-hidden relative">



    <!-- 3. FULL SECTION BACKGROUND CAROUSEL HERO -->
    <section 
      class="relative min-h-[75vh] sm:min-h-[85vh] flex items-center overflow-hidden bg-stone-950 text-white"
      @mouseenter="pauseCarousel"
      @mouseleave="startCarousel"
    >
      <!-- Full-Bleed Carousel Background Image -->
      <div class="absolute inset-0 z-0 overflow-hidden">
        <transition name="bg-fade">
          <img 
            :key="currentSlideIndex"
            :src="slides[currentSlideIndex].bgImage" 
            :alt="slides[currentSlideIndex].titleHighlight" 
            class="w-full h-full object-cover object-center scale-105 transition-all duration-1000 brightness-90"
          />
        </transition>

        <!-- Dark Fine-Dining Gradient Overlay for Contrast -->
        <div class="absolute inset-0 bg-gradient-to-r from-stone-950/90 via-stone-950/65 to-stone-950/30"></div>
        <div class="absolute inset-0 bg-gradient-to-t from-stone-950 via-transparent to-stone-950/50"></div>
      </div>

      <!-- Hero Content Container -->
      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 md:px-12 py-16 md:py-24 w-full">
        <transition name="fade-slide" mode="out-in">
          <div :key="currentSlideIndex" class="max-w-2xl space-y-5 sm:space-y-6">
            
            <!-- Subtitle -->
            <div class="inline-block">
              <span class="text-xs sm:text-sm font-sans tracking-[0.3em] font-semibold text-[#C59237] uppercase flex items-center gap-2">
                <span class="w-6 h-[1px] bg-[#C59237]"></span>
                {{ slides[currentSlideIndex].subtitle }}
              </span>
            </div>

            <!-- Main Heading -->
            <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-serif text-stone-100 leading-[1.15] font-normal tracking-wide drop-shadow-md">
              {{ slides[currentSlideIndex].titleLine1 }} <br />
              {{ slides[currentSlideIndex].titleLine2 }}
              <span class="italic text-[#C59237] font-serif block sm:inline">
                {{ slides[currentSlideIndex].titleHighlight }}
              </span>
            </h1>

            <!-- Description -->
            <p class="font-sans text-stone-300 text-sm sm:text-base leading-relaxed max-w-lg font-light drop-shadow">
              {{ slides[currentSlideIndex].description }}
            </p>

            <!-- Action Buttons -->
            <div class="flex flex-wrap items-center gap-4 pt-2 font-sans">
              <NuxtLink
                to="/reservation"
                class="px-8 py-4 bg-[#C59237] hover:bg-[#b0802c] text-white text-xs font-semibold uppercase tracking-[0.2em] transition-all duration-300 shadow-xl hover:shadow-2xl rounded-sm"
              >
                Book A Table
              </NuxtLink>

              <NuxtLink
                to="/menu"
                class="px-8 py-4 border border-stone-300/80 hover:bg-white hover:text-stone-900 text-stone-100 text-xs font-semibold uppercase tracking-[0.2em] transition-all duration-300 rounded-sm backdrop-blur-sm bg-black/20"
              >
                Explore Menu
              </NuxtLink>
            </div>

            <!-- Carousel Pagination Indicators [ — • • ] -->
            <div class="flex items-center gap-3 pt-6">
              <button
                v-for="(slide, index) in slides"
                :key="index"
                @click="goToSlide(index)"
                :class="[
                  'h-2.5 transition-all duration-300 rounded-full focus:outline-none',
                  currentSlideIndex === index ? 'w-10 bg-[#C59237]' : 'w-2.5 bg-stone-500/80 hover:bg-stone-300'
                ]"
                :aria-label="`Go to slide ${index + 1}`"
              ></button>
            </div>

          </div>
        </transition>
      </div>
    </section>

    <!-- 4. OUR MENU CATEGORIES SECTION -->


    <!-- 5. CHEF'S RECOMMENDATIONS SECTION -->
    

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const mobileMenuOpen = ref(false)
const currentSlideIndex = ref(0)
const selectedTab = ref('All items')
let timer = null

// Carousel Slides with Full-Section Background Images
const slides = [
  {
    subtitle: 'Experience Fine Dining',
    titleLine1: 'Delicious Food,',
    titleLine2: 'Unforgettable',
    titleHighlight: 'Moments',
    description: 'A perfect blend of taste, art, and ambiance. Crafted to delight your senses with every bite.',
    bgImage: 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=1800&q=80'
  },
  {
    subtitle: 'Culinary Passion',
    titleLine1: 'Smokey Barbecue &',
    titleLine2: 'Signature Gourmet',
    titleHighlight: 'Grills',
    description: 'Slow-cooked prime ribs, house-made glazes, and heirloom garnish prepared by master chefs.',
    bgImage: 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1800&q=80'
  },
  {
    subtitle: 'Handcrafted Perfection',
    titleLine1: 'Memorable Nights,',
    titleLine2: 'Exquisite Gastronomy',
    titleHighlight: 'Flavors',
    description: 'Savor organic seasonal creations in a serene, luxurious fine dining atmosphere.',
    bgImage: 'https://images.unsplash.com/photo-1514944288352-fffac99f0bdf?auto=format&fit=crop&w=1800&q=80'
  }
]

// Auto Slide Timer Functions
const startCarousel = () => {
  stopCarousel()
  timer = setInterval(() => {
    currentSlideIndex.value = (currentSlideIndex.value + 1) % slides.length
  }, 5000)
}

const pauseCarousel = () => {
  stopCarousel()
}

const stopCarousel = () => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

const goToSlide = (index) => {
  currentSlideIndex.value = index
  startCarousel() // Reset timer on manual click
}

onMounted(() => {
  startCarousel()
})

onUnmounted(() => {
  stopCarousel()
})

// Categories
const categories = [
  { name: 'Starters', image: 'https://images.unsplash.com/photo-1541544741938-0af808871cc0?auto=format&fit=crop&w=400&q=80' },
  { name: 'Main Course', image: 'https://images.unsplash.com/photo-1621996346565-e3d5d6281273?auto=format&fit=crop&w=400&q=80' },
  { name: 'Desserts', image: 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=400&q=80' },
  { name: 'Beverages', image: 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=400&q=80' },
  { name: 'Pizza', image: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=400&q=80' },
  { name: 'Chef Specials', image: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=400&q=80' }
]

// Recommendation Items
const filterTabs = ['All items', 'Starters', 'Main Course', 'Desserts', 'Beverages']

const recommendationItems = [
  { id: 1, name: 'Grilled Salmon', category: 'Main Course', description: 'Served with lemon butter sauce', price: 24.99, rating: '4.8', badge: 'Bestseller', image: 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=500&q=80' },
  { id: 2, name: 'Creamy Prawn Pasta', category: 'Main Course', description: 'Penne in creamy garlic sauce', price: 21.99, rating: '4.7', badge: 'New', image: 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=500&q=80' },
  { id: 3, name: 'Ribeye Steak', category: 'Main Course', description: 'Grilled to perfection', price: 29.99, rating: '4.9', badge: null, image: 'https://images.unsplash.com/photo-1558030006-450675393462?auto=format&fit=crop&w=500&q=80' },
  { id: 4, name: 'Classic Tiramisu', category: 'Desserts', description: 'With cocoa & mascarpone', price: 8.99, rating: '4.6', badge: null, image: 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=500&q=80' }
]

const filteredItems = computed(() => {
  if (selectedTab.value === 'All items') return recommendationItems
  return recommendationItems.filter(i => i.category === selectedTab.value)
})
</script>

<style scoped>
.nav-link {
  position: relative;
  padding-bottom: 4px;
}
.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: #C59237;
  transition: width 0.3s ease;
}
.nav-link:hover::after,
.nav-link.active-link::after {
  width: 100%;
}

/* Smooth transition for Hero Carousel Content */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Smooth crossfade transition for Full Background Image */
.bg-fade-enter-active,
.bg-fade-leave-active {
  transition: opacity 1s ease-in-out;
}

.bg-fade-enter-from,
.bg-fade-leave-to {
  opacity: 0;
}
</style>