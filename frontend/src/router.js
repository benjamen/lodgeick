import { userResource } from "@/data/user"
import { createRouter, createWebHistory } from "vue-router"
import { session } from "./data/session"

const routes = [
	{
		path: "/",
		name: "Home",
		component: () => import("@/pages/Home.vue"),
	},
	{
		name: "Login",
		path: "/account/login",
		component: () => import("@/pages/Login.vue"),
	},
	{
		name: "Signup",
		path: "/account/signup",
		component: () => import("@/pages/Signup.vue"),
	},
	{
		name: "OAuthCallback",
		path: "/oauth/callback",
		component: () => import("@/pages/OAuthCallback.vue"),
	},
	{
		path: "/account",
		component: () => import("@/layouts/AccountLayout.vue"),
		meta: { requiresAuth: true },
		redirect: "/account/profile",
		children: [
			{
				path: "profile",
				name: "AccountProfile",
				component: () => import("@/pages/account/ProfileView.vue"),
			},
			{
				path: "subscription",
				name: "AccountSubscription",
				component: () => import("@/pages/account/SubscriptionView.vue"),
			},
			{
				path: "integrations",
				name: "AccountIntegrations",
				component: () => import("@/pages/account/IntegrationsView.vue"),
			},
			{
				path: "settings",
				name: "AccountSettings",
				component: () => import("@/pages/account/SettingsView.vue"),
			},
			{
				path: "security",
				name: "AccountSecurity",
				component: () => import("@/pages/account/SecurityView.vue"),
			},
			{
				path: "delete",
				name: "AccountDelete",
				component: () => import("@/pages/account/DeleteAccountView.vue"),
			},
		],
	},
]

const router = createRouter({
	history: createWebHistory("/"),
	routes,
})

router.beforeEach(async (to, from, next) => {
	// Public routes that don't require authentication
	const publicRoutes = ["Home", "OAuthCallback", "Signup", "Login"]

	// Allow public routes without authentication
	if (publicRoutes.includes(to.name)) {
		next()
		return
	}

	// Check if user is logged in
	let isLoggedIn = session.isLoggedIn
	try {
		await userResource.promise
	} catch (error) {
		isLoggedIn = false
	}

	// Protected routes require authentication
	if (to.matched.some(record => record.meta.requiresAuth)) {
		if (!isLoggedIn) {
			// Redirect to login if not authenticated
			next({ name: "Login", query: { redirect: to.fullPath } })
			return
		}
	}

	// Redirect authenticated users away from login/signup
	if ((to.name === "Login" || to.name === "Signup") && isLoggedIn) {
		next({ name: "Home" })
		return
	}

	next()
})

export default router
