
const API='http://127.0.0.1:8000';
function token(){return localStorage.getItem('token')||'';}
async function api(url,method='GET',body=null){
  const opt={method,headers:{'Authorization':'Bearer '+token()}};
  if(body){opt.headers['Content-Type']='application/json';opt.body=JSON.stringify(body);}
  const r=await fetch(API+url,opt); return r.json();
}
