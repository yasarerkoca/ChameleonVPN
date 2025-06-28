import React, { useState } from "react";
import { createRoot } from "react-dom/client";

function App() {
  const [page, setPage] = useState("home");
  return (
    <div style={{
      fontFamily: "sans-serif",
      padding: 24,
      background: "#e7ebf0",
      minHeight: "100vh"
    }}>
      <h2>ChameleonVPN Masaüstü</h2>
      <nav>
        <button onClick={() => setPage("home")}>Ana Sayfa</button>
        <button onClick={() => setPage("servers")}>Sunucular</button>
        <button onClick={() => setPage("account")}>Hesap</button>
      </nav>
      {page === "home" && <div>
        <h3>VPN’e Hoşgeldiniz!</h3>
        <button style={{marginTop: 18, fontSize:18}}>Bağlan</button>
        <p>Kota: 10GB / 100GB</p>
      </div>}
      {page === "servers" && <div>
        <h3>Sunucu Listesi</h3>
        <ul>
          <li>Almanya - 1.2.3.4 - <span style={{color:"green"}}>Online</span></li>
          <li>ABD - 5.6.7.8 - <span style={{color:"red"}}>Offline</span></li>
        </ul>
      </div>}
      {page === "account" && <div>
        <h3>Hesap</h3>
        <div>E-posta: user@demo.com</div>
        <div>Paket: Pro</div>
        <button style={{marginTop:10}}>Çıkış</button>
      </div>}
    </div>
  );
}

const root = createRoot(document.getElementById("root"));
root.render(<App />);
