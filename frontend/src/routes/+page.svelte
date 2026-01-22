<script>
  // @ts-nocheck
  import Chart from './components/Chart.svelte';
  import { api } from '$lib/api.js';
  import { invalidateAll } from '$app/navigation';

  /** @type {import('./$types').PageData} */
  export let data;

  /**
   * Format status values from snake_case to Title Case
   * @param {string} status - The raw status string
   * @returns {string} - The formatted status string
   */
  function formatStatus(status) {
    if (!status) return '';
    return status
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(' ');
  }

  // Interactive filtering state
  let activeFilters = {
    stage: '',
    status: '',
    pod: ''
  };

  // Filtered ventures based on active filters
  $: filteredVentures = data.ventures.filter((venture) => {
    const stageMatch = !activeFilters.stage || venture.stage === activeFilters.stage;
    const statusMatch = !activeFilters.status || venture.status === activeFilters.status;
    const podMatch = !activeFilters.pod || venture.pod === activeFilters.pod;
    return stageMatch && statusMatch && podMatch;
  });

  // Calculate metrics for filtered data
  $: filteredMetrics = (() => {
    const ventures = filteredVentures;
    const total_ventures = ventures.length;
    const active_ventures = ventures.filter((v) => v.status?.toLowerCase() === 'active').length;

    const total_burn_rate = ventures.reduce((sum, v) => {
      return sum + (v.metrics?.burn_rate_monthly || 0);
    }, 0);

    const runways = ventures.map((v) => v.metrics?.runway_months || 0).filter((r) => r > 0);
    const avg_runway =
      runways.length > 0 ? Math.round(runways.reduce((a, b) => a + b, 0) / runways.length) : 0;

    return {
      total_ventures,
      active_ventures,
      total_burn_rate,
      avg_runway
    };
  })();

  // Handle chart filter events
  function handleChartFilter(event) {
    const { key, dataKey } = event.detail;
    activeFilters[dataKey] = activeFilters[dataKey] === key ? '' : key; // Toggle filter
  }

  // Clear all filters
  function clearFilters() {
    activeFilters = {
      stage: '',
      status: '',
      pod: ''
    };
  }

  // Generate random ventures
  let generating = false;
  let generateMessage = '';

  async function generateRandomVentures() {
    generating = true;
    generateMessage = '';

    try {
      const data = await api.generateRandom(20);
      generateMessage = data.message || 'Successfully generated 20 random ventures';
      // Invalidate all data to reload page data and show new ventures
      await invalidateAll();
    } catch (error) {
      generateMessage = error instanceof Error ? error.message : 'Failed to generate ventures';
    } finally {
      generating = false;
    }
  }
</script>

<svelte:head>
  <title>Venture Dashboard</title>
  <meta name="description" content="Venture portfolio dashboard and analytics" />
</svelte:head>

<div class="min-h-screen bg-gray-50">
  <div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <h1 class="text-3xl font-bold text-gray-900">Venture Dashboard</h1>
        <div class="flex items-center space-x-4">
          <button
            on:click={generateRandomVentures}
            disabled={generating}
            class="inline-flex items-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:outline-none disabled:opacity-50"
          >
            {#if generating}
              <svg class="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                ></circle>
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              Generating...
            {:else}
              <svg class="mr-2 -ml-1 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                ></path>
              </svg>
              Generate Random Ventures
            {/if}
          </button>
        </div>
      </div>
      {#if generateMessage}
        <div class="mt-4 rounded-md bg-green-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clip-rule="evenodd"
                ></path>
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-green-800">{generateMessage}</p>
            </div>
          </div>
        </div>
      {/if}
    </div>

    {#if data.error}
      <div class="mb-8 rounded-lg border border-red-200 bg-red-50 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <svg class="h-6 w-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              ></path>
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">Dashboard Error</h3>
            <div class="mt-2 text-sm text-red-700">{data.error}</div>
          </div>
        </div>
      </div>
    {:else}
      <!-- Key Metrics Cards -->
      <div class="mb-8 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
        <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <div class="flex flex-col items-center text-center">
            <div class="mb-3 flex-shrink-0">
              <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-500">
                <svg
                  class="h-6 w-6 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
                  ></path>
                </svg>
              </div>
            </div>
            <div>
              <p class="mb-1 text-3xl font-bold text-gray-900">{filteredMetrics.total_ventures}</p>
              <p class="text-sm font-medium text-gray-600">Total Ventures</p>
            </div>
          </div>
        </div>

        <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <div class="flex flex-col items-center text-center">
            <div class="mb-3 flex-shrink-0">
              <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-green-500">
                <svg
                  class="h-6 w-6 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  ></path>
                </svg>
              </div>
            </div>
            <div>
              <p class="mb-1 text-3xl font-bold text-gray-900">{filteredMetrics.active_ventures}</p>
              <p class="text-sm font-medium text-gray-600">Active Ventures</p>
            </div>
          </div>
        </div>

        <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <div class="flex flex-col items-center text-center">
            <div class="mb-3 flex-shrink-0">
              <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-red-500">
                <svg
                  class="h-6 w-6 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"
                  ></path>
                </svg>
              </div>
            </div>
            <div>
              <p class="mb-1 text-3xl font-bold text-gray-900">
                ${filteredMetrics.total_burn_rate.toLocaleString()}/mo
              </p>
              <p class="text-sm font-medium text-gray-600">Total Burn Rate</p>
            </div>
          </div>
        </div>

        <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <div class="flex flex-col items-center text-center">
            <div class="mb-3 flex-shrink-0">
              <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-yellow-500">
                <svg
                  class="h-6 w-6 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  ></path>
                </svg>
              </div>
            </div>
            <div>
              <p class="mb-1 text-3xl font-bold text-gray-900">{filteredMetrics.avg_runway}</p>
              <p class="text-sm font-medium text-gray-600">Avg Runway</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="mb-8 grid grid-cols-1 gap-8 lg:grid-cols-2">
        <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <h3 class="mb-4 text-lg font-semibold text-gray-900">Stage Distribution</h3>
          <Chart
            data={filteredVentures}
            chartType="bar"
            dataKey="stage"
            width={500}
            height={300}
            on:filter={handleChartFilter}
          />
        </div>

        <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <h3 class="mb-4 text-lg font-semibold text-gray-900">Status Overview</h3>
          <Chart
            data={filteredVentures}
            chartType="pie"
            dataKey="status"
            width={500}
            height={300}
            on:filter={handleChartFilter}
          />
        </div>
      </div>

      <!-- Additional Charts Row -->
      <div class="mb-8 grid grid-cols-1 gap-8 lg:grid-cols-2">
        <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <h3 class="mb-4 text-lg font-semibold text-gray-900">Pod Distribution</h3>
          <Chart
            data={filteredVentures}
            chartType="bar"
            dataKey="pod"
            width={500}
            height={300}
            on:filter={handleChartFilter}
          />
        </div>

        <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <h3 class="mb-4 text-lg font-semibold text-gray-900">Burn Rate vs Runway</h3>
          <Chart data={filteredVentures} chartType="scatter" width={500} height={300} />
        </div>
      </div>

    {/if}
  </div>
</div>
