<template>
  <v-progress-circular
    indeterminate
    color="red"
    v-if="flag"
  ></v-progress-circular>
</template>

<script>
export default {
  props: { flag: { required: true } },
};
</script>

<style>
</style>