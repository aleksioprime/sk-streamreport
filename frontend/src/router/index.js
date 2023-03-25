import { createRouter, createWebHistory } from 'vue-router'
import UserLogin from '@/views/UserLogin.vue'
import DashBoard from '@/views/DashBoard.vue'
import UnitList from '@/views/UnitList.vue'
import UnitMYPView from '@/views/UnitMYPView.vue'
import UserList from '@/views/UserList.vue'
import AssessList from '@/views/AssessList.vue'
import AssessWorkView from '@/views/AssessWorkView.vue'
import AssessPeriodView from '@/views/AssessPeriodView.vue'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: UnitList,
  },
  {
    path: '/login',
    name: 'login',
    component: UserLogin
  },
  {
    path: '/unit',
    name: 'unitlist',
    component: UnitList,
  },
  {
    path: '/unit/:id',
    name: 'unitmypview',
    component: UnitMYPView,
  },
  {
    path: '/user',
    name: 'userlist',
    component: UserList
  },
  {
    path: '/assessment',
    name: 'assesslist',
    component: AssessList,
  },
  {
    path: '/assessment/sumwork/:id_sumwork/class/:id_class',
    name: 'assessworkview',
    component: AssessWorkView,
  },
  {
    path: '/assessment/period/:id_period/subject/:id_subject/class/:id_class',
    name: 'assessperiodview',
    component: AssessPeriodView,
  },
]

const router = createRouter({
  routes,
  history: createWebHistory(),
})

export default router
