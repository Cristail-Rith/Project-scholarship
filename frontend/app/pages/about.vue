<script setup lang="ts">
import { ref } from 'vue'
import Navbar from '~/components/Navbar.vue';

// Highlights / Stats Data
const stats = ref([
  { label: 'Years of Tradition', value: '15+' },
  { label: 'Master Chefs', value: '08' },
  { label: 'Artisanal Recipes', value: '45+' },
  { label: 'Local Suppliers', value: '100%' }
])

// Brand Features
const features = ref([
  {
    title: 'Locally Sourced Ingredients',
    description: 'Partnering directly with organic local farmers to bring fresh, peak-season produce to your table every day.'
  },
  {
    title: 'Woodfired Craftsmanship',
    description: 'Our signature dishes are slow-cooked over natural wood embers for deep, smoky flavors and rich textures.'
  },
  {
    title: 'Uncompromised Passion',
    description: 'Every recipe is developed with dedicated precision, balancing traditional culinary heritage with modern flair.'
  }
])
</script>

<template>
  <Navbar/>
  <section class="bg-white text-stone-900 font-sans py-24 px-4 sm:px-6 lg:px-8 border-t-2 border-stone-900 selection:bg-amber-600 selection:text-white">
    <div class="max-w-7xl mx-auto space-y-20">
      
      <!-- Top Layout: Story Content & Image Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16 items-center">
        
        <!-- Left Column: Editorial Text -->
        <div class="lg:col-span-6 space-y-6">
          
          <!-- Accent Subtitle -->
          <div class="flex items-center gap-3">
            <span class="h-px w-10 bg-amber-600"></span>
            <span class="text-amber-700 text-xs font-black uppercase tracking-[0.25em]">Our Story</span>
          </div>

          <!-- Section Heading -->
          <h2 class="text-4xl sm:text-5xl font-serif font-black text-stone-900 tracking-tight leading-tight uppercase">
            Crafting Culinary <br />
            <span class="text-amber-700 italic font-serif font-normal">Memories Since 2011</span>
          </h2>

          <!-- Main Narrative -->
          <p class="text-stone-700 text-sm sm:text-base leading-relaxed font-medium">
            Founded with a simple vision: to unite people through the rich, comforting warmth of authentic woodfired cooking and uncompromised hospitality. What began as a small family kitchen has grown into a cherished dining destination.
          </p>

          <p class="text-stone-600 text-xs sm:text-sm leading-relaxed">
            We believe that extraordinary food starts long before the kitchen. It begins in the soil with our partner farmers, continues through our wood-fueled hearths, and finishes on your plate with meticulous attention to detail.
          </p>

          <!-- Action Button & Chef Quote Signature -->
          <div class="pt-4 flex flex-col sm:flex-row items-start sm:items-center gap-6">
            <button 
              class="bg-stone-900 hover:bg-amber-600 text-white font-extrabold text-xs px-8 py-4 uppercase tracking-widest transition-all duration-200 border-2 border-stone-900 hover:border-amber-600 rounded-none shadow-xs active:translate-y-0.5"
            >
              Explore Our Story
            </button>

            <div class="border-l-2 border-amber-600 pl-4 py-1">
              <p class="font-serif italic text-stone-900 font-bold text-sm">"Flavor is a memory waiting to happen."</p>
              <span class="text-[10px] text-stone-500 font-bold uppercase tracking-wider">— Master Chef & Founder</span>
            </div>
          </div>

        </div>

        <!-- Right Column: Sharp Visual Grid -->
        <div class="lg:col-span-6 relative">
          
          <div class="grid grid-cols-2 gap-4">
            <!-- Large Image -->
            <div class="border-2 border-stone-900 bg-stone-100 overflow-hidden group">
              <img 
                src="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80" 
                alt="Chef preparing grill" 
                class="w-full h-80 sm:h-96 object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
              />
            </div>

            <!-- Second Image with Offset Accent Badge -->
            <div class="space-y-4 flex flex-col justify-between">
              <div class="border-2 border-stone-900 bg-stone-100 overflow-hidden group h-full">
                <img 
                  src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80" 
                  alt="Restaurant interior ambiance" 
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
                />
              </div>

              <!-- Accent Badge Box -->
              <div class="bg-stone-900 text-white p-5 border-2 border-stone-900 rounded-none space-y-1">
                <span class="text-amber-500 text-xs font-black uppercase tracking-widest">Quality Guaranteed</span>
                <p class="text-xs font-medium text-stone-300">Flame-cooked perfection with 100% organic oakwood embers.</p>
              </div>
            </div>
          </div>

        </div>

      </div>

      <!-- Middle Divider: Key Features Row -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 border-y-2 border-stone-900 py-12">
        <div 
          v-for="(feature, idx) in features" 
          :key="idx" 
          class="space-y-2 pr-4 border-l-2 border-transparent hover:border-amber-600 pl-4 transition-colors"
        >
          <span class="text-amber-700 font-mono font-bold text-xs">0{{ idx + 1 }}.</span>
          <h3 class="text-lg font-serif font-black text-stone-900 uppercase tracking-tight">{{ feature.title }}</h3>
          <p class="text-stone-600 text-xs leading-relaxed font-medium">{{ feature.description }}</p>
        </div>
      </div>

      <!-- Bottom Stats Counter Section -->
      <div class="bg-stone-50 border-2 border-stone-900 p-8 sm:p-12">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center divide-x-0 sm:divide-x-2 divide-stone-200">
          <div 
            v-for="(stat, idx) in stats" 
            :key="idx"
            class="space-y-1"
          >
            <div class="text-4xl sm:text-5xl font-serif font-black text-amber-700">{{ stat.value }}</div>
            <div class="text-xs font-extrabold text-stone-900 uppercase tracking-widest">{{ stat.label }}</div>
          </div>
        </div>
      </div>

    </div>
  </section>
</template>