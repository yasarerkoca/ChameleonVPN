import React, { useState } from "react";
export default function ProfileModal({ user, onSave, onClose }) {
  const [email, setEmail] = useState(user.email || "");
  return (
    <div className="modal-bg">
      <div className="modal">
        <h3>Profil Düzenle</h3>
        <input value={email} onChange={e=>setEmail(e.target.value)} />
        <button onClick={()=>onSave({...user, email})}>Kaydet</button>
        <button onClick={onClose}>Kapat</button>
      </div>
    </div>
  );
}
