
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

/**
 * Fetches data from the Django API.
 *
 * @param {string} path - API endpoint path
 * @param {object} options - Fetch options (method, body, headers, etc.)
 *
 * @returns {Promise<{data: any, error: string|null}>}
 */
export async function apiFetch(path, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}/api${path}`, {
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...options.headers,
            },
        });

        // Parse JSON response
        const data = await response.json();

        // Handle unsuccessful HTTP responses
        if (!response.ok) {
            return {
                data: null,
                error: data.message || data.error || `Request failed (${response.status})`,
            };
        }

        return {
            data,
            error: null,
        };

    } catch (error) {
        return {
            data: null,
            error: error.message || "Unable to connect to the server",
        };
    }
}
