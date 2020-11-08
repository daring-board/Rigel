<template>
    <v-container>
        <v-row>
            <v-col
                cols="12"
                md="4"
            >
                <v-text-field
                    v-model="nickname"
                    :rules="nameRules"
                    :counter="10"
                    label="ニックネーム"
                    required
                ></v-text-field>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-menu
                    ref="menu"
                    v-model="menu"
                    :close-on-content-click="false"
                    transition="scale-transition"
                    offset-y
                    min-width="290px"
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                            v-model="birth_day"
                            :label=display_birth_day
                            prepend-icon="mdi-calendar"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                        ></v-text-field>
                    </template>
                    <v-date-picker
                        ref="picker"
                        v-model="birth_day"
                        :max="new Date().toISOString().substr(0, 10)"
                        min="1950-01-01"
                        @change="save"
                    ></v-date-picker>
                </v-menu>
            </v-col>
        </v-row>
        <v-btn depressed color="primary"
            v-on:click='commit()'
        >
            決定
        </v-btn>
    </v-container>
</template>

<script>
    export default {
        name: 'Registration',
        data: () => ({
            // Name
            valid: false,
            nickname: '',
            nameRules: [
                v => !!v || 'Name is required',
                v => v.length <= 10 || 'Name must be less than 10 characters',
            ],
            //Birth Day
            display_birth_day: "Birthday date",
            birth_day: null,
            menu: false,
        }),
        mounted: function (){
            this.nickname = this.$store.state.personal.nickname;
            this.date = this.$store.state.personal.birth_day;
            if (this.$store.state.personal.birth_day != ''){
                console.log(this.$store.state.personal);
                this.display_birth_day = this.$store.state.personal.birth_day;
                console.log(this.display_birth_day);
            }
        },
        watch: {
            menu (val) {
                val && setTimeout(() => (this.$refs.picker.activePicker = 'YEAR'))
            },
        },
        methods: {
            save (date) {
                this.$refs.menu.save(date)
            },
            commit(){
                this.$store.commit('setPersonal', {
                    'nickname': this.nickname,
                    'birth_day': this.birth_day,
                    'vaccins': {
                        'dummy': {
                        'status': 'complete',
                        'completed_num': 0, 'required': 3,
                        'reservation_date': '2020-11-14'
                        } 
                    }
                });
                this.$router.push('/home');
            }
        },
    }
</script>
