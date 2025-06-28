const { app, BrowserWindow } = require('electron');
function createWindow() {
  const win = new BrowserWindow({ width: 900, height: 680 });
  win.loadFile('public/index.html');
}
app.whenReady().then(createWindow);
