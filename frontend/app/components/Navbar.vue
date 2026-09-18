<template>
  <header
    class="w-full font-serif text-neutral-800 bg-neutral-50 shadow-sm sticky top-0 z-50"
  >
    <!-- Main Navigation Bar -->
    <nav
      class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between font-sans"
    >
      <!-- Left Navigation Links -->
      <div
        class="hidden lg:flex items-center gap-10   text-xs font-semibold tracking-[0.2em] text-neutral-700 uppercase"
      >
        <NuxtLink to="/" class="nav-link">HOME</NuxtLink>
        <NuxtLink to="/menu" class="nav-link">MENU</NuxtLink>
        <NuxtLink to="/about" class="nav-link">ABOUT FLAVORIA</NuxtLink>
        <NuxtLink to="/contact" class="nav-link">CONTACT AS</NuxtLink>
      </div>

      <!-- Mobile Hamburger Button -->
      <button
        @click="mobileMenuOpen = !mobileMenuOpen"
        class="lg:hidden p-2 text-neutral-700 focus:outline-none"
        aria-label="Toggle Navigation"
      >
        <svg
          class="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            v-if="!mobileMenuOpen"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M4 6h16M4 12h16M4 18h16"
          />
          <path
            v-else
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>

      <!-- Centered Logo -->
      <NuxtLink
        to="/"
        class="flex flex-col items-center group cursor-pointer text-center my-1"
      >
        <!-- Crown SVG Icon -->
        <svg
          class="w-7 h-5 text-amber-600 group-hover:text-amber-700 transition-colors mb-1"
          fill="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            d="M5 16L3 5l5.5 5L12 4l3.5 6L21 5l-2 11H5zm14 3c0 .6-.4 1-1 1H6c-.6 0-1-.4-1-1v-1h14v1z"
          />
        </svg>

        <span
          class="font-serif text-2xl md:text-3xl font-normal tracking-[0.25em] text-neutral-900 leading-none pl-1"
        >
          FLAVORIA
        </span>

        <span
          class="text-[9px] md:text-[10px] tracking-[0.35em] text-amber-800 uppercase font-sans mt-1.5 font-medium"
        >
          Fine Dining
        </span>
      </NuxtLink>

      <!-- Right Navigation Links & Action Icons -->
      <div class="flex items-center gap-6 md:gap-8">
        <!-- Desktop Navigation -->
        <div
          class="hidden lg:flex items-center gap-10 text-xs font-semibold tracking-[0.2em] text-neutral-700 uppercase"
        >
          <NuxtLink to="/reservation" class="nav-link">
            RESERVATION
          </NuxtLink>

          <!-- Pages Dropdown -->
          <div class="relative group cursor-pointer py-2">
            <span class="nav-link flex items-center gap-1">
              PAGES

              <svg
                class="w-3 h-3 text-neutral-500 group-hover:rotate-180 transition-transform duration-200"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </span>

            <!-- Dropdown Menu -->
            <div
              class="absolute top-full right-0 w-48 bg-white border border-stone-200 shadow-lg rounded-sm py-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50"
            >
              <NuxtLink
                to="/chefs"
                class="block px-4 py-2 text-xs hover:bg-amber-50 hover:text-amber-900 tracking-wider"
              >
                OUR CHEFS
              </NuxtLink>

              <NuxtLink
                to="/events"
                class="block px-4 py-2 text-xs hover:bg-amber-50 hover:text-amber-900 tracking-wider"
              >
                PRIVATE EVENTS
              </NuxtLink>

              <NuxtLink
                to="/gallery"
                class="block px-4 py-2 text-xs hover:bg-amber-50 hover:text-amber-900 tracking-wider"
              >
                GALLERY
              </NuxtLink>

              
            </div>
          </div>
        </div>

        <!-- Right Quick Action Icons -->
        <div class="flex items-center gap-4 text-neutral-700">

          <!-- Search Button -->
          <button
            @click="toggleSearch"
            class="p-1 hover:text-amber-700 transition-colors"
            aria-label="Search"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.8"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </button>

          <!-- Search Overlay -->
          <Transition
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="opacity-0 scale-95"
            enter-to-class="opacity-100 scale-100"
            leave-active-class="transition duration-200 ease-in"
            leave-from-class="opacity-100 scale-100"
            leave-to-class="opacity-0 scale-95"
          >
            <div
              v-if="searchOpen"
              class="fixed inset-0 z-[60] flex items-start justify-center pt-24 bg-black/50 backdrop-blur-sm"
              @click.self="closeSearch"
            >
              <div class="relative w-full max-w-2xl mx-4">
                <input
                  ref="searchInput"
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search products by name..."
                  autocomplete="off"
                  class="w-full px-4 py-3 pr-10 text-base text-neutral-900 bg-white border-2 border-stone-300 rounded-sm focus:outline-none focus:border-amber-700 shadow-lg"
                  @keydown.esc="closeSearch"
                />

                <svg
                  class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-stone-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="1.8"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>

                <!-- Results Dropdown -->
                <Transition
                  enter-active-class="transition duration-150 ease-out"
                  enter-from-class="opacity-0 -translate-y-1"
                  enter-to-class="opacity-100 translate-y-0"
                  leave-active-class="transition duration-150 ease-in"
                  leave-from-class="opacity-100 translate-y-0"
                  leave-to-class="opacity-0 -translate-y-1"
                >
                  <div
                    v-if="filteredProducts.length > 0"
                    class="absolute z-50 mt-1 w-full bg-white border border-stone-200 shadow-xl rounded-sm max-h-80 overflow-y-auto"
                  >
                    <button
                      v-for="product in filteredProducts"
                      :key="product.id"
                      @click="goToProduct(product)"
                      class="w-full flex items-center gap-3 p-3 text-left hover:bg-amber-50 transition-colors"
                    >
                      <img
                        :src="product.image"
                        :alt="product.title"
                        class="w-12 h-12 object-cover rounded-sm border border-stone-200"
                      />

                      <div class="flex-1 min-w-0">
                        <p
                          class="font-sans text-sm font-semibold text-neutral-900 truncate"
                        >
                          {{ product.title }}
                        </p>

                        <p
                          class="font-sans text-xs text-stone-500 truncate"
                        >
                          {{ product.category }}
                        </p>
                      </div>

                      <span
                        class="font-sans text-xs font-bold text-amber-700 shrink-0"
                      >
                        ${{ product.price.toFixed(2) }}
                      </span>
                    </button>
                  </div>
                </Transition>

                <!-- No Results -->
                <Transition
                  enter-active-class="transition duration-150 ease-out"
                  enter-from-class="opacity-0 -translate-y-1"
                  enter-to-class="opacity-100 translate-y-0"
                  leave-active-class="transition duration-150 ease-in"
                  leave-from-class="opacity-100 translate-y-0"
                  leave-to-class="opacity-0 -translate-y-1"
                >
                  <p
                    v-if="
                      filteredProducts.length === 0 &&
                      searchQuery.trim().length > 0
                    "
                    class="absolute z-50 mt-1 w-full bg-white border border-stone-200 shadow-xl rounded-sm p-4 text-sm text-stone-500 font-sans"
                  >
                    No products found for "{{ searchQuery }}"
                  </p>
                </Transition>
              </div>
            </div>
          </Transition>

          <!-- User / Account -->
          <div
            v-if="mounted && user && !isMobile"
            class="flex items-center gap-3 "
          > 
            <NuxtLink
              to="/profile"
              class="flex items-center gap-2 hover:text-amber-700 transition-colors"
              aria-label="Profile"
            >
              <img
                v-if="user.avatar"
                :src="
                  user.avatar.startsWith('http')
                    ? user.avatar
                    : config.public.apiBase + user.avatar
                "
                :alt="user.username"
                class="w-8 h-8 rounded-full object-cover border border-stone-200"
              />

              <div
                v-else
                class="w-8 h-8 rounded-full bg-[#C59237] flex items-center justify-center text-white text-xs font-bold"
              >
                {{ user.username?.charAt(0).toUpperCase() || 'U' }}
              </div>

              <span
                class="hidden lg:block text-xs font-sans font-semibold text-neutral-700 tracking-wide uppercase"
              >
                {{ user.username }}
              </span>
            </NuxtLink>

            <button
              type="button"
              @click="handleLogout"
              class="p-1 hover:text-amber-700 transition-colors"
              aria-label="Logout"
              title="Logout"
            >
              <svg
                class="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.8"
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                />
              </svg>
            </button>
          </div>

          <!-- Mobile User -->
          <div
            v-if="mounted && user && isMobile"
            class="flex items-center gap-2"
          >
            <NuxtLink
              to="/profile"
              class="flex items-center gap-1 hover:text-amber-700 transition-colors"
              aria-label="Profile"
            >
              <img
                v-if="user.avatar"
                :src="
                  user.avatar.startsWith('http')
                    ? user.avatar
                    : config.public.apiBase + user.avatar
                "
                :alt="user.username"
                class="w-7 h-7 rounded-full object-cover border border-stone-200"
              />

              <div
                v-else
                class="w-7 h-7 rounded-full bg-[#C59237] flex items-center justify-center text-white text-[10px] font-bold"
              >
                {{ user.username?.charAt(0).toUpperCase() || 'U' }}
              </div>
            </NuxtLink>

            <!-- <button
              type="button"
              @click="handleLogout"
              class="p-1 hover:text-amber-700 transition-colors md:hidden"
              aria-label="Logout"
              title="Logout"
            >
              <svg
                class="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.8"
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                />
              </svg>
            </button> -->
          </div>

          <!-- Login -->
          <NuxtLink
            v-if="!user"
            to="/login"
            class="p-1 hover:text-amber-700 transition-colors"
            aria-label="Account"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.8"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
          </NuxtLink>

          <!-- SHOPPING CART -->
          <button
            type="button"
            class="relative p-1 hover:text-amber-700 transition-colors"
            :class="{ 'cart-bounce': cartAnimating }"
            aria-label="Shopping Cart"
            @click="isCartOpen = true"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.8"
                d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
              />
            </svg>

            <!-- Cart Badge -->
            <span
              v-if="totalItems > 0"
              class="absolute -top-1 -right-1 bg-amber-700 text-white text-[10px] w-4 h-4 rounded-full flex items-center justify-center font-sans"
              :class="{ 'cart-badge-pop': cartAnimating }"
            >
              {{ totalItems }}
            </span>
          </button>
        </div>
      </div>
    </nav>

    <!-- Mobile Drawer Navigation -->
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="transform -translate-y-4 opacity-0"
      enter-to-class="transform translate-y-0 opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="transform translate-y-0 opacity-100"
      leave-to-class="transform -translate-y-4 opacity-0"
    >
      <div
        v-if="mobileMenuOpen"
        class="lg:hidden bg-neutral-900 text-stone-200 px-6 py-6 border-t border-stone-800"
      >
        <ul
          class="flex flex-col gap-4 text-sm tracking-[0.2em] font-medium uppercase"
        >
          <li>
            <NuxtLink
              @click="mobileMenuOpen = false"
              to="/"
              class="block py-2 hover:text-amber-400"
            >
              HOME
            </NuxtLink>
          </li>

          <li>
            <NuxtLink
              @click="mobileMenuOpen = false"
              to="/menu"
              class="block py-2 hover:text-amber-400"
            >
              MENU
            </NuxtLink>
          </li>

          <li>
            <NuxtLink
              @click="mobileMenuOpen = false"
              to="/about"
              class="block py-2 hover:text-amber-400"
            >
              ABOUT
            </NuxtLink>
          </li>

          <li>
            <NuxtLink
              @click="mobileMenuOpen = false"
              to="/reservation"
              class="block py-2 hover:text-amber-400"
            >
              RESERVATION
            </NuxtLink>
          </li>

          <li>
            <NuxtLink
              @click="mobileMenuOpen = false"
              to="/chefs"
              class="block py-2 hover:text-amber-400"
            >
              OUR CHEFS
            </NuxtLink>
          </li>

          <li>
            <NuxtLink
              @click="mobileMenuOpen = false"
              to="/events"
              class="block py-2 hover:text-amber-400"
            >
              PRIVATE EVENTS
            </NuxtLink>
          </li>

          <li>
            <NuxtLink
              @click="mobileMenuOpen = false"
              to="/contact"
              class="block py-2 hover:text-amber-400"
            >
              CONTACT US
            </NuxtLink>
          </li>
        </ul>
      </div>
    </Transition>
  </header>

  <!-- CART TOAST -->
  <Transition
    enter-active-class="transition-all duration-300 ease-out"
    enter-from-class="opacity-0 translate-x-8"
    enter-to-class="opacity-100 translate-x-0"
    leave-active-class="transition-all duration-300 ease-in"
    leave-from-class="opacity-100 translate-x-0"
    leave-to-class="opacity-0 translate-x-8"
  >
    <div
      v-if="cartMessage"
      class="fixed right-5 top-24 z-[100] flex items-center gap-3 rounded-xl border border-stone-200 bg-white px-4 py-3 shadow-xl"
    >
      <div
        class="flex h-8 w-8 items-center justify-center rounded-full bg-amber-100 text-amber-700"
      >
        ✓
      </div>

      <div>
        <p class="text-xs font-bold text-stone-900">
          Added to your order
        </p>

        <p class="text-[11px] text-stone-500">
          {{ cartMessage }}
        </p>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProducts } from '~/composables/useProducts'
import { useCart } from '~/composables/useCart'
import { useAuth } from '~/composables/useAuth'

const router = useRouter()
const config = useRuntimeConfig()

const { searchQuery, filteredProducts } = useProducts()

const {
  totalItems,
  cartAnimating,
  cartMessage,
  isCartOpen
} = useCart()

const { user, logout } = useAuth()

const mobileMenuOpen = ref(false)
const searchOpen = ref(false)
const searchInput = ref(null)
const isMobile = ref(false)
const mounted = ref(false)

const checkMobile = () => {
  isMobile.value =
    typeof window !== 'undefined' && window.innerWidth < 768
}

const toggleSearch = () => {
  checkMobile()

  searchOpen.value = !searchOpen.value

  if (searchOpen.value) {
    searchQuery.value = ''

    nextTick(() => {
      searchInput.value?.focus()
    })
  } else {
    searchQuery.value = ''
  }
}

const closeSearch = () => {
  searchOpen.value = false
  searchQuery.value = ''
}

const goToProduct = (product) => {
  closeSearch()
  navigateTo(`/product/${product.id}`)
}

const handleLogout = () => {
  logout()
  router.push('/login')
}

onMounted(() => {
  mounted.value = true
  checkMobile()

  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
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
  background-color: #c5a880;
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

/* Cart icon animation */
.cart-bounce {
  animation: cartBounce 0.7s ease-in-out;
}

/* Cart number animation */
.cart-badge-pop {
  animation: badgePop 0.5s ease-out;
}

@keyframes cartBounce {
  0% {
    transform: translateX(0) rotate(0deg) scale(1);
  }

  15% {
    transform: translateX(-3px) rotate(-12deg) scale(1.15);
  }

  30% {
    transform: translateX(3px) rotate(12deg) scale(1.15);
  }

  45% {
    transform: translateX(-3px) rotate(-8deg) scale(1.1);
  }

  60% {
    transform: translateX(3px) rotate(8deg) scale(1.05);
  }

  75% {
    transform: translateX(-1px) rotate(-3deg) scale(1.02);
  }

  100% {
    transform: translateX(0) rotate(0deg) scale(1);
  }
}

@keyframes badgePop {
  0% {
    transform: scale(1);
  }

  40% {
    transform: scale(1.5);
  }

  70% {
    transform: scale(0.9);
  }

  100% {
    transform: scale(1);
  }
}
</style>