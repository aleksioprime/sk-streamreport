let isRefreshing = false;
let subscribers = [];
import jwtService from "@/services/jwt/jwt.service";

function subscribeTokenRefresh(cb) {
  subscribers.push(cb);
}

function onTokenRefreshed(accessToken) {
  subscribers.forEach(cb => cb(accessToken));
  subscribers = [];
}

export async function refreshToken() {
  if (!isRefreshing) {
    isRefreshing = true;
    try {
      const response = await axios.post('/api/token/refresh/',{
        refresh: jwtService.getRefreshToken()
      });
      const newToken = response.data.access;
      isRefreshing = false;
      onTokenRefreshed(newToken);
      return newToken;
    } catch (error) {
      isRefreshing = false;
      throw error;
    }
  }
}

export default {
  refreshToken,
  subscribeTokenRefresh,
};
