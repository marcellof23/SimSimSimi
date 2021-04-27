const API = {
    GetChatbotResponse: async message => {
      return new Promise(function(resolve, reject) {
        setTimeout(function() {
          if (message === "hi") resolve("Welcome to SimSimSimibot!");
          else resolve("echo : " + message);
        }, 1500);
      });
    }
  };
  
export default API;
  