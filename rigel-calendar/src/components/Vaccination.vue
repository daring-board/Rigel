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
                v-for="i in 24"
                :key="i"
                @click="routing(i)"
            >
                {{ i }}か月
            </v-tab>
        </v-tabs>
        <List :month="$store.state.month"/>
    </div>
</template>

<script>
    import List from '@/components/List.vue'

    export default {
        name: 'Vaccination',
        components: {List},
        data: () => ({}),
        mounted: function(){
            this.$store.commit('getVaccinations');
        },
        methods: {
            routing(i){
                this.$store.commit('setMonth', i);
                // this.$router.push({path: `/vaccination/`}).catch(err => {console.log(err)});
            }
        }
    }
</script>
