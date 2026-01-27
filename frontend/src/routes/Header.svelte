<script>
  import { resolve } from '$app/paths';
  import { page } from '$app/state';
  import { authStore, logout } from '$lib/auth.js';
  import { goto } from '$app/navigation';

  function handleLogout() {
    logout();
    goto('/');
  }
</script>

<header class="flex justify-center">
  <nav class="flex justify-center">
    <svg viewBox="0 0 2 3" aria-hidden="true" class="block h-12 w-8">
      <path d="M0,0 L1,2 C1.5,3 1.5,3 2,3 L2,0 Z" class="fill-white/70" />
    </svg>
    <ul class="relative m-0 flex h-12 list-none items-center justify-center bg-white/70 p-0">
      <li
        class="relative flex h-full items-center"
        aria-current={page.url.pathname === '/dashboard' ? 'page' : undefined}
      >
        {#if page.url.pathname === '/dashboard'}
          <span
            class="absolute top-0 left-1/2 h-0 w-0 -translate-x-1/2 transform border-r-[6px] border-b-[6px] border-l-[6px] border-r-transparent border-b-orange-500 border-l-transparent"
          ></span>
        {/if}
        <a
          href={resolve('/dashboard')}
          class="flex h-full items-center px-2 text-xs font-bold tracking-wider text-gray-700 uppercase no-underline transition-colors duration-200 hover:text-orange-500"
          >Dashboard</a
        >
      </li>
      <li
        class="relative flex h-full items-center"
        aria-current={page.url.pathname === '/venture-list' ? 'page' : undefined}
      >
        {#if page.url.pathname === '/venture-list'}
          <span
            class="absolute top-0 left-1/2 h-0 w-0 -translate-x-1/2 transform border-r-[6px] border-b-[6px] border-l-[6px] border-r-transparent border-b-orange-500 border-l-transparent"
          ></span>
        {/if}
        <a
          href={resolve('/venture-list')}
          class="flex h-full items-center px-2 text-xs font-bold tracking-wider text-gray-700 uppercase no-underline transition-colors duration-200 hover:text-orange-500"
          >Venture List</a
        >
      </li>
      <li class="relative ml-auto flex h-full items-center">
        <button
          on:click={handleLogout}
          class="flex h-full items-center px-2 text-base font-extrabold tracking-wider text-red-700 uppercase no-underline transition-colors duration-200 hover:text-orange-500 focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 focus:outline-none"
          style="font-family: 'Inter', 'Arial', sans-serif; letter-spacing: 0.05em;"
        >
          Logout
        </button>
      </li>
    </ul>
    <svg viewBox="0 0 2 3" aria-hidden="true" class="block h-12 w-8">
      <path d="M0,0 L0,3 C0.5,3 0.5,3 1,2 L2,0 Z" class="fill-white/70" />
    </svg>
  </nav>
</header>
