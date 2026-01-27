import { authStore } from '$lib/auth.js';
import { goto } from '$app/navigation';
import { browser } from '$app/environment';

/** @param {Object} param0
 * @param {any} param0.event
 * @param {Function} param0.resolve
 */
export async function handle({ event, resolve }) {
  // Get current auth state
  let authState = { isAuthenticated: false };
  authStore.subscribe((state) => {
    authState = state;
  })();

  const isLoginPage = event.url.pathname === '/';
  const isPublicPage = false; // Add more public pages if needed

  if (!authState.isAuthenticated && !isLoginPage && !isPublicPage) {
    // Redirect to login if not authenticated and not on login page
    throw goto('/');
  }

  // Add auth header to fetch if authenticated
  if (authState.isAuthenticated) {
    // This is tricky in SvelteKit hooks. Perhaps better to handle in load functions.
  }

  return resolve(event);
}
