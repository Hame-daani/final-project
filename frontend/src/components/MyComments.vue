<template>
  <v-card>
    <v-card-text> my comments </v-card-text>
  </v-card>
</template>

<script>
export default {
  created() {
    this.signal();
  },
  methods: {
    signal() {
      console.log("my comments");
    },
  },
};
</script>

<style>
</style>