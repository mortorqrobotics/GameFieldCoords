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