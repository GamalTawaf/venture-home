<script>
  import Pagination from './Pagination.svelte';
  import MetricsDisplay from './MetricsDisplay.svelte';

  /** @typedef {Object} Pagination
   * @property {string|null} next
   * @property {string|null} previous
   * @property {number} currentPage
   * @property {number} totalPages
   */

  /** @typedef {Object} Venture
   * @property {string} name
   * @property {string} pod
   * @property {string} stage
   * @property {string} founder
   * @property {string} status
   * @property {string} last_update
   * @property {Metrics|null} metrics
   */

  /** @typedef {Object} Metrics
   * @property {number} [burn_rate_monthly]
   * @property {number} [runway_months]
   * @property {number} [pilot_customers]
   * @property {number} [nps_score]
   */

  /**
   * @param {string} status
   */
  function getStatusColor(status) {
    switch (status?.toLowerCase()) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'inactive':
        return 'bg-gray-100 text-gray-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'completed':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }

  /**
   * @param {string} stage
   */
  function getStageColor(stage) {
    switch (stage?.toLowerCase()) {
      case 'idea':
        return 'bg-purple-100 text-purple-800';
      case 'mvp':
        return 'bg-orange-100 text-orange-800';
      case 'growth':
        return 'bg-blue-100 text-blue-800';
      case 'scale':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }

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

  /** @type {Venture[]} */
  export let ventures = [];

  /** @type {Pagination} */
  export let pagination;
</script>

<!-- Table -->
<div class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th
            scope="col"
            class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
            >Name</th
          >
          <th
            scope="col"
            class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
            >Pod</th
          >
          <th
            scope="col"
            class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
            >Stage</th
          >
          <th
            scope="col"
            class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
            >Founder</th
          >
          <th
            scope="col"
            class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
            >Status</th
          >
          <th
            scope="col"
            class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
            >Metrics</th
          >
          <th
            scope="col"
            class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
            >Last Update</th
          >
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-200 bg-white">
        {#each ventures as venture, index}
          <tr class="transition-colors duration-150 hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{venture.name}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{venture.pod}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span
                class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium {getStageColor(
                  venture.stage
                )}"
              >
                {venture.stage}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{venture.founder}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span
                class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium {getStatusColor(
                  venture.status
                )}"
              >
                {formatStatus(venture.status)}
              </span>
            </td>
            <td class="px-6 py-4">
              <MetricsDisplay metrics={venture.metrics} />
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-500">{venture.last_update}</div>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>

<!-- Pagination -->
<Pagination {pagination} />
