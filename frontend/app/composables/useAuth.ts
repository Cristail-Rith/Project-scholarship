export interface AuthUser { id: number; username: string; email: string; full_name: string; role: string; is_active: boolean }
export const useAuth = () => {
  const user = useState<AuthUser | null>('auth-user', () => null)
  const token = useCookie<string | null>('access-token', { sameSite: 'lax' })
  const config = useRuntimeConfig()
  const login = async (username: string, password: string) => { const response = await $fetch<{ access_token: string; data: AuthUser }>(`${config.public.apiBase}/api/auth/login`, { method: 'POST', body: { username, password } }); token.value = response.access_token; user.value = response.data; return response.data }
  const register = async (details: Record<string, string>) => await $fetch(`${config.public.apiBase}/api/auth/register`, { method: 'POST', body: details })
  const fetchUser = async () => { if (!token.value) return null; try { const response = await $fetch<{ data: AuthUser }>(`${config.public.apiBase}/api/auth/me`, { headers: { Authorization: `Bearer ${token.value}` } }); user.value = response.data; return response.data } catch { logout(); return null } }
  const logout = () => { token.value = null; user.value = null; return navigateTo('/login') }
  return { user, token, login, register, fetchUser, logout, isAuthenticated: computed(() => Boolean(token.value)) }
}
