function setup() {
    createCanvas(windowWidth, windowHeight);
    angleMode(DEGREES);
    noFill();
}

function draw() {
    background(0);
    translate(width / 2, height / 2);

    let numShapes = 10;
    let numLayers = 10;
    let maxRadius = min(width, height) / 3;
    let time = millis() / 1000;

    for (let i = 0; i < numLayers; i++) {
        let radius = map(i, 0, numLayers - 1, 20, maxRadius);
        let colorOffset = map(i, 0, numLayers - 1, 0, 255);

        for (let j = 0; j < numShapes; j++) {
            let angle = map(j, 0, numShapes, 0, 360);
            let x = cos(angle + time * 60) * radius;
            let y = sin(angle + time * 60) * radius;
            let r = map(sin(time * 30 + angle), -1, 1, 20, 50);

            let red = map(sin(time + j * 10), -1, 1, 100, 255);
            let green = map(sin(time + i * 10), -1, 1, 100, 255);
            let blue = map(sin(time + (i + j) * 5), -1, 1, 100, 255);

            stroke(red, green, blue, 150);
            ellipse(x, y, r, r);
        }
    }
}

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}
