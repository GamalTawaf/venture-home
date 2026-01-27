// @ts-nocheck
import { dev } from '$app/environment';
import { authStore } from '$lib/auth.js';
import { goto } from '$app/navigation';
import { browser } from '$app/environment';
import { createApi } from '$lib/api.js';

// we don't need any JS on this page, though we'll load
// it in dev so that we get hot module replacement
export const csr = true;

// since there's no dynamic data here, we can prerender
// it so that it gets served as a static asset in production
export const prerender = false;

/** @type {import('../$types').PageLoad} */
export async function load({ fetch }) {
  // Check auth on client
  if (browser) {
    let isAuthenticated = false;
    authStore.subscribe((state) => {
      isAuthenticated = state.isAuthenticated;
    })();

    // If not authenticated in store, check localStorage directly (robust after login)
    if (!isAuthenticated) {
      const token = localStorage.getItem('authToken');
      if (!token) {
        throw goto('/');
      }
    }
  }

  try {
    // Create API instance with SvelteKit fetch
    const api = createApi(fetch);

    // Fetch all ventures for dashboard (no pagination)
    const venturesData = await api.getVentures({ page_size: 1000 });
    const ventures = venturesData.results || [];

    return {
      ventures,
      metrics: {
        total_ventures: 0,
        active_ventures: 0,
        total_burn_rate: 0,
        avg_runway: 0
      }
    };
  } catch (error) {
    console.error('Error loading dashboard data:', error);
    return {
      ventures: [],
      metrics: {
        total_ventures: 0,
        active_ventures: 0,
        total_burn_rate: 0,
        avg_runway: 0
      },
      error: error instanceof Error ? error.message : 'Failed to load data'
    };
  }
}
