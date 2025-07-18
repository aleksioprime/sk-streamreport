import axios, { AxiosError } from "axios";
import jwtService from "@/services/jwt/jwt.service";

class ApiError extends Error {
  constructor(message, response) {
    super(message);
    this.response = response;
  }
}

let isRefreshing = false;
let subscribers = [];

function subscribeTokenRefresh(cb) {
  subscribers.push(cb);
}

function onTokenRefreshed(accessToken) {
  subscribers.forEach(cb => cb(accessToken));
  subscribers = [];
}

async function refreshToken() {
  if (!isRefreshing) {
    isRefreshing = true;
    try {
      const response = await axios.post('/api/token/refresh/', {
        refresh: jwtService.getRefreshToken()
      });
      const newToken = response.data.access;
      axios.defaults.headers.common["Authorization"] = newToken ? `Bearer ${newToken}` : "";
      jwtService.saveAccessToken(newToken);
      isRefreshing = false;
      onTokenRefreshed(newToken);
      return newToken;
    } catch (error) {
      isRefreshing = false;
      throw error;
    }
  }
}

export class ApiService {
  constructor() {
    axios.interceptors.response.use(response => response, error => {
      const { config, response } = error;
      const originalRequest = config;
      if (response && response.status === 401 && !originalRequest._retry && !originalRequest.url.includes("/refresh")) {
        originalRequest._retry = true;
        return new Promise((resolve, reject) => {
          subscribeTokenRefresh(newToken => {
            originalRequest.headers['Authorization'] = 'Bearer ' + newToken;
            resolve(axios(originalRequest));
          });

          if (!isRefreshing) {
            refreshToken().catch(refreshError => {
              reject(refreshError);
            });
          }
        });
      }

      return Promise.reject(error);
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
