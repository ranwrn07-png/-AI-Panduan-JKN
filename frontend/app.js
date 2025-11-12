const metaApi = document.querySelector('meta[name="api-base"]');
const API_BASE = (metaApi && metaApi.content) ? metaApi.content : "http://localhost:8000/api";
let token = null;

function el(id){return document.getElementById(id)}

function toggleRegister(show){
  el('register-area').style.display = show ? 'block' : 'none';
}

el('btn-show-register').onclick = ()=>{ toggleRegister(true); }
el('btn-cancel-register').onclick = ()=>{ toggleRegister(false); }

el('btn-send-code').onclick = async ()=>{
  const email = el('reg-email').value.trim();
  if(!email){ alert('Masukkan email untuk menerima kode verifikasi'); return; }
  el('send-code-status').innerText = 'Mengirim kode...';
  try{
    const resp = await fetch(API_BASE + '/send_verification', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({email})});
    const data = await resp.json();
    if(data.ok){
      if(data.dev_code) el('send-code-status').innerText = 'KODE (dev): ' + data.dev_code;
      else el('send-code-status').innerText = 'Kode verifikasi telah dikirim ke email Anda.';
    }else{
      el('send-code-status').innerText = 'Gagal mengirim kode.';
    }
  }catch(e){ console.error(e); el('send-code-status').innerText = 'Error: ' + e.message }
}

el('btn-verify-register').onclick = async ()=>{
  const email = el('reg-email').value.trim();
  const pass = el('reg-pass').value.trim();
  const code = el('reg-code').value.trim();
  if(!email || !pass || !code){ alert('Email, kode, dan password harus diisi'); return; }
  try{
    const resp = await fetch(API_BASE + '/register', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({email, password: pass, verification_code: code})});
    const data = await resp.json();
    if(data.access_token){ token = data.access_token; localStorage.setItem('jkn_pintar_token', token); toggleRegister(false); afterAuth(); appendMessage('Selamat datang! Akun berhasil dibuat.', 'bot'); }
    else alert('Daftar gagal: ' + (data.detail || 'Unknown error'))
  }catch(e){console.error(e); alert('Error: ' + e.message)}
}

el('btn-login').onclick = async ()=>{
  const email = el('login-email').value.trim();
  const pass = el('login-pass').value.trim();
  if(!email || !pass) { alert('Email dan password harus diisi'); return; }
  try{
    const resp = await fetch(API_BASE + '/login', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({email, password:pass})});
    const data = await resp.json();
    if(data.access_token){ token = data.access_token; localStorage.setItem('jkn_pintar_token', token); afterAuth(); appendMessage('Login berhasil! Selamat datang kembali.', 'bot'); }
    else alert('Login gagal: ' + (data.detail || 'Email atau password salah'))
  }catch(e){console.error(e); alert('Error: ' + e.message)}
}

function afterAuth(){
  el('auth-area').style.display='none';
  el('link-area').style.display='block';
  el('chat-controls').style.display='block';
}

function beforeAuth(){
  el('auth-area').style.display='block';
  el('link-area').style.display='none';
  el('chat-controls').style.display='none';
  el('messages').innerHTML='';
  token = null;
}

el('btn-link').onclick = async ()=>{
  const jkn = el('jkn-id').value.trim();
  if(!jkn) { alert('JKN ID harus diisi'); return; }
  try{
    const resp = await fetch(API_BASE + '/link-jkn', {method:'POST', headers:{'Content-Type':'application/json','Authorization':'Bearer '+token}, body: JSON.stringify({jkn_id: jkn})});
    const data = await resp.json();
    if(data.ok) { alert('Akun JKN berhasil terlink!'); el('jkn-id').value=''; el('link-area').style.display='none'; }
    else alert('Link gagal: ' + (data.detail || 'Unknown'))
  }catch(e){console.error(e); alert('Error: ' + e.message)}
}

el('btn-skip').onclick = ()=>{
  el('link-area').style.display='none';
}

el('btn-logout').onclick = ()=>{
  if(confirm('Yakin ingin logout?')) { beforeAuth(); alert('Anda telah logout'); }
}

el('btn-send').onclick = async ()=>{
  const msg = el('message').value.trim();
  if(!msg) return;
  appendMessage(msg, 'user');
  el('message').value='';
  try{
    const resp = await fetch(API_BASE + '/chat', {method:'POST', headers:{'Content-Type':'application/json','Authorization':'Bearer '+token}, body: JSON.stringify({message: msg})});
    const data = await resp.json();
    appendMessage(data.answer, 'bot');
    if(data.sources && data.sources.length > 0) {
      const srcText = 'Sumber: ' + data.sources.map(s => s.title).join(', ');
      appendMessage(srcText, 'bot');
    }
  }catch(e){console.error(e); appendMessage('Gagal menghubungi server: ' + e.message, 'bot')}
}

function appendMessage(text, who){
  const d = document.createElement('div'); d.className = 'message ' + (who==='user'?'user':'bot'); d.innerText = text; el('messages').appendChild(d); el('chatbox').scrollTop = el('chatbox').scrollHeight;
}

// Load token dari localStorage jika ada (optional)
window.onload = ()=>{
  const savedToken = localStorage.getItem('jkn_pintar_token');
  if(savedToken) { token = savedToken; afterAuth(); appendMessage('Anda sudah login. Silakan mulai bertanya!', 'bot'); }
}
