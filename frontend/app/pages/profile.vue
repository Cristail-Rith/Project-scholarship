<template>
    <Navbar/>
  <div class="min-h-screen bg-[#FDFBF7] text-neutral-800 font-serif selection:bg-amber-200 selection:text-amber-900 overflow-x-hidden">
    
    <!-- Hero Section -->
    <section class="relative bg-stone-950 text-white py-20 md:py-28 px-4 overflow-hidden">
      <div class="absolute inset-0 z-0">
        <img 
          src="https://images.unsplash.com/photo-1577219491135-ce391730fb2c?auto=format&fit=crop&w=2000&q=80" 
          alt="Chef Background" 
          class="w-full h-full object-cover opacity-20 filter brightness-75 scale-105"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-stone-950 via-stone-950/60 to-transparent"></div>
      </div>
      
      <div class="relative max-w-4xl mx-auto text-center space-y-4 z-10">
        <span class="text-xs font-sans tracking-[0.3em] uppercase text-[#C59237] font-semibold">Master Culinary Artist</span>
        <h1 class="text-4xl md:text-6xl font-serif text-stone-100 font-normal tracking-wide">Meet Chef Marco Laurent</h1>
        <p class="font-sans text-stone-300 text-xs sm:text-sm max-w-lg mx-auto font-light leading-relaxed">
          Crafting unforgettable dining experiences through a blend of classical French technique and modern innovation.
        </p>
      </div>
    </section>

    <!-- Chef Biography & Portrait -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 py-16 md:py-24">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        
        <!-- Chef Image Banner -->
        <div class="lg:col-span-5 relative">
          <div class="relative rounded-sm overflow-hidden border border-stone-200/80 shadow-2xl bg-stone-900">
            <img 
              src="https://images.unsplash.com/photo-1583394838336-acd977736f90?auto=format&fit=crop&w=1000&q=80" 
              alt="Executive Chef Marco Laurent" 
              class="w-full h-[500px] object-cover object-top"
            />
            <div class="absolute bottom-0 inset-x-0 bg-gradient-to-t from-stone-950/90 via-stone-950/40 to-transparent p-6 text-white font-sans">
              <span class="text-[10px] tracking-[0.2em] text-[#C59237] uppercase font-semibold">Executive Chef</span>
              <h3 class="font-serif text-2xl text-stone-100">Marco Laurent</h3>
            </div>
          </div>
          <!-- Decorative Frame Overlay -->
          <div class="hidden sm:block absolute -bottom-4 -right-4 w-full h-full border-2 border-[#C59237]/40 -z-10 rounded-sm"></div>
        </div>

        <!-- Chef Narrative Content -->
        <div class="lg:col-span-7 space-y-6 font-sans">
          <span class="text-xs font-semibold tracking-[0.25em] text-[#C59237] uppercase">The Story</span>
          <h2 class="font-serif text-3xl sm:text-4xl font-normal text-stone-900 leading-snug">
            "Gastronomy is an art form that engages every human sense simultaneously."
          </h2>
          
          <div class="space-y-4 text-stone-600 text-xs sm:text-sm leading-relaxed font-light">
            <p>
              With over 18 years of culinary excellence across Paris, Tokyo, and New York, Chef Marco Laurent brings an unrivaled passion to FLAVORIA. Trained in classic French gastronomy at Le Cordon Bleu Paris, Marco spent years refining his signature style alongside Michelin-starred masters.
            </p>
            <p>
              His philosophy focuses on ingredient-first cooking—sourcing seasonal, organic produce and sustainably harvested seafood to craft balanced, visually striking dishes.
            </p>
          </div>

          <!-- Quick Achievements Bar -->
          <div class="grid grid-cols-3 gap-4 pt-6 border-t border-stone-200/80">
            <div>
              <span class="block font-serif text-2xl md:text-3xl text-[#C59237]">18+</span>
              <span class="text-[10px] uppercase tracking-wider text-stone-500 font-semibold">Years Experience</span>
            </div>
            <div>
              <span class="block font-serif text-2xl md:text-3xl text-[#C59237]">3★</span>
              <span class="text-[10px] uppercase tracking-wider text-stone-500 font-semibold">Michelin Background</span>
            </div>
            <div>
              <span class="block font-serif text-2xl md:text-3xl text-[#C59237]">25+</span>
              <span class="text-[10px] uppercase tracking-wider text-stone-500 font-semibold">Signature Dishes</span>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- Chef's Culinary Philosophy Section -->
    <section class="bg-[#FAF7F2] py-16 sm:py-20 border-t border-b border-stone-200/60">
      <div class="max-w-7xl mx-auto px-4 sm:px-6">
        <div class="text-center max-w-2xl mx-auto mb-12 space-y-2">
          <span class="text-xs font-sans tracking-[0.25em] uppercase text-[#C59237] font-semibold">Core Values</span>
          <h2 class="font-serif text-3xl font-normal text-stone-900">Culinary Pillars</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="pillar in pillars" :key="pillar.title" class="bg-white p-8 rounded-sm border border-stone-200/80 shadow-sm font-sans space-y-3">
            <div class="w-10 h-10 rounded-full bg-amber-50 flex items-center justify-center text-[#C59237] mb-4">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" :d="pillar.iconPath" />
              </svg>
            </div>
            <h3 class="font-serif text-xl text-stone-900 font-medium">{{ pillar.title }}</h3>
            <p class="text-xs text-stone-500 leading-relaxed font-light">{{ pillar.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Signature Creations Showcase -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 py-16 md:py-24">
      <div class="text-center mb-12 space-y-2">
        <span class="text-xs font-sans tracking-[0.25em] uppercase text-[#C59237] font-semibold">Handcrafted Menus</span>
        <h2 class="font-serif text-3xl md:text-4xl text-neutral-900 font-normal">Chef's Signature Dishes</h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div 
          v-for="dish in signatureDishes" 
          :key="dish.title"
          class="bg-white border border-stone-200/80 rounded-sm overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 group"
        >
          <div class="relative h-64 overflow-hidden bg-stone-900">
            <img 
              :src="dish.image" 
              :alt="dish.title" 
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            />
            <span class="absolute top-3 right-3 bg-stone-900/90 text-[#C59237] text-xs font-sans font-semibold px-3 py-1 rounded-xs backdrop-blur-sm border border-stone-700">
              {{ dish.price }}
            </span>
          </div>

          <div class="p-6 font-sans space-y-2">
            <h3 class="font-serif text-xl font-medium text-stone-900 group-hover:text-[#C59237] transition-colors">
              {{ dish.title }}
            </h3>
            <p class="text-xs text-stone-500 leading-relaxed font-light">
              {{ dish.description }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Reserve Chef's Table Call To Action -->
    <section class="relative py-20 px-4 sm:px-6 bg-stone-950 text-white overflow-hidden">
      <div class="absolute inset-0 z-0">
        <img 
          src="https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?auto=format&fit=crop&w=2000&q=80" 
          alt="Chef's Table" 
          class="w-full h-full object-cover opacity-25 filter brightness-75 scale-105"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-stone-950 via-stone-950/70 to-stone-950"></div>
      </div>

      <div class="relative z-10 max-w-3xl mx-auto text-center space-y-6 font-sans">
        <span class="text-xs font-semibold tracking-[0.25em] text-[#C59237] uppercase">Exclusive Experience</span>
        <h2 class="font-serif text-3xl sm:text-5xl font-normal text-stone-100">Experience The Chef's Table</h2>
        <p class="text-stone-300 text-xs sm:text-sm font-light leading-relaxed max-w-lg mx-auto">
          Book an intimate multi-course tasting menu curated personally by Chef Marco, complete with bespoke wine pairings.
        </p>
        <div>
          <NuxtLink 
            to="/events" 
            class="inline-block px-10 py-4 bg-[#C59237] hover:bg-[#b0802c] active:scale-[0.99] text-white text-xs font-semibold uppercase tracking-[0.2em] transition-all rounded-xs shadow-lg shadow-amber-900/20"
          >
            Reserve Private Table
          </NuxtLink>
        </div>
      </div>
    </section>

  </div>

</template>

<script setup>
import { ref } from 'vue'

const pillars = ref([
  {
    title: 'Sustainably Sourced',
    description: 'Every ingredient is handpicked daily from local organic farms and certified sustainable fisheries.',
    iconPath: 'M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z'
  },
  {
    title: 'Precision Technique',
    description: 'Combining time-honored French culinary principles with modern avant-garde cooking techniques.',
    iconPath: 'M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4'
  },
  {
    title: 'Harmonious Flavors',
    description: 'Designing delicate taste profiles that celebrate natural aromas without overwhelming the palate.',
    iconPath: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z'
  }
])

const signatureDishes = ref([
  {
    title: 'Pan-Seared Wagyu Tenderloin',
    price: '$78',
    description: 'Accompanied by caramelized baby onions, black truffle reduction, and smoked bone marrow butter.',
    image: 'https://images.unsplash.com/photo-1558030006-450675393462?auto=format&fit=crop&w=800&q=80'
  },
  {
    title: 'Glazed Wild Chilean Sea Bass',
    price: '$62',
    description: 'Served on a bed of saffron-infused risotto, roasted fennel, and kaffir lime emulsion.',
    image: 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=800&q=80'
  },
  {
    title: 'Deconstructed Dark Chocolate Sphere',
    price: '$28',
    description: 'Valrhona 70% dark chocolate shell, wild raspberry coulis, and salted hazelnut gelato.',
    image: 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=800&q=80'
  }
])
</script>