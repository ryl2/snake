// Browser-only Snake game (no Python needed)
const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');
const highEl = document.getElementById('high');
let highNameEl = document.getElementById('highName');
const nameInput = document.getElementById('nameInput');
const startOverlay = document.getElementById('startOverlay');
const playBtn = document.getElementById('playBtn');
const themeBtn = document.getElementById('themeBtn');
const gameOverOverlay = document.getElementById('gameOverOverlay');
const overScore = document.getElementById('overScore');
const restartBtn = document.getElementById('restartBtn');
const menuBtn = document.getElementById('menuBtn');

const BLOCK = 20;
const COLS = canvas.width / BLOCK;
const ROWS = canvas.height / BLOCK;

let snake = [];
let dir = {x:0,y:0};
let food = {x:0,y:0};
let score = 0;
let playerName = 'Player';
// load high score data: either new JSON key or fallback numeric
let high = 0;
let highOwner = '—';
try{
  const raw = localStorage.getItem('snakeHighData');
  if(raw){ const obj = JSON.parse(raw); high = obj.score||0; highOwner = obj.name||'—'; }
  else { high = parseInt(localStorage.getItem('snakeHigh')||'0',10)||0; highOwner = localStorage.getItem('snakeHighName')||'—'; }
}catch(e){ high = parseInt(localStorage.getItem('snakeHigh')||'0',10)||0; highOwner = localStorage.getItem('snakeHighName')||'—'; }
let speed = 8; // moves per second
const BASE_SPEED = 8;
const SPEED_INC_EVERY = 5;
const SPEED_INC = 2;
let moveInterval = 1000/speed;
let lastTime = 0;
let running = false;
let themeIndex = 0;
const THEMES = ['','theme-light','theme-night'];

// touch handling for mobile (simple swipe)
let touchStart = null;
canvas.addEventListener('touchstart', e=>{ touchStart = e.changedTouches[0]; });
canvas.addEventListener('touchend', e=>{
  if(!touchStart) return;
  const t = e.changedTouches[0];
  const dx = t.clientX - touchStart.clientX;
  const dy = t.clientY - touchStart.clientY;
  const absX = Math.abs(dx), absY = Math.abs(dy);
  const threshold = 20;
  if(absX>absY && absX>threshold){ if(dx>0) setDir(1,0); else setDir(-1,0); }
  else if(absY>threshold){ if(dy>0) setDir(0,1); else setDir(0,-1); }
  touchStart = null;
});

function setDir(x,y){ if(x!==0 && dir.x!==0) return; if(y!==0 && dir.y!==0) return; dir = {x,y}; }

function resetGame(){
  snake = [{x: Math.floor(COLS/2)*BLOCK, y: Math.floor(ROWS/2)*BLOCK}];
  dir = {x:0,y:0};
  score = 0;
  speed = BASE_SPEED;
  moveInterval = 1000/speed;
  placeFood();
  running = false;
  updateHUD();
  hideGameOver();
  showStart();
}

function placeFood(){
  while(true){
    const x = Math.floor(Math.random()*COLS)*BLOCK;
    const y = Math.floor(Math.random()*ROWS)*BLOCK;
    if(!snake.some(s=>s.x===x && s.y===y)){
      food = {x,y};
      return;
    }
  }
}

function updateHUD(){ 
  scoreEl.textContent = (playerName ? playerName + ' — ' : '') + 'Score: ' + score; 
  // update high with owner without destroying the span element
  highEl.innerHTML = `High: ${high} (<span id="highName">${highOwner || '—'}</span>)`;
  // refresh reference to highNameEl in case innerHTML replaced it
  highNameEl = document.getElementById('highName');
}

function draw(){
  // background
  ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--panel').trim() || '#000';
  ctx.fillRect(0,0,canvas.width,canvas.height);
  // food
  ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--food').trim() || '#f00';
  ctx.fillRect(food.x,food.y,BLOCK,BLOCK);
  // snake
  ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--accent').trim() || '#0f0';
  for(let i=0;i<snake.length;i++){ const s = snake[i]; ctx.fillRect(s.x,s.y,BLOCK,BLOCK); }
}

function update(){
  if(dir.x===0 && dir.y===0) return;
  const head = {x: snake[0].x + dir.x*BLOCK, y: snake[0].y + dir.y*BLOCK};
  if(head.x < 0 || head.x >= canvas.width || head.y < 0 || head.y >= canvas.height) return doGameOver();
  if(snake.some((p,i)=>i>0 && p.x===head.x && p.y===head.y)) return doGameOver();
  snake.unshift(head);
  if(head.x===food.x && head.y===food.y){
    score++;
    // new high score
    if(score>high){ 
      high = score; 
      highOwner = playerName || 'Player';
      try{ localStorage.setItem('snakeHighData', JSON.stringify({score:high,name:highOwner})); }
      catch(e){ localStorage.setItem('snakeHigh', String(high)); localStorage.setItem('snakeHighName', highOwner); }
    }
    updateHUD();
    if(score % SPEED_INC_EVERY === 0){ speed += SPEED_INC; moveInterval = 1000/speed; }
    placeFood();
  } else { snake.pop(); }
}

function doGameOver(){
  running = false;
  overScore.textContent = 'Score: ' + score;
  showGameOver();
}

function loop(ts){
  if(!lastTime) lastTime = ts;
  const delta = ts - lastTime;
  if(running && delta >= moveInterval){ update(); draw(); lastTime = ts; }
  requestAnimationFrame(loop);
}

// UI helpers
function showStart(){ startOverlay.classList.remove('hidden'); }
function hideStart(){ startOverlay.classList.add('hidden'); }
function showGameOver(){ gameOverOverlay.classList.remove('hidden'); }
function hideGameOver(){ gameOverOverlay.classList.add('hidden'); }

playBtn.addEventListener('click', ()=>{ hideStart(); running = true; });
themeBtn.addEventListener('click', ()=>{ themeIndex = (themeIndex+1)%THEMES.length; document.body.className = THEMES[themeIndex]; });
playBtn.addEventListener('click', ()=>{ 
  const name = (nameInput && nameInput.value) ? nameInput.value.trim() : '';
  playerName = name || 'Player';
  hideStart(); running = true; updateHUD();
});
restartBtn.addEventListener('click', ()=>{ hideGameOver(); running = true; resetAfterRestart(); });
menuBtn.addEventListener('click', ()=>{ resetGame(); });

function resetAfterRestart(){ snake = [{x: Math.floor(COLS/2)*BLOCK, y: Math.floor(ROWS/2)*BLOCK}]; dir = {x:0,y:0}; score = 0; updateHUD(); placeFood(); }

window.addEventListener('keydown', e=>{
  if(e.key==='ArrowLeft' || e.key==='a'){ setDir(-1,0); }
  if(e.key==='ArrowRight' || e.key==='d'){ setDir(1,0); }
  if(e.key==='ArrowUp' || e.key==='w'){ setDir(0,-1); }
  if(e.key==='ArrowDown' || e.key==='s'){ setDir(0,1); }
  if(e.key==='r'){ resetGame(); }
  if(e.key==='t'){ themeIndex = (themeIndex+1)%THEMES.length; document.body.className = THEMES[themeIndex]; }
});

resetGame();
requestAnimationFrame(loop);
