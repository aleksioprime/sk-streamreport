import { isLoggedIn } from "@/middlewares/isLoggedIn";

export const routes = [
    {
      path: "",
      name: "home",
      component: () => import("@/views/HomeView.vue"),
      meta: { 
        middlewares: [isLoggedIn],
      },
    },
    {
      path: "/login",
      name: "login",
      component: () => import("@/views/LoginView.vue"),
    },
]