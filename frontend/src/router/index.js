import { createRouter, createWebHistory } from 'vue-router'
import UserLogin from '@/views/UserLogin.vue'
import EmployeeBoard from '@/views/EmployeeBoard.vue'
import StudentBoard from '@/views/StudentBoard.vue'
import GroupBoard from '@/views/GroupBoard.vue'

import DashBoard from '@/views/DashBoard.vue'
import UnitList from '@/views/UnitList.vue'
import UnitMYPView from '@/views/UnitMYPView.vue'
// import UserList from '@/views/UserList.vue'
import AssessList from '@/views/AssessList.vue'
import AssessWorkView from '@/views/AssessWorkView.vue'
import AssessPeriodView from '@/views/AssessPeriodView.vue'
import ReportList from '@/views/ReportList.vue'

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
  // {
  //   path: '/user',
  //   name: 'userlist',
  //   component: UserList
  // },
  {
    path: '/student',
    name: 'student',
    component: StudentBoard
  },
  {
    path: '/employee',
    name: 'employee',
    component: EmployeeBoard
  },
  {
    path: '/group',
    name: 'group',
    component: GroupBoard
  },
  {
    path: '/assessment',
    name: 'assesslist',
    component: AssessList,
  },
  {
    path: '/assessment/sumwork/:id',
    name: 'assessworkview',
    component: AssessWorkView,
  },
  {
    path: '/assessment/year/:id_year/period/:id_period/subject/:id_subject',
    name: 'assessperiodview',
    component: AssessPeriodView,
  },
  {
    path: '/report',
    name: 'report',
    component: ReportList,
  },
]

const router = createRouter({
  routes,
  history: createWebHistory(),
})

export default router
