import React from "react";
export default function Servers() {
  return (
    <div>
      <h2>VPN Sunucuları</h2>
      <table>
        <thead>
          <tr><th>Sunucu</th><th>IP</th><th>Durum</th></tr>
        </thead>
        <tbody>
          <tr><td>eu-1</td><td>1.2.3.4</td><td>Online</td></tr>
          <tr><td>us-1</td><td>5.6.7.8</td><td>Offline</td></tr>
        </tbody>
      </table>
    </div>
  );
}
