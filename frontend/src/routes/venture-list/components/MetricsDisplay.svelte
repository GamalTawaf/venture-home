<script>
  /** @typedef {Object} Metrics
   * @property {number} [burn_rate_monthly]
   * @property {number} [runway_months]
   * @property {number} [pilot_customers]
   * @property {number} [nps_score]
   */

  /** @type {Metrics|null} */
  export let metrics = null;
</script>

{#if metrics}
  <div class="space-y-1">
    {#if metrics.burn_rate_monthly}
      <div class="flex items-center text-xs text-gray-600">
        <span class="font-medium">Burn:</span>
        <span class="ml-1">${metrics.burn_rate_monthly}</span>
      </div>
    {/if}
    {#if metrics.runway_months}
      <div class="flex items-center text-xs text-gray-600">
        <span class="font-medium">Runway:</span>
        <span class="ml-1">{metrics.runway_months}mo</span>
      </div>
    {/if}
    {#if metrics.pilot_customers}
      <div class="flex items-center text-xs text-gray-600">
        <span class="font-medium">Pilots:</span>
        <span class="ml-1">{metrics.pilot_customers}</span>
      </div>
    {/if}
    {#if metrics.nps_score}
      <div class="flex items-center text-xs text-gray-600">
        <span class="font-medium">NPS:</span>
        <span class="ml-1">{metrics.nps_score}</span>
      </div>
    {/if}
  </div>
{:else}
  <span class="text-xs text-gray-400">No metrics</span>
{/if}
