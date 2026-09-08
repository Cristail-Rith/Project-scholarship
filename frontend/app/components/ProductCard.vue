<template>
  <div
    :id="`product-${product.id}`"
    class="bg-white border border-stone-200/80 rounded-sm p-5 shadow-sm hover:shadow-md transition-shadow duration-300 flex flex-col justify-between group"
  >
    <div>
      <div class="relative overflow-hidden mb-4 rounded-sm h-48">
        <img
          :src="product.image"
          :alt="product.title"
          class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
        />
        <span class="absolute top-3 right-3 bg-stone-900/80 text-amber-300 text-[10px] font-sans px-2.5 py-1 tracking-wider uppercase backdrop-blur-sm">
          ★ {{ product.rating }}
        </span>
      </div>

      <div class="flex justify-between items-start mb-2">
        <h3 class="font-serif text-lg font-medium text-stone-900 group-hover:text-[#C59237] transition-colors">
          {{ product.title }}
        </h3>
        <span class="font-sans font-bold text-base text-[#C59237] ml-2">${{ product.price.toFixed(2) }}</span>
      </div>

      <p class="font-sans text-xs text-stone-500 font-light leading-relaxed mb-4">
        {{ product.description }}
      </p>
    </div>

    <button
      @click="addToCart(product)"
      class="w-full py-2.5 bg-stone-100 hover:bg-[#C59237] hover:text-white text-stone-800 text-xs font-sans font-semibold tracking-wider uppercase transition-colors duration-300 rounded-sm"
    >
      Add To Order
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
})

const addToCart = (item) => {
  console.log('Added to cart:', item.title)
}
</script>
