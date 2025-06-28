import React, { useState } from "react";
export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");
  return (
    <div className="login-box">
      <h2>Kullanıcı Girişi</h2>
      <input placeholder="E-posta" value={email} onChange={e => setEmail(e.target.value)} />
      <input type="password" placeholder="Şifre" value={pass} onChange={e => setPass(e.target.value)} />
      <button onClick={onLogin}>Giriş</button>
    </div>
  );
}
