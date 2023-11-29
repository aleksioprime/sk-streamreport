import axios, { AxiosError } from "axios";
import jwtService from "@/services/jwt/jwt.service";

class ApiError extends Error {
  constructor(message, response) {
    super(message);
    this.response = response;
  }
}

function refreshTokenProcedure() {
  return new Promise((resolve, reject) => {
    axios.post('/api/token/refresh/', {
      refresh: jwtService.getRefreshToken()
    }).then(response => {
      // Сохраняем новый access токен
      jwtService.saveAccessToken(response.data.access);
      resolve(response.data.access);
    }).catch(error => {
      reject(error);
    });
  });
}

export class ApiService {
  constructor() {
    // Добавление перехватчика ответов
    axios.interceptors.response.use(response => {
      // Обработка успешных ответов
      return response;
    }, error => {
      const originalRequest = error.config;
      // Обработка ошибок ответа (ошибка авторизации, повторный запрос, запрос обновления токена)
      if (error.response.status === 401 && !originalRequest._retry && !originalRequest.url.includes("/refresh")) {
        originalRequest._retry = true;
        // Обрабатываем истечение срока действия токена
        return refreshTokenProcedure().then(newAccessToken => {
          // Повторно устанавливаем заголовки и повторяем запрос
          originalRequest.headers['Authorization'] = 'Bearer ' + newAccessToken;
          return axios(originalRequest);
        }).catch(refreshError => {
          // Обработка ошибки обновления токена
          console.error(refreshError);
          // Перенаправление на страницу входа или очистка токенов
          return Promise.reject(refreshError);
        });
      }
      return Promise.reject(this._getError(error));
    });
  }

  _getError(e) {
    if (e instanceof AxiosError) {
      /* Возвращаем ошибку, содержащую сообщение об ошибке и ответ сервера */
      /* Если имеем дело с ошибкой Axios, пытаемся получить сообщение, которое отправил бэкенд */
      return new ApiError(
        e.response.data?.error?.message ?? e.message,
        e.response
      );
    } else {
      /* Возвращаем ошибку, содержащую сообщение об ошибке и ответ сервера */
      return new ApiError(e.message, e.response);
    }
  }

  /* Функция для запросов без тела: GET, DELETE */
  _wrapper1(method, url, config) {
    return async () => {
      try {
        const response = await method(url, config);
        return {
          __state: "success",
          ...response,
        };
      } catch (e) {
        return {
          __state: "error",
          data: this._getError(e),
        };
      }
    };
  }

  /* Функция для запросов с телом: POST, PUT, UPDATE */
  _wrapper2(method, url, payload) {
    return async () => {
      try {
        const response = await method(url, payload);
        return {
          __state: "success",
          ...response,
        };
      } catch (e) {
        return {
          __state: "error",
          data: this._getError(e),
        };
      }
    };
  }

  $get(url, config) {
    return this._wrapper1(axios.get, url, config)();
  }

  $post(url, payload) {
    return this._wrapper2(axios.post, url, payload)();
  }

  $put(url, payload) {
    return this._wrapper2(axios.put, url, payload)();
  }

  $patch(url, payload) {
    return this._wrapper2(axios.patch, url, payload)();
  }

  $delete(url) {
    return this._wrapper1(axios.delete, url)();
  }
}
