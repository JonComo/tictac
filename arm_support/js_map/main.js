var canvas = document.createElement("canvas");
var ctx = canvas.getContext("2d");

document.body.appendChild(canvas);

var width = 400;
var height = 400;

canvas.width = width;
canvas.height = height;

// arm length
let lc = 100;
let l1 = lc;

// points
let a = {x: 10, y: height/2}
let b = {x: 10, y: height/2}

// end point
let x = width/2; 
let y = height/2;

// motor angles
let t1 = 0;
let t2 = 0;

let mouse = {x: 0, y: 0};

function dot(x, y) {
    ctx.fillRect(x-2, y-2, 4, 4);
}

function to_rads(deg) {
    return deg/180 * Math.PI;
}

function dist(p1, p2) {
    return Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));
}

function uv_to(start, end) {
    let dx = end.x - start.x;
    let dy = end.y - start.y;

    let mag = Math.sqrt(dx*dx + dy*dy);

    return {x: dx/mag, y: dy/mag};
}

keys = {};
window.onkeydown = function(evt) {
    let key = evt.key;
    keys[key] = key;
}

window.onkeyup = function(evt) {
    let key = evt.key;
    if (key in keys) {
        delete keys[key];
    }
}

window.onmousemove = function(evt) {
    mouse.x = evt.offsetX;
    mouse.y = evt.offsetY;
}

function render() {
    window.requestAnimationFrame(render);

    /*
    if ("q" in keys) {
        t1 -= 1;
    }
    if ("e" in keys) {
        t1 += 1;
    }
    if ("i" in keys) {
        t2 -= 1;
    }
    if ("p" in keys) {
        t2 += 1;
    } */

    ctx.clearRect(0, 0, width, height);
    ctx.strokeRect(4, 4, width-8, height-8);

    dot(mouse.x, mouse.y);

    // inverse
    let d = dist(a, mouse);
    t1 = Math.atan2(mouse.y - a.y, mouse.x-a.x) * 180/Math.PI;
    t2 = Math.acos(d/2/l1) * 180/Math.PI;;
    //t2 = Math.acos((2 * l1 * Math.cos(t2))/mouse.x);

    dot(a.x, a.y);
    dot(b.x, b.y);

    let p1 = {x: a.x + Math.cos(to_rads(t1 + t2)) * l1, y: a.y + Math.sin(to_rads(t1 + t2)) * l1};

    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(p1.x, p1.y);
    ctx.stroke();

    dot(p1.x, p1.y);


    let p2 = {x: b.x + Math.cos(to_rads(t1 - t2)) * l1, y: b.y + Math.sin(to_rads(t1 - t2)) * l1};

    ctx.beginPath();
    ctx.moveTo(b.x, b.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.stroke();

    dot(p2.x, p2.y);

    // lines to end
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(x, y);
    ctx.moveTo(p2.x, p2.y);
    ctx.lineTo(x, y);
    ctx.stroke();

    // forward
    x = a.x + Math.cos(to_rads(t1)) * 2 * l1 * Math.cos(to_rads(t2));
    y = a.y + Math.sin(to_rads(t1)) * 2 * l1 * Math.cos(to_rads(t2));

    // iterative solve
    /*
    let p_end = {x: x, y: y};
    let d1 = dist(p1, p_end);
    let diff1 = (d1 - l1);
    let uv1 = uv_to(p_end, p1);

    x += uv1.x * diff1;
    y += uv1.y * diff1;

    let d2 = dist(p2, p_end);
    let diff = (d2 - l1);
    let uv2 = uv_to(p_end, p2);

    x += uv2.x * diff;
    y += uv2.y * diff;

    let topx = -(p1.x*p1.x) + p2.x*p2.x - Math.pow(y - p1.y ,2) + Math.pow(y - p2.y, 2);
    let botx = 2 * (p2.x - p1.x);
    let proofx = topx/botx;


    let topy = -(p1.y*p1.y) + p2.y*p2.y - Math.pow(x - p1.x ,2) + Math.pow(x - p2.x, 2);
    let boty = 2 * (p2.y - p1.y);
    let proofy = topy/boty;

    console.log('yterm: ' + Math.pow(y - p1.y ,2) + Math.pow(y - p2.y, 2));
    console.log('yterm guess: ' + Math.pow(p2.y - p1.y ,2));

    console.log('x: ' + x + ' proof x: ' + proofx);
    console.log('y: ' + y + ' proof y: ' + proofy); */
}

render();