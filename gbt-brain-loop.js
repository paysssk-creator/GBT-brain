#!/usr/bin/env node
/**
 * GBT AI Loop Brain v5.0
 * 每60秒拉起一个全新的 gbt-brain.js 进程执行一轮
 * 进程死后重启 = 永远读取最新代码 = 僵尸从根上消灭
 */
const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const GBT = path.join(os.homedir(), '.gbt');
const BRAIN = path.join(GBT, 'gbt-brain.js');
const LOG = path.join(GBT, 'brain.log');
const INTERVAL = 60000;

function log(msg) {
    const ts = new Date().toISOString().slice(0, 19).replace('T', ' ');
    const line = '[' + ts + '] ' + msg;
    console.log(line);
    try { fs.appendFileSync(LOG, line + '\n'); } catch {}
}

log('==========================================');
log('GBT AI Loop Brain v5.0');
log('   mode: one-shot brain + restart = fresh code');
log('   interval: ' + (INTERVAL / 1000) + 's');
log('   brain: ' + BRAIN);
log('==========================================');

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
        
        child.stdout.on('data', (data) => { stdout += data.toString(); });
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
