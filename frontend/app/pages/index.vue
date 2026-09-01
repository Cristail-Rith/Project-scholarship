<script setup lang="ts">
import Navbar from '~/components/Navbar.vue';

</script>

<template>
<Navbar/>
  <!-- <div class="min-h-screen bg-gray-50">
    <section class="relative overflow-hidden bg-[#047857]">
      <div class="absolute inset-0">
        <div class="absolute inset-0 bg-gradient-to-r from-[#047857] to-[#065f46]" />
      </div>
      <div class="relative mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl font-bold tracking-tight text-white sm:text-5xl md:text-6xl">
            <span class="block">Delicious Food</span>
            <span class="block text-emerald-200">Delivered To You</span>
          </h1>
          <p class="mx-auto mt-6 max-w-xl text-lg text-emerald-100 sm:text-xl">
            Experience the finest dining from the comfort of your home. Fresh ingredients, amazing flavors, fast delivery.
          </p>
          <div class="mx-auto mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <NuxtLink
              to="/menu"
              class="rounded-full bg-white px-8 py-3 text-base font-semibold text-[#047857] shadow-sm hover:bg-emerald-50 transition-colors"
            >
              View Menu
            </NuxtLink>
            <NuxtLink
              to="/orders"
              class="rounded-full border-2 border-white px-8 py-3 text-base font-semibold text-white hover:bg-white/10 transition-colors"
            >
              Order Now
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>

    <section class="py-16">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Why Choose Us
          </h2>
          <p class="mt-4 text-lg text-gray-600">
            We provide the best dining experience with quality and convenience.
          </p>
        </div>
        <div class="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          <div class="rounded-2xl bg-white p-8 shadow-sm ring-1 ring-gray-200">
            <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-[#047857] text-white mb-6">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900">Fast Delivery</h3>
            <p class="mt-2 text-gray-600">Get your food delivered hot and fresh within 30 minutes.</p>
          </div>
          <div class="rounded-2xl bg-white p-8 shadow-sm ring-1 ring-gray-200">
            <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-[#047857] text-white mb-6">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900">Quality Food</h3>
            <p class="mt-2 text-gray-600">We use only the freshest ingredients for every dish.</p>
          </div>
          <div class="rounded-2xl bg-white p-8 shadow-sm ring-1 ring-gray-200">
            <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-[#047857] text-white mb-6">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900">Best Service</h3>
            <p class="mt-2 text-gray-600">Our team is dedicated to providing excellent customer service.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="bg-white py-16">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="rounded-2xl bg-gradient-to-r from-[#047857] to-[#065f46] px-6 py-16 sm:px-12 sm:py-20 lg:flex lg:items-center lg:justify-between">
          <div>
            <h2 class="text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Ready to order?
            </h2>
            <p class="mt-4 text-lg text-emerald-100">
              Browse our menu and discover amazing dishes today.
            </p>
          </div>
          <div class="mt-8 lg:mt-0">
            <NuxtLink
              to="/menu"
              class="rounded-full bg-white px-8 py-3 text-base font-semibold text-[#047857] shadow-sm hover:bg-emerald-50 transition-colors"
            >
              Browse Menu
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>

    <footer class="bg-gray-900 py-12">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <p class="text-center text-sm text-gray-400">
          Restaurant Dining. All rights reserved.
        </p>
      </div>
    </footer>
  </div> -->
</template>
