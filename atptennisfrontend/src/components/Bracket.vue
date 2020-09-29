<template>
  <div>
    <bracket :rounds="rounds">
      <template #player="{ player }">
        <span v-if="player.id === player.original_id"> {{ player.name }} </span>
        <span v-else> {{ player.name }}* </span>
      </template>
    </bracket>
    <br />
    <table align="center">
      <tr>
        <td>
          <button class="button" @click="resetBracket()">
            Reset Bracket
          </button>
        </td>
        <td>
          <button class="button" @click="saveBracket()">
            Save Bracket
          </button>
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
import Bracket from "vue-tournament-bracket";

export default {
  name: "Example",

  components: {
    Bracket
  },
  data() {
    return {
      rounds: [
        //Semi finals
        {
          games: [
            {
              player1: {
                id: "1",
                original_id: "1",
                name: "Competitor 1",
                original_name: "Competitor 1",
                winner: false
              },
              player2: {
                id: "4",
                original_id: "4",
                name: "Competitor 4",
                original_name: "Competitor 4",
                winner: true
              },
              round_num: 1
            },
            {
              player1: {
                id: "5",
                original_id: "5",
                name: "Competitor 5",
                original_name: "Competitor 5",
                winner: false
              },
              player2: {
                id: "8",
                original_id: "8",
                name: "Competitor 8",
                original_name: "Competitor 8",
                winner: true
              },
              round_num: 1
            }
          ]
        },
        //Final
        {
          games: [
            {
              player1: {
                id: "4",
                original_id: "4",
                name: "Competitor 4",
                original_name: "Competitor 4",
                winner: false
              },
              player2: {
                id: "8",
                original_id: "8",
                name: "Competitor 8",
                original_name: "Competitor 8",
                winner: true
              },
              round_num: 2
            }
          ]
        }
      ]
    };
  },
  methods: {
    resetBracket() {
      for (var round of this.rounds) {
        for (var game of round.games) {
          game.player1.id = game.player1.original_id;
          game.player1.name = game.player1.original_name;
          game.player2.id = game.player2.original_id;
          game.player2.name = game.player2.original_name;
        }
      }
    },
    saveBracket() {}
  }
};
</script>

<style>
.vtb-wrapper {
  display: flex;
  justify-content: center;
}

.button {
  padding: 15px 25px;
  font-size: 12px;
  text-align: center;
  cursor: pointer;
  outline: none;
  color: #fff;
  background-color: #4caf50;
  border: none;
  border-radius: 15px;
  /*box-shadow: 0 9px #999;*/
}

.button:hover {
  background-color: #3e8e41;
}

.button:active {
  background-color: #3e8e41;
  box-shadow: 0 5px #666;
  transform: translateY(2px);
}

td {
  padding: 0 5px;
}
</style>
