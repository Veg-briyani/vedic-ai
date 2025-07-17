<script>
  import { onMount } from 'svelte';
  let rules = [];
  let error = '';

  onMount(async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/rules');
      if (!response.ok) throw new Error('Failed to fetch rules');
      const data = await response.json();
      rules = data.rules;
    } catch (err) {
      error = err.message;
    }
  });
</script>

<main>
  <h1>Vedic AI Rules</h1>
  {#if error}
    <p style="color: red">{error}</p>
  {:else if rules.length === 0}
    <p>Loading...</p>
  {:else}
    <ul>
      {#each rules as rule (rule.id)}
        <li><strong>{rule.id}</strong>: {rule.original_text}</li>
      {/each}
    </ul>
  {/if}
</main> 