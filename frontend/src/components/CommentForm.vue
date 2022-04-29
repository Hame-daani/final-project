<template>
  <v-card flat style="width: 700px">
    <v-card-title v-if="!editing"> Comment on this </v-card-title>
    <v-card-title v-else> Edit your comment </v-card-title>
    <v-form ref="form" class="pa-5">
      <v-textarea
        label="Write your comment here..."
        v-model="me.text"
        :rules="rules"
        hide-details="auto"
        multi-line
        clearable
        filled
        shaped
      ></v-textarea>
      <v-card-actions class="d-flex justify-end">
        <v-btn @click="cancel" v-if="editing || replying" color="red" icon>
          <v-icon> mdi-cancel </v-icon>
        </v-btn>
        <v-btn @click="submit" color="green" icon>
          <v-icon> mdi-send</v-icon>
        </v-btn>
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
    replying: {
      type: Boolean,
      default: false,
    },
    editing: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      me: { ...this.comment },
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
    cancel() {
      this.$emit("cancel");
      // this.$refs.form.reset();
    },
  },
};
</script>

<style>
</style>