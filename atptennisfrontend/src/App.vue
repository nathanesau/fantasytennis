<template>
  <div id="app">
    <h1>Bracket</h1>
    <Bracket />
  </div>
</template>

<script>
import Bracket from "./components/Bracket.vue";

export default {
  name: "App",
  components: {
    Bracket
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  align-content: center;
  align-items: center;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
