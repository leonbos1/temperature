import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core';
import { faChevronRight, faChevronLeft, faAnglesRight, faAnglesLeft, faHouse, faRightFromBracket, faTrashCan, faPen, faCalendarDays, faLocationDot } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';


library.add(
    faChevronRight,
    faChevronLeft,
    faAnglesRight,
    faAnglesLeft,
    faHouse,
    faRightFromBracket,
    faTrashCan,
    faPen,
    faCalendarDays,
    faLocationDot,
);

createApp(App)
    .component('font-awesome-icon', FontAwesomeIcon)
    .use(router)
    .mount('#app')
