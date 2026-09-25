<script setup lang="ts">
import { ref } from 'vue'
import Navbar from '~/components/Navbar.vue'
import CartSidebar from '~/components/CartSidebar.vue'
import { useCart } from '~/composables/useCart'

useCart()

const stats = ref([
  { label: 'Years of Tradition', value: '15+' },
  { label: 'Master Chefs', value: '08' },
  { label: 'Signature Recipes', value: '45+' },
  { label: 'Local Sourcing', value: '100%' }
])

const values = ref([
  {
    number: '01',
    title: 'From the Land',
    description:
      'We work closely with local growers and producers, choosing ingredients at their peak rather than forcing them into a season.'
  },
  {
    number: '02',
    title: 'From the Fire',
    description:
      'Natural wood, patient cooking and a respect for heat give our food the character that defines our kitchen.'
  },
  {
    number: '03',
    title: 'From the Heart',
    description:
      'Hospitality is more than service. It is the feeling of being welcomed, remembered and given a reason to stay.'
  }
])

const milestones = ref([
  {
    year: '2011',
    title: 'A Small Beginning',
    description:
      'Our story began with a family kitchen, a wood-fired oven and a simple belief that great food brings people together.'
  },
  {
    year: '2015',
    title: 'Finding Our Fire',
    description:
      'We built our first dedicated hearth and began developing the cooking style that would become our signature.'
  },
  {
    year: '2020',
    title: 'Growing Together',
    description:
      'Our community of farmers, makers and guests became the heart of everything we do.'
  },
  {
    year: 'Today',
    title: 'Still at the Table',
    description:
      'We continue to cook slowly, source thoughtfully and welcome every guest as part of our story.'
  }
])

const developers = ref([
  {
    name: 'Developer One', // Replace with actual name
    role: 'Lead Frontend  and Backned Engineer',
    bio: 'Crafting seamless user experiences through modern Web standards and thoughtful UI and Backend engineering .',
    image: 'https://scontent.fpnh18-5.fna.fbcdn.net/v/t39.30808-6/713783939_122260723340162078_3533463879582817884_n.jpg?stp=dst-jpg_tt6&cstp=mx832x836&ctp=s832x836&_nc_cat=102&_nc_map=urlgen_bucketless&ccb=1-7&_nc_sid=6ee11a&_nc_eui2=AeFc7MI9F7Bz_llyiOPjrJgTsRslBsorVQCxGyUGyitVAIvr2wTp9nD8Olhi6FUvBFPOQ0hwFXg9o1tQ60v-JWHB&_nc_ohc=qTOTlQXipz4Q7kNvwHB4ykS&_nc_oc=AdqGN7k6rt_SuGBmw-8uTreNMl7dpENP-wjpBRAg9XloydCc8mVkLLWGBPsxHvnKUwg&_nc_zt=23&_nc_ht=scontent.fpnh18-5.fna&_nc_gid=UnyWCGM3-_oXEspmTcKG8A&_nc_ss=7b2a8&oh=00_AQJGKbQS_NbHm0kmCwIQTBo318sjmKzJzoF9a9wurs-Zlg&oe=6ABAC4D5', // Professional Studio Photo
    tags: ['Vue 3', 'Nuxt', 'Tailwind CSS']
  },
  {
    name: 'Developer Two', // Replace with actual name
    role: 'Full Stack Architect Frontend Debug',
    bio: 'Blending cultural heritage and modern code structures to create performant, meaningful web applications.',
    image: 'https://scontent.fpnh5-1.fna.fbcdn.net/v/t39.30808-6/735178793_1772718847442991_7811778051066388255_n.jpg?stp=dst-jpg_tt6&cstp=mx1080x1080&ctp=s1080x1080&_nc_cat=107&_nc_map=urlgen_bucketless&ccb=1-7&_nc_sid=6ee11a&_nc_eui2=AeFVrzeMjFXrVZdXg4MC87oiUDefIyHUkRtQN58jIdSRG2f5jaVMrsXeamcOKJfjTCHt8IoY05E3lN7xaNFpGHYd&_nc_ohc=KdWu0OxZ0jgQ7kNvwE7IcNi&_nc_oc=AdrjT388IjvZxwwyXlEcV3h7RwufmvTDYuIrODD0D3SBUfDAHWbTz9i-G1eJC5-VBck&_nc_zt=23&_nc_ht=scontent.fpnh5-1.fna&_nc_gid=uvskhXiWTQNzmdqD7iRhag&_nc_ss=7b2a8&oh=00_AQJW3H6ZZ6erwvpTx39QkzXqcP5-j_s5YgEiCLAde_FkYQ&oe=6ABA917F', // Cultural / Temple Photo
    tags: ['Architecture', 'TypeScript', 'Node.js']
  }
])
</script>

<template>
  <Navbar />

  <main class="bg-[#f7f6f2] text-stone-900 selection:bg-amber-600 selection:text-white">

    <!-- HERO -->
    <section class="relative overflow-hidden border-b border-stone-200">
      <div class="max-w-7xl mx-auto px-6 lg:px-8 pt-20 pb-24 lg:pt-28 lg:pb-32">
        <div class="grid lg:grid-cols-12 gap-12 items-end">
          
          <div class="lg:col-span-8">
            <div class="flex items-center gap-4 mb-8">
              <span class="w-12 h-px bg-amber-600"></span>
              <span class="text-[11px] font-bold uppercase tracking-[0.35em] text-amber-700">
                Our Story
              </span>
            </div>

            <h1 class="font-serif text-5xl sm:text-6xl lg:text-8xl leading-[0.9] tracking-tight font-black text-stone-900">
              Food with <br />
              <span class="italic font-normal text-amber-700">a sense of place.</span>
            </h1>

            <p class="mt-10 max-w-2xl text-base sm:text-lg leading-relaxed text-stone-600 font-medium">
              We are a wood-fired restaurant built around honest ingredients,
              patient cooking and the belief that the best meals are the ones
              people remember long after the table is cleared.
            </p>
          </div>

          <div class="lg:col-span-4 lg:pb-2">
            <div class="lg:border-l border-stone-300 lg:pl-8">
              <span class="text-[10px] uppercase tracking-[0.3em] font-bold text-amber-700">
                Established
              </span>

              <div class="mt-2 font-serif text-5xl font-black text-stone-900">
                2011
              </div>

              <p class="mt-4 text-xs leading-relaxed text-stone-500 max-w-xs font-medium">
                One kitchen. One fire. Fifteen years of cooking for our community.
              </p>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- IMAGE + STORY -->
    <section class="max-w-7xl mx-auto px-6 lg:px-8 py-24 lg:py-32">
      <div class="grid lg:grid-cols-12 gap-12 lg:gap-20 items-center">

        <div class="lg:col-span-7">
          <div class="relative">
            <div class="aspect-[4/5] overflow-hidden bg-stone-200 rounded-md">
              <img
                src="https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=1200&q=85"
                alt="Restaurant dining experience"
                class="w-full h-full object-cover hover:scale-[1.02] transition-transform duration-700"
              />
            </div>

            <div class="absolute -bottom-6 -right-4 sm:right-6 bg-stone-900 text-white px-7 py-6 rounded-md shadow-lg border border-stone-800">
              <div class="font-serif text-4xl font-bold text-amber-500">
                15
              </div>
              <div class="mt-1 text-[9px] font-bold uppercase tracking-[0.25em] text-stone-300">
                Years at the table
              </div>
            </div>
          </div>
        </div>

        <div class="lg:col-span-5">
          <span class="text-[10px] font-bold uppercase tracking-[0.3em] text-amber-700">
            A simple beginning
          </span>

          <h2 class="mt-4 font-serif text-4xl sm:text-5xl leading-[0.95] font-bold text-stone-900 tracking-tight">
            It started with <span class="italic font-normal text-amber-700">fire.</span>
          </h2>

          <div class="mt-8 space-y-5 text-sm leading-7 text-stone-600 font-medium">
            <p>
              Our restaurant was born from a simple idea: slow food deserves
              time, good ingredients deserve respect and hospitality should
              feel personal.
            </p>
            <p>
              What began as a small family kitchen gradually became a place
              where farmers, cooks, friends and strangers could gather around
              the same table.
            </p>
            <p>
              Today, the room has grown, but the philosophy has not. We still
              cook over natural wood, work closely with local producers and
              believe that every plate should have a reason to exist.
            </p>
          </div>

          <div class="mt-10 pt-7 border-t border-stone-300">
            <p class="font-serif italic text-lg text-stone-800">
              "The best ingredient is always time."
            </p>
            <p class="mt-2 text-[9px] font-bold uppercase tracking-[0.25em] text-amber-700">
              — Founder & Master Chef
            </p>
          </div>
        </div>

      </div>
    </section>

    <!-- PHILOSOPHY -->
    <section class="bg-stone-900 text-white">
      <div class="max-w-7xl mx-auto px-6 lg:px-8 py-24 lg:py-32">
        <div class="max-w-3xl">
          <span class="text-[10px] font-bold uppercase tracking-[0.35em] text-amber-500">
            What we believe
          </span>

          <h2 class="mt-4 font-serif text-4xl sm:text-5xl lg:text-6xl leading-tight font-bold">
            Less noise. <br />
            More <span class="italic font-normal text-amber-500">substance.</span>
          </h2>
        </div>

        <div class="grid md:grid-cols-3 gap-8 mt-16 border-t border-stone-800 pt-12">
          <div
            v-for="value in values"
            :key="value.number"
            class="space-y-4"
          >
            <span class="font-mono text-xs font-bold text-amber-500">
              {{ value.number }}
            </span>

            <h3 class="font-serif text-2xl font-bold text-stone-100">
              {{ value.title }}
            </h3>

            <p class="text-sm leading-relaxed text-stone-400">
              {{ value.description }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- INGREDIENTS -->
    <section class="max-w-7xl mx-auto px-6 lg:px-8 py-24 lg:py-32">
      <div class="grid lg:grid-cols-12 gap-16">

        <div class="lg:col-span-4">
          <span class="text-[10px] font-bold uppercase tracking-[0.3em] text-amber-700">
            Our ingredients
          </span>

          <h2 class="mt-4 font-serif text-4xl sm:text-5xl font-bold text-stone-900 leading-tight">
            Good food begins <span class="italic font-normal text-amber-700">before</span> the kitchen.
          </h2>
        </div>

        <div class="lg:col-span-8">
          <div class="grid sm:grid-cols-2 gap-6">
            <div class="bg-white p-8 rounded-lg border border-stone-200 shadow-xs">
              <div class="text-4xl font-serif font-black text-amber-700">100%</div>
              <h3 class="mt-3 font-bold uppercase text-xs tracking-wider text-stone-800">Local sourcing</h3>
              <p class="mt-3 text-xs leading-relaxed text-stone-600 font-medium">
                We build long-term relationships with farmers and producers who care about the land as much as we care about the plate.
              </p>
            </div>

            <div class="bg-white p-8 rounded-lg border border-stone-200 shadow-xs">
              <div class="text-4xl font-serif font-black text-amber-700">08</div>
              <h3 class="mt-3 font-bold uppercase text-xs tracking-wider text-stone-800">Master chefs</h3>
              <p class="mt-3 text-xs leading-relaxed text-stone-600 font-medium">
                Our kitchen is driven by cooks who understand that technique should enhance an ingredient rather than hide it.
              </p>
            </div>

            <div class="bg-white p-8 rounded-lg border border-stone-200 shadow-xs">
              <div class="text-4xl font-serif font-black text-amber-700">45+</div>
              <h3 class="mt-3 font-bold uppercase text-xs tracking-wider text-stone-800">Recipes</h3>
              <p class="mt-3 text-xs leading-relaxed text-stone-600 font-medium">
                From old family recipes to new seasonal creations, our menu continues to evolve around the fire.
              </p>
            </div>

            <div class="bg-white p-8 rounded-lg border border-stone-200 shadow-xs">
              <div class="text-4xl font-serif font-black text-amber-700">01</div>
              <h3 class="mt-3 font-bold uppercase text-xs tracking-wider text-stone-800">Natural fire</h3>
              <p class="mt-3 text-xs leading-relaxed text-stone-600 font-medium">
                Our wood-fired hearth remains at the center of the kitchen, giving every dish its own depth and character.
              </p>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- TIMELINE -->
    <section class="border-y border-stone-200 bg-white">
      <div class="max-w-7xl mx-auto px-6 lg:px-8 py-24 lg:py-32">
        <div class="grid lg:grid-cols-12 gap-16">

          <div class="lg:col-span-4">
            <span class="text-[10px] font-bold uppercase tracking-[0.3em] text-amber-700">
              Our journey
            </span>

            <h2 class="mt-4 font-serif text-4xl sm:text-5xl font-bold text-stone-900">
              Fifteen years. <br />
              One <span class="italic font-normal text-amber-700">table.</span>
            </h2>
          </div>

          <div class="lg:col-span-8">
            <div
              v-for="milestone in milestones"
              :key="milestone.year"
              class="grid grid-cols-12 gap-6 py-8 border-t border-stone-200 first:border-t-0"
            >
              <div class="col-span-3 sm:col-span-2">
                <span class="font-mono text-xs font-bold text-amber-700 bg-amber-50 border border-amber-200 px-2 py-1 rounded">
                  {{ milestone.year }}
                </span>
              </div>

              <div class="col-span-9 sm:col-span-10">
                <h3 class="font-serif text-2xl font-bold text-stone-900">
                  {{ milestone.title }}
                </h3>
                <p class="mt-2 max-w-xl text-xs sm:text-sm leading-relaxed text-stone-600 font-medium">
                  {{ milestone.description }}
                </p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- STATS -->
    <section class="bg-stone-50 border-b border-stone-200">
      <div class="max-w-7xl mx-auto px-6 lg:px-8 py-16">
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">
          <div
            v-for="stat in stats"
            :key="stat.label"
            class="py-4 px-2"
          >
            <div class="font-serif text-3xl sm:text-4xl font-extrabold text-amber-700">
              {{ stat.value }}
            </div>
            <div class="mt-2 text-[10px] font-bold uppercase tracking-[0.2em] text-stone-600">
              {{ stat.label }}
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- MEET THE DEVELOPERS -->
<section class="max-w-7xl mx-auto px-6 lg:px-8 py-24 lg:py-32">
  <div class="grid lg:grid-cols-12 gap-12 lg:gap-16 items-start">
    
    <!-- Section Header Column -->
    <div class="lg:col-span-4 lg:sticky lg:top-12">
      <div class="flex items-center gap-4 mb-4">
        <span class="w-8 h-px bg-amber-600"></span>
        <span class="text-[10px] font-bold uppercase tracking-[0.35em] text-amber-700">
          Behind The Code
        </span>
      </div>

      <h2 class="font-serif text-4xl sm:text-5xl font-bold text-stone-900 leading-tight">
        Crafted with <br />
        <span class="italic font-normal text-amber-700">precision & heart.</span>
      </h2>

      <p class="mt-6 text-sm leading-relaxed text-stone-600 font-medium max-w-sm">
        Just as exceptional food requires time and technical discipline, modern digital experiences are built on clean architecture, thoughtful execution, and passion.
      </p>
    </div>

    <!-- Developers Grid Column -->
    <div class="lg:col-span-8 grid sm:grid-cols-2 gap-8">
      <div 
        v-for="(dev, index) in developers" 
        :key="index"
        class="group bg-white rounded-xl overflow-hidden border border-stone-200 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300"
      >
        <!-- Developer Image Wrapper -->
        <div class="aspect-[4/5] relative overflow-hidden bg-stone-100">
          <img 
            :src="dev.image" 
            :alt="dev.name" 
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-stone-950/60 via-transparent to-transparent opacity-80"></div>
          
          <!-- Role Badge -->
          <div class="absolute bottom-4 left-4 right-4 flex justify-between items-end">
            <span class="text-[10px] uppercase font-bold tracking-widest text-white bg-stone-900/80 backdrop-blur-md px-3 py-1.5 rounded-md border border-white/10">
              {{ dev.role }}
            </span>
          </div>
        </div>

        <!-- Content -->
        <div class="p-6">
          <h3 class="font-serif text-2xl font-bold text-stone-900">
            {{ dev.name }}
          </h3>

          <p class="mt-3 text-xs leading-relaxed text-stone-600 font-medium">
            {{ dev.bio }}
          </p>

          <!-- Tech Tags -->
          <div class="mt-6 pt-4 border-t border-stone-100 flex flex-wrap gap-2">
            <span 
              v-for="tag in dev.tags" 
              :key="tag"
              class="text-[10px] font-mono font-bold text-amber-800 bg-amber-50 px-2.5 py-1 rounded border border-amber-200/60"
            >
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
    </div>

  </div>
</section>

    <!-- FINAL CTA -->
    <section class="bg-stone-900 text-white">
      <div class="max-w-5xl mx-auto px-6 lg:px-8 py-24 text-center">
        <span class="text-[10px] font-bold uppercase tracking-[0.35em] text-amber-500">
          Come sit with us
        </span>

        <h2 class="mt-5 font-serif text-4xl sm:text-5xl lg:text-6xl leading-tight font-bold">
          Every table has <br />
          a story.
        </h2>

        <p class="max-w-xl mx-auto mt-6 text-sm leading-relaxed text-stone-400">
          Join us for food cooked slowly, ingredients chosen carefully and
          evenings meant to be remembered.
        </p>

        <div class="mt-8">
          <NuxtLink to="/RESERVATION" class="inline-flex items-center justify-center bg-amber-600 hover:bg-amber-700 text-white border border-amber-600 px-7 py-3.5 rounded-md text-xs font-bold uppercase tracking-widest transition-colors duration-200 shadow-sm"
          >
            Reserve a Table
          </NuxtLink>
        </div>
      </div>
    </section>
    
  </main>
  <CartSidebar/>
</template>