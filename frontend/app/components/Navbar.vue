<template>
  <header class="w-full font-serif text-neutral-800 bg-neutral-50 shadow-sm sticky top-0 z-50">
    <!-- Top Announcement Bar -->
    

    <!-- Main Navigation Bar -->
    <nav class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between font-sans">
      <!-- Left Navigation Links -->
      <div class="hidden lg:flex items-center gap-10 text-xs font-semibold tracking-[0.2em] text-neutral-700 uppercase">
        <NuxtLink to="/" class="nav-link">HOME</NuxtLink>
        <NuxtLink to="/menu" class="nav-link">MENU</NuxtLink>
        <NuxtLink to="/about" class="nav-link">ABOUT</NuxtLink>
      </div>

      <!-- Mobile Hamburger Button -->
      <button @click="mobileMenuOpen = !mobileMenuOpen" class="lg:hidden p-2 text-neutral-700 focus:outline-none" aria-label="Toggle Navigation">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16" />
          <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- Centered Logo -->
      <NuxtLink to="/" class="flex flex-col items-center group cursor-pointer text-center my-1">
        <!-- Crown SVG Icon -->
        <svg class="w-7 h-5 text-amber-600 group-hover:text-amber-700 transition-colors mb-1" fill="currentColor" viewBox="0 0 24 24">
          <path d="M5 16L3 5l5.5 5L12 4l3.5 6L21 5l-2 11H5zm14 3c0 .6-.4 1-1 1H6c-.6 0-1-.4-1-1v-1h14v1z"/>
        </svg>
        <span class="font-serif text-2xl md:text-3xl font-normal tracking-[0.25em] text-neutral-900 leading-none pl-1">FLAVORIA</span>
        <span class="text-[9px] md:text-[10px] tracking-[0.35em] text-amber-800 uppercase font-sans mt-1.5 font-medium">Fine Dining</span>
      </NuxtLink>

      <!-- Right Navigation Links & Action Icons -->
      <div class="flex items-center gap-6 md:gap-8">
        <div class="hidden lg:flex items-center gap-10 text-xs font-semibold tracking-[0.2em] text-neutral-700 uppercase">
          <NuxtLink to="/reservation" class="nav-link">RESERVATION</NuxtLink>
          
          <!-- Pages Dropdown -->
          <div class="relative group cursor-pointer py-2">
            <span class="nav-link flex items-center gap-1">
              PAGES
              <svg class="w-3 h-3 text-neutral-500 group-hover:rotate-180 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </span>
            <!-- Dropdown Menu -->
            <div class="absolute top-full right-0 w-48 bg-white border border-stone-200 shadow-lg rounded-sm py-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
              <NuxtLink to="/chefs" class="block px-4 py-2 text-xs hover:bg-amber-50 hover:text-amber-900 tracking-wider">OUR CHEFS</NuxtLink>
              <NuxtLink to="/events" class="block px-4 py-2 text-xs hover:bg-amber-50 hover:text-amber-900 tracking-wider">PRIVATE EVENTS</NuxtLink>
              <NuxtLink to="/gallery" class="block px-4 py-2 text-xs hover:bg-amber-50 hover:text-amber-900 tracking-wider">GALLERY</NuxtLink>
              <NuxtLink to="/contact" class="block px-4 py-2 text-xs hover:bg-amber-50 hover:text-amber-900 tracking-wider">CONTACT US</NuxtLink>
            </div>
          </div>
        </div>

        <!-- Right Quick Action Icons -->
        <div class="flex items-center gap-4 text-neutral-700">
          <!-- Search Button -->
          <button @click="toggleSearch" class="p-1 hover:text-amber-700 transition-colors" aria-label="Search">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>

          <!-- User / Account -->
          <NuxtLink to="/login" class="p-1 hover:text-amber-700 transition-colors" aria-label="Account">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </NuxtLink>

          <!-- Shopping Bag / Cart Badge -->
          <NuxtLink to="/cart" class="p-1 hover:text-amber-700 transition-colors relative" aria-label="Shopping Cart">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
            <span class="absolute -top-1 -right-1 bg-amber-700 text-white text-[10px] w-4 h-4 rounded-full flex items-center justify-center font-sans">0</span>
          </NuxtLink>
        </div>
      </div>
    </nav>

    <!-- Mobile Drawer Navigation -->
    <transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="transform -translate-y-4 opacity-0"
      enter-to-class="transform translate-y-0 opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="transform translate-y-0 opacity-100"
      leave-to-class="transform -translate-y-4 opacity-0"
    >
      <div v-if="mobileMenuOpen" class="lg:hidden bg-neutral-900 text-stone-200 px-6 py-6 border-t border-stone-800">
        <ul class="flex flex-col gap-4 text-sm tracking-[0.2em] font-medium uppercase">
          <li><NuxtLink @click="mobileMenuOpen = false" to="/" class="block py-2 hover:text-amber-400">HOME</NuxtLink></li>
          <li><NuxtLink @click="mobileMenuOpen = false" to="/menu" class="block py-2 hover:text-amber-400">MENU</NuxtLink></li>
          <li><NuxtLink @click="mobileMenuOpen = false" to="/about" class="block py-2 hover:text-amber-400">ABOUT</NuxtLink></li>
          <li><NuxtLink @click="mobileMenuOpen = false" to="/reservation" class="block py-2 hover:text-amber-400">RESERVATION</NuxtLink></li>
          <li><NuxtLink @click="mobileMenuOpen = false" to="/chefs" class="block py-2 hover:text-amber-400">OUR CHEFS</NuxtLink></li>
          <li><NuxtLink @click="mobileMenuOpen = false" to="/events" class="block py-2 hover:text-amber-400">PRIVATE EVENTS</NuxtLink></li>
          <li><NuxtLink @click="mobileMenuOpen = false" to="/contact" class="block py-2 hover:text-amber-400">CONTACT US</NuxtLink></li>
        </ul>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref } from 'vue'

const mobileMenuOpen = ref(false)

const toggleSearch = () => {
  // Add your modal or toggle search bar logic here
  console.log('Search toggled')
}
</script>

<style scoped>
/* Fine dining gold accent for hover & active links */
.nav-link {
  position: relative;
  padding-bottom: 6px;
  transition: color 0.3s ease;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background-color: #c5a880; /* Warm champagne gold */
  transition: width 0.3s ease;
}

.nav-link:hover {
  color: #a16207;
}

.nav-link:hover::after,
.nav-link.router-link-exact-active::after {
  width: 100%;
}

.nav-link.router-link-exact-active {
  color: #a16207;
}
</style>