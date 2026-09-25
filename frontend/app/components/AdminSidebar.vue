<template>
	<aside class="admin-shell" :class="{ 'admin-shell-dark': isDark }">
		<button
			type="button"
			class="mobile-toggle"
			aria-label="Open admin navigation"
			:aria-expanded="isOpen"
			@click="isOpen = true"
		>
			<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16" /></svg>
			<span>Menu</span>
		</button>

		<div v-if="isOpen" class="mobile-backdrop" @click="isOpen = false"></div>

		<nav class="sidebar" :class="{ 'sidebar-open': isOpen }" aria-label="Admin navigation">
			<div class="brand-row">
				<NuxtLink to="/admin" class="brand" @click="isOpen = false">
					<span class="brand-mark">F</span>
					<span>
						<strong>FLAVORIA</strong>
						<small>Admin workspace</small>
					</span>
				</NuxtLink>
				<button type="button" class="close-button" aria-label="Close admin navigation" @click="isOpen = false">&times;</button>
			</div>

			<div class="workspace-pill">
				<span class="status-dot"></span>
				<span>Restaurant operations</span>
			</div>

			<div class="nav-section">
				<p class="section-label">Workspace</p>
				<NuxtLink
					v-for="item in primaryLinks"
					:key="item.to"
					:to="item.to"
					class="nav-link"
					:class="{ 'nav-link-active': isActive(item.to) }"
					@click="isOpen = false"
				>
					<svg viewBox="0 0 24 24" aria-hidden="true"><path :d="item.icon" /></svg>
					<span>{{ item.label }}</span>
					<span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
				</NuxtLink>
			</div>

			<div class="nav-section">
				<p class="section-label">Manage</p>
				<NuxtLink
					v-for="item in managementLinks"
					:key="item.to"
					:to="item.to"
					class="nav-link"
					:class="{ 'nav-link-active': isActive(item.to) }"
					@click="isOpen = false"
				>
					<svg viewBox="0 0 24 24" aria-hidden="true"><path :d="item.icon" /></svg>
					<span>{{ item.label }}</span>
				</NuxtLink>
			</div>

			<div class="sidebar-spacer"></div>

			<div class="quick-card">
				<span class="quick-kicker">Today at a glance</span>
				<strong>Keep the service flowing.</strong>
				<NuxtLink to="/" @click="isOpen = false">View restaurant site <span>&rarr;</span></NuxtLink>
			</div>

			<button type="button" class="theme-toggle" :aria-pressed="isDark" @click="toggleTheme">
				<svg viewBox="0 0 24 24" aria-hidden="true"><path v-if="isDark" d="M20.5 15.5A8.5 8.5 0 018.5 3.5 8.5 8.5 0 1020.5 15.5z" /><circle v-else cx="12" cy="12" r="4" /><path v-if="!isDark" d="M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42" /></svg>
				<span>{{ isDark ? 'Switch to light mode' : 'Switch to dark mode' }}</span>
			</button>

			<div class="account-row">
				<span class="avatar">A</span>
				<span class="account-copy"><strong>Administrator</strong><small>Full access</small></span>
				<button type="button" aria-label="Sign out" title="Sign out" @click="signOut">
					<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 17l5-5-5-5M15 12H3M21 3v18" /></svg>
				</button>
			</div>
		</nav>
	</aside>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '~/composables/useAuth'
import { useAdminTheme } from '~/composables/useAdminTheme'

const route = useRoute()
const router = useRouter()
const { logout } = useAuth()
const { isDark, toggleTheme } = useAdminTheme()
const isOpen = ref(false)

const primaryLinks = [
	{ label: 'Overview', to: '/admin', icon: 'M4 13h6V4H4v9zm0 7h6v-5H4v5zm10 0h6v-9h-6v9zm0-16v5h6V4h-6z' },
	{ label: 'Orders', to: '/admin/orders', icon: 'M6 3h12v18H6V3zm3 4h6M9 11h6M9 15h4', badge: 'Live' }
]

const managementLinks = [
	{ label: 'Products', to: '/admin/products', icon: 'M4 7l8-4 8 4-8 4-8-4zm0 5l8 4 8-4M4 17l8 4 8-4' },
	{ label: 'Categories', to: '/admin/categories', icon: 'M4 5h6v6H4V5zm10 0h6v6h-6V5zM4 15h6v4H4v-4zm10 0h6v4h-6v-4z' },
	{ label: 'Tables', to: '/admin/tables', icon: 'M4 5h16M4 19h16M6 5v14M18 5v14M4 12h16' },
	{ label: 'Reservations', to: '/admin/reservations', icon: 'M4 5h16v16H4zM8 3v4m8-4v4M4 10h16m-12 4h3m-3 3h7' },
	{ label: 'Customers', to: '/admin/customer', icon: 'M12 12a4 4 0 100-8 4 4 0 000 8zm-7 9a7 7 0 0 1 14 0M19 8a3 3 0 010 6m2 7a5 5 0 00-3-4.58' },
	{ label: 'Event Inquiries', to: '/admin/event-inquiries', icon: 'M4 4h16v16H4zM8 8h8M8 12h8m-8 4h5' },
	{ label: 'Contact Requests', to: '/admin/contact-messages', icon: 'M4 4h16v16H4zM8 8h8M8 12h8m-8 4h5' },
	{ label: 'Users', to: '/admin/users', icon: 'M16 21v-2a4 4 0 00-4-4H6a4 4 0 00-4 4v2m7-8a4 4 0 100-8 4 4 0 000 8zm7-5a3 3 0 110 6m4 7v-2a4 4 0 00-3-3.87' }
]

const isActive = (path) => path === '/admin' ? route.path === path : route.path.startsWith(path)

const signOut = () => {
	logout()
	isOpen.value = false
	router.push('/login')
}
</script>

<style scoped>
.admin-shell {
	--ink: #29241f;
	--muted: #8c8176;
	--line: #e8dfd5;
	--cream: #fbf8f3;
	--gold: #b47a2b;
	font-family: ui-sans-serif, system-ui, sans-serif;
}

.sidebar {
	position: fixed;
	z-index: 50;
	display: flex;
	height: 100vh;
	min-height: 100vh;
	width: 17rem;
	flex-direction: column;
	border-right: 1px solid var(--line);
	background: var(--cream);
	padding: 1.5rem 1rem 1rem;
	color: var(--ink);
	box-shadow: 8px 0 28px rgb(41 31 19 / 4%);
	overflow-y: auto;
}

.brand-row, .brand, .account-row, .nav-link, .workspace-pill {
	display: flex;
	align-items: center;
}

.brand-row { justify-content: space-between; padding: 0 .5rem .2rem; }
.brand { gap: .7rem; color: inherit; text-decoration: none; }
.brand-mark { display: grid; height: 2.55rem; width: 2.55rem; place-items: center; border: 1px solid var(--gold); border-radius: .8rem; background: linear-gradient(145deg, rgb(180 122 43 / 12%), transparent); color: var(--gold); font-family: Georgia, serif; font-size: 1.4rem; box-shadow: inset 0 0 0 3px rgb(255 255 255 / 24%); }
.brand strong, .brand small, .account-copy strong, .account-copy small { display: block; }
.brand strong { font-family: Georgia, serif; font-size: .95rem; letter-spacing: .18em; }
.brand small { margin-top: .2rem; color: var(--muted); font-size: .62rem; letter-spacing: .08em; text-transform: uppercase; }
.close-button, .mobile-toggle { display: none; }
.workspace-pill { gap: .6rem; margin: 1.6rem .35rem 1.65rem; border: 1px solid var(--line); border-radius: .75rem; background: rgb(255 255 255 / 38%); padding: .7rem .75rem; color: var(--muted); font-size: .68rem; }
.status-dot { height: .45rem; width: .45rem; border-radius: 999px; background: #5e9a72; box-shadow: 0 0 0 3px #e3f0e5; }
.nav-section { margin-bottom: 1.35rem; }
.section-label { margin: 0 .75rem .55rem; color: #b4a79a; font-size: .62rem; font-weight: 700; letter-spacing: .18em; text-transform: uppercase; }
.nav-link { position: relative; gap: .8rem; margin: .22rem 0; border: 1px solid transparent; border-left: 2px solid transparent; border-radius: .7rem; padding: .78rem .8rem; color: #786e64; font-size: .8rem; font-weight: 600; text-decoration: none; transition: background .2s, color .2s, border-color .2s, transform .2s; }
.nav-link svg, .account-row button svg, .mobile-toggle svg { height: 1.05rem; width: 1.05rem; fill: none; stroke: currentColor; stroke-linecap: round; stroke-linejoin: round; stroke-width: 1.7; }
.nav-link:hover { transform: translateX(2px); background: #f1e9df; color: var(--ink); }
.nav-link-active { border-color: rgb(180 122 43 / 20%); border-left-color: var(--gold); background: linear-gradient(100deg, #f2e9dc, #f8f3eb); color: #875817; box-shadow: 0 4px 12px rgb(82 53 17 / 5%); }
.nav-link-active svg { color: var(--gold); }
.nav-badge { margin-left: auto; border-radius: 999px; background: #e6f0e5; padding: .18rem .45rem; color: #4b7d59; font-size: .58rem; font-weight: 700; text-transform: uppercase; }
.sidebar-spacer { flex: 1; }
.quick-card { margin: 1rem .35rem; border: 1px solid #ead9bd; border-radius: .9rem; background: linear-gradient(145deg, #fbf2e4, #f5e9d7); padding: 1rem; }
.quick-kicker { color: var(--gold); font-size: .6rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
.quick-card strong { display: block; margin: .45rem 0 .8rem; font-family: Georgia, serif; font-size: 1rem; font-weight: 400; line-height: 1.25; }
.quick-card a { color: #875817; font-size: .7rem; font-weight: 700; text-decoration: none; }
.quick-card a span { margin-left: .25rem; font-size: 1rem; }
.theme-toggle { display: flex; align-items: center; gap: .65rem; margin: 0 .35rem 1rem; border: 1px solid var(--line); border-radius: .7rem; background: transparent; padding: .7rem .75rem; color: var(--muted); cursor: pointer; font-size: .7rem; text-align: left; transition: border-color .2s, background .2s, color .2s; }
.theme-toggle:hover { border-color: var(--gold); background: rgb(180 122 43 / 7%); color: var(--ink); }
.theme-toggle svg { height: 1rem; width: 1rem; fill: none; stroke: currentColor; stroke-linecap: round; stroke-linejoin: round; stroke-width: 1.7; }
.account-row { gap: .65rem; border-top: 1px solid var(--line); padding: 1rem .35rem .2rem; }
.avatar { display: grid; height: 2rem; width: 2rem; place-items: center; border-radius: 50%; background: #302a25; color: #f4dfbd; font-family: Georgia, serif; }
.account-copy { flex: 1; min-width: 0; }
.account-copy strong { font-size: .72rem; }
.account-copy small { margin-top: .2rem; color: var(--muted); font-size: .6rem; }
.account-row button { border: 0; background: transparent; color: var(--muted); cursor: pointer; padding: .4rem; }
.account-row button:hover { color: #9a3f32; }
.nav-link:focus-visible, .theme-toggle:focus-visible, .account-row button:focus-visible, .brand:focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; }

.admin-shell-dark { --ink: #f2eee8; --muted: #aaa096; --line: #39342f; --cream: #211f1c; --gold: #d5a04d; }
.admin-shell-dark .sidebar { border-right-color: #332b20; background: radial-gradient(ellipse at 15% 0%, rgb(172 117 43 / 9%), transparent 30%), linear-gradient(180deg, #211f1b, #1a1917 65%, #191816); box-shadow: 12px 0 34px rgb(0 0 0 / 18%); }
.admin-shell-dark .brand-mark { border-color: #a77a39; background: linear-gradient(145deg, #40301c, #28231c); color: #e3b664; box-shadow: inset 0 0 0 3px rgb(226 182 100 / 7%); }
.admin-shell-dark .workspace-pill { border-color: #3b352b; background: rgb(255 255 255 / 2%); color: #b9ad9b; }
.admin-shell-dark .status-dot { box-shadow: 0 0 0 3px #263b2b; }
.admin-shell-dark .nav-link { color: #b6aea5; }
.admin-shell-dark .nav-link:hover { border-color: #393126; background: #2b2721; color: #f4ead9; }
.admin-shell-dark .nav-link-active { border-color: #5a4527; border-left-color: #e1ad55; background: linear-gradient(100deg, #3a2d1b, #2d281f); color: #f0c779; box-shadow: inset 0 0 18px rgb(195 139 54 / 5%), 0 6px 16px rgb(0 0 0 / 15%); }
.admin-shell-dark .nav-link-active svg { color: #e1ad55; }
.admin-shell-dark .nav-badge { background: #233629; color: #9ad0a6; }
.admin-shell-dark .quick-card { border-color: #51412b; background: radial-gradient(circle at 100% 0%, rgb(207 155 72 / 13%), transparent 50%), linear-gradient(145deg, #30291f, #25221d); }
.admin-shell-dark .quick-card a { color: #e4bd7d; }
.admin-shell-dark .theme-toggle { border-color: #39342c; background: rgb(255 255 255 / 2%); color: #c2b7a7; }
.admin-shell-dark .theme-toggle:hover { border-color: #70552e; background: #302719; color: #f0c779; }
.admin-shell-dark .account-row { border-top-color: #3a342b; }
.admin-shell-dark .avatar { background: #d5a04d; color: #211f1c; }
.admin-shell-dark .mobile-toggle { border-color: #4a3b27; background: #211f1b; color: #e4bd7d; }

@media (max-width: 767px) {
	.mobile-toggle { position: fixed; z-index: 40; left: 1rem; top: 1rem; display: flex; align-items: center; gap: .5rem; border: 1px solid var(--line); background: var(--cream); padding: .65rem .8rem; color: var(--ink); font-size: .7rem; font-weight: 700; box-shadow: 0 4px 12px #2e21120d; }
	.sidebar { transform: translateX(-100%); transition: transform .25s ease; }
	.sidebar-open { transform: translateX(0); }
	.mobile-backdrop { position: fixed; z-index: 45; inset: 0; background: #1e171280; }
	.close-button { display: block; border: 0; background: transparent; color: var(--muted); cursor: pointer; font-size: 1.5rem; line-height: 1; }
}
</style>
