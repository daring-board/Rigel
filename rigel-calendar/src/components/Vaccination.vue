<template>
    <v-container>
        <v-row class="text-center">
            <v-col cols="12">
                <v-timeline dense>
                    <v-timeline-item
                        v-for="(item, i) in items"
                        :key="i"
                        :color="item.color.header"
                        small
                    >
                        <v-card
                            :color="item.color.header"
                            dark
                        >
                            <v-card-title class="title">
                                {{item.month_text}}
                            </v-card-title>
                            <v-card-text class="white text--primary">
                            <v-container>
                                <v-row v-for="(v, j) in item.vaccinations" :key=j>
                                    <v-col><v-btn v-if="checkSpans(i, v.spans)" :color="checkColor(i, v, item.color)">{{v.display_name}} ({{v.status}}/{{v.needed[0]}})</v-btn></v-col>
                                </v-row>
                            </v-container>
                            </v-card-text>
                        </v-card>
                    </v-timeline-item>
                </v-timeline>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    export default {
        name: 'Vaccination',
        data: () => ({
            items: [],
        }),
        mounted: function (){
            for(let i=0;i<=24;i++){
                this.items.push({
                    month: i,
                    month_text: `${i} か月`,
                    vaccinations: {
                        biv: {display_name: 'ビブ', status: 0, needed: [3, 1], required: true, spans:[[2, 7], [12, 21]], recommends: [[2, 3], [3, 4], [4, 5], [12, 15]]},
                        pcv13: {display_name: '肺炎球菌', status: 0, needed: [3, 1], required: true, spans:[[2, 7], [12, 15]], recommends: [[2, 3], [3,4], [4, 5], [12, 15]]},
                        HepatitisB: {display_name: 'B型肺炎', status: 0, needed: [3], required: true, spans:[[2, 9]], recommends: [[2, 3], [3, 4], [7, 8]]}
                    },                    
                    color: {
                        header: 'primary',
                        recommend: 'primary',
                        required: 'cyan',
                        optional: 'yellow',
                        complete: 'grey'
                    },
                })
            }
        },
        methods: {
            checkSpans(now, spans){
                let is_in = false;
                spans.forEach(span => {
                    for(let i = span[0]; i < span[1]; i++){
                        if(i == now) is_in = true;
                    }
                });
                return is_in
            },
            checkColor(now, vaccination, color){
                let is_in = false;
                vaccination.recommends.forEach(span => {
                    for(let i = span[0]; i < span[1]; i++){
                        if(i == now) is_in = true;
                    }
                });
                if (is_in) return color.recommend;

                vaccination.spans.forEach(span => {
                    for(let i = span[0]; i < span[1]; i++){
                        if(i == now) is_in = true;
                    }
                });
                if (is_in) return color.required;
            }
        }
    }
</script>
