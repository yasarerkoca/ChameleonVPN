import React from "react";
export default function Home() {
  return (
    <div>
      <h2>VPN’e Hoşgeldin</h2>
      <div className="vpn-status">Durum: <b>Bağlı değil</b></div>
      <button className="connect-btn">Bağlan</button>
      <div style={{marginTop: 32}}>
        <h3>Kota: <span>10 GB / 100 GB</span></h3>
      </div>
    </div>
  );
}
