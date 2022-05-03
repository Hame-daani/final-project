<template>
  <v-app>
    <v-navigation-drawer permanent app expand-on-hover :mini-variant="true">
      <v-list>
        <v-list-item class="px-2">
          <v-list-item-avatar v-if="isLoggedIn">
            <v-img :src="user.pic"></v-img>
          </v-list-item-avatar>
          <v-list-item-avatar v-else>
            <v-icon>mdi-account</v-icon>
          </v-list-item-avatar>
        </v-list-item>

        <v-list-item link>
          <v-list-item-content v-if="isLoggedIn">
            <v-list-item-title
              class="text-h6 d-flex justify-space-between align-center"
            >
              {{ user.username }}
              <v-btn icon @click="logout">
                <v-icon>mdi-logout</v-icon>
              </v-btn>
            </v-list-item-title>
          </v-list-item-content>
          <v-list-item-content v-else>
            <v-list-item-title
              class="text-h6 d-flex justify-space-between align-center"
            >
              Guest
              <v-btn icon :to="{ name: 'login' }">
                <v-icon>mdi-login</v-icon>
              </v-btn>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list nav dense shaped>
        <v-list-item
          v-for="route in activeRoutes"
          :key="route.path"
          :to="route.path"
        >
          <v-list-item-icon>
            <v-icon>{{ route.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title class="text-capitalize">
            {{ route.name }}
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Sizes your content based upon application components -->
    <v-main style="background-color: #9fa8da">
      <!-- Provides the application the proper gutter -->
      <v-container fluid>
        <router-view :key="$route.fullPath"></router-view>
      </v-container>
    </v-main>

    <v-footer app>
      <!-- -->
    </v-footer>
  </v-app>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "App",

  data() {
    return {
      activeRoutes: this.$router.options.routes.filter((obj) => obj.meta.nav),
    };
  },
  computed: {
    ...mapGetters("auth", { user: "getUser", isLoggedIn: "isLoggedIn" }),
  },
  methods: {
    async logout() {
      return this.$store
        .dispatch("auth/logout")
        .then(() => this.$router.push({ name: "login" }))
        .catch((err) => alert(err.response.data));
    },
  },
};
</script>

<style lang="scss">
</style>
