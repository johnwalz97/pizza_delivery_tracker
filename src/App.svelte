<script>
  import { Matrix } from 'ml-matrix';

  let rows = 19;
  let columns = 39;
  let moves = [];
  let grid = Array(rows).fill(0).map(() => Array(columns).fill(0));

  grid[Math.floor(rows / 2)][Math.floor(columns / 2)] = 1;

  const enterMoves = () => {
  };
</script>

<!--<label style="display: inline-block;">-->
<!--  Moves-->
<!--  <input style="display: inline-block" bind:value={moves}/>-->
<!--</label>-->
<!--<button on:click={enterMoves}>Reset</button>-->

<svg class="grid">
  {#each grid as row, row_i}
    {#each row as column, col_i}
      <circle
        cx={(col_i + 1) * 40}
        cy={(row_i + 1) * 40}
        r="10"
        stroke="#333"
        stroke-width=".1"
        fill={column ? 'red' : 'lightgray'}
      />
    {/each}
  {/each}
</svg>

<style>
    .grid {
        height: 100%;
        width: 100%;
        position: fixed;
        top: -20px;
        left: -20px;
    }
</style>
