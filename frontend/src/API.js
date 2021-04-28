const API = {
    GetChatbotResponse: async message => {
      let data='';
      if (message !== "hi")
        await fetch('/api/data',{
          method: 'POST',
          headers:{'Content-type':'application/json'},
          body: JSON.stringify(message),
        }).then(r=>r.json()).then(res=>{
          data=res;
          console.log(data);
        });
      
      return new Promise(function(resolve, reject) {
        setTimeout(function() {
          if (message === "hi") {
            resolve("Welcome to SimSimSimibot!");
          }
          else if (data.id === -1) {

          }
          else if (data.id === 1) {
            console.log('1');
          }
          else if (data.id === 2) {
            console.log('2');
          }
          else if (data.id === 3) {
            console.log('3');
          }
          else if (data.id === 4) {
            console.log('4');
          }
           else if (data.id === 5) {
             console.log('5');
           }
          else if (data.id === 6) {
            resolve(data.message);            
          }
          else {
            resolve("echo : " + message);
          } 
        }, 1500);
      });
    }
  };
  
export default API;
  