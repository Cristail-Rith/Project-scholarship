<template>
  <Navbar />
  <main class="events-page min-h-screen overflow-x-hidden bg-[#FDFBF7] text-stone-800">
    <section class="relative overflow-hidden bg-stone-950 px-4 py-24 text-center text-white sm:px-6 md:py-32">
      <img
        src="https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=1800&q=80"
        alt="Private event dining room"
        class="absolute inset-0 h-full w-full object-cover opacity-35"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-stone-950 via-stone-950/65 to-stone-950/20"></div>
      <div class="relative mx-auto max-w-3xl">
        <p class="mb-4 text-xs font-semibold uppercase tracking-[0.3em] text-[#C59237]">Bespoke Celebrations</p>
        <h1 class="font-serif text-5xl font-normal tracking-wide text-stone-100 sm:text-6xl">Private Events</h1>
        <p class="mx-auto mt-6 max-w-xl font-sans text-sm font-light leading-relaxed text-stone-300">
          Host corporate galas, intimate wedding dinners, and milestone celebrations in our refined dining spaces.
        </p>
      </div>
    </section>

    <section class="mx-auto max-w-7xl px-4 py-16 sm:px-6 md:py-24">
      <div class="mb-12 text-center">
        <p class="text-xs font-semibold uppercase tracking-[0.25em] text-[#C59237]">Choose your setting</p>
        <h2 class="mt-3 font-serif text-3xl font-normal tracking-wide text-stone-900 sm:text-4xl">Our Event Spaces</h2>
      </div>
      <div class="grid grid-cols-1 gap-8 md:grid-cols-3">
        <article v-for="venue in venues" :key="venue.title" class="overflow-hidden border border-stone-200 bg-white shadow-sm transition-shadow duration-300 hover:shadow-xl">
          <div class="relative h-64 overflow-hidden bg-stone-900">
            <img :src="venue.image" :alt="venue.title" class="h-full w-full object-cover transition-transform duration-500 hover:scale-105" />
            <span class="absolute right-3 top-3 bg-stone-950/90 px-3 py-1 text-[10px] font-semibold uppercase tracking-wider text-[#C59237]">Up to {{ venue.capacity }} guests</span>
          </div>
          <div class="p-6">
            <h3 class="font-serif text-xl text-stone-900">{{ venue.title }}</h3>
            <p class="mt-3 font-sans text-sm leading-relaxed text-stone-500">{{ venue.description }}</p>
            <p class="mt-5 border-t border-stone-100 pt-4 font-sans text-xs text-stone-600"><span class="font-semibold text-stone-900">Best for:</span> {{ venue.bestFor }}</p>
          </div>
        </article>
      </div>
    </section>

    <section class="border-y border-stone-200 bg-[#FAF7F2] px-4 py-16 sm:px-6 md:py-24">
      <div class="service-grid mx-auto max-w-7xl items-center">
        <div class="font-sans">
          <p class="text-xs font-semibold uppercase tracking-[0.25em] text-[#C59237]">Custom experience</p>
          <h2 class="mt-4 max-w-lg font-serif text-4xl font-normal leading-tight text-stone-900">Tailored menus and dedicated service</h2>
          <p class="mt-6 max-w-xl text-sm leading-relaxed text-stone-600">Our event coordinator and culinary team work with you to create a seamless celebration, from the first tasting to the final toast.</p>
          <ul class="mt-8 grid gap-4 font-sans text-sm text-stone-700 sm:grid-cols-2">
            <li v-for="benefit in benefits" :key="benefit" class="flex gap-3"><span class="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-[#C59237]"></span>{{ benefit }}</li>
          </ul>
        </div>
        <img src="https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=1000&q=80" alt="Dinner party table setup" class="h-96 w-full object-cover shadow-xl" />
      </div>
    </section>

<!-- Event Inquiry Form -->
<section class="relative py-20 md:py-28 px-4 sm:px-6 overflow-hidden bg-stone-950">
  <!-- Background Image with Overlay -->
  <div class="absolute inset-0 z-0">
    <img 
      src="https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?auto=format&fit=crop&w=2000&q=80" 
      alt="Atmospheric Event Setting" 
      class="w-full h-full object-cover opacity-35 filter brightness-75 scale-105"
    />
    <div class="absolute inset-0 bg-gradient-to-b from-stone-950 via-stone-950/70 to-stone-950"></div>
  </div>

  <!-- Form Container Card -->
  <div class="relative z-10 max-w-4xl mx-auto bg-stone-900/85 backdrop-blur-md border border-stone-800/80 rounded-sm p-6 sm:p-12 shadow-2xl font-sans">
    
    <!-- Section Title -->
    <div class="text-center space-y-2 mb-10">
      <span class="text-xs font-semibold tracking-[0.25em] text-[#C59237] uppercase">Get In Touch</span>
      <h2 class="font-serif text-3xl sm:text-4xl font-normal text-stone-100">Request Event Booking</h2>
      <p class="text-xs sm:text-sm text-stone-400 font-light max-w-md mx-auto">
        Fill out the form below and our event coordinator will contact you within 24 hours.
      </p>
    </div>

    <!-- Form Inputs -->
    <form @submit.prevent="submitInquiry" class="space-y-6">
      
      <!-- Row 1: Name & Email -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div>
          <label class="block text-[11px] uppercase tracking-wider text-stone-300 font-semibold mb-2">Full Name *</label>
          <input 
            v-model="form.name" 
            type="text" 
            required 
            class="w-full bg-stone-950/70 border border-stone-700/80 text-xs px-4 py-3.5 rounded-xs text-stone-200 placeholder-stone-500 focus:outline-none focus:border-[#C59237] focus:ring-1 focus:ring-[#C59237] transition-all" 
            placeholder="John Doe" 
          />
        </div>
        <div>
          <label class="block text-[11px] uppercase tracking-wider text-stone-300 font-semibold mb-2">Email Address *</label>
          <input 
            v-model="form.email" 
            type="email" 
            required 
            class="w-full bg-stone-950/70 border border-stone-700/80 text-xs px-4 py-3.5 rounded-xs text-stone-200 placeholder-stone-500 focus:outline-none focus:border-[#C59237] focus:ring-1 focus:ring-[#C59237] transition-all" 
            placeholder="john@example.com" 
          />
        </div>
      </div>

      <!-- Row 2: Phone, Date, Guests -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div>
          <label class="block text-[11px] uppercase tracking-wider text-stone-300 font-semibold mb-2">Phone Number *</label>
          <input 
            v-model="form.phone" 
            type="tel" 
            required 
            class="w-full bg-stone-950/70 border border-stone-700/80 text-xs px-4 py-3.5 rounded-xs text-stone-200 placeholder-stone-500 focus:outline-none focus:border-[#C59237] focus:ring-1 focus:ring-[#C59237] transition-all" 
            placeholder="+1 234 567 890" 
          />
        </div>
        <div>
          <label class="block text-[11px] uppercase tracking-wider text-stone-300 font-semibold mb-2">Expected Date *</label>
          <input 
            v-model="form.date" 
            type="date" 
            required 
            class="w-full bg-stone-950/70 border border-stone-700/80 text-xs px-4 py-3.5 rounded-xs text-stone-200 focus:outline-none focus:border-[#C59237] focus:ring-1 focus:ring-[#C59237] transition-all [color-scheme:dark]" 
          />
        </div>
        <div>
          <label class="block text-[11px] uppercase tracking-wider text-stone-300 font-semibold mb-2">Guest Count *</label>
          <input 
            v-model="form.guests" 
            type="number" 
            min="5" 
            max="150" 
            required 
            class="w-full bg-stone-950/70 border border-stone-700/80 text-xs px-4 py-3.5 rounded-xs text-stone-200 placeholder-stone-500 focus:outline-none focus:border-[#C59237] focus:ring-1 focus:ring-[#C59237] transition-all" 
            placeholder="20" 
          />
        </div>
      </div>

      <!-- Row 3: Space & Type -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div>
          <label class="block text-[11px] uppercase tracking-wider text-stone-300 font-semibold mb-2">Preferred Space</label>
          <select 
            v-model="form.preferredSpace" 
            class="w-full bg-stone-950/70 border border-stone-700/80 text-xs px-4 py-3.5 rounded-xs text-stone-200 focus:outline-none focus:border-[#C59237] focus:ring-1 focus:ring-[#C59237] transition-all"
          >
            <option class="bg-stone-900 text-stone-200" value="VIP Royal Lounge">VIP Royal Lounge</option>
            <option class="bg-stone-900 text-stone-200" value="Courtyard Terrace">Courtyard Terrace</option>
            <option class="bg-stone-900 text-stone-200" value="Grand Dining Hall">Grand Dining Hall (Full Buyout)</option>
          </select>
        </div>
        <div>
          <label class="block text-[11px] uppercase tracking-wider text-stone-300 font-semibold mb-2">Event Type</label>
          <select 
            v-model="form.eventType" 
            class="w-full bg-stone-950/70 border border-stone-700/80 text-xs px-4 py-3.5 rounded-xs text-stone-200 focus:outline-none focus:border-[#C59237] focus:ring-1 focus:ring-[#C59237] transition-all"
          >
            <option class="bg-stone-900 text-stone-200" value="Corporate Dinner">Corporate Dinner</option>
            <option class="bg-stone-900 text-stone-200" value="Birthday / Anniversary">Birthday / Anniversary</option>
            <option class="bg-stone-900 text-stone-200" value="Wedding Rehearsal">Wedding Rehearsal</option>
            <option class="bg-stone-900 text-stone-200" value="Cocktail Reception">Cocktail Reception</option>
          </select>
        </div>
      </div>

      <!-- Row 4: Notes -->
      <div>
        <label class="block text-[11px] uppercase tracking-wider text-stone-300 font-semibold mb-2">Additional Notes & Requests</label>
        <textarea 
          v-model="form.notes" 
          rows="4" 
          class="w-full bg-stone-950/70 border border-stone-700/80 text-xs p-4 rounded-xs text-stone-200 placeholder-stone-500 focus:outline-none focus:border-[#C59237] focus:ring-1 focus:ring-[#C59237] transition-all" 
          placeholder="Tell us about special dietary needs, entertainment setup, or color themes..."
        ></textarea>
      </div>

      <!-- Submit Button -->
      <div class="text-center pt-4">
        <button 
          type="submit" 
          class="w-full sm:w-auto px-12 py-4 bg-[#C59237] hover:bg-[#b0802c] active:scale-[0.99] text-white text-xs font-semibold uppercase tracking-[0.2em] transition-all rounded-xs shadow-lg shadow-amber-900/20"
        >
          Submit Event Inquiry
        </button>
      </div>

    </form>
  </div>
</section>

  </main>
</template>

<script setup>
import { ref } from 'vue'

const venues = [
  {
    title: 'VIP Royal Lounge',
    capacity: '20',
    description: 'An intimate private room with a hand-carved mahogany table and dedicated butler service.',
    bestFor: 'Executive meetings and family gatherings',
    image: 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80'
  },
  {
    title: 'Courtyard Terrace',
    capacity: '45',
    description: 'An open-air garden terrace with lush greenery and ambient lighting for relaxed receptions.',
    bestFor: 'Anniversaries and social receptions',
    image: 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=800&q=80'
  },
  {
    title: 'Grand Dining Hall',
    capacity: '120',
    description: 'A full restaurant buyout with exclusive access to the dining room, bar, and chef counter.',
    bestFor: 'Corporate galas and weddings',
    image: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80'
  }
]

const benefits = [
  'Custom tasting menus and dietary accommodations',
  'Curated wine pairings by our head sommelier',
  'Integrated audio-visual setup for presentations',
  'Personalized floral arrangements and valet service'
]

const form = ref({
  name: '',
  email: '',
  phone: '',
  date: '',
  guests: 20,
  preferredSpace: 'VIP Royal Lounge',
  eventType: 'Corporate Dinner',
  notes: ''
})

const submitInquiry = () => {
  alert(`Thank you, ${form.value.name}! Your event inquiry has been submitted.`)
  form.value = {
    name: '',
    email: '',
    phone: '',
    date: '',
    guests: 20,
    preferredSpace: 'VIP Royal Lounge',
    eventType: 'Corporate Dinner',
    notes: ''
  }
}
</script>

<style scoped>
.service-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 3rem;
}

@media (min-width: 1024px) {
  .service-grid {
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: clamp(3rem, 7vw, 7rem);
  }
}
</style>