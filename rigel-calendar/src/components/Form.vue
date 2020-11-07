<template>
    <v-container>
        <v-row>
            <v-col>
                {{this.$store.state.selected.display_name}}: {{this.$store.state.selected.status}}
                <div v-if="this.$store.state.selected.status == 'complete'">
                    この予防接種は完了しています。
                </div>
                <div v-if="this.$store.state.selected.status == 'nothing'">
                    予防接種を予約した日付を入力してください。
                </div>
                <div v-if="this.$store.state.selected.status == 'reservation'">
                    予防接種が完了したら確定ボタンを押してください。
                </div>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    export default {
        name: 'Form',
        data: () => ({
            vaccin: null
        }),
    }
</script>
