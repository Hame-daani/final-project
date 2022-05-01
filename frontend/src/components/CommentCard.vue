<template>
  <v-container class="my-5">
    <v-card shaped>
      <v-row>
        <v-col class="pl-7 pt-5" cols="1">
          <v-avatar size="75">
            <router-link :to="{ name: 'profile', params: { id: me.user.id } }">
              <v-img :src="me.user.pic"></v-img>
            </router-link>
          </v-avatar>
        </v-col>
        <v-col class="pa-10" cols="3">
          <v-row>
            <span class="text-h6">
              {{ me.user.first_name }} {{ me.user.last_name }}
            </span>
          </v-row>
          <v-row>
            <span class="text-caption">
              {{ me.created_at | getDate }}
            </span>
          </v-row>
        </v-col>
        <v-col><v-divider vertical></v-divider></v-col>
        <v-col class="pt-7" cols="5">
          <span class="text-body-1" style="white-space: pre-line">
            {{ me.text }}
          </span>
        </v-col>
        <v-col><v-divider vertical></v-divider></v-col>
        <v-col class="pt-7" cols="1">
          <template v-if="isLoggedIn">
            <template v-if="getUser.id === me.user.id">
              <v-row>
                <v-dialog v-model="editing" persistent max-width="700">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn color="info" dark v-bind="attrs" v-on="on" icon>
                      <v-icon> mdi-pencil </v-icon>
                    </v-btn>
                  </template>
                  <comment-form
                    :comment="me"
                    :editing="true"
                    @cancel="editing = false"
                    @comment-submitted="update($event)"
                  />
                </v-dialog>
              </v-row>
              <v-row>
                <v-dialog v-model="deleteDialog" persistent max-width="300">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn color="red" dark v-bind="attrs" v-on="on" icon>
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </template>
                  <v-card>
                    <v-card-title class="text-h5">
                      Deleting this comment
                    </v-card-title>
                    <v-card-text>Are you sure?</v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="green darken-1"
                        text
                        @click="deleteDialog = false"
                      >
                        Cancel
                      </v-btn>
                      <v-btn color="green darken-1" text @click="deleteMe">
                        Yes
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-row>
            </template>
          </template>
        </v-col>
      </v-row>
      <v-row class="pl-5 pb-3 d-flex justify-center">
        <v-btn
          v-if="isLoggedIn && !isLiked"
          color="red"
          @click="likeComment"
          icon
        >
          <v-icon> mdi-heart-outline </v-icon>
        </v-btn>
        <v-btn
          v-if="isLoggedIn && isLiked"
          color="red"
          @click="unlikeComment"
          icon
        >
          <v-icon> mdi-heart </v-icon>
        </v-btn>
        <span class="red--text py-2 mr-15">
          <v-icon v-if="!isLoggedIn" color="red"> mdi-heart </v-icon>
          {{ this.likes.length }} Likes
        </span>
        <v-dialog v-model="replying" persistent max-width="700">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-if="isLoggedIn && !preview"
              class="pl-2"
              color="info"
              dark
              v-bind="attrs"
              v-on="on"
              icon
            >
              <v-icon> mdi-reply </v-icon>
            </v-btn>
          </template>
          <comment-form
            v-if="replying"
            :replying="true"
            @cancel="replying = false"
            @comment-submitted="reply($event)"
          />
        </v-dialog>
      </v-row>
    </v-card>
    <v-expansion-panels inset>
      <v-expansion-panel v-if="this.me.comments.length && !preview">
        <v-expansion-panel-header> Replies </v-expansion-panel-header>
        <v-expansion-panel-content>
          <comment-card
            v-for="comment in me.comments"
            :key="comment.id"
            :comment="comment"
            @comment-deleted="deleteComment($event)"
          />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import CommentForm from "./CommentForm.vue";
import CommentsService from "@/services/CommentsService";
import LikesService from "@/services/LikesService";

export default {
  name: "CommentCard",
  components: { CommentForm },
  props: {
    comment: {
      required: true,
    },
    preview: { required: false, default: false },
  },
  computed: {
    ...mapGetters("auth", ["isLoggedIn", "getUser"]),
    isLiked() {
      return this.likes.find((obj) => obj.user.id === this.getUser.id);
    },
  },
  async created() {
    this.loadLikes();
  },
  data() {
    return {
      me: { ...this.comment },
      likes: [],
      editing: false,
      replying: false,
      deleteDialog: false,
    };
  },
  methods: {
    async loadLikes() {
      return LikesService.getLikes("comments/", this.me.id)
        .then((data) => (this.likes = data))
        .catch((err) => console.log(err.reponse.data));
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
    async deleteMe() {
      this.deleteDialog = false;
      return CommentsService.delete(this.me.id)
        .then(() => this.$emit("comment-deleted", this.me.id))
        .catch((err) => console.log(err.response.data));
    },
    async reply(text) {
      const payload = {
        text: text,
      };
      return CommentsService.addComment(this.me.id, payload)
        .then((data) => this.me.comments.push(data))
        .then(() => (this.replying = false))
        .catch((err) => console.log(err.response.data));
    },
    deleteComment(id) {
      this.me.comments = this.me.comments.filter((obj) => obj.id !== id);
    },
    async likeComment() {
      return LikesService.addLike("comments/", this.me.id)
        .then(() => this.loadLikes())
        .catch((err) => console.log(err.reponse.data));
    },
    async unlikeComment() {
      return LikesService.deleteLike(this.isLiked.id)
        .then(() => this.loadLikes())
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