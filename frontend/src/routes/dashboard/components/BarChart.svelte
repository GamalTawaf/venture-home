<script>
  // @ts-nocheck
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';
  import * as d3 from 'd3';

  const dispatch = createEventDispatcher();

  /** @type {any[]} */
  export let data = [];
  /** @type {string} */
  export let dataKey = 'stage';
  /** @type {number} */
  export let width = 0;
  /** @type {number} */
  export let height = 0;

  /** @type {HTMLElement | undefined} */
  let container;

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

  /**
   * @param {any[]} data
   * @param {string} key
   */
  function createBarChart(data, key) {
    const margin = { top: 20, right: 30, bottom: 40, left: 90 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    // Count occurrences
    const counts = d3.rollup(
      data,
      /** @param {any[]} v */ (v) => v.length,
      /** @param {any} d */ (d) => d[key]
    );
    const dataArray = Array.from(counts, ([key, value]) => ({ key, value }));

    const svg = d3.select(container).append('svg').attr('width', width).attr('height', height);

    const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`);

    // Scales
    const x = d3
      .scaleLinear()
      .domain([0, d3.max(dataArray, /** @param {any} d */ (d) => d.value)])
      .range([0, innerWidth]);

    const y = d3
      .scaleBand()
      .domain(dataArray.map(/** @param {any} d */ (d) => d.key))
      .range([0, innerHeight])
      .padding(0.1);

    // Bars
    g.selectAll('.bar')
      .data(dataArray)
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', 0)
      .attr('y', /** @param {any} d */ (d) => y(d.key))
      .attr('width', /** @param {any} d */ (d) => x(d.value))
      .attr('height', y.bandwidth())
      .attr('fill', '#3b82f6')
      .attr('rx', 4)
      .style('cursor', 'pointer')
      .style('transition', 'opacity 0.2s')
      // @ts-ignore
      .on('mouseover', function () {
        d3.select(this).style('opacity', 0.7);
      })
      // @ts-ignore
      .on('mouseout', function () {
        d3.select(this).style('opacity', 1);
      })
      // @ts-ignore
      .on('click', function (event, d) {
        dispatch('filter', { key: d.key, dataKey });
      });

    // Axes
    g.append('g')
      .call(d3.axisLeft(y))
      .selectAll('text')
      .style('font-size', '12px')
      .text(/** @param {any} d */ (d) => (dataKey === 'status' ? formatStatus(d) : d));

    g.append('g').attr('transform', `translate(0,${innerHeight})`).call(d3.axisBottom(x).ticks(5));
  }

  onMount(() => {
    if (data.length > 0) {
      createBarChart(data, dataKey);
    }
  });

  $: if (data.length > 0) {
    // Clear previous chart
    d3.select(container).selectAll('*').remove();
    createBarChart(data, dataKey);
  }
</script>

<div bind:this={container} class="chart-container"></div>

<style>
  .chart-container {
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>
