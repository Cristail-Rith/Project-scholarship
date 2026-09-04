<template>
    <footer class="bg-[#141210] text-stone-300 font-serif pt-16 pb-8 border-t border-amber-900/30">
      <div class="max-w-7xl mx-auto px-6">
        <!-- Main Footer Columns Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 pb-12 border-b border-stone-800">
          
          <!-- Column 1: Brand & Logo -->
          <div class="space-y-4">
            <div class="flex flex-col items-start group">
              <svg class="w-7 h-5 text-[#C59237] mb-1" fill="currentColor" viewBox="0 0 24 24">
                <path d="M5 16L3 5l5.5 5L12 4l3.5 6L21 5l-2 11H5zm14 3c0 .6-.4 1-1 1H6c-.6 0-1-.4-1-1v-1h14v1z"/>
              </svg>
              <span class="font-serif text-2xl font-normal tracking-[0.25em] text-white">FLAVORIA</span>
              <span class="text-[9px] tracking-[0.35em] text-[#C59237] uppercase font-sans mt-1">Fine Dining</span>
            </div>
            <p class="font-sans text-xs text-stone-400 leading-relaxed font-light">
              Crafting extraordinary culinary moments through classic techniques, seasonal ingredients, and memorable hospitality.
            </p>
            <div class="pt-2 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>
              <span class="font-sans text-[11px] text-stone-400 tracking-wider">Michelin Guide Recommended 2026</span>
            </div>
          </div>

          <!-- Column 2: Quick Links -->
          <div class="font-sans">
            <h3 class="font-serif text-base text-white tracking-widest uppercase mb-4 relative pb-2 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-8 after:h-[1px] after:bg-[#C59237]">
              Navigation
            </h3>
            <ul class="space-y-2.5 text-xs text-stone-400">
              <li><NuxtLink to="/menu" class="hover:text-amber-400 transition-colors">Our Menu</NuxtLink></li>
              <li><NuxtLink to="/reservation" class="hover:text-amber-400 transition-colors">Book a Table</NuxtLink></li>
              <li><NuxtLink to="/about" class="hover:text-amber-400 transition-colors">About Flavoria</NuxtLink></li>
              <li><NuxtLink to="/events" class="hover:text-amber-400 transition-colors">Private Events & Catering</NuxtLink></li>
              <li><NuxtLink to="/chefs" class="hover:text-amber-400 transition-colors">Meet Culinary Team</NuxtLink></li>
            </ul>
          </div>

          <!-- Column 3: Opening Hours -->
          <div class="font-sans">
            <h3 class="font-serif text-base text-white tracking-widest uppercase mb-4 relative pb-2 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-8 after:h-[1px] after:bg-[#C59237]">
              Opening Hours
            </h3>
            <ul class="space-y-2 text-xs text-stone-400">
              <li class="flex justify-between border-b border-stone-800/80 pb-1.5">
                <span>Mon - Thu:</span>
                <span class="text-stone-200">11:30 AM - 10:00 PM</span>
              </li>
              <li class="flex justify-between border-b border-stone-800/80 pb-1.5">
                <span>Fri - Sat:</span>
                <span class="text-stone-200">11:30 AM - 11:30 PM</span>
              </li>
              <li class="flex justify-between pb-1">
                <span>Sunday:</span>
                <span class="text-stone-200">10:00 AM - 9:30 PM</span>
              </li>
            </ul>
          </div>

          <!-- Column 4: Newsletter & Contact -->
          <div class="font-sans space-y-4">
            <h3 class="font-serif text-base text-white tracking-widest uppercase relative pb-2 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-8 after:h-[1px] after:bg-[#C59237]">
              Newsletter
            </h3>
            <p class="text-xs text-stone-400 font-light">
              Subscribe to receive exclusive tasting menu invitations and seasonal updates.
            </p>
            <form @submit.prevent="subscribeNewsletter" class="flex items-center">
              <input 
                type="email" 
                v-model="emailInput" 
                placeholder="Your Email Address" 
                class="bg-stone-900 border border-stone-700 text-xs px-3 py-2.5 w-full text-stone-200 placeholder-stone-500 focus:outline-none focus:border-[#C59237]"
                required
              />
              <button type="submit" class="bg-[#C59237] hover:bg-amber-600 text-white px-4 py-2.5 text-xs font-semibold uppercase tracking-wider transition-colors">
                Join
              </button>
            </form>
          </div>

        </div>

        <!-- Sub-Footer / Copyright & Socials -->
        <div class="pt-8 flex flex-col md:flex-row items-center justify-between font-sans text-xs text-stone-500 gap-4">
          <p>© 2026 FLAVORIA Fine Dining. All Rights Reserved.</p>
          
          <div class="flex items-center gap-6">
            <a href="#" class="hover:text-amber-400 transition-colors">Privacy Policy</a>
            <a href="#" class="hover:text-amber-400 transition-colors">Terms of Service</a>
            <button @click="scrollToTop" class="flex items-center gap-1 text-stone-400 hover:text-[#C59237] transition-colors ml-4">
              <span>Back to Top</span>
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/></svg>
            </button>
          </div>
        </div>
      </div>
    </footer>
</template>

<script setup>
import { ref } from 'vue'

const mobileMenuOpen = ref(false)
const selectedTab = ref('All items')
const emailInput = ref('')

const categories = [
  { name: 'Starters', image: 'https://images.unsplash.com/photo-1541544741938-0af808871cc0?auto=format&fit=crop&w=400&q=80' },
  { name: 'Main Course', image: 'https://images.unsplash.com/photo-1621996346565-e3d5d6281273?auto=format&fit=crop&w=400&q=80' },
  { name: 'Desserts', image: 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=400&q=80' },
  { name: 'Beverages', image: 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=400&q=80' },
  { name: 'Pizza', image: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=400&q=80' },
  { name: 'Chef Specials', image: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=400&q=80' }
]

const filterTabs = ['All items', 'Starters', 'Main Course', 'Desserts', 'Beverages']

const recommendationItems = [
  { id: 1, name: 'Grilled Salmon', description: 'Served with lemon butter sauce', price: 24.99, rating: '4.8', badge: 'Bestseller', image: 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=500&q=80' },
  { id: 2, name: 'Creamy Prawn Pasta', description: 'Penne in creamy garlic sauce', price: 21.99, rating: '4.7', badge: 'New', image: 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=500&q=80' },
  { id: 3, name: 'Ribeye Steak', description: 'Grilled to perfection', price: 29.99, rating: '4.9', badge: null, image: 'https://images.unsplash.com/photo-1558030006-450675393462?auto=format&fit=crop&w=500&q=80' },
  { id: 4, name: 'Classic Tiramisu', description: 'With cocoa & mascarpone', price: 8.99, rating: '4.6', badge: null, image: 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=500&q=80' },
  { id: 5, name: 'Truffle Mushroom Risotto', description: 'Creamy arborio rice', price: 18.99, rating: null, badge: null, image: 'https://images.unsplash.com/photo-1633964913295-ceb43826e7c9?auto=format&fit=crop&w=500&q=80' },
  { id: 6, name: 'Margherita Pizza', description: 'Fresh basil & mozzarella', price: 16.99, rating: null, badge: null, image: 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?auto=format&fit=crop&w=500&q=80' },
  { id: 7, name: 'Mango Passion Mocktail', description: 'Tropical refreshing drink', price: 7.99, rating: null, badge: null, image: 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=500&q=80' },
  { id: 8, name: 'Chocolate Lava Cake', description: 'Served with vanilla ice cream', price: 9.99, rating: null, badge: null, image: 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=500&q=80' }
]

const subscribeNewsletter = () => {
  alert(`Thank you for subscribing with ${emailInput.value}!`)
  emailInput.value = ''
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
.nav-link {
  position: relative;
  padding-bottom: 4px;
}
.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: #C59237;
  transition: width 0.3s ease;
}
.nav-link:hover::after,
.nav-link.active-link::after {
  width: 100%;
}
</style>