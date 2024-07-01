let layers = 10;           // Number of layers
let detail = 48;           // Detail level of each layer (number of circles per layer)
let maxRadius;             // Maximum radius for outermost layer
let centerShapes = 5;      // Number of central dynamic shapes

// Movement parameters
let moveSpeed = 0.02;      // Speed of movement
let moveDistance = 50;     // Distance of movement

function setup() {
    createCanvas(windowWidth, windowHeight);
    maxRadius = min(width, height) / 3;  // Calculate maximum radius dynamically
    angleMode(DEGREES);
    noFill();
    colorMode(HSB, 360, 100, 100, 100);
}

function draw() {
    background(0);
    translate(width / 2, height / 2);
    rotate(frameCount * 0.3);  // Slow rotation of the entire mandala

    let time = millis() / 1000;
    drawOuterLayers(time);
    drawCenterShapes(time);
}

// Draws detailed and multiplied circles in concentric layers
function drawOuterLayers(time) {
    for (let i = 0; i < layers; i++) {
        let radius = map(i, 0, layers - 1, 40, maxRadius);
        let baseColor = map(i, 0, layers, 0, 360);  // Color hues spread across layers

        for (let j = 0; j < detail; j++) {
            let angle = map(j, 0, detail, 0, 360);
            let x = cos(angle) * radius;
            let y = sin(angle) * radius;

            let rotationAngle = (frameCount * 15 + angle * 10) % 360;  // Spin each circle
            let circleRadius = map(sin(time * 9 + angle * 2), -1, 1, 5, 20);

            // Calculate movement offset
            let moveOffset = sin((angle + frameCount * 2) * moveSpeed) * moveDistance;

            push();
            translate(x + moveOffset, y);
            rotate(rotationAngle);

            let colorHue = (baseColor + angle) % 360;
            let brightness = map(i, 0, layers - 1, 50, 100);
            stroke(colorHue, 100, brightness, 80);
            ellipse(0, 0, circleRadius, circleRadius);

            // Draw additional details inside each circle
            drawDetailedCircles(circleRadius);
            pop();
        }
    }
}

// Draws intricate detailed circles inside each main circle
function drawDetailedCircles(circleRadius) {
    for (let k = 0; k < 12; k++) {
        let innerAngle = map(k, 0, 12, 0, 360);
        let innerX = cos(innerAngle) * circleRadius / 2.5;
        let innerY = sin(innerAngle) * circleRadius / 2.5;
        let innerRadius = circleRadius / 5;
        ellipse(innerX, innerY, innerRadius, innerRadius);
    }
}

// Draws dynamic central shapes
function drawCenterShapes(time) {
    let centerRadius = 100;

    for (let i = 0; i < centerShapes; i++) {
        let angleOffset = frameCount * 2 + i * 72;  // Different starting angles

        for (let j = 0; j < 6; j++) {
            let angle = map(j, 0, 6, 0, 360);
            let x = cos(angle + angleOffset) * centerRadius;
            let y = sin(angle + angleOffset) * centerRadius;

            let shapeRadius = map(sin(time * 7 + j * 60), -1, 1, 40, 60);

            push();
            translate(x, y);
            rotate(-angleOffset);  // Rotate opposite direction for effect

            strokeWeight(2);
            stroke(255, 100);

            beginShape();
            for (let k = 0; k < 360; k += 45) {
                let sx = cos(k) * shapeRadius;
                let sy = sin(k) * shapeRadius;
                vertex(sx, sy);
            }
            endShape(CLOSE);

            // Additional detailed circles inside the hexagons
            drawHexagonDetail(shapeRadius);
            pop();
        }
    }
}

// Draws detailed circles inside the central hexagons
function drawHexagonDetail(shapeRadius) {
    for (let m = 0; m < 6; m++) {
        let detailAngle = map(m, 0, 6, 0, 360);
        let detailX = cos(detailAngle) * shapeRadius / 3;
        let detailY = sin(detailAngle) * shapeRadius / 3;
        let detailRadius = shapeRadius / 10;
        ellipse(detailX, detailY, detailRadius, detailRadius);
    }
}

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}
