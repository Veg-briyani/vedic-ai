<script lang="ts">
  import { onMount } from 'svelte';
  import RuleCard from './lib/RuleCard.svelte';
  import axios from 'axios';

  let rules: any[] = [];

  onMount(async () => {
    const { data } = await axios.get('http://127.0.0.1:8000/rules');
    rules = data.rules;
  });
</script>

<h1>Vedic AI Rules</h1>
{#each rules as r (r.id)}
  <RuleCard rule={r} />
{/each}

<style>
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style>
