import { createRouter, createWebHistory } from 'vue-router'
const routes = [
    {
        path: '/',
        name: 'home',
        component: () => import('@/views/Home.vue')
    },
    {
        path: '/personal',
        name: 'personal',
        component: () => import('@/views/Personal.vue')
    },
    {
        path:'/task',
        name:'Task',
        component:()=> import('@/views/Task.vue')
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
