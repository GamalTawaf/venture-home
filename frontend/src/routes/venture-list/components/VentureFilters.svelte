<script>
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';

  /** @typedef {Object} Filters
   * @property {string} search
   * @property {string} pod
   * @property {string} stage
   * @property {string} status
   * @property {string} ordering
   */

  /** @typedef {Object} Pagination
   * @property {number} count
   * @property {number} currentPage
   * @property {number} totalPages
   */

  /** @typedef {Object} Venture
   * @property {string} pod
   * @property {string} stage
   * @property {string} status
   */

  /**
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

  /** @type {string} */
  export let searchQuery = '';

  /** @type {string} */
  export let selectedPod = '';

  /** @type {string} */
  export let selectedStage = '';

  /** @type {string} */
  export let selectedStatus = '';

  /** @type {string} */
  export let selectedOrdering = '-last_update';

  /** @type {Venture[]} */
  export let ventures = [];

  /** @type {Pagination} */
  export let pagination;

  // Get unique values for filter dropdowns (from all data, not just current page)
  $: uniquePods = [...new Set(ventures.map(/** @param {Venture} v */ (v) => v.pod))].sort();
  $: uniqueStages = [...new Set(ventures.map(/** @param {Venture} v */ (v) => v.stage))].sort();
  $: uniqueStatuses = [...new Set(ventures.map(/** @param {Venture} v */ (v) => v.status))].sort();

  function applyFilters() {
    const url = new URL($page.url);

    // Reset to page 1 when applying filters
    url.searchParams.set('page', '1');

    // Set filter parameters
    if (searchQuery.trim()) {
      url.searchParams.set('search', searchQuery.trim());
    } else {
      url.searchParams.delete('search');
    }

    if (selectedPod) {
      url.searchParams.set('pod', selectedPod);
    } else {
      url.searchParams.delete('pod');
    }

    if (selectedStage) {
      url.searchParams.set('stage', selectedStage);
    } else {
      url.searchParams.delete('stage');
    }

    if (selectedStatus) {
      url.searchParams.set('status', selectedStatus);
    } else {
      url.searchParams.delete('status');
    }

    if (selectedOrdering) {
      url.searchParams.set('ordering', selectedOrdering);
    } else {
      url.searchParams.delete('ordering');
    }

    goto(url.toString());
  }

  function clearFilters() {
    searchQuery = '';
    selectedPod = '';
    selectedStage = '';
    selectedStatus = '';
    selectedOrdering = '-last_update';

    goto('/venture-list?page=1');
  }
</script>

<!-- Filters -->
<div class="mb-6 rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
  <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
    <!-- Search -->
    <div>
      <label for="search" class="mb-1 block text-sm font-medium text-gray-700">Search</label>
      <input
        id="search"
        type="text"
        bind:value={searchQuery}
        placeholder="Search ventures..."
        class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
      />
    </div>

    <!-- Pod Filter -->
    <div>
      <label for="pod-filter" class="mb-1 block text-sm font-medium text-gray-700">Pod</label>
      <select
        id="pod-filter"
        bind:value={selectedPod}
        class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
      >
        <option value="">All Pods</option>
        {#each uniquePods as pod}
          <option value={pod}>{pod}</option>
        {/each}
      </select>
    </div>

    <!-- Stage Filter -->
    <div>
      <label for="stage-filter" class="mb-1 block text-sm font-medium text-gray-700">Stage</label>
      <select
        id="stage-filter"
        bind:value={selectedStage}
        class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
      >
        <option value="">All Stages</option>
        {#each uniqueStages as stage}
          <option value={stage}>{stage}</option>
        {/each}
      </select>
    </div>

    <!-- Status Filter -->
    <div>
      <label for="status-filter" class="mb-1 block text-sm font-medium text-gray-700">Status</label>
      <select
        id="status-filter"
        bind:value={selectedStatus}
        class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
      >
        <option value="">All Statuses</option>
        {#each uniqueStatuses as status}
          <option value={status}>{formatStatus(status)}</option>
        {/each}
      </select>
    </div>

    <!-- Sort/Order -->
    <div>
      <label for="ordering" class="mb-1 block text-sm font-medium text-gray-700">Sort By</label>
      <select
        id="ordering"
        bind:value={selectedOrdering}
        class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
      >
        <option value="-last_update">Last Updated (Newest)</option>
        <option value="last_update">Last Updated (Oldest)</option>
        <option value="name">Name (A-Z)</option>
        <option value="-name">Name (Z-A)</option>
        <option value="pod">Pod (A-Z)</option>
        <option value="-pod">Pod (Z-A)</option>
        <option value="stage">Stage (A-Z)</option>
        <option value="-stage">Stage (Z-A)</option>
      </select>
    </div>
  </div>

  <!-- Filter Actions -->
  <div class="mt-4 flex gap-2">
    <button
      on:click={applyFilters}
      class="inline-flex items-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:outline-none"
    >
      Apply Filters
    </button>
    <button
      on:click={clearFilters}
      class="inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:outline-none"
    >
      Clear Filters
    </button>
  </div>

  <div class="mt-4 text-sm text-gray-600">
    Showing {ventures.length} of {pagination.count} ventures (Page {pagination.currentPage} of {pagination.totalPages})
  </div>
</div>
