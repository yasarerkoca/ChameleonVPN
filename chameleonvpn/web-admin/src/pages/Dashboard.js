import React from "react";
export default function Dashboard() {
  return (
    <div>
      <h2>Yönetim Paneli</h2>
      <div className="cards">
        <div className="card">Aktif Kullanıcı: <b>152</b></div>
        <div className="card">Bağlı Sunucu: <b>7</b></div>
        <div className="card">Trafik (GB): <b>23.2</b></div>
      </div>
      <div className="chart-area">
        <h3>Trafik Grafiği</h3>
        <div className="chart-placeholder">[Grafik Alanı]</div>
      </div>
    </div>
  );
}
