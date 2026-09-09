<script setup lang="ts">

const categories = [
  'All',
  'Appetizers',
  'Soups',
  'Main Courses',
  'Pizza',
  'Desserts',
  'Drinks'
]

const activeCategory = ref('All')

const menu = [
  {
    id: 1,
    category: 'Appetizers',
    name: 'Italian Bruschetta',
    description: 'Fresh tomatoes, basil, garlic and olive oil served on toasted bread.',
    price: 6.50,
    image: 'https://images.unsplash.com/photo-1572695157366-5e585ab2b69f?auto=format&fit=crop&w=600&q=80'
  },
  {
    id: 2,
    category: 'Appetizers',
    name: 'Crispy Calamari',
    description: 'Golden crispy calamari served with our special dipping sauce.',
    price: 8.50,
    image: 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?auto=format&fit=crop&w=600&q=80'
  },
  {
    id: 3,
    category: 'Soups',
    name: 'Creamy Mushroom Soup',
    description: 'A rich and creamy mushroom soup prepared with fresh herbs.',
    price: 5.00,
    image: 'https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=600&q=80'
  },
  {
    id: 4,
    category: 'Main Courses',
    name: 'Grilled Chicken',
    description: 'Tender grilled chicken breast served with vegetables and potatoes.',
    price: 12.00,
    image: 'https://images.unsplash.com/photo-1532550907401-a500c9a57435?auto=format&fit=crop&w=600&q=80'
  },
  {
    id: 5,
    category: 'Main Courses',
    name: 'Beef Steak',
    description: 'Juicy grilled beef steak served with vegetables and special sauce.',
    price: 18.00,
    image: 'https://images.unsplash.com/photo-1546964124-0cce460f38ef?auto=format&fit=crop&w=600&q=80'
  },
  {
    id: 6,
    category: 'Main Courses',
    name: 'Creamy Pasta',
    description: 'Italian pasta with creamy sauce, parmesan cheese and herbs.',
    price: 10.50,
    image: 'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=600&q=80'
  },
  {
    id: 7,
    category: 'Pizza',
    name: 'Margherita Pizza',
    description: 'Classic pizza with tomato sauce, mozzarella and fresh basil.',
    price: 9.00,
    image: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=600&q=80'
  },
  {
    id: 8,
    category: 'Pizza',
    name: 'Pepperoni Pizza',
    description: 'Crispy pizza topped with mozzarella cheese and pepperoni.',
    price: 11.00,
    image: 'https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&w=600&q=80'
  },
  {
    id: 9,
    category: 'Pizza',
    name: 'Vegetable Pizza',
    description: 'Fresh vegetables, mozzarella and tomato sauce on crispy dough.',
    price: 10.00,
    image: 'https://images.unsplash.com/photo-1579751626657-72bc17010498?auto=format&fit=crop&w=600&q=80'
  },
  {
    id: 10,
    category: 'Desserts',
    name: 'Chocolate Cake',
    description: 'Soft chocolate cake served with chocolate cream and berries.',
    price: 6.00,
    image: 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=600&q=80'
  },
  {
    id: 11,
    category: 'Desserts',
    name: 'Strawberry Waffle',
    description: 'Fresh crispy waffle served with strawberries and cream.',
    price: 7.00,
    image: 'https://images.unsplash.com/photo-1562376552-0d160a2f238d?auto=format&fit=crop&w=600&q=80'
  },
  {
    id: 12,
    category: 'Drinks',
    name: 'Fresh Orange Juice',
    description: 'Freshly squeezed orange juice served chilled.',
    price: 3.50,
    image: 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?auto=format&fit=crop&w=600&q=80'
  }
]

const filteredMenu = computed(() => {
  if (activeCategory.value === 'All') {
    return menu
  }

  return menu.filter(item => item.category === activeCategory.value)
})

</script>

<template>

  <div class="min-h-screen bg-white text-black">


    <!-- ================= HERO ================= -->

    <section class="relative h-82.5 overflow-hidden">

      <img
        src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1600&q=80"
        alt="Food"
        class="absolute inset-0 w-full h-full object-cover"
      />

      <div class="absolute inset-0 bg-black/75"></div>


      <div
        class="relative h-full max-w-6xl mx-auto px-6 flex items-center justify-center text-center"
      >

        <div>

          <p
            class="text-orange-500 uppercase tracking-[4px] text-sm font-bold mb-4"
          >
            Delicious Food
          </p>

          <h1
            class="text-5xl md:text-6xl font-extrabold mb-5 text-white">Our <span class="text-orange-500">Menu</span>
          </h1>

          <p class="text-orange-500 max-w-xl mx-auto">
            Discover our delicious selection of freshly prepared
            dishes made with quality ingredients and lots of love.
          </p>

        </div>

      </div>

    </section>


    <!-- ================= MENU ================= -->

    <section class="max-w-6xl mx-auto px-6 py-16">


      <!-- Section title -->

      <div class="text-center mb-10">

        <p
          class="text-orange-500 uppercase tracking-[3px] text-sm font-bold mb-3"
        >
          Food Lover
        </p>

        <h2 class="text-4xl font-extrabold">
          Choose Your
          <span class="text-orange-500">
            Favorite Food
          </span>
        </h2>

      </div>


      <!-- ================= CATEGORY BUTTONS ================= -->

      <div
        class="flex flex-wrap justify-center gap-3 mb-12"
      >

        <button
          v-for="category in categories"
          :key="category"
          @click="activeCategory = category"
          class="px-5 py-2 rounded-full text-sm font-semibold border transition"
          :class="
            activeCategory === category
              ? 'bg-orange-500 border-orange-500 text-white'
              : 'border-gray-700 text-gray-400 hover:border-orange-500 hover:text-orange-500'
          "
        >
          {{ category }}
        </button>

      </div>


      <!-- ================= FOOD GRID ================= -->

      <div
        class="grid sm:grid-cols-2 lg:grid-cols-3 gap-7"
      >

        <div
          v-for="item in filteredMenu"
          :key="item.id"
          class="bg-white border-3 border-orange-500 rounded-lg overflow-hidden group hover:border-yellow-400 transition duration-300"
        >

          <!-- Image -->

          <div class="relative overflow-hidden">

            <img
              :src="item.image"
              :alt="item.name"
              class="w-full h-56 object-cover group-hover:scale-105 transition duration-500"
            />

            <!-- Price -->

            <button
              class="absolute top-4 right-4 bg-orange-500 px-4 py-2 rounded-full font-bold text-md cursor-pointer hover:bg-white hover:scale-105 transition duration-500"
            >
              ♡
            </button>

          </div>


          <!-- Content -->

          <div class="p-5">

            <p
              class="text-orange-500 uppercase text-[20px] tracking-widest font-bold mb-2"
            >
              {{ item.category }}
            </p>

            <h3 class="text-xl font-bold mb-2">
              {{ item.name }}
            </h3>

            <p
              class="text-gray-500 text-sm leading-6 mb-5 line-clamp-1"
            >
              {{ item.description }}
            </p>


            <!-- Bottom -->

            <div
              class="flex items-center justify-between"
            >

              <span
                class="text-orange-500 font-bold"
              >
                ${{ item.price.toFixed(2) }}
              </span>

              <button
                class="bg-orange-500 hover:bg-orange-600 px-4 py-2  rounded-md text-xs font-bold transition"
              >
                + ADD TO CART
              </button>

            </div>

          </div>

        </div>

      </div>


      <!-- Empty state -->

      <div
        v-if="filteredMenu.length === 0"
        class="text-center py-20 text-gray-500"
      >
        No food found in this category.
      </div>

    </section>


    <!-- ================= SPECIAL OFFER ================= -->

    <section class="bg-orange-500">

      <div
        class="max-w-6xl mx-auto px-6 py-14"
      >

        <div
          class="flex flex-col md:flex-row items-center justify-between gap-8"
        >

          <div>

            <p
              class="uppercase tracking-[3px] text-sm font-bold mb-2"
            >
              Today's Special
            </p>

            <h2 class="text-3xl md:text-4xl font-extrabold">
              Get 20% Off Your First Order
            </h2>

            <p class="mt-3 text-sm max-w-xl">
              Enjoy our delicious meals and receive a special
              discount when you place your first order with us.
            </p>

          </div>


          <button
            class="bg-[#15151b] hover:bg-black px-8 py-3 rounded-md font-bold text-sm whitespace-nowrap transition"
          >
            ORDER NOW
          </button>

        </div>

      </div>

    </section>


    <!-- ================= FOOTER ================= -->

    <footer class="bg-[#303036]">

      <div class="max-w-6xl mx-auto px-6 py-12">

        <div class="grid md:grid-cols-3 gap-10">


          <!-- Logo -->

          <div>

            <div
              class="flex items-center gap-2 mb-4"
            >

              <div
                class="w-10 h-10 rounded-full border-2 border-orange-500 flex items-center justify-center text-orange-500"
              >
                ♡
              </div>

              <h2 class="text-xl font-bold">
                Food <span class="text-orange-500">
                  Lover
                </span>
              </h2>

            </div>

            <p
              class="text-gray-400 text-sm leading-6"
            >
              Delicious food, friendly service and
              a warm atmosphere. Welcome to Food Lover.
            </p>

          </div>


          <!-- Quick Links -->

          <div>

            <h3 class="font-bold text-lg mb-4">
              Quick Links
            </h3>

            <div
              class="space-y-2 text-sm text-gray-400"
            >

              <NuxtLink
                to="/"
                class="block hover:text-orange-500"
              >
                Home
              </NuxtLink>

              <NuxtLink
                to="/about"
                class="block hover:text-orange-500"
              >
                About Us
              </NuxtLink>

              <NuxtLink
                to="/menu"
                class="block hover:text-orange-500"
              >
                Menu
              </NuxtLink>

              <NuxtLink
                to="/contact"
                class="block hover:text-orange-500"
              >
                Contact
              </NuxtLink>

            </div>

          </div>


          <!-- Contact -->

          <div>

            <h3 class="font-bold text-lg mb-4">
              Contact Us
            </h3>

            <div
              class="space-y-3 text-sm text-gray-400"
            >

              <p>📍 Phnom Penh, Cambodia</p>

              <p>📞 +855 12 345 678</p>

              <p>✉️ foodlover@gmail.com</p>

            </div>

          </div>

        </div>


        <!-- Bottom -->

        <div
          class="border-t border-gray-700 mt-10 pt-6 text-center"
        >

          <div
            class="flex justify-center gap-4 mb-4"
          >

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