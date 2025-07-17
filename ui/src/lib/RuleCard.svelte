<script lang="ts">
  import axios from 'axios';
  export let rule: any;
  let rating = 3;

  async function submitFeedback(ruleId: string, score: number) {
    await axios.post('http://127.0.0.1:8000/feedback', { rule_id: ruleId, rating: score });
    alert('Thanks!');
  }
</script>

<article class="rule-card">
  <h3>{rule.id}</h3>
  <p>{rule.original_text}</p>
  <small>Source: {rule.metadata.source_name} · Confidence: {rule.metadata.confidence}</small>

  <div class="feedback">
    <input type="range" min="1" max="5" bind:value={rating} />
    <span>{rating}</span>
    <button on:click={() => submitFeedback(rule.id, rating)}>Rate</button>
  </div>
</article>

<style>
  .rule-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
    background: #3e2a2a;
  }
  .feedback {
    margin-top: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  input[type="range"] {
    width: 100px;
  }
  button {
    background: #6366f1;
    color: #fff;
    border: none;
    border-radius: 4px;
    padding: 0.3rem 0.8rem;
    cursor: pointer;
    font-size: 1rem;
    transition: background 0.2s;
  }
  button:hover {
    background: #4f46e5;
  }
</style> 