#!/usr/bin/env node
/**
 * ⚕ GBT小土豆全能开发者 — AI自主大脑 v6.0
 * 闭环: 观察→分析→判断→规划→决策→执行→反思→记忆
 * 持续观察系统状态 → DeepSeek思考决策 → 执行动作 → 观察结果 → 循环
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');
const https = require('https');

const GBT = path.join(os.homedir(), '.gbt');
const CLINE = path.join(os.homedir(), '.cline');
const LOG = path.join(GBT, 'brain.log');
const INTERVAL = 60000;

let API_KEY = '', API_BASE = 'https://api.deepseek.com/v1', API_MODEL = 'deepseek-chat';
try {
  const pf = path.join(CLINE, 'data', 'settings', 'providers.json');
  if (fs.existsSync(pf)) {
    const p = JSON.parse(fs.readFileSync(pf, 'utf-8'));
    for (const [, v] of Object.entries(p.providers || {})) {
      if (v.settings?.apiKey) {
        API_KEY = v.settings.apiKey;
        if (v.settings.baseUrl) API_BASE = v.settings.baseUrl;
        if (v.settings.model) API_MODEL = v.settings.model;
      }
    }
  }
} catch {}

function log(msg) { const ts = new Date().toISOString().slice(0, 19).replace('T', ' '); const line = `[${ts}] ${msg}`; console.log(line); fs.appendFileSync(LOG, line + '\n'); }

function sh(cmd, timeout = 5000) { try { return execSync(cmd, { encoding: 'utf-8', timeout, stdio: 'pipe' }).trim(); } catch { return ''; } }

function observe() {
  const s = { ts: new Date().toISOString(), host: os.hostname() };
  const mem = os.freemem() / 1024 / 1024 / 1024, total = os.totalmem() / 1024 / 1024 / 1024;
  s.memory = { freeGB: mem.toFixed(1), totalGB: total.toFixed(1), usagePct: ((1 - mem / total) * 100).toFixed(0) + '%' };
  s.processes = sh('tasklist /FO CSV /NH 2>nul').split('\n').filter(l => l).length;
  s.chromeTabs = sh('tasklist /FI "IMAGENAME eq chrome.exe" /FO CSV /NH 2>nul').split('\n').filter(l => l).length;
  try { const vf = path.join(GBT, 'VULN-FINDINGS.json'); if (fs.existsSync(vf)) { const v = JSON.parse(fs.readFileSync(vf, 'utf-8')); s.lastScan = { total: v.summary?.total || 0, high: v.summary?.high || 0 }; } } catch {}
  try { s.gitDirty = sh('git -C "' + GBT + '" status --porcelain 2>nul').split('\n').filter(l => l).length; } catch { s.gitDirty = 0; }
  return s;
}

const ACTIONS = [
  { id: 'scan', desc: '代码安全扫描', risk: 'low', urgency: 3, cmd: 'node "' + path.join(CLINE, 'scanner.js') + '" --project "' + GBT + '"' },
  { id: 'audit', desc: '项目健康审计', risk: 'low', urgency: 2, cmd: 'node "' + path.join(CLINE, 'audit.js') + '" --project "' + GBT + '"' },
  { id: 'evolve', desc: '自我进化', risk: 'medium', urgency: 2, cmd: 'node "' + path.join(CLINE, 'self-evolve.js') + '" --project "' + GBT + '" --dry-run' },
  { id: 'clean_chrome', desc: '清理Chrome残留', risk: 'low', urgency: 5, cmd: 'taskkill /F /FI "IMAGENAME eq chrome.exe" 2>nul' },
  { id: 'git_backup', desc: '提交未保存改动', risk: 'low', urgency: 4, cmd: 'git -C "' + GBT + '" add -A && git -C "' + GBT + '" commit -m "auto-brain-backup"' },
  { id: 'health', desc: '压力测试体检', risk: 'low', urgency: 1, cmd: 'node "' + path.join(CLINE, 'stress-test.js') + '" --project "' + GBT + '"' },
  { id: 'wait', desc: '等待下一轮', risk: 'none', urgency: 0, cmd: 'echo system healthy' },
  // v6.0 新增工具
  { id: 'auto_fix', desc: '自动修复扫描发现的问题', risk: 'medium', urgency: 4, cmd: 'node "' + path.join(CLINE, 'auto-fix.js') + '" --project "' + GBT + '"' },
  { id: 'self_evolve_live', desc: '自我进化(实跑)', risk: 'high', urgency: 2, cmd: 'node "' + path.join(CLINE, 'self-evolve.js') + '" --project "' + GBT + '"' },
  { id: 'desktop_check', desc: '截屏检查桌面状态', risk: 'low', urgency: 1, cmd: 'node "' + path.join(CLINE, 'desktop-control.js') + '" screen' },
  { id: 'browser_open', desc: '打开浏览器指定页面', risk: 'low', urgency: 1, cmd: 'start "" "http://localhost:6080"' },
  { id: 'notify', desc: '向用户发送通知', risk: 'low', urgency: 1, cmd: 'echo "NOTIFY: Brain cycle complete" > "' + path.join(GBT, 'last-notify.txt') + '"' },
];

const GOALS_FILE = path.join(GBT, 'goals.json');
function loadGoals() { try { return JSON.parse(fs.readFileSync(GOALS_FILE, 'utf-8')); } catch { return { goals: [] }; } }
function checkGoals(s) {
  const g = loadGoals();
  const results = [];
  for (const goal of g.goals || []) {
    let met = true, detail = '';
    if (goal.id === 'g1') { /* 压测6h一次, 由schedule驱动 */ }
    else if (goal.id === 'g2') { met = (s.lastScan?.high || 0) === 0; detail = '高危:' + (s.lastScan?.high || 0); }
    else if (goal.id === 'g4') { met = parseFloat(s.memory?.freeGB || 0) > 2; detail = '空闲:' + (s.memory?.freeGB || 0) + 'GB'; }
    else if (goal.id === 'g5') { met = s.chromeTabs < 15; detail = 'Chrome:' + s.chromeTabs; }
    else if (goal.id === 'g6') { met = s.gitDirty === 0; detail = 'Git未提交:' + s.gitDirty; }
    else if (goal.id === 'g7') { met = (s.lastScan?.high || 0) === 0; detail = '需自愈:' + (!met); }
    if (!met) results.push({ goal: goal.id, title: goal.title, detail, priority: goal.priority });
  }
  return results;
}

function ruleDecide(s) {
  if (parseFloat(s.memory?.freeGB || 99) < 1) return { action: 'clean_chrome', reason: '内存' + s.memory?.freeGB + 'GB' };
  if (s.chromeTabs > 20) return { action: 'clean_chrome', reason: s.chromeTabs + '个Chrome进程' };
  if (s.gitDirty > 3) return { action: 'git_backup', reason: s.gitDirty + '个文件未提交' };
  const h = new Date().getHours();
  if (h === 2 || h === 14) return { action: 'scan', reason: '定时深度扫描' };
  return { action: 'wait', reason: '系统正常' };
}

async function callLLM(prompt) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({ model: API_MODEL, messages: [{ role: 'user', content: prompt }], max_tokens: 200, temperature: 0.3 });
    const url = new URL(API_BASE + '/chat/completions');
    const req = https.request({ hostname: url.hostname, path: url.pathname, method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + API_KEY }, timeout: 30000 }, res => {
      let d = ''; res.on('data', c => d += c); res.on('end', () => {
        try { resolve(JSON.parse(d).choices[0].message.content); } catch { reject(new Error('parse fail')); }
      });
    });
    req.on('error', reject); req.write(body); req.end();
  });
}

async function think(s) {
  if (!API_KEY) { log('BRAIN: 无API Key,规则决策'); return ruleDecide(s); }
  const caps = ACTIONS.map(c => `- ${c.id}: ${c.desc}`).join('\n');
  const p = `你是GBT小土豆的AI大脑。观察系统决定行动。\n【状态】内存:${s.memory?.freeGB}GB/${s.memory?.totalGB}GB(${s.memory?.usagePct}) Chrome:${s.chromeTabs} 进程:${s.processes} 扫描问题:${s.lastScan?.total||0} Git未提交:${s.gitDirty}\n【可做】\n${caps}\n【规则】内存<1GB→clean_chrome Chrome>20→clean_chrome Git>3→git_backup 超过6h没扫→scan 否则→wait\n输出JSON:{"action":"id","reason":"理由"}`;
  try {
    const r = await callLLM(p);
    let j = {};
    try { j = JSON.parse(r.match(/\{[\s\S]*\}/)?.[0] || '{}'); } catch {}
    if (!j.action) {

  if (!j.action && j.best) j.action = j.best;
      // 尝试从文本中提取action关键词
      const txt = (r || '').toLowerCase();
      for (const a of ACTIONS) { if (txt.includes(a.id)) { j.action = a.id; j.reason = 'AI推导'; break; } }
    }
    if (!j.action) j = ruleDecide(s);
    log('② JUDGE->③ DECIDE: ' + (j.action || 'wait') + ' | ' + (j.reason || ''));
    return j;
  } catch (e) { log('BRAIN: LLM失败→' + e.message + ',降级规则'); return ruleDecide(s); }
}

function execute(a) {
  const c = ACTIONS.find(x => x.id === a);
  if (!c) return { ok: false, error: '?' };
  try {
    log('EXEC: ' + c.id + ' ' + c.desc);
    const o = execSync(c.cmd, { encoding: 'utf-8', timeout: 60000, stdio: 'pipe', cwd: GBT }).trim().slice(0, 200);
    return { ok: true, output: o };
  } catch (e) { return { ok: false, error: (e.stdout || e.stderr || e.message || '').slice(0, 200) }; }
}

const MEM_FILE = path.join(GBT, 'memory', 'brain-reflect.json');
function loadMem() { try { return fs.existsSync(MEM_FILE) ? JSON.parse(fs.readFileSync(MEM_FILE, 'utf-8')) : { cycles: [], learnings: [], stats: { totalActions: 0, successActions: 0, failActions: 0 } }; } catch { return { cycles: [], learnings: [], stats: { totalActions: 0, successActions: 0, failActions: 0 } }; } }
function saveMem(m) { try { fs.writeFileSync(MEM_FILE, JSON.stringify(m, null, 2)); } catch {} }

async function reflect(s, d, r) {
  const mem = loadMem();
  mem.stats.totalActions++;
  if (r?.ok) mem.stats.successActions++;
  else if (r) mem.stats.failActions++;

  // 记录本轮
  const entry = { cycle: mem.cycles.length + 1, ts: new Date().toISOString(), state: s, decision: d, result: r?.ok ? 'success' : (r ? 'fail' : 'wait'), detail: r?.output || r?.error || '' };
  mem.cycles.push(entry);
  if (mem.cycles.length > 100) mem.cycles = mem.cycles.slice(-100);

  // 反思：从结果中学习
  if (r && !r.ok) {
    const lesson = { ts: new Date().toISOString(), action: d.action, error: r.error?.slice(0, 100) || '', learning: '动作 ' + d.action + ' 失败，下次降级处理' };
    mem.learnings.push(lesson);
    log('REFLECT: 失败教训 → ' + lesson.learning);
  } else if (r?.ok) {
    const lesson = { ts: new Date().toISOString(), action: d.action, learning: '动作 ' + d.action + ' 成功，' + (r.output || '').slice(0, 50) };
    mem.learnings.push(lesson);
    log('REFLECT: 成功经验 → ' + lesson.learning);
  } else {
    log('REFLECT: 本轮无操作，系统稳定');
  }
  if (mem.learnings.length > 50) mem.learnings = mem.learnings.slice(-50);

  saveMem(mem);
  return mem;
}

async function brainLoop() {
  log('══════════════════════════════════════');
  log('⚕ GBT AI自主大脑 v5.0 启动');
  log('   模型: ' + (API_KEY ? API_MODEL : '规则引擎'));
  log('   间隔: ' + (INTERVAL / 1000) + '秒');
  log('   闭环: 观察→分析→判断→决策→执行→反思→记忆');
  log('══════════════════════════════════════');
  let cycle = 0;
  while (true) {
    cycle++;
    log('── 周期 #' + cycle + ' ──');

    // ① 观察
    const s = observe();
    log('① OBSERVE: 内存' + s.memory?.freeGB + 'GB | Chrome' + s.chromeTabs + ' | Git' + s.gitDirty + ' | 扫描' + (s.lastScan?.total || 0) + '问题');

    // ② 目标检查
    const unmet = checkGoals(s);
    if (unmet.length > 0) {
      log('② GOALS: ' + unmet.length + '个未达标 → ' + unmet.map(g => g.title + '(' + g.detail + ')').join(' '));
      // 自愈逻辑: 高危问题>0 → 触发auto_fix
      if (unmet.find(g => g.goal === 'g2' || g.goal === 'g7')) {
        log('🩺 SELF-HEAL: 检测到高危问题，自动修复...');
        execute('auto_fix');
      }
    } else {
      log('② GOALS: 全部达标 ✅');
    }

    // ③ 分析+判断+决策
    const d = await think(s);

    // ④ 执行
    let r = null;
    if (d.action && d.action !== 'wait') {
      r = execute(d.action);
      log('④ EXEC: ' + (r.ok ? '✅' : '❌') + ' ' + (r.output || r.error || ''));
    } else {
      log('④ EXEC: 跳过');
    }

    // ⑤ 反思
    const mem = await reflect(s, d, r);

    // ⑥ 记忆总结
    const total = mem.stats.totalActions;
    const rate = total > 0 ? (mem.stats.successActions / total * 100).toFixed(0) : '-';
    log('⑤⑥ REFLECT+MEM: 总' + total + '次 | 成功率' + rate + '% | 教训' + mem.learnings.length + '条');

    log('SLEEP: ' + (INTERVAL / 1000) + 's...');
    await new Promise(r => setTimeout(r, INTERVAL));
  }
}

brainLoop().catch(e => { log('CRASH: ' + e.message); process.exit(1); });