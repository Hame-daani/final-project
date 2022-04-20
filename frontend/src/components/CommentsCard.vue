<template>
  <v-card v-if="!editing">
    <v-card-title>
      {{ me.user.username }}
    </v-card-title>
    <v-card-subtitle>
      {{ me.created_at | getDate }}
    </v-card-subtitle>
    <v-card-text>
      {{ me.text }}
    </v-card-text>
    <v-card-actions>
      <v-btn
        color="info"
        v-if="isLoggedIn && getUser.id === me.user.id"
        @click="enableEditing"
        >Edit</v-btn
      >
    </v-card-actions>
  </v-card>
  <comment-form
    v-else
    :comment="me"
    @cancel-editing="cancelEditing"
    @comment-submitted="update($event)"
  />
</template>

<script>
import { mapGetters } from "vuex";
import CommentForm from "./CommentForm.vue";
import CommentsService from "@/services/CommentsService";

export default {
  components: { CommentForm },
  props: {
    comment: {
      required: true,
    },
  },
  computed: {
    ...mapGetters("auth", ["isLoggedIn", "getUser"]),
  },
  data() {
    return {
      me: { ...this.comment },
      editing: false,
    };
  },
  methods: {
    enableEditing() {
      this.editing = true;
    },
    cancelEditing() {
      this.editing = false;
    },
    async update(text) {
      const payload = {
        text: text,
      };
      return CommentsService.update(this.me.id, payload)
        .then((data) => (this.me = data))
        .then(() => (this.editing = false))
        .catch((err) => console.log(err.reponse.data));
    },
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