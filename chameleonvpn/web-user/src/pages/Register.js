import React, { useState } from "react";
export default function Register({ onRegister }) {
  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");
  return (
    <div className="login-box">
      <h2>Kayıt Ol</h2>
      <input placeholder="E-posta" value={email} onChange={e => setEmail(e.target.value)} />
      <input type="password" placeholder="Şifre" value={pass} onChange={e => setPass(e.target.value)} />
      <button onClick={() => onRegister(email, pass)}>Kayıt</button>
    </div>
  );
}
