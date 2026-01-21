<script>
	import { page } from '$app/stores';

	/** @type {import('./$types').PageData} */
	export let data;
</script>

<svelte:head>
	<title>Venture List</title>
	<meta name="description" content="List of ventures" />
</svelte:head>

<div class="venture-list">
	<h1>Venture List</h1>

	{#if data.error}
		<p class="error">Error loading ventures: {data.error}</p>
	{:else if data.ventures.length === 0}
		<p>No ventures found.</p>
	{:else}
		<table>
			<thead>
				<tr>
					<th>ID</th>
					<th>Name</th>
					<th>Pod</th>
					<th>Stage</th>
					<th>Founder</th>
					<th>Status</th>
					<th>Last Update</th>
					<th>Metrics</th>
				</tr>
			</thead>
			<tbody>
				{#each data.ventures as venture}
					<tr>
						<td>{venture.id}</td>
						<td>{venture.name}</td>
						<td>{venture.pod}</td>
						<td>{venture.stage}</td>
						<td>{venture.founder}</td>
						<td>{venture.status}</td>
						<td>{venture.last_update}</td>
						<td>
							{#if venture.metrics}
								<ul>
									{#if venture.metrics.burn_rate_monthly}<li>Burn Rate: ${venture.metrics.burn_rate_monthly}</li>{/if}
									{#if venture.metrics.runway_months}<li>Runway: {venture.metrics.runway_months} months</li>{/if}
									{#if venture.metrics.pilot_customers}<li>Pilot Customers: {venture.metrics.pilot_customers}</li>{/if}
									{#if venture.metrics.nps_score}<li>NPS: {venture.metrics.nps_score}</li>{/if}
								</ul>
							{/if}
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	{/if}
</div>

<style>
	.venture-list {
		padding: 1rem;
	}

	table {
		width: 100%;
		border-collapse: collapse;
		margin-top: 1rem;
	}

	th, td {
		border: 1px solid #ddd;
		padding: 8px;
		text-align: left;
	}

	th {
		background-color: #f2f2f2;
	}

	.error {
		color: red;
	}

	ul {
		margin: 0;
		padding-left: 1rem;
	}
</style>
