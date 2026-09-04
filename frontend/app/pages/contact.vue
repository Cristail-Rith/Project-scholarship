```vue
<template>
  <div
    class="min-h-screen bg-[#F8F5EF] text-[#25211D] selection:bg-[#C59237] selection:text-white"
  >
    <!-- =========================================================
         ANNOUNCEMENT BAR
    ========================================================== -->
    <div
      class="hidden md:block bg-[#191714] text-[#D8D0C4] border-b border-white/10"
    >
      <div
        class="max-w-[1400px] mx-auto px-8 py-2.5 flex items-center justify-between font-sans text-[10px] uppercase tracking-[0.22em]"
      >
        <div class="flex items-center gap-8">
          <a
            href="tel:+12345678900"
            class="flex items-center gap-2.5 hover:text-[#D5A64C] transition-colors"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.6"
                d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
              />
            </svg>
            +1 234 567 8900
          </a>

          <a
            href="mailto:hello@flavoria.com"
            class="flex items-center gap-2.5 hover:text-[#D5A64C] transition-colors"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.6"
                d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
              />
            </svg>
            hello@flavoria.com
          </a>
        </div>

        <div class="text-[#D5A64C]">
          Complimentary delivery on orders above $50
        </div>

        <div class="flex items-center gap-4">
          <span class="text-[#81786D]">Follow</span>

          <div class="flex gap-3">
            <a href="#" aria-label="Facebook" class="hover:text-[#D5A64C] transition-colors">
              <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24">
                <path d="M9 8H6v4h3v12h5V12h3.642L18 8h-4V6.333C14 5.374 14.5 5 15.5 5H18V0h-3.808C10.592 0 9 1.583 9 4.615V8z"/>
              </svg>
            </a>

            <a href="#" aria-label="Instagram" class="hover:text-[#D5A64C] transition-colors">
              <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24">
                <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.07 4.849-.07zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.79 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- =========================================================
         NAVIGATION
    ========================================================== -->
    <header
      class="sticky top-0 z-50 bg-[#F8F5EF]/95 backdrop-blur-xl border-b border-[#29251F]/10"
    >
      <nav class="max-w-[1400px] mx-auto px-6 lg:px-10 h-[82px] flex items-center justify-between">
        <!-- Mobile menu -->
        <button
          @click="mobileMenuOpen = !mobileMenuOpen"
          class="lg:hidden w-10 h-10 flex items-center justify-center rounded-full border border-[#29251F]/10 hover:border-[#C59237] transition-colors"
          aria-label="Toggle Menu"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M4 7h16M4 12h16M4 17h16"
            />
          </svg>
        </button>

        <!-- Left navigation -->
        <div
          class="hidden lg:flex items-center gap-9 font-sans text-[10px] font-semibold tracking-[0.24em] text-[#514A42] uppercase"
        >
          <NuxtLink to="/" class="nav-link">Home</NuxtLink>
          <NuxtLink to="/menu" class="nav-link">Menu</NuxtLink>
          <NuxtLink to="/about" class="nav-link">About</NuxtLink>
        </div>

        <!-- Logo -->
        <NuxtLink
          to="/"
          class="absolute left-1/2 -translate-x-1/2 flex flex-col items-center group"
        >
          <div
            class="w-9 h-9 rounded-full border border-[#C59237]/60 flex items-center justify-center mb-1.5 group-hover:border-[#C59237] group-hover:rotate-45 transition-all duration-500"
          >
            <svg
              class="w-4 h-4 text-[#C59237] group-hover:-rotate-45 transition-transform duration-500"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M5 16L3 5l5.5 5L12 4l3.5 6L21 5l-2 11H5zm14 3c0 .6-.4 1-1 1H6c-.6 0-1-.4-1-1v-1h14v1z"/>
            </svg>
          </div>

          <span class="font-serif text-[22px] md:text-[25px] tracking-[0.28em] text-[#201D19] leading-none">
            FLAVORIA
          </span>

          <span class="text-[7px] md:text-[8px] tracking-[0.42em] text-[#A27B38] uppercase font-sans mt-2">
            Fine Dining
          </span>
        </NuxtLink>

        <!-- Right navigation -->
        <div class="flex items-center gap-5 lg:gap-9 ml-auto">
          <div
            class="hidden lg:flex items-center gap-9 font-sans text-[10px] font-semibold tracking-[0.24em] text-[#514A42] uppercase"
          >
            <NuxtLink to="/reservation" class="nav-link">Reservation</NuxtLink>
            <NuxtLink to="/contact" class="nav-link active-link">Contact</NuxtLink>
          </div>

          <div class="flex items-center gap-3">
            <button
              class="nav-icon"
              aria-label="Search"
            >
              <svg class="w-[18px] h-[18px]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.6"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </button>

            <NuxtLink
              to="/login"
              class="nav-icon"
              aria-label="Account"
            >
              <svg class="w-[18px] h-[18px]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.6"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                />
              </svg>
            </NuxtLink>
          </div>
        </div>
      </nav>

      <!-- Mobile navigation -->
      <transition name="mobile-menu">
        <div
          v-if="mobileMenuOpen"
          class="lg:hidden border-t border-[#29251F]/10 bg-[#F8F5EF] px-6 py-6"
        >
          <div class="flex flex-col gap-5 font-sans text-[11px] font-semibold tracking-[0.25em] uppercase">
            <NuxtLink @click="mobileMenuOpen = false" to="/" class="mobile-nav-link">Home</NuxtLink>
            <NuxtLink @click="mobileMenuOpen = false" to="/menu" class="mobile-nav-link">Menu</NuxtLink>
            <NuxtLink @click="mobileMenuOpen = false" to="/about" class="mobile-nav-link">About</NuxtLink>
            <NuxtLink @click="mobileMenuOpen = false" to="/reservation" class="mobile-nav-link">Reservation</NuxtLink>
            <NuxtLink @click="mobileMenuOpen = false" to="/contact" class="mobile-nav-link active-mobile">Contact</NuxtLink>
          </div>
        </div>
      </transition>
    </header>

    <!-- =========================================================
         HERO
    ========================================================== -->
    <section class="relative min-h-[470px] md:min-h-[560px] overflow-hidden bg-[#171512]">
      <img
        src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=2000&q=85"
        alt="Flavoria restaurant interior"
        class="absolute inset-0 w-full h-full object-cover scale-105"
      />

      <div class="absolute inset-0 bg-[#100E0C]/65"></div>
      <div class="absolute inset-0 bg-gradient-to-b from-black/30 via-transparent to-black/70"></div>

      <!-- Decorative frame -->
      <div class="absolute inset-5 md:inset-8 border border-white/15 pointer-events-none"></div>

      <div
        class="relative z-10 min-h-[470px] md:min-h-[560px] flex items-center justify-center px-6"
      >
        <div class="text-center text-white max-w-3xl">
          <div class="flex items-center justify-center gap-4 mb-7">
            <span class="h-px w-10 bg-[#C59237]"></span>
            <span class="font-sans text-[10px] uppercase tracking-[0.38em] text-[#D5A64C] font-semibold">
              Get In Touch
            </span>
            <span class="h-px w-10 bg-[#C59237]"></span>
          </div>

          <h1
            class="font-serif font-normal text-5xl sm:text-6xl md:text-7xl leading-[0.95] tracking-tight"
          >
            Contact Us
            <span class="block italic text-[#D9CBB7] mt-2">
              & Reservations
            </span>
          </h1>

          <p class="max-w-xl mx-auto mt-7 text-sm md:text-base text-white/65 font-sans font-light leading-relaxed">
            Join us for an evening of thoughtful cuisine, intimate hospitality,
            and unforgettable moments.
          </p>

          <div class="flex items-center justify-center gap-3 mt-8 font-sans text-[9px] uppercase tracking-[0.25em]">
            <NuxtLink to="/" class="text-white/55 hover:text-white transition-colors">
              Home
            </NuxtLink>
            <span class="text-[#C59237]">•</span>
            <span class="text-[#D5A64C]">Contact</span>
          </div>
        </div>
      </div>
    </section>

    <!-- =========================================================
         CONTACT CARDS
    ========================================================== -->
    <section class="relative py-20 md:py-24 px-6">
      <div class="max-w-[1200px] mx-auto">
        <div class="text-center mb-12">
          <span class="section-kicker">At Your Service</span>
          <h2 class="section-title mt-3">Let us take care of the details</h2>
          <div class="gold-line mx-auto mt-5"></div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <!-- Reservation -->
          <div class="contact-card group">
            <div class="card-number">01</div>

            <div class="icon-circle">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.6"
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
            </div>

            <h3 class="font-serif text-2xl text-[#28231E]">
              Table Reservation
            </h3>

            <p class="card-copy">
              Secure your table online or speak directly with our hospitality team.
            </p>

            <a href="tel:+12345678900" class="gold-link">
              +1 234 567 8900
              <span>→</span>
            </a>
          </div>

          <!-- General -->
          <div class="contact-card group">
            <div class="card-number">02</div>

            <div class="icon-circle">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.6"
                  d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                />
              </svg>
            </div>

            <h3 class="font-serif text-2xl text-[#28231E]">
              General Inquiries
            </h3>

            <p class="card-copy">
              Questions about our menu, dietary needs, celebrations, or feedback?
            </p>

            <a href="mailto:hello@flavoria.com" class="gold-link">
              hello@flavoria.com
              <span>→</span>
            </a>
          </div>

          <!-- Events -->
          <div class="contact-card group">
            <div class="card-number">03</div>

            <div class="icon-circle">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.6"
                  d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                />
              </svg>
            </div>

            <h3 class="font-serif text-2xl text-[#28231E]">
              Private Events
            </h3>

            <p class="card-copy">
              From intimate dinners to weddings and corporate celebrations.
            </p>

            <a href="mailto:events@flavoria.com" class="gold-link">
              events@flavoria.com
              <span>→</span>
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- =========================================================
         FORM + LOCATION
    ========================================================== -->
    <section class="bg-[#211E1A] text-white py-20 md:py-28 px-6 relative overflow-hidden">
      <!-- Decorative background -->
      <div class="absolute top-0 right-0 w-[500px] h-[500px] rounded-full border border-white/5 translate-x-1/2 -translate-y-1/2"></div>
      <div class="absolute bottom-0 left-0 w-[350px] h-[350px] rounded-full border border-[#C59237]/10 -translate-x-1/2 translate-y-1/2"></div>

      <div class="relative max-w-[1250px] mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16">
          <!-- FORM -->
          <div class="lg:col-span-7">
            <div class="mb-10">
              <span class="section-kicker text-[#D5A64C]">
                Send A Message
              </span>

              <h2 class="font-serif text-4xl md:text-5xl font-normal mt-3 leading-tight">
                Reserve a table
                <span class="block italic text-[#D5C7B3]">
                  or tell us how we can help.
                </span>
              </h2>

              <p class="mt-5 max-w-xl text-sm text-white/50 font-sans leading-relaxed">
                Complete the form below and our team will be in touch shortly.
                For immediate reservation assistance, please call us directly.
              </p>
            </div>

            <form
              @submit.prevent="submitContactForm"
              class="space-y-7 font-sans"
            >
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-7">
                <div class="field-group">
                  <label class="field-label">
                    Your Name <span>*</span>
                  </label>
                  <input
                    v-model="form.name"
                    type="text"
                    placeholder="John Doe"
                    class="dark-input"
                    required
                  />
                </div>

                <div class="field-group">
                  <label class="field-label">
                    Email Address <span>*</span>
                  </label>
                  <input
                    v-model="form.email"
                    type="email"
                    placeholder="john@example.com"
                    class="dark-input"
                    required
                  />
                </div>

                <div class="field-group">
                  <label class="field-label">
                    Phone <span>*</span>
                  </label>
                  <input
                    v-model="form.phone"
                    type="tel"
                    placeholder="+1 234 567 890"
                    class="dark-input"
                    required
                  />
                </div>

                <div class="field-group">
                  <label class="field-label">Preferred Date</label>
                  <input
                    v-model="form.date"
                    type="date"
                    class="dark-input"
                  />
                </div>

                <div class="field-group sm:col-span-2">
                  <label class="field-label">Number of Guests</label>

                  <select
                    v-model="form.guests"
                    class="dark-input appearance-none cursor-pointer"
                  >
                    <option value="1">1 Person</option>
                    <option value="2">2 People</option>
                    <option value="4">4 People</option>
                    <option value="6">6+ People</option>
                  </select>
                </div>
              </div>

              <div class="field-group">
                <label class="field-label">Special Requests / Message</label>

                <textarea
                  v-model="form.message"
                  rows="5"
                  placeholder="Dietary preferences, celebrations, accessibility needs, or anything else we should know..."
                  class="dark-input resize-none"
                ></textarea>
              </div>

              <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 pt-2">
                <p class="text-[10px] leading-relaxed text-white/35 max-w-xs">
                  By submitting this form, you agree to be contacted by the
                  Flavoria hospitality team regarding your request.
                </p>

                <button
                  type="submit"
                  class="luxury-button group"
                >
                  <span>Send Request</span>
                  <span class="button-arrow group-hover:translate-x-1 transition-transform">
                    →
                  </span>
                </button>
              </div>
            </form>
          </div>

          <!-- LOCATION -->
          <div class="lg:col-span-5">
            <div class="lg:pl-8 lg:border-l lg:border-white/10">
              <span class="section-kicker text-[#D5A64C]">
                Visit Flavoria
              </span>

              <h3 class="font-serif text-3xl md:text-4xl mt-3">
                Find us in the
                <span class="italic text-[#D5C7B3]">heart of the city.</span>
              </h3>

              <!-- Address -->
              <div class="mt-9 pb-7 border-b border-white/10">
                <div class="flex gap-4">
                  <div class="gold-icon">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="1.6"
                        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                      />
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="1.6"
                        d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                    </svg>
                  </div>

                  <div>
                    <span class="info-label">Address</span>

                    <p class="mt-2 text-sm text-white/60 leading-7 font-sans">
                      123 Culinary Avenue<br />
                      Gourmet District<br />
                      New York, NY 10001, USA
                    </p>
                  </div>
                </div>
              </div>

              <!-- Hours -->
              <div class="py-7 border-b border-white/10">
                <div class="flex gap-4">
                  <div class="gold-icon">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="1.6"
                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                  </div>

                  <div class="w-full">
                    <span class="info-label">Opening Hours</span>

                    <div class="mt-3 space-y-3 font-sans text-xs">
                      <div class="hours-row">
                        <span class="text-white/40">Mon — Thu</span>
                        <span>11:30 AM — 10:00 PM</span>
                      </div>

                      <div class="hours-row">
                        <span class="text-white/40">Fri — Sat</span>
                        <span>11:30 AM — 11:30 PM</span>
                      </div>

                      <div class="hours-row">
                        <span class="text-white/40">Sunday</span>
                        <span>10:00 AM — 9:30 PM</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Phone -->
              <div class="py-7">
                <div class="flex gap-4">
                  <div class="gold-icon">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="1.6"
                        d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
                      />
                    </svg>
                  </div>

                  <div>
                    <span class="info-label">Reservations</span>

                    <a
                      href="tel:+12345678900"
                      class="block mt-2 font-serif text-xl text-[#D5A64C] hover:text-[#E5BD6E] transition-colors"
                    >
                      +1 234 567 8900
                    </a>
                  </div>
                </div>
              </div>

              <!-- Map -->
              <div class="relative h-72 rounded-sm overflow-hidden border border-white/10 group">
                <iframe
                  title="Restaurant Location Map"
                  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d193595.15830869428!2d-74.119763973046!3d40.69766374874431!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c24fa5d33f083b%3A0xc80b8f06e177fe62!2sNew%20York%2C%20NY!5e0!3m2!1sen!2sus!4v1680000000000!5m2!1sen!2sus"
                  class="w-full h-full border-0 grayscale contrast-75 opacity-70 group-hover:opacity-90 transition-opacity duration-500"
                  allowfullscreen=""
                  loading="lazy"
                  referrerpolicy="no-referrer-when-downgrade"
                ></iframe>

                <div class="absolute inset-0 pointer-events-none border border-[#C59237]/20"></div>

                <div class="absolute bottom-4 left-4 bg-[#171512]/90 backdrop-blur px-4 py-2.5 border border-white/10">
                  <span class="font-sans text-[9px] uppercase tracking-[0.2em] text-[#D5A64C]">
                    Gourmet District
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- =========================================================
         FINAL CTA
    ========================================================== -->
    <section class="bg-[#F8F5EF] py-20 px-6">
      <div class="max-w-4xl mx-auto text-center">
        <span class="section-kicker">An Evening Awaits</span>

        <h2 class="font-serif text-4xl md:text-5xl lg:text-6xl font-normal mt-4 leading-tight">
          Come for the cuisine.
          <span class="block italic text-[#8B6A32]">
            Stay for the experience.
          </span>
        </h2>

        <p class="font-sans text-sm text-[#71695F] max-w-xl mx-auto mt-5 leading-relaxed">
          We look forward to welcoming you to Flavoria and making your next
          occasion something worth remembering.
        </p>

        <NuxtLink
          to="/reservation"
          class="inline-flex items-center gap-5 mt-8 px-8 py-4 bg-[#211E1A] text-white font-sans text-[10px] font-semibold uppercase tracking-[0.24em] hover:bg-[#C59237] transition-colors duration-300"
        >
          Reserve Your Table
          <span>→</span>
        </NuxtLink>
      </div>
    </section>

    <!-- =========================================================
         FOOTER
    ========================================================== -->
    <Footer/>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import Footer from '~/components/Footer.vue'

const mobileMenuOpen = ref(false)

const form = reactive({
  name: '',
  email: '',
  phone: '',
  date: '',
  guests: '2',
  message: ''
})

const submitContactForm = () => {
  alert(
    `Thank you, ${form.name}! Your request has been sent. We will contact you shortly.`
  )

  form.name = ''
  form.email = ''
  form.phone = ''
  form.date = ''
  form.guests = '2'
  form.message = ''
}
</script>

<style scoped>
/* =========================================================
   NAVIGATION
========================================================= */

.nav-link {
  position: relative;
  padding-bottom: 7px;
  transition: color 0.3s ease;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background: #c59237;
  transition: width 0.35s ease;
}

.nav-link:hover,
.nav-link.active-link {
  color: #9a722c;
}

.nav-link:hover::after,
.nav-link.active-link::after {
  width: 100%;
}

.nav-icon {
  width: 36px;
  height: 36px;
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #514a42;
  transition:
    color 0.3s ease,
    background-color 0.3s ease;
}

.nav-icon:hover {
  color: #9a722c;
  background: rgba(197, 146, 55, 0.08);
}

.mobile-nav-link {
  color: #514a42;
  transition: color 0.25s ease;
}

.mobile-nav-link:hover,
.active-mobile {
  color: #a07832;
}

/* =========================================================
   TYPOGRAPHY
========================================================= */

.section-kicker {
  display: inline-block;
  font-family: ui-sans-serif, system-ui, sans-serif;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: #a07832;
}

.section-title {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 2rem;
  line-height: 1.15;
  font-weight: 400;
  color: #29241f;
}

.gold-line {
  width: 42px;
  height: 1px;
  background: #c59237;
}

/* =========================================================
   CONTACT CARDS
========================================================= */

.contact-card {
  position: relative;
  padding: 42px 32px 38px;
  min-height: 315px;
  background: #fffdf9;
  border: 1px solid rgba(41, 37, 31, 0.09);
  text-align: center;
  overflow: hidden;
  transition:
    transform 0.45s ease,
    box-shadow 0.45s ease,
    border-color 0.45s ease;
}

.contact-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-top: 2px solid transparent;
  transition: border-color 0.4s ease;
}

.contact-card:hover {
  transform: translateY(-6px);
  border-color: rgba(197, 146, 55, 0.25);
  box-shadow: 0 24px 55px rgba(45, 37, 27, 0.09);
}

.contact-card:hover::before {
  border-color: #c59237;
}

.card-number {
  position: absolute;
  top: 18px;
  right: 22px;
  font-family: ui-sans-serif, system-ui, sans-serif;
  font-size: 9px;
  letter-spacing: 0.2em;
  color: rgba(41, 37, 31, 0.22);
}

.icon-circle {
  width: 54px;
  height: 54px;
  margin: 0 auto 24px;
  border: 1px solid rgba(197, 146, 55, 0.4);
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #c59237;
  transition:
    background-color 0.4s ease,
    color 0.4s ease,
    transform 0.4s ease;
}

.contact-card:hover .icon-circle {
  background: #c59237;
  color: white;
  transform: rotate(8deg);
}

.card-copy {
  max-width: 260px;
  margin: 12px auto 20px;
  font-family: ui-sans-serif, system-ui, sans-serif;
  font-size: 12px;
  line-height: 1.8;
  color: #82786c;
}

.gold-link {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-family: ui-sans-serif, system-ui, sans-serif;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #a07832;
  transition: gap 0.3s ease;
}

.gold-link:hover {
  gap: 14px;
}

/* =========================================================
   FORM
========================================================= */

.field-group {
  position: relative;
}

.field-label {
  display: block;
  margin-bottom: 9px;
  font-family: ui-sans-serif, system-ui, sans-serif;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.58);
}

.field-label span {
  color: #d5a64c;
}

.dark-input {
  width: 100%;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.045);
  color: white;
  padding: 14px 15px;
  font-family: ui-sans-serif, system-ui, sans-serif;
  font-size: 12px;
  outline: none;
  border-radius: 0;
  transition:
    border-color 0.3s ease,
    background-color 0.3s ease;
}

.dark-input::placeholder {
  color: rgba(255, 255, 255, 0.25);
}

.dark-input:focus {
  border-color: rgba(197, 146, 55, 0.8);
  background: rgba(255, 255, 255, 0.07);
}

.dark-input option {
  background: #211e1a;
  color: white;
}

.luxury-button {
  display: inline-flex;
  align-items: center;
  gap: 20px;
  padding: 15px 24px;
  background: #c59237;
  color: white;
  font-family: ui-sans-serif, system-ui, sans-serif;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  transition:
    background-color 0.3s ease,
    transform 0.3s ease;
}

.luxury-button:hover {
  background: #d5a64c;
  transform: translateY(-1px);
}

.button-arrow {
  font-size: 15px;
  line-height: 1;
}

/* =========================================================
   LOCATION
========================================================= */

.gold-icon {
  width: 34px;
  height: 34px;
  flex-shrink: 0;
  border: 1px solid rgba(197, 146, 55, 0.4);
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #d5a64c;
}

.info-label {
  font-family: ui-sans-serif, system-ui, sans-serif;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.75);
}

.hours-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

/* =========================================================
   FOOTER
========================================================= */

.footer-heading {
  position: relative;
  display: inline-block;
  margin-bottom: 22px;
  padding-bottom: 9px;
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 14px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: white;
}

.footer-heading::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 28px;
  height: 1px;
  background: #c59237;
}

.footer-link {
  transition: color 0.25s ease;
}

.footer-link:hover {
  color: #d5a64c;
}

/* =========================================================
   MOBILE MENU ANIMATION
========================================================= */

.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition:
    opacity 0.25s ease,
    transform 0.25s ease;
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* =========================================================
   RESPONSIVE REFINEMENTS
========================================================= */

@media (max-width: 640px) {
  .contact-card {
    min-height: auto;
    padding: 38px 25px 34px;
  }

  .hours-row {
    align-items: flex-start;
    flex-direction: column;
    gap: 3px;
  }
}
</style>
```
