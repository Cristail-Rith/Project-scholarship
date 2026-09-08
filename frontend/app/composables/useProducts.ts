import { ref, computed } from 'vue'

interface Product {
  id: number
  title: string
  name?: string
  category: string
  price: number
  rating: string
  description: string
  image: string
}

const products = ref<Product[]>([
  {
    id: 1,
    title: 'Pan-Seared Duck Breast',
    name: 'Pan-Seared Duck Breast',
    category: 'Main Course',
    price: 34.0,
    rating: '4.9',
    description:
      'Served with cherry reduction sauce, truffle potato puree, and heirloom vegetables.',
    image:
      'https://images.unsplash.com/photo-1514944288352-fffac99f0bdf?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 2,
    title: 'Truffle Mushroom Risotto',
    name: 'Truffle Mushroom Risotto',
    category: 'Starters',
    price: 22.5,
    rating: '4.8',
    description:
      'Arborio rice infused with wild forest mushrooms, aged parmesan, and black truffle oil.',
    image:
      'https://images.unsplash.com/photo-1633964913295-ceb43826e7c9?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 3,
    title: 'Valrhona Chocolate Lava',
    name: 'Valrhona Chocolate Lava',
    category: 'Desserts',
    price: 16.0,
    rating: '5.0',
    description:
      'Warm molten chocolate cake served with Madagascar vanilla bean gelée & berry coulis.',
    image:
      'https://images.unsplash.com/photo-1604908177520-1f3e5b8c9f2d?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 4,
    title: 'Grilled Salmon',
    name: 'Grilled Salmon',
    category: 'Main Course',
    price: 24.99,
    rating: '4.8',
    description: 'Served with lemon butter sauce',
    image:
      'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=500&q=80',
  },
  {
    id: 5,
    title: 'Creamy Prawn Pasta',
    name: 'Creamy Prawn Pasta',
    category: 'Main Course',
    price: 21.99,
    rating: '4.7',
    description: 'Penne in creamy garlic sauce',
    image:
      'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=500&q=80',
  },
  {
    id: 6,
    title: 'Ribeye Steak',
    name: 'Ribeye Steak',
    category: 'Main Course',
    price: 29.99,
    rating: '4.9',
    description: 'Grilled to perfection',
    image:
      'https://images.unsplash.com/photo-1558030006-450675393462?auto=format&fit=crop&w=500&q=80',
  },
  {
    id: 7,
    title: 'Classic Tiramisu',
    name: 'Classic Tiramisu',
    category: 'Desserts',
    price: 8.99,
    rating: '4.6',
    description: 'With cocoa & mascarpone',
    image:
      'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=500&q=80',
  },
  {
    id: 8,
    title: 'Margherita Pizza',
    name: 'Margherita Pizza',
    category: 'Pizza',
    price: 18.5,
    rating: '4.7',
    description: 'Wood-fired pizza with San Marzano tomatoes, mozzarella, and fresh basil.',
    image:
      'https://images.unsplash.com/photo-1593033885483-9e1c5e8b8d7a?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 9,
    title: 'Caesar Salad',
    name: 'Caesar Salad',
    category: 'Starters',
    price: 12.0,
    rating: '4.5',
    description: 'Crisp romaine, parmesan, house croutons, and creamy Caesar dressing.',
    image:
      'https://images.unsplash.com/photo-1550141567-15998fff2757?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 10,
    title: 'Grilled Ribeye Steak',
    name: 'Grilled Ribeye Steak',
    category: 'Main Course',
    price: 36.99,
    rating: '4.9',
    description: 'Dry-aged ribeye with garlic butter, rosemary, and roasted fingerling potatoes.',
    image:
      'https://images.unsplash.com/photo-1600891964599-f61017601b9b?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 11,
    title: 'Fresh Berry Mojito',
    name: 'Fresh Berry Mojito',
    category: 'Beverages',
    price: 9.5,
    rating: '4.6',
    description: 'Mint, muddled berries, lime, and white rum served over crushed ice.',
    image:
      'https://images.unsplash.com/photo-1535969522824-5d46ef90e71f?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 12,
    title: 'Sea Bass en Croute',
    name: 'Sea Bass en Croute',
    category: 'Main Course',
    price: 28.0,
    rating: '4.8',
    description: 'Herb-crusted sea bass wrapped in puff pastry with a citrus beurre blanc.',
    image:
      'https://images.unsplash.com/photo-1519210681838-1d5e865c5925?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 13,
    title: 'Panna Cotta',
    name: 'Panna Cotta',
    category: 'Desserts',
    price: 10.0,
    rating: '4.7',
    description: 'Silky vanilla bean panna cotta with mixed berry compote.',
    image:
      'https://images.unsplash.com/photo-1563379926898-15b95c3b1c9b?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 14,
    title: 'Classic Mojito',
    name: 'Classic Mojito',
    category: 'Beverages',
    price: 7.5,
    rating: '4.4',
    description: 'Fresh mint, lime, white rum, and soda in a traditional Cuban mojito.',
    image:
      'https://images.unsplash.com/photo-1592876073715-4d1f8ca9f6c2?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: 15,
    title: 'Caprese Salad',
    name: 'Caprese Salad',
    category: 'Starters',
    price: 11.0,
    rating: '4.5',
    description: 'Heirloom tomatoes, burrata, fresh basil, and aged balsamic glaze.',
    image:
      'https://images.unsplash.com/photo-1600897638408-4b1bbf14e5e6?auto=format&fit=crop&w=600&q=80',
  },
])

const searchQuery = ref('')

const filteredProducts = computed(() => {
  if (!searchQuery.value.trim()) return []
  const q = searchQuery.value.toLowerCase().trim()
  return products.value.filter(
    (p) =>
      p.title.toLowerCase().includes(q) ||
      (p.name && p.name.toLowerCase().includes(q)) ||
      p.category.toLowerCase().includes(q),
  )
})

export function useProducts() {
  return {
    products,
    searchQuery,
    filteredProducts,
  }
}
