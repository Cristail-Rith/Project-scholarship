interface User {
	id: number
	username: string
	email: string
	phone: string
	avatar: string
	role: string
}

interface AuthResponse {
	access_token: string
	user: User
	message: string
}

export function useAuth() {
	const config = useRuntimeConfig()
	const user = useState<User | null>('auth-user', () => null)
	const token = useState<string | null>('auth-token', () => null)

	if (import.meta.client) {
		if (!token.value) {
			token.value = localStorage.getItem('access_token')
		}
		if (!user.value) {
			const storedUser = localStorage.getItem('auth-user')
			user.value = storedUser ? JSON.parse(storedUser) : null
		}
	}

	async function login(email: string, password: string) {
		const response = await $fetch<AuthResponse>('/login', {
			baseURL: config.public.apiBase,
			method: 'POST',
			body: { email, username: email, password },
		})
		token.value = response.access_token
		user.value = response.user
		if (import.meta.client) {
			localStorage.setItem('access_token', response.access_token)
			localStorage.setItem('auth-user', JSON.stringify(response.user))
		}
		return response
	}

	async function register(username: string, email: string, phone: string, password: string) {
		return await $fetch<{ message: string; user: User }>('/register', {
			baseURL: config.public.apiBase,
			method: 'POST',
			body: { username, email, phone, password },
		})
	}

	function logout() {
		user.value = null
		token.value = null
		if (import.meta.client) {
			localStorage.removeItem('access_token')
			localStorage.removeItem('auth-user')
		}
	}

	return { user, token, login, register, logout }
}
