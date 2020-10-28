<template>
  <v-container>
    <v-row v-if="is_alert">
      <v-col>
        <v-alert
          border="top"
          color="red lighten-2"
          dark
        >
          お誕生日が登録されていません。
        </v-alert>
      </v-col>
    </v-row>
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
  import firebase from 'firebase/app';
  import 'firebase/auth';

  export default {
    name: 'Home',
    data: () => ({
      is_alert: false
    }),
    created: function() {
      firebase.auth().onAuthStateChanged(user => {
        console.log(user);
        this.$store.commit('getPersonal');
      });
      this.$store.commit('getVaccinations');
    },
    methods: {
      vaccination_route(){
        let today = new Date();
        if(this.$store.state.personal === null){
          // Alart を表示
          console.log('Alartを表示')
          this.is_alert = true;
        }else{
          this.is_alert = false;
          let year = today.getFullYear();
          let month = today.getMonth()+1;
          let birth_info = this.$store.state.personal.birth_day.split('-');
          let year_diff = year - parseInt(birth_info[0], 10);
          let month_diff = year_diff * 12 + month - parseInt(birth_info[1], 10);
          console.log(month_diff);
          console.log(this.$store.state.personal);
          this.$store.commit('setMonth', month_diff-1);
          this.$router.push({path: `/vaccination/`}).catch(err => {console.log(err)});
        }
      }
    }
  }
</script>
