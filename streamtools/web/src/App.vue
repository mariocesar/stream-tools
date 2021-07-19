<template>
  <div id="app" class="flex flex-col h-full border border-red-400">
    <div class="flex-grow border border-blue-500">
      "{{messages}}"
      <div class="" v-for="(message, n) in messages" v-bind:key="n">
        {{ message.source }}
        {{ message.author }}
        {{ message.content }}
      </div>
    </div>
    <div class="bg-white h-20 border border-blue-500"></div>
  </div>
</template>

<script>
export default {
  name: "App",
  components: {},
  computed: {
    messages() {
      return this.$store.state.messages;
    }
  }
};
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
}

body {
  height: 100vh;
}
</style>
