<template>
    <navbar/>
  <div class="min-h-screen bg-[#FDFBF7] text-neutral-800 font-serif selection:bg-amber-200 selection:text-amber-900 overflow-x-hidden">
    
    <!-- Hero Banner Header -->
    <section class="relative bg-stone-950 text-white py-20 md:py-28 px-4 overflow-hidden">
      <img 
        src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1800&q=80" 
        alt="Restaurant Atmosphere" 
        class="absolute inset-0 w-full h-full object-cover opacity-25 filter brightness-75 scale-105"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-stone-950 via-stone-950/60 to-transparent"></div>
      
      <div class="relative max-w-4xl mx-auto text-center space-y-4 z-10">
        <span class="text-xs font-sans tracking-[0.3em] uppercase text-[#C59237] font-semibold">Visual Atmosphere</span>
        <h1 class="text-4xl md:text-6xl font-serif text-stone-100 font-normal tracking-wide">Our Gallery</h1>
        <p class="font-sans text-stone-300 text-xs sm:text-sm max-w-lg mx-auto font-light leading-relaxed">
          Take a glimpse into the FLAVORIA experience—from masterfully plated dishes to intimate dining spaces and memorable events.
        </p>
      </div>
    </section>

    <!-- Main Gallery Section -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 py-12 md:py-16">
      
      <!-- Category Filter Tabs -->
      <div class="flex flex-wrap justify-center items-center gap-3 sm:gap-6 font-sans text-xs font-semibold tracking-widest uppercase mb-10 sm:mb-12">
        <button
          v-for="category in categories"
          :key="category"
          @click="activeCategory = category"
          :class="[
            'px-5 py-2.5 rounded-xs transition-all duration-300 border',
            activeCategory === category 
              ? 'bg-[#C59237] text-white border-[#C59237] shadow-sm' 
              : 'bg-white text-stone-600 border-stone-200 hover:border-[#C59237] hover:text-[#C59237]'
          ]"
        >
          {{ category }}
        </button>
      </div>

      <!-- Gallery Grid -->
      <transition-group 
        tag="div" 
        name="gallery-fade"
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        <div
          v-for="(item, index) in filteredItems"
          :key="item.id"
          @click="openLightbox(index)"
          class="relative bg-stone-900 rounded-sm overflow-hidden group cursor-pointer border border-stone-200/80 shadow-sm hover:shadow-xl transition-all duration-500 h-72"
        >
          <!-- Image -->
          <img 
            :src="item.image" 
            :alt="item.title"
            class="w-full h-full object-cover object-center group-hover:scale-110 transition-transform duration-700 brightness-95 group-hover:brightness-100"
          />

          <!-- Dark Overlay on Hover -->
          <div class="absolute inset-0 bg-gradient-to-t from-stone-950/90 via-stone-950/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-6">
            <span class="text-[10px] font-sans font-semibold tracking-[0.25em] text-[#C59237] uppercase mb-1">
              {{ item.category }}
            </span>
            <h3 class="font-serif text-lg text-white font-medium">
              {{ item.title }}
            </h3>
            <p v-if="item.description" class="text-xs font-sans text-stone-300 font-light mt-1 line-clamp-2">
              {{ item.description }}
            </p>

            <!-- Zoom Icon Accent -->
            <div class="absolute top-4 right-4 w-9 h-9 rounded-full bg-black/40 backdrop-blur-md flex items-center justify-center text-white border border-white/20">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v6m3-3H7" />
              </svg>
            </div>
          </div>
        </div>
      </transition-group>

    </section>

    <!-- Fullscreen Lightbox Modal -->
    <transition name="modal-fade">
      <div 
        v-if="lightboxOpen" 
        class="fixed inset-0 z-50 bg-stone-950/95 backdrop-blur-md flex items-center justify-center p-4 sm:p-8"
        @click.self="closeLightbox"
      >
        <!-- Close Button -->
        <button 
          @click="closeLightbox" 
          class="absolute top-6 right-6 text-stone-400 hover:text-white p-2 transition-colors z-10"
          aria-label="Close Lightbox"
        >
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <!-- Previous Button -->
        <button 
          @click="prevImage" 
          class="absolute left-4 sm:left-8 top-1/2 -translate-y-1/2 text-stone-400 hover:text-white p-3 rounded-full bg-stone-900/60 hover:bg-stone-900 border border-stone-800 transition-colors z-10"
          aria-label="Previous Image"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <!-- Next Button -->
        <button 
          @click="nextImage" 
          class="absolute right-4 sm:right-8 top-1/2 -translate-y-1/2 text-stone-400 hover:text-white p-3 rounded-full bg-stone-900/60 hover:bg-stone-900 border border-stone-800 transition-colors z-10"
          aria-label="Next Image"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>

        <!-- Lightbox Content Card -->
        <div class="max-w-4xl w-full bg-stone-900 rounded-sm overflow-hidden border border-stone-800 shadow-2xl flex flex-col md:flex-row max-h-[85vh]">
          <div class="md:w-2/3 bg-black flex items-center justify-center min-h-[300px]">
            <img 
              :src="filteredItems[lightboxIndex].image" 
              :alt="filteredItems[lightboxIndex].title" 
              class="w-full h-full max-h-[70vh] object-contain"
            />
          </div>
          
          <div class="md:w-1/3 p-6 font-sans space-y-3 flex flex-col justify-between bg-stone-900">
            <div class="space-y-2">
              <span class="text-[10px] font-semibold tracking-[0.2em] text-[#C59237] uppercase">
                {{ filteredItems[lightboxIndex].category }}
              </span>
              <h3 class="font-serif text-2xl text-stone-100">
                {{ filteredItems[lightboxIndex].title }}
              </h3>
              <p class="text-xs text-stone-400 leading-relaxed font-light">
                {{ filteredItems[lightboxIndex].description }}
              </p>
            </div>

            <div class="pt-4 border-t border-stone-800 flex items-center justify-between text-xs text-stone-500">
              <span>FLAVORIA Collection</span>
              <span>{{ lightboxIndex + 1 }} / {{ filteredItems.length }}</span>
            </div>
          </div>
        </div>

      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const activeCategory = ref('All')
const lightboxOpen = ref(false)
const lightboxIndex = ref(0)

const categories = ['All', 'Dishes', 'Ambiance', 'Drinks', 'Events']

const galleryItems = ref([
  { id: 1, title: 'Seared Wagyu Ribeye', category: 'Dishes', description: 'Served with truffled mushroom jus and microgreens.', image: 'https://images.unsplash.com/photo-1558030006-450675393462?auto=format&fit=crop&w=1000&q=80' },
  { id: 2, title: 'Main Dining Hall', category: 'Ambiance', description: 'Warm ambient lighting designed for intimate conversations.', image: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1000&q=80' },
  { id: 3, title: 'Smokey Bourbon Cocktail', category: 'Drinks', description: 'Infused with oak smoke and artisanal bitters.', image: 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=1000&q=80' },
  { id: 4, title: 'Pan-Seared Sea Bass', category: 'Dishes', description: 'Accompanied by saffron risotto and dill oil.', image: 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=1000&q=80' },
  { id: 5, title: 'Private Chef Dining Table', category: 'Events', description: 'Exclusive seating for private tasting menus.', image: 'https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?auto=format&fit=crop&w=1000&q=80' },
  { id: 6, title: 'Artisan Berry Tart', category: 'Dishes', description: 'Fresh seasonal berries over vanilla bean custard.', image: 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=1000&q=80' },
  { id: 7, title: 'Outdoor Courtyard Bar', category: 'Ambiance', description: 'Serene garden atmosphere under soft evening lights.', image: 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=1000&q=80' },
  { id: 8, title: 'Vintage Red Wine Pairing', category: 'Drinks', description: 'Curated wine collection from historic European vineyards.', image: 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?auto=format&fit=crop&w=1000&q=80' },
  { id: 9, title: 'Gourmet Wine Tasting Night', category: 'Events', description: 'Monthly sommelier-led wine and dine pairing event.', image: 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?auto=format&fit=crop&w=1000&q=80' }
])

const filteredItems = computed(() => {
  if (activeCategory.value === 'All') return galleryItems.value
  return galleryItems.value.filter(item => item.category === activeCategory.value)
})

const openLightbox = (index) => {
  lightboxIndex.value = index
  lightboxOpen.value = true
  document.body.style.overflow = 'hidden'
}

const closeLightbox = () => {
  lightboxOpen.value = false
  document.body.style.overflow = ''
}

const prevImage = () => {
  lightboxIndex.value = (lightboxIndex.value - 1 + filteredItems.value.length) % filteredItems.value.length
}

const nextImage = () => {
  lightboxIndex.value = (lightboxIndex.value + 1) % filteredItems.value.length
}

const handleKeydown = (e) => {
  if (!lightboxOpen.value) return
  if (e.key === 'Escape') closeLightbox()
  if (e.key === 'ArrowLeft') prevImage()
  if (e.key === 'ArrowRight') nextImage()
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
/* Gallery Item Transition */
.gallery-fade-move,
.gallery-fade-enter-active,
.gallery-fade-leave-active {
  transition: all 0.5s ease;
}

.gallery-fade-enter-from,
.gallery-fade-leave-to {
  opacity: 0;
  transform: scale(0.92);
}

.gallery-fade-leave-active {
  position: absolute;
}

/* Modal Transition */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>