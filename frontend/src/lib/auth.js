import { writable } from 'svelte/store';
import { browser } from '$app/environment';

/** @typedef {Object} AuthState
 * @property {string|null} token
 * @property {Object|null} user
 * @property {boolean} isAuthenticated
 */

export const authStore = writable(
  /** @type {AuthState} */ ({
    token: null,
    user: null,
    isAuthenticated: false
  })
);

// Initialize from localStorage if in browser
if (browser) {
  const token = localStorage.getItem('authToken');
  if (token) {
    authStore.set(
      /** @type {AuthState} */ ({
        token,
        user: null, // Could decode token for user info
        isAuthenticated: true
      })
    );
  }
}

// Helper functions
/** @param {string} token */
export function login(token) {
  if (browser) {
    localStorage.setItem('authToken', token);
  }
  authStore.set(
    /** @type {AuthState} */ ({
      token,
      user: null,
      isAuthenticated: true
    })
  );
}

export function logout() {
  if (browser) {
    localStorage.removeItem('authToken');
  }
  authStore.set(
    /** @type {AuthState} */ ({
      token: null,
      user: null,
      isAuthenticated: false
    })
  );
}
