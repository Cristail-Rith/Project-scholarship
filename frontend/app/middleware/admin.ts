export default defineNuxtRouteMiddleware((to, from) => {
	const userState = useState('auth-user')
	const tokenState = useState('auth-token')

	if (import.meta.client) {
		if (!tokenState.value) {
			tokenState.value = localStorage.getItem('access_token') || null
		}
		if (!userState.value) {
			const storedUser = localStorage.getItem('auth-user')
			userState.value = storedUser ? JSON.parse(storedUser) : null
		}
	}

	if (!userState.value) {
		return navigateTo('/login')
	}

	if (userState.value.role !== 'admin') {
		return navigateTo('/')
	}
})
