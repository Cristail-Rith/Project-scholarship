<template>
<!-- STREAMING_CHUNK:Configuring top announcement bar and brand header... -->
<!-- 1. TOP ANNOUNCEMENT BAR -->
<div class="relative z-10 bg-[#1C1917] text-stone-300 text-xs py-2.5 px-4 sm:px-6 hidden md:block border-b border-stone-800 font-sans">
  <div class="max-w-7xl mx-auto flex flex-wrap justify-between items-center gap-4 tracking-wide">
    <div class="flex items-center gap-6">
      <a href="tel:+85523123456" class="flex items-center gap-2 hover:text-[#C59237] transition-colors">
        <svg class="w-3.5 h-3.5 shrink-0 text-[#C59237]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
        <span>+855 23 123 456</span>
      </a>
      <a href="mailto:reservations@flavoria.com" class="flex items-center gap-2 hover:text-[#C59237] transition-colors">
        <svg class="w-3.5 h-3.5 shrink-0 text-[#C59237]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
        <span>reservations@flavoria.com</span>
      </a>
    </div>
    <div class="font-medium tracking-wider text-[#C59237]">Instant Online Confirmation & Seating Choice</div>
    <div class="flex items-center gap-4">
      <span class="text-[11px] uppercase tracking-widest text-stone-400 font-semibold">Follow Us:</span>
      <div class="flex gap-3">
        <a href="#" class="hover:text-[#C59237] transition-colors" aria-label="Facebook"><svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24"><path d="M9 8H6v4h3v12h5V12h3.642L18 8h-4V6.333C14 5.374 14.5 5 15.5 5H18V0h-3.808C10.592 0 9 1.583 9 4.615V8z"/></svg></a>
        <a href="#" class="hover:text-[#C59237] transition-colors" aria-label="Instagram"><svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg></a>
      </div>
    </div>
  </div>
</div>

<!-- STREAMING_CHUNK:Rendering navigation header with mobile drawer... -->
<!-- 2. MAIN NAVBAR -->
<Navbar/>

<!-- STREAMING_CHUNK:Creating reservation page hero banner... -->
<!-- 3. PAGE HERO BANNER -->
<section class="relative bg-stone-950 text-white py-16 sm:py-24 px-4 sm:px-6 overflow-hidden">
  <div class="absolute inset-0 bg-gradient-to-t from-stone-950 via-stone-950/70 to-stone-950/40 z-10"></div>
  <img src="https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?auto=format&fit=crop&w=1800&q=80" alt="FLAVORIA Dining Hall" class="absolute inset-0 w-full h-full object-cover opacity-35 filter brightness-90" />
  
  <div class="relative max-w-4xl mx-auto text-center space-y-4 z-20">
    <span class="text-xs sm:text-sm font-sans tracking-[0.35em] uppercase text-[#C59237] font-semibold flex items-center justify-center gap-2">
      <span class="w-8 h-[1px] bg-[#C59237]"></span>
      Online Table Reservation
      <span class="w-8 h-[1px] bg-[#C59237]"></span>
    </span>
    <h1 class="text-3xl sm:text-5xl md:text-6xl font-serif tracking-wide font-normal leading-tight text-stone-100">
      Book Your Fine Dining Experience
    </h1>
    <p class="font-sans text-stone-300 text-xs sm:text-sm md:text-base font-light max-w-xl mx-auto leading-relaxed">
      Reserve your seat in advance to experience our seasonal tasting menus, vintage wine pairings, and signature culinary creations.
    </p>
  </div>
</section>

<!-- STREAMING_CHUNK:Building interactive table booking form and step selector... -->
<!-- 4. INTERACTIVE RESERVATION WIZARD & LIVE PREVIEW -->
<section class="py-12 sm:py-16 max-w-7xl mx-auto px-4 sm:px-6">
  
  <!-- Stepper Navigation -->
  <div class="max-w-3xl mx-auto mb-10 font-sans">
    <div class="flex items-center justify-between relative">
      <div class="absolute left-0 top-1/2 -translate-y-1/2 w-full h-[2px] bg-stone-200 z-0"></div>
      <div class="absolute left-0 top-1/2 -translate-y-1/2 h-[2px] bg-[#C59237] transition-all duration-500 z-0" :style="{ width: ((currentStep - 1) / 2) * 100 + '%' }"></div>

      <div
        v-for="step in 3"
        :key="step"
        class="relative z-10 flex flex-col items-center cursor-pointer"
        @click="goToStep(step)"
      >
        <div
          :class="[
            'w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-300',
            currentStep >= step ? 'bg-[#C59237] text-white shadow-md' : 'bg-stone-200 text-stone-500'
          ]"
        >
          {{ step }}
        </div>
        <span class="text-[11px] font-semibold tracking-wider uppercase mt-2 hidden sm:block" :class="currentStep >= step ? 'text-stone-900' : 'text-stone-400'">
          {{ step === 1 ? 'Date & Party' : step === 2 ? 'Seating & Occasion' : 'Contact Details' }}
        </span>
      </div>
    </div>
  </div>

  <!-- Reservation Container Grid -->
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
    
    <!-- Left: Reservation Form (Steps) -->
    <div class="lg:col-span-7 bg-white p-6 sm:p-10 rounded-xl border border-stone-200/90 shadow-sm">
      
      <!-- SUCCESS CONFIRMATION STATE -->
      <div v-if="bookingConfirmed" class="text-center py-8 space-y-5 font-sans">
        <div class="w-16 h-16 bg-amber-100 text-[#C59237] rounded-full flex items-center justify-center mx-auto text-2xl font-bold">
          ✓
        </div>
        <h2 class="font-serif text-2xl sm:text-3xl text-stone-900">Reservation Confirmed!</h2>
        <p class="text-stone-600 text-xs sm:text-sm max-w-md mx-auto leading-relaxed">
          Thank you, <strong class="text-stone-900">{{ form.firstName }} {{ form.lastName }}</strong>. We look forward to welcoming you to FLAVORIA. A confirmation email has been dispatched to <strong>{{ form.email }}</strong>.
        </p>
        
        <div class="bg-[#FAF8F5] border border-stone-200 rounded-lg p-5 text-left text-xs space-y-2 max-w-md mx-auto">
          <div class="flex justify-between"><span class="text-stone-500">Booking Ref:</span> <span class="font-bold text-[#C59237]">{{ reservationCode }}</span></div>
          <div class="flex justify-between"><span class="text-stone-500">Date & Time:</span> <span class="font-semibold text-stone-800">{{ form.date }} @ {{ form.time }}</span></div>
          <div class="flex justify-between"><span class="text-stone-500">Party Size:</span> <span class="font-semibold text-stone-800">{{ form.guests }} Guests</span></div>
          <div class="flex justify-between"><span class="text-stone-500">Seating Area:</span> <span class="font-semibold text-stone-800">{{ selectedArea.name }}</span></div>
        </div>

        <div class="pt-4 flex justify-center gap-4">
          <button @click="resetForm" class="px-6 py-3 bg-[#C59237] hover:bg-amber-600 text-white text-xs font-semibold uppercase tracking-wider rounded transition-colors">
            Book Another Table
          </button>
          <NuxtLink to="/menu" class="px-6 py-3 border border-stone-300 hover:bg-stone-100 text-stone-800 text-xs font-semibold uppercase tracking-wider rounded transition-colors">
            View Menu
          </NuxtLink>
        </div>
      </div>

      <!-- FORM STEP 1: PARTY SIZE, DATE, & TIME -->
      <form v-else-if="currentStep === 1" @submit.prevent="nextStep" class="space-y-6 font-sans">
        <div>
          <span class="text-[11px] uppercase tracking-widest text-[#C59237] font-semibold block mb-1">Step 1 of 3</span>
          <h2 class="font-serif text-2xl text-stone-900">Select Date & Guest Count</h2>
        </div>

        <!-- Party Size Selector -->
        <div>
          <label class="block text-stone-700 text-xs font-semibold uppercase tracking-wider mb-2">Number of Guests</label>
          <div class="grid grid-cols-4 sm:grid-cols-6 gap-2">
            <button
              v-for="count in [1, 2, 3, 4, 5, 6, 7, 8]"
              :key="count"
              type="button"
              @click="form.guests = count"
              :class="[
                'py-2.5 text-xs font-bold rounded-md border transition-all',
                form.guests === count ? 'bg-[#C59237] text-white border-[#C59237] shadow-sm' : 'bg-[#FAF8F5] text-stone-700 border-stone-200 hover:border-amber-400'
              ]"
            >
              {{ count }} {{ count === 1 ? 'Guest' : 'Guests' }}
            </button>
          </div>
        </div>

        <!-- Date Picker -->
        <div>
          <label class="block text-stone-700 text-xs font-semibold uppercase tracking-wider mb-2">Reservation Date</label>
          <input
            v-model="form.date"
            type="date"
            :min="todayDate"
            class="w-full bg-[#FAF8F5] border border-stone-300 rounded-md px-4 py-3 text-xs text-stone-800 focus:outline-none focus:border-[#C59237] transition-colors"
            required
          />
        </div>

        <!-- Time Slots -->
        <div>
          <label class="block text-stone-700 text-xs font-semibold uppercase tracking-wider mb-2">Available Dining Slots</label>
          
          <!-- Meal Period Tabs -->
          <div class="flex gap-4 border-b border-stone-200 pb-2 mb-3 text-xs font-semibold">
            <button type="button" @click="activePeriod = 'lunch'" :class="activePeriod === 'lunch' ? 'text-[#C59237] border-b-2 border-[#C59237] pb-1' : 'text-stone-400'">Lunch Service</button>
            <button type="button" @click="activePeriod = 'dinner'" :class="activePeriod === 'dinner' ? 'text-[#C59237] border-b-2 border-[#C59237] pb-1' : 'text-stone-400'">Dinner Service</button>
          </div>

          <div class="grid grid-cols-3 sm:grid-cols-4 gap-2">
            <button
              v-for="time in currentPeriodSlots"
              :key="time"
              type="button"
              @click="form.time = time"
              :class="[
                'py-2.5 text-xs font-medium rounded-md border transition-all',
                form.time === time ? 'bg-[#C59237] text-white border-[#C59237] font-bold shadow-sm' : 'bg-[#FAF8F5] text-stone-700 border-stone-200 hover:border-amber-400'
              ]"
            >
              {{ time }}
            </button>
          </div>
        </div>

        <div class="pt-4 flex justify-end">
          <button type="submit" class="px-8 py-3.5 bg-[#C59237] hover:bg-amber-600 text-white text-xs font-semibold uppercase tracking-widest rounded transition-colors shadow-md">
            Continue to Seating →
          </button>
        </div>
      </form>

      <!-- STREAMING_CHUNK:Configuring seating area selection cards... -->
      <!-- FORM STEP 2: SEATING AREA & OCCASION -->
      <form v-else-if="currentStep === 2" @submit.prevent="nextStep" class="space-y-6 font-sans">
        <div>
          <span class="text-[11px] uppercase tracking-widest text-[#C59237] font-semibold block mb-1">Step 2 of 3</span>
          <h2 class="font-serif text-2xl text-stone-900">Choose Atmosphere & Occasion</h2>
        </div>

        <!-- Seating Area Selection Cards -->
        <div>
          <label class="block text-stone-700 text-xs font-semibold uppercase tracking-wider mb-2">Dining Atmosphere</label>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div
              v-for="area in diningAreas"
              :key="area.id"
              @click="form.areaId = area.id"
              :class="[
                'p-4 rounded-lg border cursor-pointer transition-all flex flex-col justify-between',
                form.areaId === area.id ? 'border-[#C59237] bg-amber-50/40 ring-1 ring-[#C59237]' : 'border-stone-200 bg-[#FAF8F5] hover:border-stone-300'
              ]"
            >
              <div>
                <div class="flex justify-between items-center mb-1">
                  <h3 class="font-serif font-semibold text-sm text-stone-900">{{ area.name }}</h3>
                  <span v-if="form.areaId === area.id" class="text-[#C59237] text-xs font-bold">Selected</span>
                </div>
                <p class="text-[11px] text-stone-500 leading-relaxed">{{ area.description }}</p>
              </div>
              <span class="text-[10px] uppercase tracking-wider text-amber-800 font-semibold mt-3 block">{{ area.tag }}</span>
            </div>
          </div>
        </div>

        <!-- Special Occasion Picker -->
        <div>
          <label class="block text-stone-700 text-xs font-semibold uppercase tracking-wider mb-2">Special Occasion (Optional)</label>
          <select v-model="form.occasion" class="w-full bg-[#FAF8F5] border border-stone-300 rounded-md px-4 py-3 text-xs text-stone-800 focus:outline-none focus:border-[#C59237] transition-colors">
            <option value="Casual Fine Dining">Casual Fine Dining</option>
            <option value="Birthday Celebration">Birthday Celebration</option>
            <option value="Anniversary">Anniversary</option>
            <option value="Business Dinner">Business Dinner</option>
            <option value="Romantic Date Night">Romantic Date Night</option>
          </select>
        </div>

        <div class="pt-4 flex justify-between items-center">
          <button type="button" @click="currentStep = 1" class="text-xs text-stone-500 hover:text-stone-800 underline font-medium">
            ← Back
          </button>
          <button type="submit" class="px-8 py-3.5 bg-[#C59237] hover:bg-amber-600 text-white text-xs font-semibold uppercase tracking-widest rounded transition-colors shadow-md">
            Continue to Guest Details →
          </button>
        </div>
      </form>

      <!-- STREAMING_CHUNK:Setting up guest detail inputs and dietary preferences... -->
      <!-- FORM STEP 3: CONTACT & DIETARY REQUESTS -->
      <form v-else-if="currentStep === 3" @submit.prevent="submitReservation" class="space-y-5 font-sans">
        <div>
          <span class="text-[11px] uppercase tracking-widest text-[#C59237] font-semibold block mb-1">Step 3 of 3</span>
          <h2 class="font-serif text-2xl text-stone-900">Guest & Contact Information</h2>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-stone-700 text-xs font-semibold uppercase tracking-wider mb-1">First Name *</label>
            <input v-model="form.firstName" type="text" placeholder="John" required class="w-full bg-[#FAF8F5] border border-stone-300 rounded px-3.5 py-2.5 text-xs text-stone-800 focus:outline-none focus:border-[#C59237]" />
          </div>
          <div>
            <label class="block text-stone-700 text-xs font-semibold uppercase tracking-wider mb-1">Last Name *</label>
            <input v-model="form.lastName" type="text" placeholder="Doe" required class="w-full bg-[#FAF8F5] border border-stone-300 rounded px-3.5 py-2.5 text-xs text-stone-800 focus:outline-none focus:border-[#C59237]" />
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-stone-700 text-xs font-semibold uppercase tracking-wider mb-1">Email Address *</label>
            <input v-model="form.email" type="email" placeholder="john@example.com" required class="w-full bg-[#FAF8F5] border border-stone-300 rounded px-3.5 py-2.5 text-xs text-stone-800 focus:outline-none focus:border-[#C59237]" />
          </div>
          <div>
            <label class="block text-stone-700 text-xs font-semibold uppercase tracking-wider mb-1">Phone Number *</label>
            <input v-model="form.phone" type="tel" placeholder="+855 12 345 678" required class="w-full bg-[#FAF8F5] border border-stone-300 rounded px-3.5 py-2.5 text-xs text-stone-800 focus:outline-none focus:border-[#C59237]" />
          </div>
        </div>

        <!-- Dietary Checklist -->
        <div>
          <label class="block text-stone-700 text-xs font-semibold uppercase tracking-wider mb-2">Dietary Restrictions & Preferences</label>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
            <label v-for="diet in dietaryOptions" :key="diet" class="flex items-center gap-2 text-xs text-stone-600 bg-[#FAF8F5] border border-stone-200 p-2 rounded cursor-pointer hover:bg-stone-100">
              <input type="checkbox" :value="diet" v-model="form.dietary" class="accent-[#C59237]" />
              <span>{{ diet }}</span>
            </label>
          </div>
        </div>

        <div>
          <label class="block text-stone-700 text-xs font-semibold uppercase tracking-wider mb-1">Special Notes / Seating Request</label>
          <textarea v-model="form.notes" rows="3" placeholder="High chair needed, quiet table, flower arrangement request..." class="w-full bg-[#FAF8F5] border border-stone-300 rounded px-3.5 py-2.5 text-xs text-stone-800 focus:outline-none focus:border-[#C59237] resize-y"></textarea>
        </div>

        <div class="pt-4 flex justify-between items-center">
          <button type="button" @click="currentStep = 2" class="text-xs text-stone-500 hover:text-stone-800 underline font-medium">
            ← Back
          </button>
          <button type="submit" class="px-8 py-3.5 bg-[#C59237] hover:bg-amber-600 text-white text-xs font-semibold uppercase tracking-widest rounded transition-colors shadow-md">
            Confirm Reservation
          </button>
        </div>
      </form>

    </div>

    <!-- STREAMING_CHUNK:Creating dynamic reservation summary card... -->
    <!-- Right: Live Booking Summary Card -->
    <div class="lg:col-span-5 bg-[#1C1917] text-stone-200 p-6 sm:p-8 rounded-xl shadow-xl border border-stone-800 sticky top-28 font-sans space-y-6">
      <div class="border-b border-stone-800 pb-4">
        <span class="text-[10px] font-bold tracking-[0.3em] uppercase text-[#C59237]">Live Overview</span>
        <h3 class="font-serif text-2xl text-stone-100 mt-1">Reservation Summary</h3>
      </div>

      <div class="space-y-4 text-xs font-light">
        <div class="flex justify-between items-center py-2 border-b border-stone-800/60">
          <span class="text-stone-400">Date:</span>
          <span class="font-semibold text-stone-100">{{ form.date || 'Not selected' }}</span>
        </div>

        <div class="flex justify-between items-center py-2 border-b border-stone-800/60">
          <span class="text-stone-400">Time Slot:</span>
          <span class="font-semibold text-[#C59237]">{{ form.time }}</span>
        </div>

        <div class="flex justify-between items-center py-2 border-b border-stone-800/60">
          <span class="text-stone-400">Party Size:</span>
          <span class="font-semibold text-stone-100">{{ form.guests }} {{ form.guests === 1 ? 'Guest' : 'Guests' }}</span>
        </div>

        <div class="flex justify-between items-center py-2 border-b border-stone-800/60">
          <span class="text-stone-400">Atmosphere:</span>
          <span class="font-semibold text-stone-100">{{ selectedArea.name }}</span>
        </div>

        <div class="flex justify-between items-center py-2 border-b border-stone-800/60">
          <span class="text-stone-400">Occasion:</span>
          <span class="font-semibold text-stone-100">{{ form.occasion }}</span>
        </div>

        <div v-if="form.dietary.length > 0" class="py-2 border-b border-stone-800/60">
          <span class="text-stone-400 block mb-1">Dietary Preferences:</span>
          <div class="flex flex-wrap gap-1">
            <span v-for="d in form.dietary" :key="d" class="bg-stone-800 text-stone-300 text-[10px] px-2 py-0.5 rounded">
              {{ d }}
            </span>
          </div>
        </div>
      </div>

      <!-- Guarantee Badge -->
      <div class="bg-[#26221F] p-4 rounded-lg border border-stone-800 flex items-start gap-3 text-xs text-stone-400 font-light">
        <svg class="w-5 h-5 text-[#C59237] shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
        </svg>
        <div>
          <strong class="block text-stone-200 font-semibold mb-0.5">Instant Booking Guarantee</strong>
          <span>No deposit required for standard tables up to 6 guests. Instant SMS & email notification.</span>
        </div>
      </div>
    </div>

  </div>
</section>

<!-- 5. PRIVATE DINING CALLOUT BANNER -->
<section class="bg-[#1C1917] text-white py-14 px-6 relative overflow-hidden my-8">
  <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative z-10">
    <div class="lg:col-span-8 space-y-3">
      <span class="text-xs font-sans tracking-[0.3em] uppercase text-[#C59237] font-semibold">Banquets & Celebrations</span>
      <h2 class="text-2xl sm:text-4xl font-serif">Planning a Larger Group or Private Event?</h2>
      <p class="font-sans text-stone-300 text-xs sm:text-sm font-light max-w-2xl leading-relaxed">
        For parties of 10 or more guests, customized multi-course tasting menus, or full restaurant buyouts, our dedicated events team is at your service.
      </p>
    </div>
    <div class="lg:col-span-4 flex lg:justify-end">
      <a href="mailto:events@flavoria.com" class="px-8 py-4 bg-[#C59237] hover:bg-amber-600 text-white font-sans text-xs font-semibold uppercase tracking-widest rounded-sm shadow-lg transition-colors">
        Inquire For Private Events
      </a>
    </div>
  </div>
</section>

<!-- STREAMING_CHUNK:Rendering dining policies and FAQ section... -->
<!-- 6. RESERVATION POLICIES & FAQ SECTION -->
<section class="py-12 sm:py-16 max-w-7xl mx-auto px-4 sm:px-6 font-sans">
  <div class="text-center mb-10">
    <h2 class="text-2xl md:text-3xl font-serif text-stone-900 tracking-wider uppercase font-normal">
      Reservation Policies
    </h2>
    <div class="flex items-center justify-center gap-3 mt-3 text-[#C59237]">
      <span class="w-10 h-[1px] bg-amber-600/40"></span>
      <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M5 16L3 5l5.5 5L12 4l3.5 6L21 5l-2 11H5zm14 3c0 .6-.4 1-1 1H6c-.6 0-1-.4-1-1v-1h14v1z"/></svg>
      <span class="w-10 h-[1px] bg-amber-600/40"></span>
    </div>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
    <div class="bg-white p-6 rounded-lg border border-stone-200/80 shadow-sm space-y-2">
      <div class="text-[#C59237] font-bold text-lg font-serif">01. Dress Code</div>
      <h3 class="font-serif text-stone-900 font-semibold text-sm">Smart Casual Elegance</h3>
      <p class="text-xs text-stone-500 font-light leading-relaxed">
        We kindly ask guests to refrain from beachwear, athletic shorts, and flip-flops to preserve the refined atmosphere.
      </p>
    </div>

    <div class="bg-white p-6 rounded-lg border border-stone-200/80 shadow-sm space-y-2">
      <div class="text-[#C59237] font-bold text-lg font-serif">02. Grace Period</div>
      <h3 class="font-serif text-stone-900 font-semibold text-sm">15-Minute Seating Hold</h3>
      <p class="text-xs text-stone-500 font-light leading-relaxed">
        Tables will be held for up to 15 minutes past your reserved time before being released to our walk-in waitlist.
      </p>
    </div>

    <div class="bg-white p-6 rounded-lg border border-stone-200/80 shadow-sm space-y-2">
      <div class="text-[#C59237] font-bold text-lg font-serif">03. Cancellations</div>
      <h3 class="font-serif text-stone-900 font-semibold text-sm">Flexibility & Notice</h3>
      <p class="text-xs text-stone-500 font-light leading-relaxed">
        Kindly notify us at least 6 hours in advance for cancellations or headcount changes so we can accommodate others.
      </p>
    </div>

    <div class="bg-white p-6 rounded-lg border border-stone-200/80 shadow-sm space-y-2">
      <div class="text-[#C59237] font-bold text-lg font-serif">04. Valet & Parking</div>
      <h3 class="font-serif text-stone-900 font-semibold text-sm">Complimentary Valet</h3>
      <p class="text-xs text-stone-500 font-light leading-relaxed">
        Complimentary valet parking is available at the main entrance for all dining guests upon arrival.
      </p>
    </div>
  </div>
</section>

<!-- STREAMING_CHUNK:Building footer and copyright notice... -->
<!-- 7. FOOTER COMPONENT -->
<footer class="bg-[#141210] text-stone-300 font-serif pt-12 sm:pt-16 pb-8 border-t border-amber-900/30">
  <div class="max-w-7xl mx-auto px-4 sm:px-6">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 md:gap-10 pb-10 border-b border-stone-800 font-sans">
      
      <div class="space-y-3 font-serif">
        <div class="flex flex-col items-start group">
          <svg class="w-7 h-5 text-[#C59237] mb-1" fill="currentColor" viewBox="0 0 24 24"><path d="M5 16L3 5l5.5 5L12 4l3.5 6L21 5l-2 11H5zm14 3c0 .6-.4 1-1 1H6c-.6 0-1-.4-1-1v-1h14v1z"/></svg>
          <span class="font-serif text-2xl font-normal tracking-[0.25em] text-white">FLAVORIA</span>
          <span class="text-[9px] tracking-[0.35em] text-[#C59237] uppercase font-sans mt-0.5">Fine Dining</span>
        </div>
        <p class="font-sans text-xs text-stone-400 leading-relaxed font-light">Crafting extraordinary culinary moments through classic techniques, local flavors, and refined hospitality.</p>
      </div>

      <div>
        <h3 class="font-serif text-sm sm:text-base text-white tracking-widest uppercase mb-4 relative pb-2 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-8 after:h-[1px] after:bg-[#C59237]">Navigation</h3>
        <ul class="space-y-2.5 text-xs text-stone-400">
          <li><NuxtLink to="/menu" class="hover:text-amber-400 transition-colors">Our Menu</NuxtLink></li>
          <li><NuxtLink to="/reservation" class="hover:text-amber-400 transition-colors">Book a Table</NuxtLink></li>
          <li><NuxtLink to="/about" class="hover:text-amber-400 transition-colors">About Us</NuxtLink></li>
          <li><NuxtLink to="/contact" class="hover:text-amber-400 transition-colors">Contact Us</NuxtLink></li>
        </ul>
      </div>

      <div>
        <h3 class="font-serif text-sm sm:text-base text-white tracking-widest uppercase mb-4 relative pb-2 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-8 after:h-[1px] after:bg-[#C59237]">Opening Hours</h3>
        <ul class="space-y-2 text-xs text-stone-400">
          <li class="flex justify-between border-b border-stone-800/80 pb-1.5"><span>Mon - Thu:</span> <span class="text-stone-200">11:00 AM - 10:00 PM</span></li>
          <li class="flex justify-between border-b border-stone-800/80 pb-1.5"><span>Fri - Sat:</span> <span class="text-stone-200">11:00 AM - 11:00 PM</span></li>
          <li class="flex justify-between pb-1"><span>Sunday:</span> <span class="text-stone-200">10:00 AM - 9:30 PM</span></li>
        </ul>
      </div>

      <div class="space-y-3">
        <h3 class="font-serif text-sm sm:text-base text-white tracking-widest uppercase relative pb-2 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-8 after:h-[1px] after:bg-[#C59237]">Newsletter</h3>
        <p class="text-xs text-stone-400 font-light">Subscribe to receive exclusive tasting menu invitations.</p>
        <form @submit.prevent class="flex items-center">
          <input type="email" placeholder="Your Email Address" class="bg-stone-900 border border-stone-700 text-xs px-3 py-2.5 w-full text-stone-200 focus:outline-none focus:border-[#C59237]" />
          <button type="submit" class="bg-[#C59237] hover:bg-amber-600 text-white px-3.5 py-2.5 text-xs font-semibold uppercase tracking-wider transition-colors shrink-0">Join</button>
        </form>
      </div>

    </div>

    <div class="pt-6 flex flex-col sm:flex-row items-center justify-between font-sans text-xs text-stone-500 gap-3">
      <p>© 2026 FLAVORIA Fine Dining. All Rights Reserved.</p>
      <div class="flex items-center gap-6">
        <a href="#" class="hover:text-amber-400 transition-colors">Privacy Policy</a>
        <a href="#" class="hover:text-amber-400 transition-colors">Terms of Service</a>
      </div>
    </div>
  </div>
</footer>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'

const mobileMenuOpen = ref(false)
const currentStep = ref(1)
const bookingConfirmed = ref(false)
const reservationCode = ref('')
const activePeriod = ref('dinner')

const form = reactive({
  guests: 2,
  date: '',
  time: '7:00 PM',
  areaId: 1,
  occasion: 'Casual Fine Dining',
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  dietary: [],
  notes: '',
})

const todayDate = new Date().toISOString().split('T')[0]

const periodSlots = {
  lunch: ['11:30 AM', '12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM'],
  dinner: ['5:30 PM', '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM', '8:00 PM', '8:30 PM'],
}

const currentPeriodSlots = computed(() => periodSlots[activePeriod.value])

const diningAreas = [
  { id: 1, name: 'Main Dining Room', description: 'Our signature setting for an elegant evening.', tag: 'Classic atmosphere' },
  { id: 2, name: 'Garden Terrace', description: 'An open-air table surrounded by quiet greenery.', tag: 'Al fresco dining' },
  { id: 3, name: 'Chef\'s Counter', description: 'A front-row seat to the rhythm of our kitchen.', tag: 'Interactive experience' },
  { id: 4, name: 'Private Dining', description: 'A secluded setting for celebrations and milestones.', tag: 'By request' },
]

const dietaryOptions = ['Vegetarian', 'Vegan', 'Gluten-free', 'Nut allergy', 'Dairy-free', 'No seafood']

const selectedArea = computed(() =>
  diningAreas.find((area) => area.id === form.areaId) || diningAreas[0],
)

const goToStep = (step) => {
  if (step <= currentStep.value) currentStep.value = step
}

const nextStep = () => {
  if (currentStep.value < 3) currentStep.value += 1
}

const submitReservation = () => {
  reservationCode.value = `FLV-${Date.now().toString().slice(-6)}`
  bookingConfirmed.value = true
}

const resetForm = () => {
  bookingConfirmed.value = false
  reservationCode.value = ''
  currentStep.value = 1
  form.firstName = ''
  form.lastName = ''
  form.email = ''
  form.phone = ''
  form.dietary = []
  form.notes = ''
}
</script>
