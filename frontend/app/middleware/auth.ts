export default defineNuxtRouteMiddleware(async () => { const { token, fetchUser } = useAuth(); if (!token.value) return navigateTo('/login'); if (import.meta.client) await fetchUser() })
