<script setup lang="ts">

const features = [
  {
    icon: '🍕',
    title: 'Fresh Ingredients',
    text: 'We carefully select fresh and high-quality ingredients for every meal we prepare.'
  },
  {
    icon: '👨‍🍳',
    title: 'Professional Chefs',
    text: 'Our experienced chefs prepare delicious meals with passion and attention to detail.'
  },
  {
    icon: '❤️',
    title: 'Made With Love',
    text: 'Every dish is made with love to give our customers a memorable dining experience.'
  }
]

const stats = [
  { number: '10+', label: 'Years Experience' },
  { number: '50+', label: 'Food Items' },
  { number: '10K+', label: 'Happy Customers' },
  { number: '20+', label: 'Professional Staff' }
]

</script>



<template>
  <div class="min-h-screen bg-[#15151b] text-white">

    <Navbar/>

    <!-- ================= HERO ================= -->
    <section
      class="relative min-h-107.5 flex items-center overflow-hidden"
    >

      <!-- Background image -->
      <img
        src="https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?auto=format&fit=crop&w=1600&q=80"
        alt="Restaurant food"
        class="absolute inset-0 w-full h-full object-cover"
      />

      <!-- Overlay -->
      <div class="absolute inset-0 bg-black/75"></div>

      <div class="relative max-w-6xl mx-auto px-6 w-full">

        <div class="max-w-xl">

          <p class="text-orange-500 uppercase tracking-[4px] text-sm font-bold mb-4">
            Welcome To Food Lover
          </p>

          <h1 class="text-5xl md:text-6xl font-extrabold leading-tight mb-5">
            About
            <span class="text-orange-500">Our Restaurant</span>
          </h1>

          <p class="text-gray-300 leading-7 max-w-lg">
            We believe that great food brings people together.
            Our restaurant is dedicated to serving delicious,
            fresh and memorable meals in a warm and friendly
            environment.
          </p>

          <div class="mt-8 flex gap-4">

            <NuxtLink
              to="/menu"
              class="bg-orange-500 hover:bg-orange-600 px-7 py-3 rounded-md font-bold text-sm transition"
            >
              VIEW OUR MENU
            </NuxtLink>

            <NuxtLink
              to="/contact"
              class="border border-orange-500 text-orange-500 hover:bg-orange-500 hover:text-white px-7 py-3 rounded-md font-bold text-sm transition"
            >
              CONTACT US
            </NuxtLink>

          </div>

        </div>

      </div>
    </section>


    <!-- ================= ABOUT US ================= -->
    <section class="max-w-6xl mx-auto px-6 py-20">

      <div class="grid md:grid-cols-2 gap-12 items-center">

        <!-- Image -->
        <div class="relative">

          <img
            src="https://images.unsplash.com/photo-1552566626-52f8b828add9?auto=format&fit=crop&w=900&q=80"
            alt="Restaurant"
            class="w-full h-107.5 object-cover rounded-lg"
          />

          <!-- Orange decoration -->
          <div
            class="absolute -bottom-5 -right-5 w-32 h-32 border-8 border-orange-500 rounded-lg -z-10"
          ></div>

        </div>


        <!-- Content -->
        <div>

          <p class="text-orange-500 uppercase tracking-[3px] text-sm font-bold mb-3">
            Our Story
          </p>

          <h2 class="text-4xl font-extrabold mb-6">
            We Make Food
            <span class="text-orange-500">With Passion</span>
          </h2>

          <p class="text-gray-400 leading-7 mb-5">
            Food Lover started with a simple idea: create a place
            where people can enjoy delicious food, relax with
            friends and family, and feel at home.
          </p>

          <p class="text-gray-400 leading-7 mb-6">
            From our kitchen to your table, every meal is carefully
            prepared using fresh ingredients and traditional
            cooking techniques. We always focus on quality,
            flavor and customer satisfaction.
          </p>

          <div class="flex items-center gap-4">

            <div class="w-12 h-12 bg-orange-500 rounded-full flex items-center justify-center text-2xl">
              👨‍🍳
            </div>

            <div>
              <h3 class="font-bold">
                Experienced Chefs
              </h3>

              <p class="text-sm text-gray-500">
                Cooking with passion since 2015
              </p>
            </div>

          </div>

        </div>

      </div>

    </section>


    <!-- ================= STATS ================= -->
    <section class="bg-orange-500 py-14">

      <div class="max-w-6xl mx-auto px-6">

        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">

          <div
            v-for="stat in stats"
            :key="stat.label"
          >
            <h3 class="text-4xl font-extrabold mb-2">
              {{ stat.number }}
            </h3>

            <p class="text-sm font-semibold uppercase tracking-wide">
              {{ stat.label }}
            </p>
          </div>

        </div>

      </div>

    </section>


    <!-- ================= WHY CHOOSE US ================= -->
    <section class="max-w-6xl mx-auto px-6 py-20">

      <div class="text-center mb-12">

        <p class="text-orange-500 uppercase tracking-[3px] text-sm font-bold mb-3">
          Why Choose Us
        </p>

        <h2 class="text-4xl font-extrabold">
          What Makes Us <span class="text-orange-500">Special?</span>
        </h2>

        <p class="text-gray-500 max-w-xl mx-auto mt-4">
          We are committed to providing excellent food and
          excellent service to every customer.
        </p>

      </div>


      <!-- Feature Cards -->
      <div class="grid md:grid-cols-3 gap-6">

        <div
          v-for="feature in features"
          :key="feature.title"
          class="bg-[#202026] border border-gray-800 rounded-lg p-8 text-center hover:border-orange-500 transition duration-300"
        >

          <div
            class="w-16 h-16 mx-auto mb-5 bg-orange-500/10 border border-orange-500 rounded-full flex items-center justify-center text-3xl"
          >
            {{ feature.icon }}
          </div>

          <h3 class="text-xl font-bold mb-3">
            {{ feature.title }}
          </h3>

          <p class="text-gray-500 text-sm leading-6">
            {{ feature.text }}
          </p>

        </div>

      </div>

    </section>


    <!-- ================= MISSION ================= -->
    <section class="bg-[#202026]">

      <div class="max-w-6xl mx-auto px-6 py-20">

        <div class="grid md:grid-cols-2 gap-12 items-center">

          <div>

            <p class="text-orange-500 uppercase tracking-[3px] text-sm font-bold mb-3">
              Our Mission
            </p>

            <h2 class="text-4xl font-extrabold mb-6">
              Good Food.
              <span class="text-orange-500">
                Good Mood.
              </span>
            </h2>

            <p class="text-gray-400 leading-7 mb-6">
              Our mission is to make every visit special.
              We want our customers to enjoy not only great
              food but also great service and a comfortable
              atmosphere.
            </p>

            <ul class="space-y-4">

              <li class="flex gap-3 items-center">
                <span class="text-orange-500 text-xl">✓</span>
                <span class="text-gray-300">
                  Fresh and quality ingredients
                </span>
              </li>

              <li class="flex gap-3 items-center">
                <span class="text-orange-500 text-xl">✓</span>
                <span class="text-gray-300">
                  Delicious meals prepared daily
                </span>
              </li>

              <li class="flex gap-3 items-center">
                <span class="text-orange-500 text-xl">✓</span>
                <span class="text-gray-300">
                  Friendly and professional service
                </span>
              </li>

              <li class="flex gap-3 items-center">
                <span class="text-orange-500 text-xl">✓</span>
                <span class="text-gray-300">
                  Comfortable restaurant atmosphere
                </span>
              </li>

            </ul>

          </div>


          <!-- Food Image -->
          <div class="grid grid-cols-2 gap-4">

            <img
              src="https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=700&q=80"
              class="w-full h-64 object-cover rounded-lg"
              alt="Fresh food"
            />

            <img
              src="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=700&q=80"
              class="w-full h-64 object-cover rounded-lg mt-10"
              alt="Pizza"
            />

          </div>

        </div>

      </div>

    </section>


    <!-- ================= CTA ================= -->
    <section class="relative py-20 overflow-hidden">

      <div class="absolute inset-0">
        <img
          src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1600&q=80"
          class="w-full h-full object-cover"
          alt="Restaurant interior"
        />

        <div class="absolute inset-0 bg-black/80"></div>
      </div>

      <div class="relative max-w-3xl mx-auto px-6 text-center">

        <h2 class="text-4xl md:text-5xl font-extrabold mb-5">
          Ready To Enjoy
          <span class="text-orange-500">Our Food?</span>
        </h2>

        <p class="text-gray-300 mb-8">
          Visit us today and discover delicious food made
          with passion and fresh ingredients.
        </p>

        <NuxtLink
          to="/menu"
          class="inline-block bg-orange-500 hover:bg-orange-600 px-8 py-3 rounded-md font-bold transition"
        >
          EXPLORE OUR MENU
        </NuxtLink>

      </div>

    </section>


    <!-- ================= FOOTER ================= -->
    <footer class="bg-[#303036]">

      <div class="max-w-6xl mx-auto px-6 py-12">

        <div class="grid md:grid-cols-3 gap-10">

          <!-- Logo -->
          <div>

            <div class="flex items-center gap-2 mb-4">

              <div
                class="w-10 h-10 rounded-full border-2 border-orange-500 flex items-center justify-center text-orange-500"
              >
                ♡
              </div>

              <h2 class="text-xl font-bold">
                Food <span class="text-orange-500">Lover</span>
              </h2>

            </div>

            <p class="text-gray-400 text-sm leading-6">
              Delicious food, friendly service and a warm
              atmosphere. Welcome to Food Lover.
            </p>

          </div>


          <!-- Quick Links -->
          <div>

            <h3 class="font-bold text-lg mb-4">
              Quick Links
            </h3>

            <div class="space-y-2 text-sm text-gray-400">

              <NuxtLink to="/" class="block hover:text-orange-500">
                Home
              </NuxtLink>

              <NuxtLink to="/about" class="block hover:text-orange-500">
                About Us
              </NuxtLink>

              <NuxtLink to="/menu" class="block hover:text-orange-500">
                Menu
              </NuxtLink>

              <NuxtLink to="/contact" class="block hover:text-orange-500">
                Contact
              </NuxtLink>

            </div>

          </div>


          <!-- Contact -->
          <div>

            <h3 class="font-bold text-lg mb-4">
              Contact Us
            </h3>

            <div class="space-y-3 text-sm text-gray-400">

              <p>📍 Phnom Penh, Cambodia</p>
              <p>📞 +855 12 345 678</p>
              <p>✉️ foodlover@gmail.com</p>

            </div>

          </div>

        </div>


        <!-- Bottom -->
        <div class="border-t border-gray-700 mt-10 pt-6 text-center">

          <div class="flex justify-center gap-4 mb-4">

            <a
              href="#"
              class="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center hover:bg-orange-500 transition"
            >
              f
            </a>

            <a
              href="#"
              class="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center hover:bg-orange-500 transition"
            >
              ◎
            </a>

            <a
              href="#"
              class="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center hover:bg-orange-500 transition"
            >
              📷
            </a>

            <a
              href="#"
              class="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center hover:bg-orange-500 transition"
            >
              p
            </a>

          </div>

          <p class="text-gray-500 text-xs">
            © 2026 Food Lover. All Rights Reserved.
          </p>

        </div>

      </div>

    </footer>

  </div>
</template>