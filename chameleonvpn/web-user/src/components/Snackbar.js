import React from "react";
export default function Snackbar({ msg, onClose }) {
  if (!msg) return null;
  return (
    <div className="snackbar">
      {msg}
      <button onClick={onClose} style={{marginLeft:12}}>Kapat</button>
    </div>
  );
}
