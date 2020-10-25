<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="4">
        <v-card @click="vaccination_route()">予防接種</v-card>
      </v-col>
      <v-col cols="4">
        <v-card @click="$router.push('registration')">お誕生日登録</v-card>
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
    methods: {
      vaccination_route(){
        let today = new Date();
        if(this.$store.state.personal.birth_day === ''){
          // Alart を表示
          console.log('Alartを表示')
        }else{
          let year = today.getFullYear();
          let month = today.getMonth()+1;
          let birth_info = this.$store.state.personal.birth_day.split('-');
          let year_diff = year - parseInt(birth_info[0], 10);
          let month_diff = year_diff * 12 + month - parseInt(birth_info[1], 10);
          console.log(month_diff);
          console.log(this.$store.state.personal);
          this.$router.push({path: `/vaccination/${month_diff}`}).catch(err => {console.log(err)});
        }
      }
    }
  }
</script>
