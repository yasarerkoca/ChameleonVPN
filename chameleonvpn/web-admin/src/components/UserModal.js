import React from "react";
export default function UserModal({ user, onClose }) {
  return (
    <div className="modal-bg">
      <div className="modal">
        <h3>Kullanıcı Detay</h3>
        <div>ID: {user.id}</div>
        <div>Email: {user.email}</div>
        <div>Admin: {user.is_admin ? "Evet" : "Hayır"}</div>
        <button onClick={onClose}>Kapat</button>
      </div>
    </div>
  );
}
