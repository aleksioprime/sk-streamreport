import { createRouter, createWebHistory } from 'vue-router'
import UserLogin from '@/views/UserLogin.vue'
import DashBoard from '@/views/DashBoard.vue'

import AdminEmployee from '@/views/AdminEmployee.vue'
import AdminStudent from '@/views/AdminStudent.vue'
import AdminGroup from '@/views/AdminGroup.vue'
import AdminLoad from '@/views/AdminLoad.vue'
import AdminSyllabus from '@/views/AdminSyllabus.vue'
import UnitMYP from '@/views/UnitMYP.vue'
import UnitMYPView from '@/views/UnitMYPView.vue'
import UnitMYPIDView from '@/views/UnitMYPIDView.vue'
import UnitDP from '@/views/UnitDP.vue'
import UnitDPView from '@/views/UnitDPView.vue'
import ReportTeacher from '@/views/ReportTeacher.vue'
import ReportMentor from '@/views/ReportMentor.vue'
import AssessSchedule from '@/views/AssessSchedule.vue'
import AssessList from '@/views/AssessList.vue'
import AssessWorkView from '@/views/AssessWorkView.vue'
import AssessPeriodView from '@/views/AssessPeriodView.vue'
import ExtraContest from '@/views/ExtraContest.vue'
import ExtraTeaching from '@/views/ExtraTeaching.vue'
import AssessmentGroup from '@/views/AssessmentGroupView.vue'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: DashBoard,
  },
  {
    path: '/login',
    name: 'login',
    component: UserLogin
  },
  {
    path: '/myp',
    name: 'unitmyp',
    component: UnitMYP,
    meta: {
      permissions: ['teacher']
    },
  },
  {
    path: '/myp/:id',
    name: 'unitmypview',
    component: UnitMYPView,
    meta: {
      permissions: ['teacher']
    },
  },
  {
    path: '/myp/idu/:id',
    name: 'unitmypidview',
    component: UnitMYPIDView,
    meta: {
      permissions: ['teacher']
    },
  },
  {
    path: '/dp',
    name: 'unitdp',
    component: UnitDP,
    meta: {
      permissions: ['teacher']
    },
  },
  {
    path: '/dp/:id',
    name: 'unitdpview',
    component: UnitDPView,
    meta: {
      permissions: ['teacher']
    },
  },
  {
    path: '/student',
    name: 'student',
    component: AdminStudent
  },
  {
    path: '/employee',
    name: 'employee',
    component: AdminEmployee
  },
  {
    path: '/group',
    name: 'group',
    component: AdminGroup
  },
  {
    path: '/load',
    name: 'load',
    component: AdminLoad
  },
  {
    path: '/syllabus',
    name: 'syllabus',
    component: AdminSyllabus
  },
  {
    path: '/assessment',
    name: 'assesslist',
    component: AssessList,
  },
  {
    path: '/assessment/group',
    name: 'assessgroup',
    component: AssessmentGroup,
  },
  {
    path: '/schedule',
    name: 'assessSchedule',
    component: AssessSchedule,
  },
  {
    path: '/assessment/sumwork/:id',
    name: 'assessworkview',
    component: AssessWorkView,
  },
  {
    path: '/assessment/group/:id_group/period/:id_period/subject/:id_subject',
    name: 'assessPeriodView',
    component: AssessPeriodView,
  },
  {
    path: '/report/teacher/group/:id_group/subject/:id_subject',
    name: 'reportTeacher',
    component: ReportTeacher,
  },
  {
    path: '/report/mentor/group/:id_group/',
    name: 'reportMentor',
    component: ReportMentor,
  },
  {
    path: '/extra/contest',
    name: 'extraContest',
    component: ExtraContest,
  },
  {
    path: '/extra/teaching',
    name: 'extraTeaching',
    component: ExtraTeaching,
  },
]

const router = createRouter({
  routes,
  history: createWebHistory(),
})

export default router
