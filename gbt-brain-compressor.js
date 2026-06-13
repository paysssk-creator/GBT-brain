#!/usr/bin/env node
/**
 * GBT 长线自保压缩器
 * 防止日志/记忆/上下文无限膨胀导致崩溃
 */
const fs = require('fs');
const path = require('path');
const os = require('os');

const GBT = path.join(os.homedir(), '.gbt');
const LOG = path.join(GBT, 'brain.log');
const MEM = path.join(GBT, 'memory', 'brain-reflect.json');
const ARCHIVE_DIR = path.join(GBT, 'brain-archives');

// 阈值
const LOG_MAX_SIZE = 1024 * 1024;       // 1MB 触发轮转
const LOG_ARCHIVE_KEEP = 5;              // 保留最近5个归档
const MEM_MAX_LEARNINGS = 100;           // 学习记录上限
const MEM_MAX_CYCLES = 200;              // 周期记录上限

function log(msg) {
    const ts = new Date().toISOString().slice(0, 19).replace('T', ' ');
    console.log('[' + ts + '] [compressor] ' + msg);
}

// ====== 日志轮转 ======
function rotateLog() {
    if (!fs.existsSync(LOG)) return;
    const stat = fs.statSync(LOG);
    if (stat.size < LOG_MAX_SIZE) return;

    log('log size=' + (stat.size / 1024).toFixed(0) + 'KB > 1MB, rotating...');

    // 创建归档目录
    if (!fs.existsSync(ARCHIVE_DIR)) fs.mkdirSync(ARCHIVE_DIR, { recursive: true });

    // 归档: brain-archive-2026-06-13.log
    const date = new Date().toISOString().slice(0, 10);
    const archiveName = 'brain-archive-' + date + '-' + Date.now() + '.log';
    const archivePath = path.join(ARCHIVE_DIR, archiveName);

    fs.renameSync(LOG, archivePath);
    log('archived to ' + archiveName);

    // 清理旧归档 (保留最近 LOG_ARCHIVE_KEEP 个)
    try {
        const archives = fs.readdirSync(ARCHIVE_DIR)
            .filter(f => f.startsWith('brain-archive-'))
            .sort()
            .reverse();
        for (let i = LOG_ARCHIVE_KEEP; i < archives.length; i++) {
            fs.unlinkSync(path.join(ARCHIVE_DIR, archives[i]));
            log('deleted old archive: ' + archives[i]);
        }
    } catch (e) {
        log('archive cleanup error: ' + e.message);
    }
}

// ====== 记忆压缩 ======
function compressMemory() {
    if (!fs.existsSync(MEM)) return;

    let mem;
    try {
        mem = JSON.parse(fs.readFileSync(MEM, 'utf-8'));
    } catch (e) {
        log('memory parse error: ' + e.message);
        return;
    }

    let changed = false;

    // 压缩学习记录: 超过阈值时, 合并旧的学习为摘要
    if (mem.learnings && mem.learnings.length > MEM_MAX_LEARNINGS) {
        const old = mem.learnings.slice(0, mem.learnings.length - 50);
        const recent = mem.learnings.slice(-50);

        // 提取关键教训
        const failCount = old.filter(l => l.learning.includes('失败') || l.error).length;
        const successCount = old.filter(l => l.learning.includes('成功')).length;
        const actions = [...new Set(old.map(l => l.action).filter(Boolean))];

        const summary = {
            ts: new Date().toISOString(),
            type: 'compressed',
            learning: '[压缩] 历史' + old.length + '条→' +
                '成功' + successCount + '/失败' + failCount +
                ' | 涉及动作: ' + actions.join(',')
        };

        mem.learnings = [summary, ...recent];
        changed = true;
        log('memory compressed: ' + old.length + ' learnings → 1 summary + ' + recent.length + ' recent');
    }

    // 压缩周期记录: 保留最近周期
    if (mem.cycles && mem.cycles.length > MEM_MAX_CYCLES) {
        const cut = mem.cycles.length - 100;
        mem.cycles = mem.cycles.slice(-100);
        changed = true;
        log('cycles trimmed: removed ' + cut + ' old cycles, kept 100');
    }

    if (changed) {
        fs.writeFileSync(MEM, JSON.stringify(mem, null, 2), 'utf-8');
    }
}

// ====== 上下文续写保护 ======
function contextGuard() {
    // 检测 brain.log 是否有最近写入（防卡死）
    if (!fs.existsSync(LOG)) return 'ok';

    const stat = fs.statSync(LOG);
    const age = Date.now() - stat.mtimeMs;

    if (age > 5 * 60 * 1000) {  // 5分钟无写入 = 可能卡死
        log('WARNING: brain.log no writes for ' + (age / 60000).toFixed(1) + 'min');
        return 'warn:stale';
    }

    return 'ok';
}

// ====== 主入口 ======
function run() {
    const report = [];

    // 1. 日志轮转
    const logBefore = fs.existsSync(LOG) ? fs.statSync(LOG).size : 0;
    rotateLog();
    const logAfter = fs.existsSync(LOG) ? fs.statSync(LOG).size : 0;
    if (logBefore > LOG_MAX_SIZE) {
        report.push('log rotated: ' + (logBefore / 1024).toFixed(0) + 'KB → ' + (logAfter / 1024).toFixed(0) + 'KB');
    }

    // 2. 记忆压缩
    compressMemory();

    // 3. 上下文守护
    const ctx = contextGuard();
    if (ctx !== 'ok') report.push('context: ' + ctx);

    return { ok: true, actions: report.length ? report : ['all clean'] };
}

// 直接运行时执行
if (require.main === module) {
    const result = run();
    console.log(JSON.stringify(result));
}

module.exports = { rotateLog, compressMemory, contextGuard, run };
