<template>
  <Navbar/>
  <div class="min-h-screen bg-[#FDFBF7] text-neutral-800 font-serif selection:bg-amber-200 selection:text-amber-900 overflow-x-hidden">
    
    <!-- Hero Banner Header -->
    <section class="relative bg-stone-950 text-white py-20 md:py-28 px-4 overflow-hidden">
      <img 
        src="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1800&q=80" 
        alt="Kitchen Background" 
        class="absolute inset-0 w-full h-full object-cover opacity-20 filter brightness-75 scale-105"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-stone-950 via-stone-950/60 to-transparent"></div>
      
      <div class="relative max-w-4xl mx-auto text-center space-y-4 z-10">
        <span class="text-xs font-sans tracking-[0.3em] uppercase text-[#C59237] font-semibold">Master Culinary Artists</span>
        <h1 class="text-4xl md:text-6xl font-serif text-stone-100 font-normal tracking-wide">Meet Our Chefs</h1>
        <p class="font-sans text-stone-300 text-xs sm:text-sm max-w-lg mx-auto font-light leading-relaxed">
          Behind every exquisite flavor is a team of passionate artisans dedicated to elevating local ingredients into extraordinary culinary experiences.
        </p>
      </div>
    </section>

    <!-- Executive Chef Showcase Section -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 py-16 md:py-24">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        <!-- Image Box -->
        <div class="lg:col-span-5 relative">
          <div class="relative z-10 rounded-sm overflow-hidden shadow-2xl border border-stone-200/60 bg-stone-900">
            <img 
              :src="executiveChef.image" 
              :alt="executiveChef.name" 
              class="w-full h-[480px] object-cover object-top hover:scale-105 transition-transform duration-700"
            />
          </div>
          <!-- Golden Accent Frame -->
          <div class="absolute -bottom-4 -right-4 w-full h-full border-2 border-[#C59237]/40 -z-0 rounded-sm hidden sm:block"></div>
        </div>

        <!-- Bio Content -->
        <div class="lg:col-span-7 space-y-6 font-sans">
          <div class="space-y-1">
            <span class="text-xs font-semibold tracking-[0.25em] text-[#C59237] uppercase">{{ executiveChef.title }}</span>
            <h2 class="font-serif text-3xl sm:text-4xl font-normal text-stone-900 tracking-wide">{{ executiveChef.name }}</h2>
          </div>

          <p class="text-stone-600 text-sm md:text-base leading-relaxed font-light">
            {{ executiveChef.bio }}
          </p>

          <!-- Quote Box -->
          <blockquote class="border-l-2 border-[#C59237] pl-4 italic font-serif text-stone-700 text-base md:text-lg bg-[#FAF7F2] py-3 pr-4 rounded-r-sm">
            "{{ executiveChef.quote }}"
          </blockquote>

          <!-- Specialties & Accolades Grid -->
          <div class="grid grid-cols-2 gap-4 pt-2 border-t border-stone-200/80 font-sans">
            <div>
              <span class="block text-[11px] uppercase tracking-wider text-stone-400 font-semibold mb-1">Culinary Focus</span>
              <span class="text-xs font-semibold text-stone-800">{{ executiveChef.specialty }}</span>
            </div>
            <div>
              <span class="block text-[11px] uppercase tracking-wider text-stone-400 font-semibold mb-1">Experience</span>
              <span class="text-xs font-semibold text-stone-800">{{ executiveChef.experience }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Culinary Team Grid -->
    <section class="bg-[#FAF7F2] py-16 sm:py-20 border-t border-b border-stone-200/60">
      <div class="max-w-7xl mx-auto px-4 sm:px-6">
        
        <!-- Section Title -->
        <div class="text-center mb-14">
          <h2 class="text-2xl md:text-3xl font-serif text-neutral-900 tracking-wider uppercase font-normal">
            The Culinary Masters
          </h2>
          <div class="flex items-center justify-center gap-3 mt-3 text-[#C59237]">
            <span class="w-10 h-[1px] bg-amber-600/40"></span>
            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M5 16L3 5l5.5 5L12 4l3.5 6L21 5l-2 11H5zm14 3c0 .6-.4 1-1 1H6c-.6 0-1-.4-1-1v-1h14v1z"/></svg>
            <span class="w-10 h-[1px] bg-amber-600/40"></span>
          </div>
        </div>

        <!-- Team Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          <NuxtLink 
            v-for="chef in culinaryTeam" 
            :key="chef.name"
            :to="{ path: '/chefDetail', query: { chef: chef.name } }"
            class="bg-white border border-stone-200/80 rounded-sm overflow-hidden shadow-sm hover:shadow-lg transition-all duration-300 group"
          >
            <!-- Image Area -->
            <div class="relative overflow-hidden h-80 bg-stone-900">
              <img 
                :src="chef.image" 
                :alt="chef.name" 
                class="w-full h-full object-cover object-top group-hover:scale-105 transition-transform duration-500"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-stone-950/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end p-4">
                <p class="text-xs text-stone-300 italic font-serif">"{{ chef.quote }}"</p>
              </div>
            </div>

            <!-- Card Info -->
            <div class="p-6 font-sans space-y-2">
              <span class="text-[10px] font-semibold tracking-[0.2em] text-[#C59237] uppercase">{{ chef.role }}</span>
              <h3 class="font-serif text-xl font-medium text-stone-900">{{ chef.name }}</h3>
              <p class="text-stone-500 text-xs leading-relaxed line-clamp-3 font-light">
                {{ chef.description }}
              </p>
            </div>
          </NuxtLink>
        </div>

      </div>
    </section>

  </div>
</template>

<script setup>
import { ref } from 'vue'

const executiveChef = ref({
  name: 'Chef Jean-Luc Moreau',
  title: 'Executive Chef & Founder',
  specialty: 'Modern French & Southeast Asian Fusion',
  experience: '22+ Years in Michelin-starred establishments',
  bio: 'Trained under world-renowned culinary icons in Paris and Lyon, Chef Jean-Luc brings a passion for technical precision and artistic presentation to FLAVORIA. His signature approach harmonizes classic French gastronomy with fragrant regional botanicals.',
  quote: 'Food is an emotional language. When we cook, we communicate reverence for nature and love for our guests.',
  image: 'https://images.unsplash.com/photo-1577219491135-ce391730fb2c?auto=format&fit=crop&w=800&q=80'
})

const culinaryTeam = ref([
  {
    name: 'Antoine Laurent',
    role: 'Head Pastry Chef',
    description: 'Master of delicate soufflés, artisan chocolates, and modern plated desserts designed to conclude every meal on a memorable note.',
    quote: 'Dessert is the final impression—it should feel like a sweet symphony.',
    image: 'https://images.unsplash.com/photo-1581299894007-aaa50297cf16?auto=format&fit=crop&w=800&q=80'
  },
  {
    name: 'Elena Rostova',
    role: 'Sous Chef',
    description: 'Expert in seafood preparation, broth infusions, and precision temperature cooking with a focus on sustainable sourcing.',
    quote: 'Respect every ingredient, from the simple leaf to the rarest catch.',
    image: 'https://images.unsplash.com/photo-1583394838336-acd977736f90?auto=format&fit=crop&w=800&q=80'
  },
  {
    name: 'Sokha Chan',
    role: 'Grill & Roast Specialist',
    description: 'Specializes in high-heat charcoal searing, dry-aged steaks, and aromatic house-blend marinades.',
    quote: 'Fire brings out the truest, most primal depth in fine meats.',
    image: 'https://images.unsplash.com/photo-1607631568010-a87245c0daf8?auto=format&fit=crop&w=800&q=80'
  }
])
</script>