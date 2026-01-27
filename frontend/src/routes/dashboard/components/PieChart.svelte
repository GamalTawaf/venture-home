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
  export let width = 600;
  /** @type {number} */
  export let height = 400;

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
  function createPieChart(data, key) {
    const margin = { top: 20, right: 20, bottom: 80, left: 20 }; // Increased bottom margin for legend
    const radius = Math.min(width, height - 60) / 2 - margin.top; // Reduced height for legend

    const counts = d3.rollup(
      data,
      /** @param {any[]} v */ (v) => v.length,
      /** @param {any} d */ (d) => d[key]
    );
    const dataArray = Array.from(counts, ([key, value]) => ({ key, value }));

    const color = d3.scaleOrdinal(d3.schemeCategory10);

    const svg = d3
      .select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${width / 2},${height / 2 - 20})`); // Move up for legend

    const pie = d3.pie().value(/** @param {any} d */ (d) => d.value);
    const arc = d3.arc().innerRadius(0).outerRadius(radius);

    const arcs = svg.selectAll('arc').data(pie(dataArray)).enter().append('g').attr('class', 'arc');

    arcs
      .append('path')
      .attr('d', arc)
      .attr('fill', /** @param {any} d @param {any} i */ (d, i) => color(i))
      .attr('stroke', 'white')
      .style('stroke-width', '2px')
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
        dispatch('filter', { key: d.data.key, dataKey });
      });

    // Add numbers to slices
    arcs
      .append('text')
      .attr('transform', /** @param {any} d */ (d) => `translate(${arc.centroid(d)})`)
      .attr('text-anchor', 'middle')
      .style('font-size', '14px')
      .style('font-weight', 'bold')
      .style('fill', 'white')
      .text(/** @param {any} d */ (d) => d.data.value);

    // Create legend
    const legend = d3
      .select(container)
      .select('svg')
      .append('g')
      .attr('class', 'legend')
      .attr('transform', `translate(${width / 2 - 100}, ${height - 50})`);

    const legendItems = legend
      .selectAll('.legend-item')
      .data(dataArray)
      .enter()
      .append('g')
      .attr('class', 'legend-item')
      // @ts-ignore
      .attr('transform', (d, i) => `translate(${i * 80}, 0)`);

    // Legend color squares
    legendItems
      .append('rect')
      .attr('width', 12)
      .attr('height', 12)
      // @ts-ignore
      .attr('fill', (d, i) => color(i))
      .attr('rx', 2);

    // Legend text
    legendItems
      .append('text')
      .attr('x', 18)
      .attr('y', 9)
      .style('font-size', '12px')
      .style('fill', '#374151')
      .text(/** @param {any} d */ (d) => formatStatus(d.key));
  }

  onMount(() => {
    if (data.length > 0) {
      createPieChart(data, dataKey);
    }
  });

  $: if (data.length > 0) {
    // Clear previous chart
    d3.select(container).selectAll('*').remove();
    createPieChart(data, dataKey);
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
