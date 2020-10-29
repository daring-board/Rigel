<template>
    <v-container>
        <v-row>
            <v-col>
                <v-data-table
                    :headers="headers"
                    :items="items"
                    class="elevation-1"
                >
                    <template v-slot:item.required="{ item }">
                        <v-chip
                            :color="(item.required == '定期')? 'green': 'orange'"
                            dark
                        >
                            {{ item.required }}
                        </v-chip>
                    </template>
                    <template v-slot:item.status="{ item }">
                        <v-btn
                            :color="color(item.status)"
                        >{{btnWord(item.status)}}</v-btn>
                    </template>
                </v-data-table>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    export default {
        name: 'List',
        data: () => ({
            items: [],
            headers: [
                {text: '予防接種', value: 'display_name'},
                {text: '接種状況', value: 'state'},
                {text: '間隔日数', value: 'days'},
                {text: '定期or任意', value: 'required'},
                {text: '状態', value: 'status'},
            ]
        }),
        props: ['month'],
        methods: {
            setItems(vaccinations) {
                const keys = Object.keys(vaccinations);
                keys.forEach(k => {
                    let vac = vaccinations[k];
                    let month = parseInt(this.month)+1;
                    if(vac.spans.indexOf(month) < 0){
                        return
                    }
                    if(vac.recommends.indexOf(month) < 0){
                        return
                    }
                    let interval = `${vac.interval.num} ${vac.interval.unit}`;
                    vac.days = interval;
                    vac.state = `0 / ${vac.needed} 回`;
                    vac.required = (vac.required)? '定期': '任意';
                    console.log(this.$store.state.personal)
                    if(k in this.$store.state.personal.status){
                        vac.status = this.$store.state.personal.status[k];
                    }else{
                        vac.status = 'nothing'
                    }
                    this.items.push(vac);
                });
            },
            color(status){
                let color = 'white';
                if(status == 'nothing'){
                    color = '#F8BBD0';
                }else if(status == 'reservation'){
                    color = '#FFFF8D';
                }else if(status == 'complete'){
                    color = '#64FFDA'
                }
                return color;
            },
            btnWord(status){
                let word = '未定義';
                if(status == 'nothing'){
                    word = '何もしていない';
                }else if(status == 'reservation'){
                    word = '予約済み(○月×日)';
                }else if(status == 'complete'){
                    word = '完了'
                }
                return word;
            }
        },
        watch:  {
            month: {
                handler: function(){
                    this.items = [];
                    console.log(this.month)
                    const vaccinations = this.$store.state.vaccinations;
                    console.log(JSON.stringify(vaccinations));
                    if(vaccinations == null){
                        this.$store.commit('getPersonal').then(() => {
                            this.setItems(vaccinations);
                            console.log(this.items);
                        });
                    }else{
                        this.setItems(vaccinations);
                        console.log(this.items);
                    }
                },
                immediate: true
            }
        }
    }
</script>
