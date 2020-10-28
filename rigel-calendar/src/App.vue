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
        <v-list-item @click="routing('/home')">
          <v-list-item-icon><v-icon>mdi-home</v-icon></v-list-item-icon>
          <v-list-item-content>ホーム</v-list-item-content>
        </v-list-item>
        <v-list-item @click="vaccination_route()">
          <v-list-item-icon><v-icon>mdi-needle</v-icon></v-list-item-icon>
          <v-list-item-content>予防接種</v-list-item-content>
        </v-list-item>
        <v-list-item @click="routing('/registration')">
          <v-list-item-icon><v-icon>mdi-needle</v-icon></v-list-item-icon>
          <v-list-item-content>お誕生日登録</v-list-item-content>
        </v-list-item>
        <v-list-item @click="routing('/about')">
          <v-list-item-icon><v-icon>mdi-help-box</v-icon></v-list-item-icon>
          <v-list-item-content>ヘルプ</v-list-item-content>
       </v-list-item>
        <v-list-item @click="sign_out()">
          <v-list-item-icon><v-icon>mdi-help-box</v-icon></v-list-item-icon>
          <v-list-item-content>サインアウト</v-list-item-content>
       </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import firebase from 'firebase/app';
import 'firebase/auth'

export default {
  name: 'App',
  data: () => ({
    drawer: false,
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
        this.$router.push({path: `/vaccination/`}).catch(err => {console.log(err)});
      }
    },
    routing(target){
      this.$router.push({path: target}).catch(err => {console.log(err)});
    },
    sign_out(){
      firebase.auth().signOut();
    }
  }
};
</script>
