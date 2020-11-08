<template>
    <div>
        <v-card-title class="header">{{this.$store.state.selected.display_name}}</v-card-title>
        <v-divider></v-divider>
        <div v-if="check_status() == 'complete'">
            この予防接種は完了しています。
        </div>
        <div v-if="check_status() == 'nothing'">
            <v-card-subtitle>予防接種を予約した日付を入力してください。</v-card-subtitle>
            <v-date-picker 
                full-width
                v-model="selected_date"></v-date-picker>
        </div>
        <div v-if="check_status() == 'reservation'">
            予防接種が完了したら確定ボタンを押してください。
        </div>
    </div>
</template>

<script>
    export default {
        name: 'Form',
        data: () => ({}),
        methods: {
            check_status(){
                return this.$store.state.selected.my.status;
            }
        },
        computed: {
            selected_date: {
                get () { return this.$store.state.selected.my.reservation_date },
                set (val) { this.$store.commit('setReservationDate', val) },
            }
        }
    }
</script>
