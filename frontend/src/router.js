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
]

const router = createRouter({
	history: createWebHistory("/frontend"),
	routes,
})

router.beforeEach(async (to, from, next) => {
	// Allow Home page (catalog browsing), Signup, Login, and OAuth callback without authentication
	if (to.name === "Home" || to.name === "OAuthCallback" || to.name === "Signup" || to.name === "Login") {
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

	// Redirect logic - redirect to home if already logged in
	if ((to.name === "Login" || to.name === "Signup") && isLoggedIn) {
		next({ name: "Home" })
	} else if (!isLoggedIn) {
		next({ name: "Login" })
	} else {
		next()
	}
})

export default router
