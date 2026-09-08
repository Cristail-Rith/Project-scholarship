<template>
	<Navbar />
	<main class="chef-detail min-h-screen overflow-hidden bg-[#FDFBF7] text-stone-800">
		<section class="relative overflow-hidden bg-stone-950 px-4 py-20 text-white sm:px-6 md:py-28">
			<img :src="chef.image" :alt="chef.name" class="absolute inset-0 h-full w-full object-cover opacity-25" />
			<div class="absolute inset-0 bg-gradient-to-r from-stone-950 via-stone-950/85 to-stone-950/30"></div>
			<div class="relative mx-auto max-w-7xl">
				<NuxtLink to="/chefs" class="font-sans text-xs uppercase tracking-[0.2em] text-stone-300 transition-colors hover:text-[#C59237]">&larr; Back to our chefs</NuxtLink>
				<div class="mt-16 max-w-2xl">
					<p class="text-xs font-semibold uppercase tracking-[0.3em] text-[#C59237]">{{ chef.role }}</p>
					<h1 class="mt-4 font-serif text-5xl font-normal leading-tight text-stone-100 sm:text-7xl">{{ chef.name }}</h1>
					<p class="mt-6 max-w-xl font-sans text-sm leading-relaxed text-stone-300">{{ chef.description }}</p>
				</div>
			</div>
		</section>

		<section class="mx-auto grid max-w-7xl grid-cols-1 gap-12 px-4 py-16 sm:px-6 md:py-24 lg:grid-cols-12 lg:gap-20">
			<div class="lg:col-span-5">
				<div class="relative">
					<img :src="chef.image" :alt="chef.name" class="relative z-10 h-[30rem] w-full object-cover object-top shadow-xl sm:h-[36rem]" />
					<div class="absolute -bottom-4 -right-4 h-full w-full border border-[#C59237]/50"></div>
				</div>
			</div>

			<div class="flex flex-col justify-center lg:col-span-7">
				<p class="font-sans text-xs font-semibold uppercase tracking-[0.25em] text-[#C59237]">The craft behind the plate</p>
				<h2 class="mt-4 font-serif text-4xl font-normal leading-tight text-stone-900 sm:text-5xl">A point of view, served with intention.</h2>
				<p class="mt-6 font-sans text-base font-light leading-8 text-stone-600">{{ chef.bio }}</p>
				<blockquote class="mt-8 border-l-2 border-[#C59237] bg-[#FAF7F2] px-6 py-5 font-serif text-lg italic leading-relaxed text-stone-700">“{{ chef.quote }}”</blockquote>

				<dl class="mt-10 grid grid-cols-1 gap-6 border-t border-stone-200 pt-6 font-sans sm:grid-cols-2">
					<div>
						<dt class="text-[11px] font-semibold uppercase tracking-wider text-stone-400">Culinary focus</dt>
						<dd class="mt-2 text-sm font-semibold text-stone-900">{{ chef.specialty }}</dd>
					</div>
					<div>
						<dt class="text-[11px] font-semibold uppercase tracking-wider text-stone-400">Experience</dt>
						<dd class="mt-2 text-sm font-semibold text-stone-900">{{ chef.experience }}</dd>
					</div>
				</dl>
			</div>
		</section>

		<section class="border-y border-stone-200 bg-[#FAF7F2] px-4 py-16 sm:px-6 md:py-20">
			<div class="mx-auto max-w-7xl">
				<div class="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
					<div>
						<p class="text-xs font-semibold uppercase tracking-[0.25em] text-[#C59237]">Meet the team</p>
						<h2 class="mt-3 font-serif text-3xl font-normal text-stone-900">More culinary voices</h2>
					</div>
					<NuxtLink to="/chefs" class="font-sans text-xs font-semibold uppercase tracking-[0.2em] text-stone-600 hover:text-[#C59237]">View all chefs &rarr;</NuxtLink>
				</div>
				<div class="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2">
					<NuxtLink v-for="member in relatedChefs" :key="member.name" :to="{ path: '/chefDetail', query: { chef: member.name } }" class="group flex items-center gap-5 border border-stone-200 bg-white p-4 transition-shadow hover:shadow-lg">
						<img :src="member.image" :alt="member.name" class="h-24 w-20 object-cover object-top" />
						<div>
							<p class="text-[10px] font-semibold uppercase tracking-[0.2em] text-[#C59237]">{{ member.role }}</p>
							<h3 class="mt-2 font-serif text-xl text-stone-900 group-hover:text-[#C59237]">{{ member.name }}</h3>
						</div>
					</NuxtLink>
				</div>
			</div>
		</section>
	</main>
</template>

<script setup>
import { computed } from 'vue'

const route = useRoute()

const chefs = [
	{
		name: 'Chef Jean-Luc Moreau',
		role: 'Executive Chef & Founder',
		specialty: 'Modern French & Southeast Asian Fusion',
		experience: '22+ years in Michelin-starred establishments',
		description: 'Precision, warmth, and a deep respect for ingredients define every service led by Chef Jean-Luc.',
		bio: 'Trained in Paris and Lyon, Chef Jean-Luc brings technical precision and artistic presentation to FLAVORIA. His signature approach harmonizes classic French gastronomy with fragrant regional botanicals and the seasons of Southeast Asia.',
		quote: 'Food is an emotional language. When we cook, we communicate reverence for nature and love for our guests.',
		image: 'https://images.unsplash.com/photo-1577219491135-ce391730fb2c?auto=format&fit=crop&w=1000&q=80'
	},
	{
		name: 'Antoine Laurent',
		role: 'Head Pastry Chef',
		specialty: 'Modern plated desserts and artisan chocolate',
		experience: '14 years in patisserie and fine dining',
		description: 'Master of delicate souffles, artisan chocolates, and modern plated desserts.',
		bio: 'Antoine balances classical French pastry technique with a playful, modern sensibility. His desserts are composed like small works of architecture, with texture and restraint in equal measure.',
		quote: 'Dessert is the final impression. It should feel like a sweet symphony.',
		image: 'https://images.unsplash.com/photo-1581299894007-aaa50297cf16?auto=format&fit=crop&w=1000&q=80'
	},
	{
		name: 'Elena Rostova',
		role: 'Sous Chef',
		specialty: 'Seafood, broth infusions, and precision cooking',
		experience: '12 years across coastal kitchens',
		description: 'An expert in seafood preparation, broth infusions, and sustainable sourcing.',
		bio: 'Elena brings a quiet precision to the pass and a strong instinct for balance. Her cooking lets exceptional produce speak clearly, supported by layered broths and bright seasonal herbs.',
		quote: 'Respect every ingredient, from the simple leaf to the rarest catch.',
		image: 'https://images.unsplash.com/photo-1583394838336-acd977736f90?auto=format&fit=crop&w=1000&q=80'
	},
	{
		name: 'Sokha Chan',
		role: 'Grill & Roast Specialist',
		specialty: 'Charcoal cooking and aromatic marinades',
		experience: '16 years mastering live-fire kitchens',
		description: 'Specialist in charcoal searing, dry-aged steaks, and house-blend marinades.',
		bio: 'Sokha turns live fire into a precise instrument. His marinades draw on Cambodian aromatics, while his approach to heat creates deeply flavored, beautifully restrained dishes.',
		quote: 'Fire brings out the truest depth in fine ingredients.',
		image: 'https://images.unsplash.com/photo-1607631568010-a87245c0daf8?auto=format&fit=crop&w=1000&q=80'
	}
]

const chef = computed(() => {
	const selectedName = typeof route.query.chef === 'string' ? route.query.chef : ''
	return chefs.find((member) => member.name === selectedName) || chefs[0]
})

const relatedChefs = computed(() => chefs.filter((member) => member.name !== chef.value.name))
</script>
