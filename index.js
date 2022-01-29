let fieldWidth = 1646;
let fieldHeight = 823;

let x;
let y;

document.addEventListener('mousemove', (e) => {
    let mouseX = e.clientX;
    let mouseY = e.clientY;
    let elementMouseIsOver = document.elementFromPoint(mouseX, mouseY);
    if(elementMouseIsOver.tagName !== "IMG") return;

    let {x: xOffset, y: yOffset, width, height } = elementMouseIsOver.getBoundingClientRect();
    x = mouseX - xOffset;
    y = mouseY - yOffset;

    document.querySelector('.coords').textContent = `x: ${x}px, y: ${y}px`;
    document.querySelector('.pos').textContent = `x: ${((x / width) * fieldWidth).toFixed(2)}cm y: ${((y / height) * fieldHeight).toFixed(2)}cm`;
})

document.addEventListener('click', (e) => {
    if(e.target.tagName !== "IMG") return;
    let { width, height } = document.querySelector('img').getBoundingClientRect();
    document.querySelector('#savePos').innerHTML += `<br>x: ${((x / width) * fieldWidth).toFixed(2)}cm y: ${((y / height) * fieldHeight).toFixed(2)}cm`
})

const roundTo = (num, place) => {
    return Math.round(num * (10 * place)) / (10 * place);
}

const convertToCm = (num, x=true) => {
    let total;
    let image;
    let { width, height } = document.querySelector('img').getBoundingClientRect();
    if(x) {
        total = fieldWidth
        image = width;
    } else {
        total = fieldHeight;
        image = height;
    }
    return (num / image) * total;
}

let positions = [];
document.addEventListener('mousedown', (e) => {
    if(e.button !== 1) return; // middle click

    if(!positions[0]) return positions[0] = [convertToCm(x), convertToCm(y, false)];
    if(!positions[1]) positions[1] = [convertToCm(x), convertToCm(y, false)];

    console.log("distance", `${roundTo(Math.hypot(positions[1][0] - positions[0][0], positions[1][1] - positions[0][1]) / 100, 2)} meters`)
    positions = [];
})