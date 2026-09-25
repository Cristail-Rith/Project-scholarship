import { ref, onMounted, watch } from 'vue'

const isDark = ref(false)
const STORAGE_KEY = 'admin-theme'

export const useAdminTheme = () => {
  const route = useRoute()

  const applyTheme = (dark: boolean) => {
    isDark.value = dark
    if (import.meta.client) {
      document.documentElement.classList.toggle('admin-dark', dark)
      document.documentElement.style.colorScheme = dark ? 'dark' : 'light'
      localStorage.setItem(STORAGE_KEY, dark ? 'dark' : 'light')
    }
  }

  onMounted(() => {
    applyTheme(localStorage.getItem(STORAGE_KEY) === 'dark')
  })

  watch(() => route.path, path => {
    if (!import.meta.client) return
    if (path === '/admin' || path.startsWith('/admin/')) {
      applyTheme(localStorage.getItem(STORAGE_KEY) === 'dark')
      return
    }
    document.documentElement.classList.remove('admin-dark')
    document.documentElement.style.colorScheme = 'light'
  })

  const toggleTheme = () => applyTheme(!isDark.value)

  return { isDark, toggleTheme }
}
