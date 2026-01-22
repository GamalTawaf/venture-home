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
  /** @type {number} */
  export let width = 600;
  /** @type {number} */
  export let height = 400;

  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  /**
   * @param {CustomEvent} event
   */
  function handleFilter(event) {
    dispatch('filter', event.detail);
  }
</script>

{#if chartType === 'bar'}
  <BarChart {data} {dataKey} {width} {height} on:filter={handleFilter} />
{:else if chartType === 'pie'}
  <PieChart {data} {dataKey} {width} {height} on:filter={handleFilter} />
{:else if chartType === 'scatter'}
  <ScatterChart {data} {width} {height} />
{/if}
