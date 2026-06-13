# 代码扫描报告

**时间**: 2026-06-13T19:00:22.194Z
**项目**: C:\Users\ADMIN\.gbt

## 摘要
| 严重度 | 数量 |
|--------|------|
| 🔴 High | 12 |
| 🟠 Medium | 2 |
| 🟡 Low | 24 |
| 🔵 Info | 16 |
| **总计** | **54** |

## 发现列表
- **[MEDIUM]** `desktop\noVNC\app\ui.js:1188` — 直接设置 innerHTML 可能导致 XSS
  ```
  document.getElementById('noVNC_fingerprint').innerHTML = fingerprint;
  ```
- **[MEDIUM]** `desktop\noVNC\core\util\browser.js:15` — 代码中残留 debugger 语句
  ```
  // requried for Chrome debugger
  ```
- **[LOW]** `artwork\draw_1781248614800.js:53` — 生产代码中残留 console.log
  ```
  console.log('OK');
  ```
- **[LOW]** `desktop\noVNC\app\ui.js:974` — 使用了已废弃的 API / 属性
  ```
  Log.Debug(">> UI.clipboardReceive: " + e.detail.text.substr(0, 40) + "...");
  ```
- **[LOW]** `desktop\noVNC\app\ui.js:981` — 使用了已废弃的 API / 属性
  ```
  Log.Debug(">> UI.clipboardSend: " + text.substr(0, 40) + "...");
  ```
- **[LOW]** `desktop\noVNC\core\input\keyboard.js:73` — 使用了已废弃的 API / 属性
  ```
  if (e.keyIdentifier.substr(0, 2) !== 'U+') {
  ```
- **[LOW]** `desktop\noVNC\core\input\keyboard.js:77` — 使用了已废弃的 API / 属性
  ```
  const codepoint = parseInt(e.keyIdentifier.substr(2), 16);
  ```
- **[LOW]** `desktop\noVNC\core\rfb.js:1718` — 使用了已废弃的 API / 属性
  ```
  bytesResult.push(parseInt(hexResult.substr(c, 2), 16));
  ```
- **[LOW]** `desktop\noVNC\tests\assertions.js:21` — 生产代码中残留 console.log
  ```
  console.log("expected data: %o, actual data: %o", targetData, data);
  ```
- **[LOW]** `desktop\noVNC\tests\assertions.js:46` — 生产代码中残留 console.log
  ```
  console.log("expected data: %o, actual data: %o", targetData, data);
  ```
- **[LOW]** `desktop\noVNC\utils\convert.js:98` — 生产代码中残留 console.log
  ```
  console.log(`Writing ${outPath}`);
  ```
- **[LOW]** `desktop\noVNC\utils\convert.js:109` — 生产代码中残留 console.log
  ```
  console.log(`  and ${outPath}.map`);
  ```
- **[LOW]** `desktop\noVNC\utils\convert.js:136` — 生产代码中残留 console.log
  ```
  console.log(`Removing ${paths.libDirBase}`);
  ```
- **[LOW]** `desktop\noVNC\utils\genkeysymdef.js:30` — 生产代码中残留 console.log
  ```
  console.log("Error: No filename specified\n");
  ```
- **[LOW]** `desktop\noVNC\utils\genkeysymdef.js:34` — 生产代码中残留 console.log
  ```
  console.log("Parses a *nix keysymdef.h to generate Unicode code point mappings");
  ```
- **[LOW]** `desktop\noVNC\utils\genkeysymdef.js:35` — 生产代码中残留 console.log
  ```
  console.log("Usage: node parse.js [options] filename:");
  ```
- **[LOW]** `desktop\noVNC\utils\genkeysymdef.js:36` — 生产代码中残留 console.log
  ```
  console.log("  -h [ --help ]                 Produce this help message");
  ```
- **[LOW]** `desktop\noVNC\utils\genkeysymdef.js:37` — 生产代码中残留 console.log
  ```
  console.log("  filename                      The keysymdef.h file to parse");
  ```
- **[LOW]** `desktop\noVNC\utils\genkeysymdef.js:127` — 生产代码中残留 console.log
  ```
  console.log(out);
  ```
- **[LOW]** `gbt-brain-compressor.js:23` — 生产代码中残留 console.log
  ```
  console.log('[' + ts + '] [compressor] ' + msg);
  ```
- **[LOW]** `gbt-brain-compressor.js:151` — 生产代码中残留 console.log
  ```
  console.log(JSON.stringify(result));
  ```
- **[LOW]** `gbt-brain-loop.js:23` — 生产代码中残留 console.log
  ```
  console.log(line);
  ```
- **[LOW]** `gbt-brain-new.js:32` — 生产代码中残留 console.log
  ```
  function log(msg) { const ts = new Date().toISOString().slice(0, 19).replace('T', ' '); const line = `[${ts}] ${msg}`; c
  ```
- **[LOW]** `gbt-brain-new.js:70` — 使用了已废弃的 API / 属性
  ```
  const req = https.request({ hostname: url.hostname, path: url.pathname, method: 'POST', headers: { 'Content-Type': 'appl
  ```
- **[LOW]** `gbt-brain.js:32` — 生产代码中残留 console.log
  ```
  function log(msg) { const ts = new Date().toISOString().slice(0, 19).replace('T', ' '); const line = `[${ts}] ${msg}`; c
  ```
- **[LOW]** `gbt-brain.js:70` — 使用了已废弃的 API / 属性
  ```
  const req = https.request({ hostname: url.hostname, path: url.pathname, method: 'POST', headers: { 'Content-Type': 'appl
  ```
- **[INFO]** `artwork\draw_1781248614800.js:52` — 同步 I/O 可能阻塞事件循环
  ```
  fs.writeFileSync('artwork.png', canvas.toBuffer('image/png'));
  ```
- **[INFO]** `desktop\noVNC\utils\genkeysymdef.js:41` — 同步 I/O 可能阻塞事件循环
  ```
  const buf = fs.readFileSync(filename);
  ```
- **[INFO]** `gbt-brain-compressor.js:66` — 同步 I/O 可能阻塞事件循环
  ```
  mem = JSON.parse(fs.readFileSync(MEM, 'utf-8'));
  ```
- **[INFO]** `gbt-brain-compressor.js:106` — 同步 I/O 可能阻塞事件循环
  ```
  fs.writeFileSync(MEM, JSON.stringify(mem, null, 2), 'utf-8');
  ```
- **[INFO]** `gbt-brain-new.js:21` — 同步 I/O 可能阻塞事件循环
  ```
  const p = JSON.parse(fs.readFileSync(pf, 'utf-8'));
  ```
- **[INFO]** `gbt-brain-new.js:34` — 同步 I/O 可能阻塞事件循环
  ```
  function sh(cmd, timeout = 5000) { try { return execSync(cmd, { encoding: 'utf-8', timeout, stdio: 'pipe' }).trim(); } c
  ```
- **[INFO]** `gbt-brain-new.js:42` — 同步 I/O 可能阻塞事件循环
  ```
  try { const vf = path.join(GBT, 'VULN-FINDINGS.json'); if (fs.existsSync(vf)) { const v = JSON.parse(fs.readFileSync(vf,
  ```
- **[INFO]** `gbt-brain-new.js:103` — 同步 I/O 可能阻塞事件循环
  ```
  const o = execSync(c.cmd, { encoding: 'utf-8', timeout: 60000, stdio: 'pipe', cwd: GBT }).trim().slice(0, 200);
  ```
- **[INFO]** `gbt-brain-new.js:109` — 同步 I/O 可能阻塞事件循环
  ```
  function loadMem() { try { return fs.existsSync(MEM_FILE) ? JSON.parse(fs.readFileSync(MEM_FILE, 'utf-8')) : { cycles: [
  ```
- **[INFO]** `gbt-brain-new.js:110` — 同步 I/O 可能阻塞事件循环
  ```
  function saveMem(m) { try { fs.writeFileSync(MEM_FILE, JSON.stringify(m, null, 2)); } catch {} }
  ```
- **[INFO]** `gbt-brain.js:21` — 同步 I/O 可能阻塞事件循环
  ```
  const p = JSON.parse(fs.readFileSync(pf, 'utf-8'));
  ```
- **[INFO]** `gbt-brain.js:34` — 同步 I/O 可能阻塞事件循环
  ```
  function sh(cmd, timeout = 5000) { try { return execSync(cmd, { encoding: 'utf-8', timeout, stdio: 'pipe' }).trim(); } c
  ```
- **[INFO]** `gbt-brain.js:42` — 同步 I/O 可能阻塞事件循环
  ```
  try { const vf = path.join(GBT, 'VULN-FINDINGS.json'); if (fs.existsSync(vf)) { const v = JSON.parse(fs.readFileSync(vf,
  ```
- **[INFO]** `gbt-brain.js:103` — 同步 I/O 可能阻塞事件循环
  ```
  const o = execSync(c.cmd, { encoding: 'utf-8', timeout: 60000, stdio: 'pipe', cwd: GBT }).trim().slice(0, 200);
  ```
- **[INFO]** `gbt-brain.js:109` — 同步 I/O 可能阻塞事件循环
  ```
  function loadMem() { try { return fs.existsSync(MEM_FILE) ? JSON.parse(fs.readFileSync(MEM_FILE, 'utf-8')) : { cycles: [
  ```
- **[INFO]** `gbt-brain.js:110` — 同步 I/O 可能阻塞事件循环
  ```
  function saveMem(m) { try { fs.writeFileSync(MEM_FILE, JSON.stringify(m, null, 2)); } catch {} }
  ```
- **[HIGH]** `desktop\noVNC\tests\test.rfb.js:298` — 硬编码密码
  ```
  client.sendCredentials({ password: 'pass' });
  ```
- **[HIGH]** `desktop\noVNC\tests\test.rfb.js:299` — 硬编码密码
  ```
  expect(client._rfbCredentials).to.deep.equal({ password: 'pass' });
  ```
- **[HIGH]** `desktop\noVNC\tests\test.rfb.js:304` — 硬编码密码
  ```
  client.sendCredentials({ password: 'pass' });
  ```
- **[HIGH]** `desktop\noVNC\tests\test.rfb.js:1248` — 硬编码密码
  ```
  client._rfbCredentials = { password: 'passwd' };
  ```
- **[HIGH]** `desktop\noVNC\tests\test.rfb.js:1261` — 硬编码密码
  ```
  client._rfbCredentials = { password: 'passwd' };
  ```
- **[HIGH]** `desktop\noVNC\tests\test.rfb.js:1287` — 硬编码密码
  ```
  client._rfbCredentials = { password: 'password'};
  ```
- **[HIGH]** `desktop\noVNC\tests\test.rfb.js:1296` — 硬编码密码
  ```
  password: 'password' };
  ```
- **[HIGH]** `desktop\noVNC\tests\test.rfb.js:1401` — 硬编码密码
  ```
  password: 'password123456' };
  ```
- **[HIGH]** `desktop\noVNC\tests\test.rfb.js:1423` — 硬编码密码
  ```
  password: 'password' };
  ```
- **[HIGH]** `desktop\noVNC\tests\test.rfb.js:1454` — 硬编码密码
  ```
  password: 'password' };
  ```
- **[HIGH]** `desktop\noVNC\tests\test.rfb.js:1628` — 硬编码密码
  ```
  client._rfbCredentials = { username: 'username', password: 'password' };
  ```
- **[HIGH]** `desktop\noVNC\tests\test.rfb.js:1674` — 硬编码密码
  ```
  client._rfbCredentials = { username: 'a'.repeat(300), password: 'a'.repeat(300) };
  ```
