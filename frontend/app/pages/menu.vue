<script setup lang="ts">
import { ref, computed } from 'vue'
import Caroursel from '~/components/Caroursel.vue'
import Footer from '~/components/Footer.vue'
import Navbar from '~/components/Navbar.vue'

interface MenuItem {
  id: string
  name: string
  description: string
  price: number
  category: 'Appetizers' | 'Mains' | 'Desserts' | 'Drinks'
  image: string
  tags: string[]
  isPopular?: boolean
}

interface CartItem extends MenuItem {
  quantity: number
}

// Active Filter States
const activeCategory = ref<'All' | 'Appetizers' | 'Mains' | 'Desserts' | 'Drinks'>('All')
const searchQuery = ref('')
const isCartOpen = ref(false)

// Sample Menu Data
const menuItems = ref<MenuItem[]>([
  {
    id: 'm1',
    name: 'Margherita Woodfired Pizza',
    description: 'San Marzano tomatoes, fresh buffalo mozzarella, organic basil leaves, extra virgin olive oil.',
    price: 18.50,
    category: 'Mains',
    image: 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?auto=format&fit=crop&w=600&q=80',
    tags: ['Vegetarian'],
    isPopular: true
  },
  {
    id: 'm2',
    name: 'Prime Angus Ribeye Steak',
    description: '12oz grilled Angus beef served with garlic herb butter, roasted rosemary, and sea salt.',
    price: 42.00,
    category: 'Mains',
    image: 'https://images.unsplash.com/photo-1558030006-450675393462?auto=format&fit=crop&w=600&q=80',
    tags: ['Gluten-Free', 'Chef Special'],
    isPopular: true
  },
  {
    id: 'm3',
    name: 'Truffle Parmesan Fries',
    description: 'Crispy hand-cut russet potatoes tossed in black truffle oil, fresh parmesan, and chives.',
    price: 9.50,
    category: 'Appetizers',
    image: 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=600&q=80',
    tags: ['Popular']
  },
  {
    id: 'm4',
    name: 'Artisan Cheese Board',
    description: 'Selection of aged cheeses, honey comb, dried figs, candied walnuts, and warm crostini.',
    price: 24.00,
    category: 'Appetizers',
    image: 'https://images.unsplash.com/photo-1631379578550-7038263db699?auto=format&fit=crop&w=600&q=80',
    tags: ['Vegetarian']
  },
  {
    id: 'm5',
    name: 'House-made Tiramisu',
    description: 'Espresso-soaked ladyfingers layered with sweet mascarpone cream and dusted with dark cocoa.',
    price: 8.50,
    category: 'Desserts',
    image: 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=600&q=80',
    tags: ['Contains Nuts'],
    isPopular: true
  },
  {
    id: 'm6',
    name: 'Smoked Old Fashioned',
    description: 'Small-batch bourbon whiskey, aromatic bitters, orange peel, infused with natural applewood smoke.',
    price: 15.00,
    category: 'Drinks',
    image: 'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?auto=format&fit=crop&w=600&q=80',
    tags: ['Signature']
  }
])

// Shopping Cart State
const cart = ref<CartItem[]>([])

// Filter Computation
const filteredMenu = computed(() => {
  return menuItems.value.filter(item => {
    const matchesCategory = activeCategory.value === 'All' || item.category === activeCategory.value
    const matchesSearch = item.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          item.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesCategory && matchesSearch
  })
})

// Cart Computations
const totalCartItems = computed(() => cart.value.reduce((sum, item) => sum + item.quantity, 0))
const totalCartPrice = computed(() => cart.value.reduce((sum, item) => sum + (item.price * item.quantity), 0))

// Add to Cart Action
const addToCart = (item: MenuItem) => {
  const existing = cart.value.find(c => c.id === item.id)
  if (existing) {
    existing.quantity += 1
  } else {
    cart.value.push({ ...item, quantity: 1 })
  }
}

const updateQuantity = (id: string, delta: number) => {
  const item = cart.value.find(c => c.id === id)
  if (!item) return
  item.quantity += delta
  if (item.quantity <= 0) {
    cart.value = cart.value.filter(c => c.id !== id)
  }
}
</script>

<template>
<Navbar/>
<Caroursel/>
  <section class="bg-white text-stone-900 font-sans selection:bg-amber-600 selection:text-white py-20 px-4 sm:px-6 lg:px-8 relative ">
    
    <div class="max-w-7xl mx-auto space-y-14">
      
      <!-- Styled Editorial Section Header -->
      <div class="text-center space-y-4 max-w-3xl mx-auto">
        <div class="flex items-center justify-center gap-3">
          <span class="h-px w-12 bg-amber-600"></span>
          <span class="text-amber-700 text-xs font-black uppercase tracking-[0.25em]">Culinary Excellence</span>
          <span class="h-px w-12 bg-amber-600"></span>
        </div>
        <h2 class="text-4xl sm:text-5xl font-serif font-black text-stone-900 tracking-tight uppercase">Our Menu</h2>
        <p class="text-stone-600 text-xs sm:text-sm leading-relaxed max-w-xl mx-auto font-medium">
          Fresh ingredients, artisanal recipes, and woodfired perfection crafted daily for an unmatched dining experience.
        </p>
      </div>

      <!-- Controls Bar: Sharp Category Navigation & Search Bar -->
      <div class="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-6 border-b-2 border-stone-900 pb-6">
        
        <!-- Category Buttons with Hover Effects -->
        <div class="flex items-center gap-1.5 overflow-x-auto pb-2 md:pb-0 scrollbar-none">
          <button 
            v-for="cat in ['All', 'Appetizers', 'Mains', 'Desserts', 'Drinks'] as const" 
            :key="cat"
            @click="activeCategory = cat"
            :class="activeCategory === cat 
              ? 'bg-stone-900 text-white border-stone-900 font-extrabold shadow-sm' 
              : 'bg-white text-stone-700 border-stone-300 hover:border-stone-900 hover:text-stone-900 font-bold'"
            class="px-5 py-2.5 rounded-none text-xs whitespace-nowrap border-2 transition-all duration-200 uppercase tracking-widest"
          >
            {{ cat }}
          </button>
        </div>

        <!-- Styled Search Input -->
        <div class="relative w-full md:w-80">
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Search menu items..." 
            class="w-full bg-stone-50 border-2 border-stone-300 text-stone-900 placeholder-stone-400 text-xs rounded-none py-2.5 pl-10 pr-4 focus:outline-none focus:border-amber-600 focus:bg-white transition-all font-medium"
          />
          <svg class="w-4 h-4 text-stone-500 absolute left-3.5 top-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>
      </div>

      <!-- Item Grid (Maintained 6 Items) -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div 
          v-for="item in filteredMenu" 
          :key="item.id"
          class="bg-white border-2 border-stone-200 rounded-none overflow-hidden hover:border-amber-600 transition-all duration-300 flex flex-col justify-between group shadow-xs hover:shadow-xl"
        >
          <!-- Image Section with Overlay Tags -->
          <div class="relative h-56 w-full overflow-hidden bg-stone-100 border-b-2 border-stone-100 group-hover:border-amber-600 transition-colors">
            <img 
              :src="item.image" 
              :alt="item.name" 
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out"
            />
            <!-- Badges -->
            <div class="absolute top-3 left-3 flex flex-wrap gap-1.5">
              <span 
                v-if="item.isPopular" 
                class="bg-amber-600 text-white font-black text-[10px] px-2.5 py-1 rounded-none uppercase tracking-widest border border-amber-700 shadow-xs"
              >
                ★ Featured
              </span>
              <span 
                v-for="(tag, idx) in item.tags" 
                :key="idx"
                class="bg-stone-900 text-white text-[10px] font-bold px-2.5 py-1 rounded-none uppercase tracking-wider"
              >
                {{ tag }}
              </span>
            </div>

            <!-- Floating Price Badge -->
            <div class="absolute bottom-3 right-3 bg-white border-2 border-stone-900 px-3 py-1 shadow-sm">
              <span class="font-serif font-black text-stone-900 text-base">${{ item.price.toFixed(2) }}</span>
            </div>
          </div>

          <!-- Content Section -->
          <div class="p-6 flex-1 flex flex-col justify-between space-y-6">
            <div class="space-y-2">
              <h3 class="text-xl font-bold text-stone-900 group-hover:text-amber-700 transition-colors font-serif leading-tight">
                {{ item.name }}
              </h3>
              <p class="text-stone-600 text-xs leading-relaxed line-clamp-3 font-medium">
                {{ item.description }}
              </p>
            </div>

            <!-- Action Button -->
            <button 
              @click="addToCart(item)"
              class="w-full bg-stone-900 hover:bg-amber-600 text-white font-extrabold text-xs py-3.5 rounded-none transition-all duration-200 flex items-center justify-center gap-2 uppercase tracking-widest border-2 border-stone-900 hover:border-amber-600 active:translate-y-0.5"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
              </svg>
              Add To Order
            </button>
          </div>
        </div>
      </div>

      <!-- Filter Empty State -->
      <div v-if="filteredMenu.length === 0" class="text-center py-20 border-2 border-dashed border-stone-300 space-y-3">
        <p class="text-stone-500 text-xs font-bold uppercase tracking-widest">No matching dishes found</p>
        <button 
          @click="searchQuery = ''; activeCategory = 'All'" 
          class="bg-stone-900 text-white text-xs font-bold px-4 py-2 uppercase tracking-wider hover:bg-amber-600 transition-colors"
        >
          Reset Search Filters
        </button>
      </div>

    </div>

    <!-- Floating Order Drawer Button -->
    <div v-if="totalCartItems > 0" class="fixed bottom-8 right-8 z-40">
      <button 
        @click="isCartOpen = true"
        class="bg-stone-900 hover:bg-amber-600 text-white font-black px-6 py-4 rounded-none border-2 border-stone-900 hover:border-amber-600 shadow-2xl flex items-center gap-4 transition-all duration-200"
      >
        <span class="bg-amber-600 text-white text-xs px-2.5 py-1 rounded-none font-mono font-bold">{{ totalCartItems }}</span>
        <span class="text-xs uppercase tracking-widest">Your Order</span>
        <span class="font-serif font-black text-amber-400 border-l border-stone-700 pl-3">${{ totalCartPrice.toFixed(2) }}</span>
      </button>
    </div>

    <!-- Order Side Drawer -->
    <div v-if="isCartOpen" class="fixed inset-0 z-50 flex justify-end bg-stone-950/60 backdrop-blur-xs">
      <div class="bg-white w-full max-w-md h-full shadow-2xl flex flex-col justify-between p-6 text-stone-900 border-l-4 border-stone-900">
        
        <!-- Header -->
        <div class="flex items-center justify-between border-b-2 border-stone-900 pb-4">
          <div class="space-y-0.5">
            <span class="text-[10px] font-black uppercase tracking-widest text-amber-700">Order Summary</span>
            <h3 class="text-xl font-black text-stone-900 uppercase font-serif">Selected Dishes</h3>
          </div>
          <button @click="isCartOpen = false" class="text-stone-400 hover:text-stone-900 text-2xl font-bold">✕</button>
        </div>

        <!-- Items -->
        <div class="flex-1 overflow-y-auto py-4 space-y-4 divide-y divide-stone-200">
          <div v-for="item in cart" :key="item.id" class="pt-4 flex items-center justify-between gap-4">
            <div class="space-y-1">
              <h4 class="text-xs font-extrabold text-stone-900 uppercase tracking-wide">{{ item.name }}</h4>
              <p class="text-xs text-amber-700 font-mono font-bold">${{ (item.price * item.quantity).toFixed(2) }}</p>
            </div>

            <!-- Quantity Counter -->
            <div class="flex items-center border-2 border-stone-900 bg-white">
              <button @click="updateQuantity(item.id, -1)" class="w-8 h-8 flex items-center justify-center text-xs text-stone-900 hover:bg-stone-100 font-black">-</button>
              <span class="text-xs font-mono font-bold text-stone-900 w-6 text-center">{{ item.quantity }}</span>
              <button @click="updateQuantity(item.id, 1)" class="w-8 h-8 flex items-center justify-center text-xs text-stone-900 hover:bg-stone-100 font-black">+</button>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="border-t-2 border-stone-900 pt-4 space-y-4">
          <div class="flex justify-between items-center text-sm font-black uppercase tracking-wider">
            <span class="text-stone-600">Subtotal</span>
            <span class="text-2xl font-serif text-amber-700">${{ totalCartPrice.toFixed(2) }}</span>
          </div>

          <button 
            @click="alert('Proceeding to Checkout!')" 
            class="w-full bg-amber-600 hover:bg-amber-700 text-white font-extrabold py-4 rounded-none text-xs uppercase tracking-widest transition-all duration-200 border-2 border-amber-600"
          >
            Checkout Order
          </button>
        </div>

      </div>
    </div>

  </section>
  <Footer/>
</template>

<style scoped>
</style>