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

/** @type {import('./$types').PageLoad} */
export async function load({ fetch, url }) {
  // Check auth on client
  if (browser) {
    let isAuthenticated = false;
    authStore.subscribe((state) => {
      isAuthenticated = state.isAuthenticated;
    })();

    if (!isAuthenticated) {
      throw goto('/login');
    }
  }

  try {
    const page = url.searchParams.get('page') || '1';
    const search = url.searchParams.get('search') || '';
    const pod = url.searchParams.get('pod') || '';
    const stage = url.searchParams.get('stage') || '';
    const status = url.searchParams.get('status') || '';
    const ordering = url.searchParams.get('ordering') || '-last_update';

    // Build query parameters object
    const params = {
      page
    };
    if (search) params.search = search;
    if (pod) params.pod = pod;
    if (stage) params.stage = stage;
    if (status) params.status = status;
    if (ordering) params.ordering = ordering;

    // Create API instance with SvelteKit fetch
    const api = createApi(fetch);
    const data = await api.getVentures(params);
    return {
      ventures: data.results || [],
      pagination: {
        count: data.count || 0,
        next: data.next,
        previous: data.previous,
        currentPage: parseInt(page),
        totalPages: Math.ceil((data.count || 0) / 20) // Assuming PAGE_SIZE is 20
      },
      filters: {
        search,
        pod,
        stage,
        status,
        ordering
      }
    };
  } catch (error) {
    console.error('Error fetching ventures:', error);
    return {
      ventures: [],
      pagination: {
        count: 0,
        next: null,
        previous: null,
        currentPage: 1,
        totalPages: 0
      },
      filters: {
        search: '',
        pod: '',
        stage: '',
        status: '',
        ordering: '-last_update'
      },
      error: error instanceof Error ? error.message : 'Failed to fetch ventures'
    };
  }
}
