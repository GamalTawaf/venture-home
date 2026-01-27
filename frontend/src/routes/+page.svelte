<script>
  import { login } from '$lib/auth.js';
  import { goto } from '$app/navigation';
  import { api } from '$lib/api.js';

  let username = '';
  let password = '';
  let error = '';
  let loading = false;

  async function handleLogin() {
    loading = true;
    error = '';

    try {
      const data = await api.login(username, password);
      login(data.access);
      // Wait a short moment to ensure auth state is updated before redirect
      await new Promise((resolve) => setTimeout(resolve, 150));
      goto('/dashboard');
    } catch (err) {
      error = err instanceof Error ? err.message : 'Login failed';
    } finally {
      loading = false;
    }
  }
</script>

<div class="flex min-h-screen items-center justify-center bg-gray-50">
  <div class="w-full max-w-md space-y-8 rounded-lg bg-white p-8 shadow-md">
    <div>
      <h2 class="text-center text-3xl font-extrabold text-gray-900">Sign in to your account</h2>
    </div>
    <form class="mt-8 space-y-6" on:submit|preventDefault={handleLogin}>
      <div class="-space-y-px rounded-md shadow-sm">
        <div>
          <label for="username" class="sr-only">Username</label>
          <input
            id="username"
            name="username"
            type="text"
            required
            class="relative block w-full rounded-t-md border-0 px-3 py-1.5 text-gray-900 ring-1 ring-gray-300 ring-inset placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-indigo-600 focus:ring-inset sm:text-sm sm:leading-6"
            placeholder="Username"
            bind:value={username}
          />
        </div>
        <div>
          <label for="password" class="sr-only">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            required
            class="relative block w-full rounded-b-md border-0 px-3 py-1.5 text-gray-900 ring-1 ring-gray-300 ring-inset placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-indigo-600 focus:ring-inset sm:text-sm sm:leading-6"
            placeholder="Password"
            bind:value={password}
          />
        </div>
      </div>

      {#if error}
        <div class="text-sm text-red-600">{error}</div>
      {/if}

      <div>
        <button
          type="submit"
          disabled={loading}
          class="group relative flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50"
        >
          {loading ? 'Signing in...' : 'Sign in'}
        </button>
      </div>
    </form>
  </div>
</div>
