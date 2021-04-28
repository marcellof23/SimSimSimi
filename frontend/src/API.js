function parseTanggal(text) {
  var date = new Date(text);
  var tahun = date.getFullYear();
  var bulan = date.getMonth();
  var tanggal = date.getDate();
  var hari = date.getDay();
  var jam = date.getHours();
  var menit = date.getMinutes();
  var detik = date.getSeconds();
  switch(hari) {
    case 0: hari = "Minggu"; break;
    case 1: hari = "Senin"; break;
    case 2: hari = "Selasa"; break;
    case 3: hari = "Rabu"; break;
    case 4: hari = "Kamis"; break;
    case 5: hari = "Jum'at"; break;
    case 6: hari = "Sabtu"; break;
    default:
      hari = "unknown"; break;
  }
  switch(bulan) {
    case 0: bulan = "Januari"; break;
    case 1: bulan = "Februari"; break;
    case 2: bulan = "Maret"; break;
    case 3: bulan = "April"; break;
    case 4: bulan = "Mei"; break;
    case 5: bulan = "Juni"; break;
    case 6: bulan = "Juli"; break;
    case 7: bulan = "Agustus"; break;
    case 8: bulan = "September"; break;
    case 9: bulan = "Oktober"; break;
    case 10: bulan = "November"; break;
    case 11: bulan = "Desember"; break;
    default:
      hari = "unknown"; break;
  }
  var ans = hari + ", " + tanggal + " " + bulan + " " + tahun;
  ans  = ans + " "+ ((jam < 10)?"0":"") + jam + ":" + ((menit < 10)?"0":"") + menit + ":" + ((detik < 10)?"0":"") + detik;
  return ans;
};

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
            resolve(data.message)
          }
          else if (data.id === 1) {
            resolve(data.message)
          }
          else if (data.id === 2) {
            let answer = "";
            if (data.message !== 'naon') {
              answer = data.message;
            }
            else {
              answer ="[DEADLINE]\n"+data.item.map( (a, i) => `${i+1}. ${a.jenis_task} - ${a.kode_matkul} - ${a.topik} - ${parseTanggal(a.tanggal)}`).join('\n');
              parseTanggal(data.item[0].tanggal);
              if (data.item.length < 1) {
                answer = "Tidak ada deadline! Silahkan bermain :)"
              }
            }
            resolve(answer);
          }
          else if (data.id === 3) {
            let answer ="[DEADLINE]\n"+data.item.map( (a, i) => `${i+1}. ${a.jenis_task} - ${a.kode_matkul} - ${a.topik} - ${parseTanggal(a.tanggal)}`).join('\n');
            parseTanggal(data.item[0].tanggal);
            if (data.item.length < 1) {
              answer = "Tidak ada deadline! Silahkan bermain :)"
            }
            resolve(answer);
          }
          else if (data.id === 4) {
            resolve(data.message);
          }
           else if (data.id === 5) {
            resolve(data.message);
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
  