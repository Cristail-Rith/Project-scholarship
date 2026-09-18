export default defineNuxtRouteMiddleware((to) => {
  if (import.meta.server) return

  const { token, user } = useAuth()
  if (!token.value) {
    token.value = localStorage.getItem('access_token')
  }
  if (!user.value) {
    const storedUser = localStorage.getItem('auth-user')
    if (storedUser) {
      try {
        user.value = JSON.parse(storedUser)
      } catch {
        localStorage.removeItem('auth-user')
      }
    }
  }

  if (!token.value) {
    return navigateTo({
      path: '/login',
      query: { redirect: to.fullPath },
    })
  }
})
