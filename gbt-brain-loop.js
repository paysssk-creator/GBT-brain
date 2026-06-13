#!/usr/bin/env node
/**
 * GBT AI Loop Brain v5.1 — 长线自保循环器
 * 每60秒拉起一个全新的 gbt-brain.js 进程执行一轮
 * 进程死后重启 = 永远读取最新代码 = 僵尸从根上消灭
 * + 自保: 日志轮转 (1MB) + 记忆压缩 (100条) + 上下文续写守护
 */
const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const GBT = path.join(os.homedir(), '.gbt');
const BRAIN = path.join(GBT, 'gbt-brain.js');
const LOG = path.join(GBT, 'brain.log');
const COMPRESSOR = path.join(GBT, 'gbt-brain-compressor.js');
const INTERVAL = 60000;
const LOG_MAX_SIZE = 1024 * 1024;  // 1MB

function log(msg) {
    const ts = new Date().toISOString().slice(0, 19).replace('T', ' ');
    const line = '[' + ts + '] ' + msg;
    console.log(line);
    try { fs.appendFileSync(LOG, line + '\n'); } catch {}
}

// ====== 自保: 日志/记忆/上下文检查 ======
function selfPreserve() {
    const compressor = require(COMPRESSOR);
    const report = compressor.run();
    if (report.actions && report.actions.length && report.actions[0] !== 'all clean') {
        log('[preserve] ' + report.actions.join(' | '));
    }

    // 硬限: 日志超过2MB强制截断
    if (fs.existsSync(LOG)) {
        const stat = fs.statSync(LOG);
        if (stat.size > LOG_MAX_SIZE * 2) {
            log('[preserve] LOG HARD LIMIT: ' + (stat.size / 1024).toFixed(0) + 'KB, force rotate');
            compressor.rotateLog();
            log('[preserve] log rotated');
        }
    }
}

// ====== 上下文续写守护 ======
let lastBrainOutput = Date.now();

function contextGuard() {
    const stall = Date.now() - lastBrainOutput;
    if (stall > 5 * 60 * 1000) {  // 5分钟无输出
        log('[guard] WARNING: no brain output for ' + (stall / 60000).toFixed(0) + 'min — but loop continues');
    }
    if (stall > 30 * 60 * 1000) {  // 30分钟无输出, 强制重启循环器内部状态
        log('[guard] context reset after 30min stall');
        lastBrainOutput = Date.now();
    }
}

log('==========================================');
log('GBT AI Loop Brain v5.1 — Self-Preserving');
log('   mode: one-shot brain + restart = fresh code');
log('   interval: ' + (INTERVAL / 1000) + 's');
log('   preserve: log<1MB | memory<100learnings | context guard');
log('==========================================');

// 启动时立即执行一次自保检查
selfPreserve();

let runCount = 0;

async function runBrainCycle() {
    return new Promise((resolve) => {
        runCount++;
        log('loop#' + runCount + ' → spawning gbt-brain.js');

        const child = spawn('node', [BRAIN], {
            cwd: GBT,
            stdio: 'pipe',
            timeout: 120000
        });

        let stdout = '';
        let stderr = '';

        child.stdout.on('data', (data) => { stdout += data.toString(); lastBrainOutput = Date.now(); });
        child.stderr.on('data', (data) => { stderr += data.toString(); });

        child.on('close', (code) => {
            if (code !== 0) {
                log('loop#' + runCount + ' ← brain exited code=' + code + (stderr ? ' err=' + stderr.slice(0, 100) : ''));
            } else {
                log('loop#' + runCount + ' ← brain done');
            }
            resolve();
        });

        child.on('error', (err) => {
            log('loop#' + runCount + ' ← brain spawn error: ' + err.message);
            resolve();
        });
    });
}

async function loop() {
    while (true) {
        try {
            await runBrainCycle();
        } catch (e) {
            log('LOOP_CRASH: ' + e.message);
        }
        log('sleeping ' + (INTERVAL / 1000) + 's...');
        await new Promise(r => setTimeout(r, INTERVAL));
    }
}

loop().catch(e => {
    log('FATAL: ' + e.message);
    process.exit(1);
});
