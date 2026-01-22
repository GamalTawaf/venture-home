<script>
  import VentureFilters from './components/VentureFilters.svelte';
  import VentureTable from './components/VentureTable.svelte';

  /** @type {import('./$types').PageData} */
  export let data;

  // Filter form data
  let searchQuery = data.filters.search;
  let selectedPod = data.filters.pod;
  let selectedStage = data.filters.stage;
  let selectedStatus = data.filters.status;
  let selectedOrdering = data.filters.ordering;

  // Use filtered ventures directly from API
  $: ventures = data.ventures;
</script>

<svelte:head>
  <title>Venture List</title>
  <meta name="description" content="List of ventures" />
</svelte:head>

<div class="min-h-screen bg-gray-50 p-6">
  <div class="mx-auto max-w-7xl">
    <div class="mb-8">
      <h1 class="mb-2 text-3xl font-bold text-gray-900">Venture Portfolio</h1>
      <p class="text-gray-600">Track and manage your startup ventures</p>
    </div>

    {#if data.error}
      <div class="rounded-lg border border-red-200 bg-red-50 p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">Error loading ventures</h3>
            <div class="mt-2 text-sm text-red-700">{data.error}</div>
          </div>
        </div>
      </div>
    {:else if data.ventures.length === 0}
      <div class="rounded-lg border border-gray-200 bg-white p-12 text-center shadow-sm">
        <svg
          class="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
          />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No ventures found</h3>
        <p class="mt-1 text-sm text-gray-500">Get started by adding your first venture.</p>
      </div>
    {:else}
      <VentureFilters
        bind:searchQuery
        bind:selectedPod
        bind:selectedStage
        bind:selectedStatus
        bind:selectedOrdering
        {ventures}
        pagination={data.pagination}
      />

      <VentureTable {ventures} pagination={data.pagination} />
    {/if}
  </div>
</div>
