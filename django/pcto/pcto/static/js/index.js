
// Custom pixel ratio aware canvas
const canvas = document.getElementById('bg');
const ctx = canvas.getContext('2d');
let W, H, DPR;

function resize(){
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    W = canvas.width = Math.floor(window.innerWidth * DPR);
    H = canvas.height = Math.floor(window.innerHeight * DPR);
    canvas.style.width = window.innerWidth + 'px';
    canvas.style.height = window.innerHeight + 'px';
    ctx.setTransform(DPR,0,0,DPR,0,0);
}

window.addEventListener('resize', resize);
resize();

// Particle network
const particles = [];
const PARTICLE_COUNT = Math.max(28, Math.floor((window.innerWidth*window.innerHeight)/80000));

for (let i=0; i < PARTICLE_COUNT; i++) {
    particles.push({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        vx: (Math.random()-0.5) * 0.4,
        vy: (Math.random()-0.5) * 0.4,
        r: 1 + Math.random() * 2
    });
}

const mouse = {
    x: -9999,
    y: -9999,
    px: 0,
    py: 0
}

window.addEventListener('mousemove', e=>{
    mouse.x = e.clientX;
    mouse.y = e.clientY
});
window.addEventListener('mouseleave', ()=>{
    mouse.x = -9999;
    mouse.y = -9999
});

function step(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // background subtle gradient overlay
    const g = ctx.createLinearGradient(0, 0, 0, window.innerHeight);
    g.addColorStop(0, 'rgba(12,14,22,0.12)');
    g.addColorStop(1, 'rgba(8,9,14,0.3)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, window.innerWidth, window.innerHeight);

    // update particles
    for (let p of particles) {
        p.x += p.vx;
        p.y += p.vy;
        
        if (p.x < -20)
            p.x = window.innerWidth + 20;
        
        if (p.x > window.innerWidth + 20)
            p.x = -20;
        
        if (p.y < -20)
            p.y = window.innerHeight + 20;
        
        if (p.y > window.innerHeight + 20)
            p.y = -20;
    }

    // draw connections
    for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++){
            const a = particles[i], b = particles[j];
            const dx = a.x - b.x, dy = a.y - b.y;
            const d2 = dx * dx + dy * dy;
            if (d2 < 90000) { // threshold
                const alpha = Math.max(0, 0.9 - d2 / 90000);
                ctx.beginPath();
                ctx.moveTo(a.x, a.y);
                ctx.lineTo(b.x, b.y);
                ctx.strokeStyle = `rgba(120,92,255,${alpha * 0.12})`;
                ctx.lineWidth = 1;
                ctx.stroke();
            }
        }
    }

    // mouse attraction
    if (mouse.x > -9000) {
        for (let p of particles) {
            const dx = mouse.x - p.x;
            const dy = mouse.y - p.y;
            const d2 = dx * dx + dy * dy;
            if (d2 < 90000) {
                const f = (1 - d2 / 90000) * 0.08;
                p.vx += dx * 0.0008 * f;
                p.vy += dy * 0.0008 * f;
                p.vx *= 0.995; p.vy *= 0.995;
            }
        }
    }

    // draw particles
    for (let p of particles) {
        ctx.beginPath();
        ctx.fillStyle = 'rgba(124,92,255,0.96)';
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fill();
    }

    requestAnimationFrame(step);
}
requestAnimationFrame(step);

// Headline morph and entrance using GSAP
gsap.from('#hero', {
    duration:1,
    y:24,
    autoAlpha:0,
    ease:'power3.out'
});

gsap.from('.panel .card', {
    duration:0.9, 
    y:18, 
    autoAlpha:0, 
    stagger:0.08, 
    delay:0.15, 
    ease:'power2.out'
});

// Dynamic headline words
const words = [
    'Connetti menti.',
    'Costruisci il futuro.',
    'Sperimenta.',
    'Collabora.'
];

let wi = 0;
const head = document.getElementById('headline');

setInterval(()=>{
    const next = words[wi % words.length];
    gsap.to(head, {
        duration:0.42,
        y:-8,
        autoAlpha:0,
        ease:'power2.in',
        onComplete:()=>{
            head.textContent = next;
            gsap.fromTo(
                head,
                {
                    y:8,
                    autoAlpha:0
                },
                {
                    duration:0.6,
                    y:0,
                    autoAlpha:1,
                    ease:'elastic.out(1,0.6)'
            });
        }
    });
    wi++;
}, 4200);

// Custom cursor smoothing
const cursor = document.getElementById('cursor');
let cx = window.innerWidth / 2, cy = window.innerHeight / 2; let tx = cx, ty = cy;

window.addEventListener('mousemove', e=>{
    tx = e.clientX;
    ty = e.clientY
});

function tick(){
    cx += (tx - cx) * 0.18;
    cy += (ty - cy) * 0.18;
    cursor.style.transform = `translate(${cx}px, ${cy}px) translate(-50%,-50%)`;
    requestAnimationFrame(tick);
}
tick();

// Button hover effect
const cta = document.getElementById('main-cta');
cta.addEventListener('mousemove', e=>{
    const rect = cta.getBoundingClientRect();
    const px = (e.clientX - rect.left) / rect.width - 0.5;
    const py = (e.clientY - rect.top) / rect.height - 0.5;
    cta.style.transform = `translateZ(0) perspective(600px) rotateX(${-py * 6}deg) rotateY(${px * 10}deg)`;
});
cta.addEventListener('mouseleave', ()=>{
    cta.style.transform='none'
});

// subtle parallax on vector strip
const vec = document.querySelector('.vector-strip');
window.addEventListener('scroll', ()=>{
    const s = window.scrollY;
    if(vec) vec.style.transform = `translateY(${s*0.12}px)`;
});

// Accessibility fallback: reduce motion respect
const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
if(mq.matches){
    gsap.globalTimeline.timeScale(0.2);
}