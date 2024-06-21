export const initTelegramAuth = () => {
  return new Promise((resolve, reject) => {
    if (window.Telegram && window.Telegram.WebApp) {
      window.Telegram.WebApp.ready();
      resolve(window.Telegram.WebApp);
    } else {
      reject(new Error("Telegram WebApp is not available"));
    }
  });
};

export const getTelegramAuthData = (webApp) => {
  if (webApp && webApp.initDataUnsafe && webApp.initDataUnsafe.user) {
    return {
      id: webApp.initDataUnsafe.user.id,
      first_name: webApp.initDataUnsafe.user.first_name,
      last_name: webApp.initDataUnsafe.user.last_name,
      username: webApp.initDataUnsafe.user.username,
    };
  }
  return null;
};
