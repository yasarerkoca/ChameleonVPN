import React, { useState } from "react";
export default function ForgotPassword({ onReset }) {
  const [email, setEmail] = useState("");
  return (
    <div className="login-box">
      <h2>Parolamı Unuttum</h2>
      <input placeholder="E-posta" value={email} onChange={e => setEmail(e.target.value)} />
      <button onClick={() => onReset(email)}>Sıfırla</button>
    </div>
  );
}
