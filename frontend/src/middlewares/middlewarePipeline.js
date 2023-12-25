import JwtService from "@/services/jwt/jwt.service";

export const middlewarePipeline = (router) => {
    router.beforeEach(async (to, from) => {
      // if (to.path === '/login' && JwtService.getAccessToken()) {
      //   console.log('Перенаправление обратно на страницу, с которой пользователь пришёл');
      //   // return (from.path); // Перенаправление обратно на страницу, с которой пользователь пришёл
      // }
      const middlewares = to.meta.middlewares;
      if (!middlewares) {
        return true;
      }
      
      for (const middleware of middlewares) {
        const result = await middleware({ to, from });
        if (
          typeof result === "object" ||
          typeof result === "string" ||
          result === false
        ) {
          return result;
        }
      }
      return true;
    });
  };
  