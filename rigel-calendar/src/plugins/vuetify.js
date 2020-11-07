import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        themes: {
            light: {
                primary: '#9575CD',
                secondary: '#B39DDB',
                accent: '#bbe2f1',
                error: '#b71c1c',
                info: '#bbe2f1',
                success: '#CFD8DC',
                warning: '#FFC9D2',
                text_default: "#424242"
            },
        },
    },
});
