<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
      clippedLeft
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"/>
      <div class="d-flex align-center">
        ライフマネージャー
      </div>
    </v-app-bar>
    <v-navigation-drawer
      dark app clipped bottom temporary v-model="drawer"
    >
      <v-list>
        <v-list-item @click="$router.push('/')">
          <v-list-item-icon><v-icon>mdi-home</v-icon></v-list-item-icon>
          <v-list-item-content>ホーム</v-list-item-content>
        </v-list-item>
        <v-list-item @click="$router.push('vaccination')">
          <v-list-item-icon><v-icon>mdi-needle</v-icon></v-list-item-icon>
          <v-list-item-content>予防接種</v-list-item-content>
        </v-list-item>
        <v-list-item @click="$router.push('about')">
          <v-list-item-icon><v-icon>mdi-help-box</v-icon></v-list-item-icon>
          <v-list-item-content>About</v-list-item-content>
       </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data: () => ({
    drawer: false,
  }),
};
</script>
