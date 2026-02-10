<script>
  // @ts-nocheck
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';
  import * as d3 from 'd3';

  const dispatch = createEventDispatcher();

  /** @type {any[]} */
  export let data = [];
  /** @type {number} */
  export let width = 0;
  /** @type {number} */
  export let height = 0;

  /** @type {HTMLElement | undefined} */
  let container;

  /**
   * @param {any[]} data
   */
  function createScatterPlot(data) {
    const margin = { top: 20, right: 30, bottom: 40, left: 60 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    // Filter data with metrics
    const scatterData = data.filter(
      /** @param {any} d */ (d) =>
        d.metrics && d.metrics.burn_rate_monthly && d.metrics.runway_months
    );

    // Create tooltip
    const tooltip = d3
      .select(container)
      .append('div')
      .attr('class', 'tooltip')
      .style('position', 'absolute')
      .style('visibility', 'hidden')
      .style('background-color', 'rgba(0, 0, 0, 0.8)')
      .style('color', 'white')
      .style('padding', '8px')
      .style('border-radius', '4px')
      .style('font-size', '12px')
      .style('pointer-events', 'none')
      .style('z-index', '1000');

    const svg = d3.select(container).append('svg').attr('width', width).attr('height', height);

    const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`);

    // Scales
    const x = d3
      .scaleLinear()
      .domain([0, d3.max(scatterData, /** @param {any} d */ (d) => d.metrics.burn_rate_monthly)])
      .range([0, innerWidth]);

    const y = d3
      .scaleLinear()
      .domain([0, d3.max(scatterData, /** @param {any} d */ (d) => d.metrics.runway_months)])
      .range([innerHeight, 0]);

    // Points
    g.selectAll('.dot')
      .data(scatterData)
      .enter()
      .append('circle')
      .attr('class', 'dot')
      .attr('cx', /** @param {any} d */ (d) => x(d.metrics.burn_rate_monthly))
      .attr('cy', /** @param {any} d */ (d) => y(d.metrics.runway_months))
      .attr('r', 6)
      .attr('fill', '#ef4444')
      .attr('opacity', 0.7)
      .attr('cursor', 'pointer')
      // @ts-ignore
      .on('mouseover', function (event, d) {
        tooltip.style('visibility', 'visible').text(d.name);
      })
      // @ts-ignore
      .on('mousemove', function (event) {
        tooltip.style('top', event.pageY - 10 + 'px').style('left', event.pageX + 10 + 'px');
      })
      .on('mouseout', function () {
        tooltip.style('visibility', 'hidden');
      });

    // Axes
    g.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(d3.axisBottom(x).tickFormat(/** @param {number} d */ (d) => `$${d / 1000}k`));

    g.append('g').call(d3.axisLeft(y));

    svg
      .append('text')
      .attr('x', width / 2)
      .attr('y', height - 5)
      .attr('text-anchor', 'middle')
      .style('font-size', '12px')
      .text('Monthly Burn Rate');

    svg
      .append('text')
      .attr('transform', 'rotate(-90)')
      .attr('x', -height / 2)
      .attr('y', 15)
      .attr('text-anchor', 'middle')
      .style('font-size', '12px')
      .text('Runway (Months)');
  }

  onMount(() => {
    if (data.length > 0) {
      createScatterPlot(data);
    }
  });

  $: if (data.length > 0) {
    // Clear previous chart
    d3.select(container).selectAll('*').remove();
    createScatterPlot(data);
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
