<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="4">
        <v-card @click="$router.push('vaccination')">予防接種</v-card>
      </v-col>
      <v-col cols="4">
        <v-card @click="$router.push('about')">ヘルプ</v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: 'Home',
    data: () => ({
    }),
  }
</script>
