<template>

  <div class="login-container">

    <!-- LEFT SIDE -->
    <section class="hero-section">
      <div class="hero-overlay"></div>

      <div class="hero-content">
        <div class="food-icon">
          🍴
        </div>

        <h1>
          Great food<br />
          brings people<br />
          together.
        </h1>

        <p>
          Sign in to order your favorite meals and keep track of
          your orders.
        </p>
      </div>
    </section>

    <!-- RIGHT SIDE -->
    <section class="form-section">
      <div class="login-box">

        <!-- Back -->
        <NuxtLink to="/" class="back-link">
          ← Back to home
        </NuxtLink>

        <!-- Heading -->
        <div class="heading">
          <h2>Welcome back</h2>
          <p>Sign in to your account to continue.</p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleLogin">

          <!-- Username -->
          <div class="form-group">
            <label for="email">Email or username</label>

            <input
              id="email"
              v-model="email"
              type="text"
              placeholder="you@example.com"
              autocomplete="email"
              required
            />
          </div>

          <!-- Password -->
          <div class="form-group">
            <label for="password">Password</label>

            <div class="password-wrapper">
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                autocomplete="current-password"
                required
              />

              <button
                type="button"
                class="password-button"
                @click="showPassword = !showPassword"
              >
                {{ showPassword ? '◉' : '◉' }}
              </button>
            </div>
          </div>

          <!-- Options -->
          <div class="form-options">

            <label class="remember">
              <input
                v-model="rememberMe"
                type="checkbox"
              />
              <span>Remember me</span>
            </label>

            <NuxtLink to="/login" class="forgot">
              Forgot password?
            </NuxtLink>

          </div>

          <!-- Login button -->
          <button type="submit" class="login-button">
            Sign In
          </button>

        </form>

        <!-- Message -->
        <p v-if="message" class="message">
          {{ message }}
        </p>

        <!-- Register -->
        <div class="register">
          Don't have an account?
          <NuxtLink to="/register">
            Create one
          </NuxtLink>
        </div>

      </div>
    </section>

  </div>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const showPassword = ref(false)
const message = ref('')

const { login } = useAuth()

const handleLogin = async () => {
  if (!email.value || !password.value) {
    message.value = 'Please enter your email and password.'
    return
  }

  try {
    const response = await login(email.value, password.value)
    message.value = 'Login successful!'
    await navigateTo(response.user.role === 'admin' ? '/admin' : '/')
  } catch (error) {
    message.value = error?.data?.message || 'Invalid email or password.'
  }
}
</script>

<style scoped>

/* ========================================
   RESET
======================================== */

* {
  box-sizing: border-box;
}

.login-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  background: #fefdfd;
  font-family:
    'Times New Roman', Times, serif;
  
}


/* ========================================
   LEFT SIDE
======================================== */

.hero-section {
  position: relative;
  width: 50%;
  min-height: 100vh;
  

  background-image: url('https://www.marinabaysands.com/content/dam/marinabaysands/restaurant-landing/view-all/restaurants-directory-masthead-mobile-1080x1440.jpg');
  background-size: cover;
  background-position: center;

  display: flex;
  align-items: center;
  overflow: hidden;
}


/* Dark overlay */

.hero-overlay {
  position: absolute;
  inset: 0;

  background: rgba(20, 48, 65, 0.62);
}


/* Hero content */

.hero-content {
  position: relative;
  z-index: 2;

  width: 100%;
  max-width: 520px;

  margin-left: auto;
  margin-right: auto;

  padding: 40px;
  color: goldenrod;
}


/* Fork icon */

.food-icon {
  font-size: 38px;
  margin-bottom: 35px;
  filter: grayscale(1);
}


/* Hero title */

.hero-content h1 {
  margin: 0;

  font-size: 43px;
  line-height: 1.18;
  font-weight: 800;
  letter-spacing: -1px;
}


/* Hero description */

.hero-content p {
  max-width: 430px;

  margin-top: 24px;
  margin-bottom: 0;

  font-size: 17px;
  line-height: 1.6;

  color: white;
}


/* ========================================
   RIGHT SIDE
======================================== */

.form-section {
  width: 50%;
  min-height: 100vh;

  display: flex;
  align-items: center;
  justify-content: center;

  background: white;
}


/* Login box */

.login-box {
  width: 100%;
  max-width: 375px;
}


/* ========================================
   BACK LINK
======================================== */

.back-link {
  display: inline-block;

  margin-bottom: 35px;

  color: #ff7200;
  text-decoration: none;

  font-size: 14px;
  font-weight: 600;
}

.back-link:hover {
  color: #e96000;
}


/* ========================================
   HEADING
======================================== */

.heading h2 {
  margin: 0;

  color: goldenrod;

  font-size: 31px;
  line-height: 1.2;

  font-weight: 800;
  letter-spacing: -0.5px;
}

.heading p {
  margin: 8px 0 30px;

  color: #7b8088;

  font-size: 14px;
  line-height: 1.5;
}


/* ========================================
   FORM
======================================== */

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;

  margin-bottom: 9px;

  color: #263344;

  font-size: 13px;
  font-weight: 700;
}


/* Input */

.form-group input {
  width: 100%;
  height: 46px;

  padding: 0 15px;

  border: 1px solid #e3e5e8;
  border-radius: 11px;

  background: #ffffff;

  color: #263344;

  font-size: 14px;

  outline: none;

  transition:
    border-color 0.2s,
    box-shadow 0.2s;
}

.form-group input::placeholder {
  color: #a9adb3;
}

.form-group input:focus {
  border-color: #ff7200;

  box-shadow:
    0 0 0 3px rgba(255, 114, 0, 0.08);
}


/* ========================================
   PASSWORD
======================================== */

.password-wrapper {
  position: relative;
}

.password-wrapper input {
  padding-right: 45px;
}

.password-button {
  position: absolute;

  right: 12px;
  top: 50%;

  transform: translateY(-50%);

  border: none;
  background: transparent;

  color: #8d4b4b;

  cursor: pointer;

  font-size: 13px;
}


/* ========================================
   OPTIONS
======================================== */

.form-options {
  display: flex;

  align-items: center;
  justify-content: space-between;

  margin-top: -2px;
  margin-bottom: 20px;

  font-size: 12px;
}


/* Remember */

.remember {
  display: flex;

  align-items: center;
  gap: 7px;

  color: #777d84;

  cursor: pointer;
}

.remember input {
  width: 12px;
  height: 12px;

  accent-color: #ff7200;

  cursor: pointer;
}


/* Forgot */

.forgot {
  color: #ff7200;

  text-decoration: none;

  font-weight: 700;
}

.forgot:hover {
  text-decoration: underline;
}


/* ========================================
   LOGIN BUTTON
======================================== */

.login-button {
  width: 100%;
  height: 47px;

  border: none;
  border-radius: 10px;

  background: #ff7200;

  color: white;

  font-size: 14px;
  font-weight: 700;

  cursor: pointer;

  box-shadow:
    0 5px 12px rgba(255, 114, 0, 0.18);

  transition:
    background 0.2s,
    transform 0.2s,
    box-shadow 0.2s;
}

.login-button:hover {
  background: #ed6500;

  box-shadow:
    0 7px 16px rgba(255, 114, 0, 0.25);
}

.login-button:active {
  transform: translateY(1px);
}


/* ========================================
   MESSAGE
======================================== */

.message {
  margin: 15px 0 0;

  text-align: center;

  color: #ff7200;

  font-size: 13px;
  font-weight: 600;
}


/* ========================================
   REGISTER
======================================== */

.register {
  margin-top: 28px;

  text-align: center;

  color: #85898f;

  font-size: 12px;
}

.register a {
  color: #ff7200;

  text-decoration: none;

  font-weight: 700;
}

.register a:hover {
  text-decoration: underline;
}


/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 900px) {

  .login-container {
    flex-direction: column;
  }

  .hero-section {
    width: 100%;
    min-height: 350px;
  }

  .form-section {
    width: 100%;
    min-height: auto;

    padding: 60px 25px;
  }

  .hero-content {
    padding: 50px;
  }

  .hero-content h1 {
    font-size: 38px;
  }

}


@media (max-width: 500px) {

  .hero-section {
    min-height: 300px;
  }

  .hero-content {
    padding: 35px;
  }

  .hero-content h1 {
    font-size: 32px;
  }

  .hero-content p {
    font-size: 14px;
  }

  .login-box {
    max-width: 100%;
  }

}

</style>

