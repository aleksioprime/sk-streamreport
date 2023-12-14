import { isLoggedIn } from "@/middlewares/isLoggedIn";

export const routes = [
    {
      path: "",
      name: "home",
      component: () => import("@/views/HomeView.vue"),
      meta: { 
        layout: "DefaultLayout",
        middlewares: [isLoggedIn],
      },
    },
    {
      path: "/login",
      name: "login",
      component: () => import("@/views/LoginView.vue"),
      meta: { 
        layout: "LoginLayout",
      },
    },
    {
      path: "/profile",
      name: "profile",
      component: () => import("@/views/UserProfileView.vue"),
      meta: { 
        layout: "DefaultLayout",
        middlewares: [isLoggedIn],
      },
    },
    {
      path: "/report/extra",
      name: "reportExtra",
      component: () => import("@/views/ReportExtraView.vue"),
      meta: { 
        layout: "DefaultLayout",
        middlewares: [isLoggedIn],
      },
    },
    {
      path: "/report/teacher",
      name: "reportTeacher",
      component: () => import("@/views/ReportTeacherView.vue"),
      meta: { 
        layout: "DefaultLayout",
        middlewares: [isLoggedIn],
      },
    },
    {
      path: "/report/mentor",
      name: "reportMentor",
      component: () => import("@/views/ReportMentorView.vue"),
      meta: { 
        layout: "DefaultLayout",
        middlewares: [isLoggedIn],
      },
    },
    {
      path: "/unit/pyp",
      name: "unitPyp",
      component: () => import("@/views/UnitPypView.vue"),
      meta: { 
        layout: "DefaultLayout",
        middlewares: [isLoggedIn],
      },
    },
    {
      path: "/unit/pyp/:id",
      name: "unitPypDetail",
      component: () => import("@/views/UnitPypDetail.vue"),
      meta: { 
        layout: "DefaultLayout",
        middlewares: [isLoggedIn],
      },
    },
]