
<script>
  import Header from './Header.svelte';
  import ChatWidget from '$lib/components/ChatWidget.svelte';
  import { authStore } from '$lib/auth.js';
  import './layout.css';

  /** @type {{children: import('svelte').Snippet}} */
  let { children } = $props();
  import { derived } from 'svelte/store';
  const isAuthenticatedStore = derived(authStore, ($authStore) => $authStore.isAuthenticated);
</script>

<div class="flex min-h-screen flex-col">
  {#if $isAuthenticatedStore}
    <Header />
  {/if}
  <main class="mx-auto box-border flex w-full max-w-5xl flex-1 flex-col p-4">
    {@render children()}
  </main>
  {#if $isAuthenticatedStore}
    <ChatWidget />
  {/if}
</div>
