<template>
  <v-card>
    <v-card-title>
      {{ me.user.username }}
    </v-card-title>
    <v-card-subtitle>
      {{ me.created_at | getDate }}
    </v-card-subtitle>
    <v-card-text>
      {{ me.text }}
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    comment: {
      required: true,
    },
  },
  data() {
    return {
      me: { ...this.comment },
    };
  },
  filters: {
    decimalPlace(num) {
      return parseFloat(num).toFixed(2);
    },
    getDate(timestamp) {
      const d = new Date(timestamp);
      return d.toLocaleString();
    },
  },
};
</script>

<style>
</style>