<template>
	<aside class="admin-shell">
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

const route = useRoute()
const isOpen = ref(false)

const primaryLinks = [
	{ label: 'Overview', to: '/admin', icon: 'M4 13h6V4H4v9zm0 7h6v-5H4v5zm10 0h6v-9h-6v9zm0-16v5h6V4h-6z' },
	{ label: 'Orders', to: '/admin/orders', icon: 'M6 3h12v18H6V3zm3 4h6M9 11h6M9 15h4', badge: 'Live' }
]

const managementLinks = [
	{ label: 'Products', to: '/admin/products', icon: 'M4 7l8-4 8 4-8 4-8-4zm0 5l8 4 8-4M4 17l8 4 8-4' },
	{ label: 'Categories', to: '/admin/categories', icon: 'M4 5h6v6H4V5zm10 0h6v6h-6V5zM4 15h6v4H4v-4zm10 0h6v4h-6v-4z' },
	{ label: 'Tables', to: '/admin/tables', icon: 'M4 5h16M4 19h16M6 5v14M18 5v14M4 12h16' },
	{ label: 'Users', to: '/admin/users', icon: 'M16 21v-2a4 4 0 00-4-4H6a4 4 0 00-4 4v2m7-8a4 4 0 100-8 4 4 0 000 8zm7-5a3 3 0 110 6m4 7v-2a4 4 0 00-3-3.87' }
]

const isActive = (path) => path === '/admin' ? route.path === path : route.path.startsWith(path)

const signOut = () => {
	isOpen.value = false
	navigateTo('/login')
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
	min-height: 100vh;
	width: 17rem;
	flex-direction: column;
	border-right: 1px solid var(--line);
	background: var(--cream);
	padding: 1.5rem 1rem 1rem;
	color: var(--ink);
}

.brand-row, .brand, .account-row, .nav-link, .workspace-pill {
	display: flex;
	align-items: center;
}

.brand-row { justify-content: space-between; padding: 0 .5rem; }
.brand { gap: .7rem; color: inherit; text-decoration: none; }
.brand-mark { display: grid; height: 2.3rem; width: 2.3rem; place-items: center; border: 1px solid var(--gold); color: var(--gold); font-family: Georgia, serif; font-size: 1.4rem; }
.brand strong, .brand small, .account-copy strong, .account-copy small { display: block; }
.brand strong { font-family: Georgia, serif; font-size: .95rem; letter-spacing: .18em; }
.brand small { margin-top: .2rem; color: var(--muted); font-size: .62rem; letter-spacing: .08em; text-transform: uppercase; }
.close-button, .mobile-toggle { display: none; }
.workspace-pill { gap: .5rem; margin: 2rem .35rem 1.8rem; border: 1px solid var(--line); padding: .65rem .7rem; color: var(--muted); font-size: .68rem; }
.status-dot { height: .45rem; width: .45rem; border-radius: 999px; background: #5e9a72; box-shadow: 0 0 0 3px #e3f0e5; }
.nav-section { margin-bottom: 1.5rem; }
.section-label { margin: 0 .75rem .55rem; color: #b4a79a; font-size: .62rem; font-weight: 700; letter-spacing: .18em; text-transform: uppercase; }
.nav-link { position: relative; gap: .8rem; margin: .2rem 0; border-left: 2px solid transparent; border-radius: 0 .25rem .25rem 0; padding: .75rem .8rem; color: #786e64; font-size: .8rem; font-weight: 600; text-decoration: none; transition: background .2s, color .2s, border-color .2s; }
.nav-link svg, .account-row button svg, .mobile-toggle svg { height: 1.05rem; width: 1.05rem; fill: none; stroke: currentColor; stroke-linecap: round; stroke-linejoin: round; stroke-width: 1.7; }
.nav-link:hover { background: #f1e9df; color: var(--ink); }
.nav-link-active { border-color: var(--gold); background: #f2e9dc; color: #875817; }
.nav-badge { margin-left: auto; border-radius: 999px; background: #e6f0e5; padding: .18rem .45rem; color: #4b7d59; font-size: .58rem; font-weight: 700; text-transform: uppercase; }
.sidebar-spacer { flex: 1; }
.quick-card { margin: 1rem .35rem; border: 1px solid #ead9bd; background: #f8eedf; padding: 1rem; }
.quick-kicker { color: var(--gold); font-size: .6rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
.quick-card strong { display: block; margin: .45rem 0 .8rem; font-family: Georgia, serif; font-size: 1rem; font-weight: 400; line-height: 1.25; }
.quick-card a { color: #875817; font-size: .7rem; font-weight: 700; text-decoration: none; }
.quick-card a span { margin-left: .25rem; font-size: 1rem; }
.account-row { gap: .65rem; border-top: 1px solid var(--line); padding: 1rem .35rem .2rem; }
.avatar { display: grid; height: 2rem; width: 2rem; place-items: center; border-radius: 50%; background: #302a25; color: #f4dfbd; font-family: Georgia, serif; }
.account-copy { flex: 1; min-width: 0; }
.account-copy strong { font-size: .72rem; }
.account-copy small { margin-top: .2rem; color: var(--muted); font-size: .6rem; }
.account-row button { border: 0; background: transparent; color: var(--muted); cursor: pointer; padding: .4rem; }
.account-row button:hover { color: #9a3f32; }

@media (max-width: 767px) {
	.mobile-toggle { position: fixed; z-index: 40; left: 1rem; top: 1rem; display: flex; align-items: center; gap: .5rem; border: 1px solid var(--line); background: var(--cream); padding: .65rem .8rem; color: var(--ink); font-size: .7rem; font-weight: 700; box-shadow: 0 4px 12px #2e21120d; }
	.sidebar { transform: translateX(-100%); transition: transform .25s ease; }
	.sidebar-open { transform: translateX(0); }
	.mobile-backdrop { position: fixed; z-index: 45; inset: 0; background: #1e171280; }
	.close-button { display: block; border: 0; background: transparent; color: var(--muted); cursor: pointer; font-size: 1.5rem; line-height: 1; }
}
</style>
