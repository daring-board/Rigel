<template>
    <div>
        <v-tabs
            background-color="secondary"
            dark
            next-icon="mdi-arrow-right-bold-box-outline"
            prev-icon="mdi-arrow-left-bold-box-outline"
            show-arrows
            v-model="$store.state.month"
        >
            <v-tabs-slider color="cyan"></v-tabs-slider>
            <v-tab
                v-for="i in 40"
                :key="i"
                @click="routing(i)"
            >
                {{get_month(i)}}
            </v-tab>
        </v-tabs>
        <v-card
            class="mx-auto"
            outlined
        >
            <v-card-title>{{$store.state.personal.nickname}}の予防接種</v-card-title>
        </v-card>
        <v-divider></v-divider>
        <List :month="$store.state.month"/>
    </div>
</template>

<script>
    import List from '@/components/List.vue'

    export default {
        name: 'Vaccination',
        components: {List},
        data: () => ({}),
        created: function(){
            this.$store.commit('getVaccinations');
        },
        methods: {
            routing(i){
                this.$store.commit('setMonth', i);
            },
            get_month(i){
                let birth_info = this.$store.state.personal.birth_day.split('-');
                let month = parseInt(birth_info[1], 10)+i;
                let year = parseInt(birth_info[0], 10);
                if(month > 12){
                    year = year + Math.floor(month / 12);
                    month = month % 12;
                }
                return `${year}年${month}月`
            }
        }
    }
</script>
