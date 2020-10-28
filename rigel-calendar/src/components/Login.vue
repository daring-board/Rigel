<template>
    <v-container>
        <v-row>
            <div id="firebaseui-auth-container"></div>
        </v-row>
    </v-container>
</template>

<script>
import firebase from 'firebase/app';
import firebaseui from 'firebaseui-ja';
 
export default {
    mounted() {
        var ui = firebaseui.auth.AuthUI.getInstance() || new firebaseui.auth.AuthUI(firebase.auth());
        ui.start('#firebaseui-auth-container',{
            signInOptions: [
                firebase.auth.GoogleAuthProvider.PROVIDER_ID,
            ],
            signInSuccessUrl: '/home',
        });
    },
    methods: {
        logout: function() {
            firebase.auth().signOut().then(
                () => console.log("Sign out.")
            );
        }
    }
}
</Script>