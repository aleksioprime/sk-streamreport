import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/routes";
import { middlewarePipeline } from "@/middlewares/middlewarePipeline";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// import JwtService from "@/services/jwt/jwt.service";
// router.beforeEach((to, from, next) => {
//   if (to.path === '/login') {
//     console.log('Перенаправление обратно на страницу, с которой пользователь пришёл');
//     next(from.path); // Перенаправление обратно на страницу, с которой пользователь пришёл
//   } else {
//     console.log('Продолжаем нормальный маршрут');
//     next(); // Продолжить нормальный маршрут
//   }
// });

middlewarePipeline(router);

export default router;