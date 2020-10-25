<template>
    <v-container>
        <v-row>
            <v-col>
                <v-data-table
                    :headers="headers"
                    :items="items"
                    class="elevation-1"
                ></v-data-table>
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
                {text: '定期or任意', value: 'required'}
            ]
        }),
        props: ['month'],
        watch:  {
            month: {
                handler: function(){
                    this.items = [];
                    const vaccinations = this.$store.state.vaccinations;
                    const keys = Object.keys(vaccinations);
                    keys.forEach(k => {
                        let vac = vaccinations[k];
                        let month = parseInt(this.month);
                        if(vac.spans.indexOf(month) < 0){
                            return
                        }
                        if(vac.recommends.indexOf(month) < 0){
                            return
                        }
                        let interval = `${vac.interval.num} ${vac.interval.unit}`;
                        vac.days = interval;
                        vac.state = `${vac.status} 回`
                        this.items.push(vac);
                    });
                    console.log(this.items);
                },
                immediate: true
            }
        }
    }
</script>
