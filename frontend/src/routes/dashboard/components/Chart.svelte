<script>
  import BarChart from './BarChart.svelte';
  import PieChart from './PieChart.svelte';
  import ScatterChart from './ScatterChart.svelte';

  /** @type {any[]} */
  export let data = [];
  /** @type {string} */
  export let chartType = 'bar'; // 'bar', 'pie', 'scatter'
  /** @type {string} */
  export let dataKey = 'stage'; // 'stage', 'status', 'pod', 'metrics'

  // Responsive width/height
  let width = 0;
  let height = 0;
  let chartContainer;

  import { onMount } from 'svelte';
  onMount(() => {
    if (chartContainer) {
      width = chartContainer.clientWidth;
      height = chartContainer.clientHeight;
    }
    // Optionally, listen for resize events
    window.addEventListener('resize', updateSize);
    updateSize();
    return () => window.removeEventListener('resize', updateSize);
  });

  function updateSize() {
    if (chartContainer) {
      width = chartContainer.clientWidth;
      height = chartContainer.clientHeight;
    }
  }

  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  /**
   * @param {CustomEvent} event
   */
  function handleFilter(event) {
    dispatch('filter', event.detail);
  }
</script>

<div bind:this={chartContainer} class="w-full h-full">
  {#if chartType === 'bar'}
    <BarChart {data} {dataKey} {width} {height} on:filter={handleFilter} />
  {:else if chartType === 'pie'}
    <PieChart {data} {dataKey} {width} {height} on:filter={handleFilter} />
  {:else if chartType === 'scatter'}
    <ScatterChart {data} {width} {height} />
  {/if}
</div>
