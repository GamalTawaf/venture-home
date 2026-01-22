<script>
  import { goto } from '$app/navigation';

  /** @typedef {Object} Pagination
   * @property {string|null} next
   * @property {string|null} previous
   * @property {number} currentPage
   * @property {number} totalPages
   */

  /** @type {Pagination} */
  export let pagination;

  function goToPage(/** @type {number} */ pageNumber) {
    const url = new URL(window.location.href);
    url.searchParams.set('page', pageNumber.toString());
    goto(url.toString());
  }

  function goToNextPage() {
    if (pagination.next) {
      const url = new URL(pagination.next);
      const page = url.searchParams.get('page');
      if (page) {
        goToPage(parseInt(page));
      }
    }
  }

  function goToPreviousPage() {
    if (pagination.previous) {
      const url = new URL(pagination.previous);
      const page = url.searchParams.get('page');
      if (page) {
        goToPage(parseInt(page));
      }
    }
  }
</script>

{#if pagination.totalPages > 1}
  <div
    class="mt-6 flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6"
  >
    <div class="flex flex-1 justify-between sm:hidden">
      {#if pagination.previous}
        <button
          on:click={goToPreviousPage}
          class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Previous
        </button>
      {/if}
      {#if pagination.next}
        <button
          on:click={goToNextPage}
          class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Next
        </button>
      {/if}
    </div>
    <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
      <div>
        <p class="text-sm text-gray-700">
          Showing page <span class="font-medium">{pagination.currentPage}</span> of
          <span class="font-medium">{pagination.totalPages}</span>
        </p>
      </div>
      <div>
        <nav class="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
          {#if pagination.previous}
            <button
              on:click={goToPreviousPage}
              class="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-gray-300 ring-inset hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
            >
              <span class="sr-only">Previous</span>
              <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path
                  fill-rule="evenodd"
                  d="M12.79 5.23a.75.75 0 01-.02 1.06L8.832 10l3.938 3.71a.75.75 0 11-1.04 1.08l-4.5-4.25a.75.75 0 010-1.08l4.5-4.25a.75.75 0 011.06.02z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
          {/if}

          <!-- Page numbers -->
          {#each Array.from({ length: Math.min(5, pagination.totalPages) }, (_, i) => {
            const startPage = Math.max(1, pagination.currentPage - 2);
            return startPage + i;
          }).filter((page) => page <= pagination.totalPages) as pageNumber}
            <button
              on:click={() => goToPage(pageNumber)}
              class="relative inline-flex items-center px-4 py-2 text-sm font-semibold {pageNumber ===
              pagination.currentPage
                ? 'z-10 bg-blue-600 text-white focus:z-20 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600'
                : 'text-gray-900 ring-1 ring-gray-300 ring-inset hover:bg-gray-50 focus:z-20 focus:outline-offset-0'}"
            >
              {pageNumber}
            </button>
          {/each}

          {#if pagination.next}
            <button
              on:click={goToNextPage}
              class="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-gray-300 ring-inset hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
            >
              <span class="sr-only">Next</span>
              <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path
                  fill-rule="evenodd"
                  d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
          {/if}
        </nav>
      </div>
    </div>
  </div>
{/if}
