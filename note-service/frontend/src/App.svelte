<script>
  let items = [
    { id: 1, name: "Apple" },
    { id: 2, name: "Banana" },
    { id: 3, name: "Cherry" },
    { id: 4, name: "Date" },
    { id: 5, name: "Elderberry" }
  ];
  let searchQuery = "";
  let searchResults = [];

  async function filterItems() {
    const response = await fetch(`http://localhost:3000/search?q=${searchQuery}`);
    searchResults = await response.json();
  }
</script>

<style>
  /* Add some basic styling (optional) */
  .search-result { margin-top: 20px; }
  .search-content { margin: 0 10px; padding: 10px; background-color: #EEE;}
</style>

<div>
  <input type="text" bind:value={searchQuery} placeholder="Search from notes...">
  <button on:click={filterItems}>Search</button>
</div>

<div class="search-result">
  {#if searchResults.length > 0}
      {#each searchResults as section}
        <div class="search-result"><h1>{section['path']}</h1>
          {#each section['topics'] as topic}
            <h3>{topic['header']}</h3>
            <!-- <p>{@html topic['content'].replace(/\n/g, '<br>')}</p>-->
            <pre class="search-content">{topic['content']}</pre>
          {/each}
        </div>
      {/each}
  {:else}
    <p>No results found.</p>
  {/if}
</div>
