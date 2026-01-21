import { dev } from '$app/environment';

// we don't need any JS on this page, though we'll load
// it in dev so that we get hot module replacement
export const csr = dev;

// since there's no dynamic data here, we can prerender
// it so that it gets served as a static asset in production
export const prerender = false;

/** @type {import('./$types').PageLoad} */
export async function load({ fetch }) {
	try {
		const response = await fetch('http://backend:8000/dashboard/ventures');
		if (!response.ok) {
			throw new Error('Failed to fetch ventures');
		}
		const data = await response.json();
		return {
			ventures: data.ventures
		};
	} catch (error) {
		console.error('Error fetching ventures:', error);
		return {
			ventures: [],
			error: error.message
		};
	}
}
