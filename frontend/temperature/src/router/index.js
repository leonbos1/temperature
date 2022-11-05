import { createRouter, createWebHistory } from 'vue-router'
import Manage from '../views/manage.vue'
import Home from '../views/home.vue'
import Login from '../views/login.vue'
import Extra from '../views/extra.vue'

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
        path: '/manage',
        name: 'Manage',
        component: Manage,
        beforeEnter: (_to,_from,next) => {
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