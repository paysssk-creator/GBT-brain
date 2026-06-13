# 代码扫描报告

**时间**: 2026-06-13T14:02:19.789Z
**项目**: C:\Users\ADMIN\.gbt

## 摘要
| 严重度 | 数量 |
|--------|------|
| 🔴 High | 12 |
| 🟠 Medium | 2 |
| 🟡 Low | 17 |
| 🔵 Info | 2 |
| **总计** | **33** |

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
- **[INFO]** `artwork\draw_1781248614800.js:52` — 同步 I/O 可能阻塞事件循环
  ```
  fs.writeFileSync('artwork.png', canvas.toBuffer('image/png'));
  ```
- **[INFO]** `desktop\noVNC\utils\genkeysymdef.js:41` — 同步 I/O 可能阻塞事件循环
  ```
  const buf = fs.readFileSync(filename);
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
