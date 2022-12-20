import { createRouter, createWebHistory } from 'vue-router'
import ManageTemps from '../views/manage_temps.vue'
import ManageUsers from '../views/manage_users.vue'
import Home from '../views/home.vue'
import Login from '../views/login.vue'	
import ManageSensors from '../views/manage-sensors.vue'
import graph from '../views/graph.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/graphs',
        name: 'graphs',
        component: graph
    },
    {
        path: '/managetemps',
        name: 'ManageTemps',
        component: ManageTemps,
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
        path: '/manageusers',
        name: 'ManageUsers',
        component: ManageUsers,
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
        path: '/managesensors',
        name: 'ManageSensors',
        component: ManageSensors,
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