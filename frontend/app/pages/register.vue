<script setup lang="ts">
const form = ref({
  name: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: ''
})

const showPassword = ref(false)
const showConfirmPassword = ref(false)
const message = ref('')
const success = ref(false)

function register() {
  message.value = ''
  success.value = false

  if (
    !form.value.name ||
    !form.value.email ||
    !form.value.phone ||
    !form.value.password ||
    !form.value.confirmPassword
  ) {
    message.value = 'Please fill in all fields.'
    return
  }

  if (form.value.password.length < 6) {
    message.value = 'Password must be at least 6 characters.'
    return
  }

  if (form.value.password !== form.value.confirmPassword) {
    message.value = 'Passwords do not match.'
    return
  }

  success.value = true
  message.value = 'Account created successfully!'

  console.log(form.value)
}
</script>

<template>
  <div class="min-h-screen grid grid-cols-1 lg:grid-cols-2 bg-[#fffaf2]">

    <!-- =========================
         LEFT SIDE
    ========================== -->
    <div class="relative hidden lg:block min-h-screen overflow-hidden">

      <!-- Background image -->
      <img
        src="https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?w=1200"
        alt="Restaurant food"
        class="absolute inset-0 w-full h-full object-cover"
      />

      <!-- Dark overlay -->
      <div class="absolute inset-0 bg-black/30"></div>

      <!-- Brand -->
      <div class="absolute top-12 left-14 z-10 text-white">
        <h1 class="text-4xl font-medium">
          Cookie Store
        </h1>

        <p class="mt-2 text-sm font-sans opacity-90">
          Good food. Good mood.
        </p>
      </div>

      <!-- Bottom text -->
      <div class="absolute bottom-14 left-14 z-10 text-white max-w-md">

        <h2 class="text-4xl font-medium leading-tight">
          Delicious food,
          <br />
          made for you.
        </h2>

        <p class="mt-4 text-sm font-sans text-white/80">
          Discover delicious meals and order your favorites
          from Cookie Store.
        </p>

      </div>

    </div>


    <!-- =========================
         RIGHT SIDE
    ========================== -->
    <div class="min-h-screen flex items-center justify-center px-5 py-10 sm:px-10">

      <!-- Register Card -->
      <div
        class="w-full max-w-md bg-white rounded-xl p-6 sm:p-9 shadow-[0_8px_30px_rgba(0,0,0,0.08)]"
      >

        <!-- Header -->
        <div class="text-center mb-7">

          <h2 class="text-3xl font-medium text-gray-900">
            Create an account
          </h2>

          <p class="mt-2 text-sm font-sans text-gray-400">
            Join us and order your favorite food.
          </p>

        </div>


        <!-- Form -->
        <form
          @submit.prevent="register"
          class="space-y-4"
        >

          <!-- Full Name -->
          <div>

            <label
              class="block mb-2 text-sm font-semibold font-sans text-gray-700"
            >
              Full name
            </label>

            <input
              v-model="form.name"
              type="text"
              placeholder="Enter your full name"
              class="w-full px-3 py-3 border border-gray-200 rounded-lg outline-none font-sans text-sm transition focus:border-[#dfad55] focus:ring-4 focus:ring-[#dfad55]/10"
            />

          </div>


          <!-- Email -->
          <div>

            <label
              class="block mb-2 text-sm font-semibold font-sans text-gray-700"
            >
              Email address
            </label>

            <input
              v-model="form.email"
              type="email"
              placeholder="Enter your email"
              class="w-full px-3 py-3 border border-gray-200 rounded-lg outline-none font-sans text-sm transition focus:border-[#dfad55] focus:ring-4 focus:ring-[#dfad55]/10"
            />

          </div>


          <!-- Phone -->
          <div>

            <label
              class="block mb-2 text-sm font-semibold font-sans text-gray-700"
            >
              Phone number
            </label>

            <input
              v-model="form.phone"
              type="tel"
              placeholder="Enter your phone number"
              class="w-full px-3 py-3 border border-gray-200 rounded-lg outline-none font-sans text-sm transition focus:border-[#dfad55] focus:ring-4 focus:ring-[#dfad55]/10"
            />

          </div>


          <!-- Password -->
          <div>

            <label
              class="block mb-2 text-sm font-semibold font-sans text-gray-700"
            >
              Password
            </label>

            <div class="relative">

              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Create a password"
                class="w-full px-3 py-3 pr-16 border border-gray-200 rounded-lg outline-none font-sans text-sm transition focus:border-[#dfad55] focus:ring-4 focus:ring-[#dfad55]/10"
              />

              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-sans text-[#c28e3c] hover:text-[#9f712d]"
              >
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>

            </div>

          </div>


          <!-- Confirm Password -->
          <div>

            <label
              class="block mb-2 text-sm font-semibold font-sans text-gray-700"
            >
              Confirm password
            </label>

            <div class="relative">

              <input
                v-model="form.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                placeholder="Confirm your password"
                class="w-full px-3 py-3 pr-16 border border-gray-200 rounded-lg outline-none font-sans text-sm transition focus:border-[#dfad55] focus:ring-4 focus:ring-[#dfad55]/10"
              />

              <button
                type="button"
                @click="showConfirmPassword = !showConfirmPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-sans text-[#c28e3c] hover:text-[#9f712d]"
              >
                {{ showConfirmPassword ? 'Hide' : 'Show' }}
              </button>

            </div>

          </div>


          <!-- Terms -->
          <div class="flex items-center gap-2 py-1">

            <input
              id="terms"
              type="checkbox"
              required
              class="w-4 h-4 accent-[#dfad55]"
            />

            <label
              for="terms"
              class="text-xs font-sans text-gray-500"
            >
              I agree to the

              <a
                href="#"
                class="text-[#c28e3c] hover:underline"
              >
                Terms & Conditions
              </a>
            </label>

          </div>


          <!-- Message -->
          <div
            v-if="message"
            :class="[
              'px-3 py-2 rounded-md text-xs font-sans text-center',
              success
                ? 'bg-green-50 text-green-600'
                : 'bg-[#fff5df] text-[#9a6c25]'
            ]"
          >
            {{ message }}
          </div>


          <!-- Register Button -->
          <button
            type="submit"
            class="w-full py-3 mt-2 rounded-lg bg-[#dfad55] hover:bg-[#c9953d] text-white text-base transition duration-200 hover:-translate-y-0.5"
          >
            Create account
          </button>

        </form>


        <!-- Login -->
        <div
          class="flex justify-center gap-1 mt-6 text-xs font-sans text-gray-400"
        >

          <span>
            Already have an account?
          </span>

          <NuxtLink
            to="/login"
            class="font-bold text-[#c28e3c] hover:underline"
          >
            Login
          </NuxtLink>

        </div>

      </div>

    </div>

  </div>
</template>