function setup() {
    createCanvas(windowWidth, windowHeight);
    angleMode(DEGREES);
    noFill();
}

function draw() {
    background(0);
    translate(width / 2, height / 2);
    rotate(frameCount * 0.5);  // Spin the whole canvas

    let numLayers = 10;        // Number of concentric layers
    let maxRadius = min(width, height) / 3;  // Maximum radius for outermost layer
    let time = millis() / 1000;

    for (let i = 0; i < numLayers; i++) {
        let radius = map(i, 0, numLayers - 1, 30, maxRadius);
        let detail = 36;  // Number of circles in each layer

        for (let j = 0; j < detail; j++) {
            let angle = map(j, 0, detail, 0, 360);
            let x = cos(angle) * radius;
            let y = sin(angle) * radius;

            let rotationAngle = (frameCount * 2 + angle * 5) % 360;  // Spin each circle

            let circleRadius = map(sin(time * 2 + angle), -1, 1, 10, 30);

            push();
            translate(x, y);
            rotate(rotationAngle);

            let red = map(sin(time + j * 5), -1, 1, 50, 255);
            let green = map(sin(time + i * 5), -1, 1, 50, 255);
            let blue = map(sin(time + (i + j) * 2.5), -1, 1, 50, 255);

            stroke(red, green, blue, 150);
            ellipse(0, 0, circleRadius, circleRadius);

            // Draw smaller detailed circles inside
            for (let k = 0; k < 6; k++) {
                let innerAngle = map(k, 0, 6, 0, 360);
                let innerX = cos(innerAngle) * circleRadius / 3;
                let innerY = sin(innerAngle) * circleRadius / 3;

                ellipse(innerX, innerY, circleRadius / 3, circleRadius / 3);
            }

            pop();
        }
    }

    drawCenterShapes();
}

function drawCenterShapes() {
    let numShapes = 3;  // Number of central shapes
    let centerRadius = 80;

    for (let i = 0; i < numShapes; i++) {
        let angleOffset = frameCount * 2 + i * 120;  // Different starting angles

        for (let j = 0; j < 6; j++) {
            let angle = map(j, 0, 6, 0, 360);
            let x = cos(angle + angleOffset) * centerRadius;
            let y = sin(angle + angleOffset) * centerRadius;

            let shapeRadius = map(sin(millis() / 500 + j * 45), -1, 1, 30, 50);

            push();
            translate(x, y);
            rotate(-angleOffset);  // Rotate opposite direction for effect

            strokeWeight(2);
            stroke(255, 200);

            beginShape();
            for (let k = 0; k < 360; k += 45) {
                let sx = cos(k) * shapeRadius;
                let sy = sin(k) * shapeRadius;
                vertex(sx, sy);
            }
            endShape(CLOSE);

            pop();
        }
    }
}

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}
