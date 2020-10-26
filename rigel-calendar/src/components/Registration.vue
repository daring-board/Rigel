<template>
    <v-container>
        <v-row>
            <v-col
                cols="6"
                md="4"
            >
                <v-text-field
                    v-model="last_name"
                    :rules="nameRules"
                    :counter="10"
                    label="姓"
                    required
                ></v-text-field>
            </v-col>
            <v-col
                cols="6"
                md="4"
            >
                <v-text-field
                    v-model="first_name"
                    :rules="nameRules"
                    :counter="10"
                    label="名"
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
            last_name: '', first_name: '',
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
            this.last_name = this.$store.state.personal.last_name;
            this.first_name = this.$store.state.personal.first_name;
            this.date = this.$store.state.personal.birth_day;
            if (this.$store.state.personal.birth_day != ''){
                console.log(this.$store.state.personal);
                this.display_birth_day = this.$store.state.personal.birth_day;
                console.log(this.display_birth_day);
            }
            console.log(this.$store.state.uid)
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
                    'last_name': this.last_name,
                    'first_name': this.first_name,
                    'birth_day': this.birth_day
                });
                this.$router.push('/');
            }
        },
    }
</script>
