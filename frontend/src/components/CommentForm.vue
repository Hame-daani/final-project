<template>
  <v-card>
    <v-card-title v-if="!editing"> Comment on this </v-card-title>
    <v-card-title v-else> Edit your comment </v-card-title>
    <v-form ref="form">
      <v-text-field
        label="text"
        v-model="me.text"
        :rules="rules"
        hide-details="auto"
        multi-line
        clearable
        required
      ></v-text-field>
      <v-card-actions>
        <v-btn @click="submit"> Submit </v-btn>
      </v-card-actions>
    </v-form>
  </v-card>
</template>

<script>
export default {
  props: {
    comment: {
      required: false,
      default() {
        return {
          text: "",
        };
      },
    },
  },
  data() {
    return {
      me: { ...this.comment },
      editing: this.comment.text,
      rules: [
        (value) => !!value || "Required.",
        // (value) => (value && value.length >= 3) || "Min 3 characters",
      ],
    };
  },
  methods: {
    submit() {
      if (this.$refs.form.validate()) {
        this.$emit("comment-submitted", this.me.text);
        this.$refs.form.reset();
      }
    },
  },
};
</script>

<style>
</style>