const { createCanvas } = require('canvas');
const canvas = createCanvas(800, 600);
const ctx = canvas.getContext('2d');

// 背景
const bgGrad = ctx.createLinearGradient(0, 0, 800, 600);
bgGrad.addColorStop(0, '#0a0e17');
bgGrad.addColorStop(1, '#161b22');
ctx.fillStyle = bgGrad;
ctx.fillRect(0, 0, 800, 600);

// 根据描述绘制: ������˳��������,�޺�ƹ⵹ӳ��ˮ��,���Ч��,��̬��˸
// 主图形
ctx.save();
ctx.translate(800/2, 600/2);

// 示例: 旋转几何图案
const sides = 6;
const layers = 12;
for (let l = 0; l < layers; l++) {
  const radius = 240 * (1 - l / layers);
  const alpha = 0.3 + 0.5 * (l / layers);
  ctx.strokeStyle = `#3fb950${Math.round(alpha * 255).toString(16).padStart(2, '0')}`;
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let i = 0; i <= sides; i++) {
    const angle = (Math.PI * 2 / sides) * i - Math.PI / 2 + l * 0.1;
    const x = Math.cos(angle) * radius;
    const y = Math.sin(angle) * radius;
    if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  }
  ctx.closePath();
  ctx.stroke();
}

// 中心装饰
ctx.fillStyle = '#3fb950';
ctx.beginPath();
ctx.arc(0, 0, 20, 0, Math.PI * 2);
ctx.fill();

ctx.restore();

// 文字
ctx.fillStyle = '#f0f6fc';
ctx.font = 'bold 28px sans-serif';
ctx.textAlign = 'center';
ctx.fillText('������˳��������,�޺�ƹ⵹ӳ��ˮ��,��', 800/2, 600 - 40);

// 导出
const fs = require('fs');
fs.writeFileSync('artwork.png', canvas.toBuffer('image/png'));
console.log('OK');
