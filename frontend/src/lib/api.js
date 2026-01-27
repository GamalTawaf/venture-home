import { authStore, logout } from './auth.js';
import { browser } from '$app/environment';
import { goto } from '$app/navigation';

/**
 * Helper function to handle 401 Unauthorized responses
 * @param {Response} response - Fetch response
 */
function handle401(response) {
  if (response.status === 401) {
    logout();
    if (browser) {
      goto('/');
    }
  }
}

/**
 * API client utility for making authenticated requests
 */
class ApiClient {
  /**
   * @param {typeof fetch} [fetchFn] - Optional fetch function (e.g., from SvelteKit load function)
   */
  constructor(fetchFn = fetch) {
    this.fetchFn = fetchFn;
  }

  /**
   * Get authorization headers if user is authenticated
   * @returns {Record<string, string>} Headers object with auth token if available
   */
  getAuthHeaders() {
    /** @type {Record<string, string>} */
    let headers = {
      'Content-Type': 'application/json'
    };

    if (browser) {
      let token = null;
      authStore.subscribe((state) => {
        token = state.token;
      })();

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }

    return headers;
  }

  /**
   * Make a GET request
   * @param {string} url - The API endpoint URL
   * @param {Object} options - Additional fetch options
   * @returns {Promise<Response>} Fetch response
   */
  async get(url, options = {}) {
    const response = await this.fetchFn(url, {
      method: 'GET',
      headers: this.getAuthHeaders(),
      ...options
    });
    handle401(response);
    return response;
  }

  /**
   * Make a POST request
   * @param {string} url - The API endpoint URL
   * @param {Object} data - Request body data
   * @param {Object} options - Additional fetch options
   * @returns {Promise<Response>} Fetch response
   */
  async post(url, data = {}, options = {}) {
    const response = await this.fetchFn(url, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data),
      ...options
    });
    handle401(response);
    return response;
  }

  /**
   * Make a PUT request
   * @param {string} url - The API endpoint URL
   * @param {Object} data - Request body data
   * @param {Object} options - Additional fetch options
   * @returns {Promise<Response>} Fetch response
   */
  async put(url, data = {}, options = {}) {
    const response = await this.fetchFn(url, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data),
      ...options
    });
    handle401(response);
    return response;
  }

  /**
   * Make an unauthenticated POST request (for login/register)
   * @param {string} url - The API endpoint URL
   * @param {Object} data - Request body data
   * @param {Object} options - Additional fetch options
   * @returns {Promise<Response>} Fetch response
   */
  async postUnauthenticated(url, data = {}, options = {}) {
    return this.fetchFn(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data),
      ...options
    });
  }
}

// Create and export a singleton instance (uses native fetch by default)
export const apiClient = new ApiClient();

/**
 * Create an API client instance with a custom fetch function
 * @param {typeof fetch} fetchFn - The fetch function to use (e.g., from SvelteKit load)
 * @returns {ApiClient} New API client instance
 */
export function createApiClient(fetchFn) {
  return new ApiClient(fetchFn);
}

// Base API URL
export const API_BASE_URL = 'http://localhost:8000';

// API endpoints
export const API_ENDPOINTS = {
  VENTURES: `${API_BASE_URL}/ventures/`,
  VENTURES_METRICS: `${API_BASE_URL}/ventures/metrics/`,
  VENTURES_CHAT: `${API_BASE_URL}/ventures/chat/`,
  VENTURES_GENERATE_RANDOM: `${API_BASE_URL}/ventures/generate_random/`,
  AUTH_LOGIN: `${API_BASE_URL}/auth/login`,
  AUTH_REFRESH: `${API_BASE_URL}/auth/refresh/`,
  AUTH_REGISTER: `${API_BASE_URL}/auth/register/`
};

/**
 * Helper function to make API calls and parse JSON response
 * Note: 401 handling is done by handle401() in ApiClient methods, so we don't duplicate it here
 * @template T
 * @param {Response} response - Fetch response
 * @returns {Promise<T>} Parsed JSON data
 */
async function handleApiResponse(response) {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || errorData.error || `HTTP ${response.status}`);
  }
  return response.json();
}

/**
 * @typedef {Object} ApiMethods
 * @property {(params?: Record<string, any>) => Promise<any>} getVentures
 * @property {(question: string) => Promise<any>} chat
 * @property {(count?: number) => Promise<any>} generateRandom
 * @property {(username: string, password: string) => Promise<any>} login
 * @property {(refresh: string) => Promise<any>} refreshToken
 * @property {(username: string, password: string, email: string) => Promise<any>} register
 */

/**
 * Create API methods with optional custom fetch function
 * @param {typeof fetch} [fetchFn] - Optional fetch function (e.g., from SvelteKit load function)
 * @returns {ApiMethods} API methods object
 */
function createApiMethods(fetchFn) {
  const client = fetchFn ? createApiClient(fetchFn) : apiClient;

  return {
    /**
     * Get ventures with optional query parameters
     * @param {Record<string, any>} params - Query parameters
     * @returns {Promise<any>} API response
     */
    getVentures: (params = {}) => {
      const url = new URL(API_ENDPOINTS.VENTURES);
      Object.keys(params).forEach((key) => {
        if (params[key] !== undefined && params[key] !== null) {
          url.searchParams.append(key, params[key]);
        }
      });
      return client.get(url.toString()).then(handleApiResponse);
    },
    /**
     * Send a chat message to the AI
     * @param {string} question - The question to ask
     * @returns {Promise<any>} Chat response
     */
    chat: (question) =>
      client.post(API_ENDPOINTS.VENTURES_CHAT, { question }).then(handleApiResponse),

    /**
     * Generate random ventures
     * @param {number} count - Number of ventures to generate
     * @returns {Promise<any>} API response
     */
    generateRandom: (count = 20) =>
      client.post(API_ENDPOINTS.VENTURES_GENERATE_RANDOM, { count }).then(handleApiResponse),

    /**
     * Login user
     * @param {string} username - Username
     * @param {string} password - Password
     * @returns {Promise<any>} Auth tokens
     */
    login: (username, password) =>
      client
        .postUnauthenticated(API_ENDPOINTS.AUTH_LOGIN, { username, password })
        .then(handleApiResponse),

    /**
     * Refresh auth token
     * @param {string} refresh - Refresh token
     * @returns {Promise<any>} New tokens
     */
    refreshToken: (refresh) =>
      client.postUnauthenticated(API_ENDPOINTS.AUTH_REFRESH, { refresh }).then(handleApiResponse),

    /**
     * Register new user
     * @param {string} username - Username
     * @param {string} password - Password
     * @param {string} email - Email
     * @returns {Promise<any>} User data
     */
    register: (username, password, email) =>
      client
        .postUnauthenticated(API_ENDPOINTS.AUTH_REGISTER, { username, password, email })
        .then(handleApiResponse)
  };
}

// Default API methods (uses native fetch for client-side calls)
/** @type {ApiMethods} */
export const api = createApiMethods();

// Export function to create API methods with SvelteKit fetch
export const createApi = createApiMethods;
