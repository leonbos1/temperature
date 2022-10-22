import { createRouter, createWebHistory } from 'vue-router'
import Manage from '../views/manage.vue'
import Home from '../views/home.vue'
import Login from '../views/login.vue'
import Extra from '../views/extra.vue'
import Daily from '../views/daily-graph.vue'	
import Weekly from '../views/weekly-graph.vue'	
import Monthly from '../views/monthly-graph.vue'	
const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/extra',
        name: 'Extra',
        component: Extra
    },
    {
        path: '/daily',
        name: 'Daily',
        component: Daily
    },
    {
        path: '/weekly',
        name: 'Weekly',
        component: Weekly
    },
    {
        path: '/monthly',
        name: 'Monthly',
        component: Monthly
    },
    {
        path: '/manage',
        name: 'Manage',
        component: Manage,
        beforeEnter: (_to,_from,next) => {
            //TODO make this safe lol
            if (localStorage.getItem("token")) {
                next()
            }
            else {
                next("/login")
            }
        }
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router