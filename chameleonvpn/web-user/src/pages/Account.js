import React from "react";
export default function Account({ user, onEdit }) {
  return (
    <div>
      <h2>Hesabım</h2>
      <div>E-Posta: {user.email}</div>
      <div>Paket: {user.package}</div>
      <button onClick={onEdit}>Düzenle</button>
      <button>Çıkış</button>
    </div>
  );
}
