import { io } from "socket.io-client"
import { socketio_port } from "../../../../sites/common_site_config.json"

let socket = null
export function initSocket() {
	// Disable socket.io for development
	// TODO: Configure proper socketio_port when needed
	socket = {
		on: () => {},
		emit: () => {},
		off: () => {},
	}
	return socket
}

export function useSocket() {
	return socket
}
