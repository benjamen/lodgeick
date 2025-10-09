import path from "node:path"
import vue from "@vitejs/plugin-vue"
import frappeui from "frappe-ui/vite"
import { defineConfig } from "vite"

// https://vitejs.dev/config/
export default defineConfig({
	// Base path: "/" for both dev and production
	// Assets are served from /assets/lodgeick/frontend/ by Frappe
	base: "/",
	plugins: [
		frappeui({
			lucideIcons: true,
		}),
		vue(),
	],
	build: {
		chunkSizeWarningLimit: 1500,
		outDir: "../lodgeick/public/frontend",
		emptyOutDir: true,
		target: "es2015",
		sourcemap: true,
		// Ensure assets use absolute paths from the /assets/ directory
		assetsDir: "assets",
	},
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "src"),
			"tailwind.config.js": path.resolve(__dirname, "tailwind.config.js"),
		},
	},
	optimizeDeps: {
		include: ["feather-icons", "showdown", "highlight.js/lib/core", "interactjs"],
	},
	server: {
		host: '0.0.0.0',
		proxy: {
			// Proxy backend routes to Frappe
			"^/(app|api|assets|files|desk)": {
				target: "http://127.0.0.1:8090",
				ws: true,
				changeOrigin: true,
			},
		},
	},
})
