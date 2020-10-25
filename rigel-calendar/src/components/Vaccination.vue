<template>
    <div>
        <v-tabs
            background-color="secondary"
            dark
            next-icon="mdi-arrow-right-bold-box-outline"
            prev-icon="mdi-arrow-left-bold-box-outline"
            show-arrows
        >
            <v-tabs-slider color="cyan"></v-tabs-slider>
            <v-tab
                v-for="i in 24"
                :key="i"
                @click="routing(i)"
                :active="i == month"
            >
                {{ i }}か月
            </v-tab>
        </v-tabs>
        <List :month='month'/>
    </div>
</template>

<script>
    import List from '@/components/List.vue'
    export default {
        name: 'Vaccination',
        components: {List},
        data: () => ({
            items: [],
        }),
        props: ['month'],
        methods: {
            routing(i){
                this.$router.push({path: `/vaccination/${i}`}).catch(err => {console.log(err)});
            }
        }
    }
</script>
