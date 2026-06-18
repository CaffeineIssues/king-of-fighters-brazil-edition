import "./style.css";
const canvas = document.getElementById("game");

if (!canvas) {
  throw new Error(
    'Canvas with id="game" was not found. Check your index.html.',
  );
}

const ctx = canvas.getContext("2d");

if (!ctx) {
  throw new Error("Could not get 2D canvas context.");
}

ctx.imageSmoothingEnabled = false;

// Shared visual floor line.
// Bigger number = characters lower.
const GROUND_Y = canvas.height + 35;

// Set true so you can see the line where feet should align.
const DEBUG_FLOOR_LINE = true;

// Optional final manual tweaks.
// Positive = move down.
// Negative = move up.
const P1_FOOT_OFFSET_Y = -45;
const P2_FOOT_OFFSET_Y = -45;

const DISTANCE_FROM_CENTER = 140;

function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();

    img.onload = () => resolve(img);

    img.onerror = () => {
      reject(new Error(`Could not load image: ${src}`));
    };

    img.src = src;
  });
}

function getVisibleBounds(image) {
  const tempCanvas = document.createElement("canvas");
  const tempCtx = tempCanvas.getContext("2d");

  tempCanvas.width = image.width;
  tempCanvas.height = image.height;

  tempCtx.drawImage(image, 0, 0);

  const imageData = tempCtx.getImageData(0, 0, image.width, image.height);
  const data = imageData.data;

  let minX = image.width;
  let minY = image.height;
  let maxX = -1;
  let maxY = -1;

  for (let y = 0; y < image.height; y++) {
    for (let x = 0; x < image.width; x++) {
      const index = (y * image.width + x) * 4;
      const alpha = data[index + 3];

      if (alpha > 10) {
        if (x < minX) minX = x;
        if (y < minY) minY = y;
        if (x > maxX) maxX = x;
        if (y > maxY) maxY = y;
      }
    }
  }

  if (maxX === -1 || maxY === -1) {
    return {
      x: 0,
      y: 0,
      width: image.width,
      height: image.height,
    };
  }

  return {
    x: minX,
    y: minY,
    width: maxX - minX + 1,
    height: maxY - minY + 1,
  };
}

async function loadSpriteFrame(src) {
  const image = await loadImage(src);
  const bounds = getVisibleBounds(image);

  return {
    image,
    bounds,
    src,
  };
}

async function loadFramesAuto(folder) {
  const frames = [];
  let index = 0;

  while (true) {
    const src = `${folder}/${index}.png`;

    try {
      const frame = await loadSpriteFrame(src);
      frames.push(frame);
      index++;
    } catch {
      break;
    }
  }

  if (frames.length === 0) {
    throw new Error(`No sprites found in folder: ${folder}`);
  }

  console.log(`Loaded ${frames.length} sprites from ${folder}`);

  return frames;
}

class Stage {
  constructor({ image, x = 0, y = 0, scaleX = 1, scaleY = 1 }) {
    this.image = image;
    this.x = x;
    this.y = y;
    this.scaleX = scaleX;
    this.scaleY = scaleY;
  }

  draw(ctx) {
    const w = this.image.width * this.scaleX;
    const h = this.image.height * this.scaleY;

    ctx.drawImage(this.image, this.x, this.y, w, h);
  }
}

class Fighter {
  constructor({
    frames,
    centerX,
    groundY,
    scale = 2,
    flip = false,
    frameDelay = 8,
    footOffsetY = 0,
  }) {
    this.frames = frames;
    this.centerX = centerX;
    this.groundY = groundY;
    this.scale = scale;
    this.flip = flip;
    this.frameDelay = frameDelay;
    this.footOffsetY = footOffsetY;

    this.frameIndex = 0;
    this.tick = 0;
  }

  update() {
    this.tick++;

    if (this.tick >= this.frameDelay) {
      this.tick = 0;
      this.frameIndex = (this.frameIndex + 1) % this.frames.length;
    }
  }

  draw(ctx) {
    const frame = this.frames[this.frameIndex];
    const img = frame.image;
    const b = frame.bounds;

    const w = b.width * this.scale;
    const h = b.height * this.scale;

    const drawX = this.centerX - w / 2;
    const drawY = this.groundY - h + this.footOffsetY;

    ctx.save();

    if (this.flip) {
      ctx.translate(drawX + w, drawY);
      ctx.scale(-1, 1);

      ctx.drawImage(img, b.x, b.y, b.width, b.height, 0, 0, w, h);
    } else {
      ctx.drawImage(img, b.x, b.y, b.width, b.height, drawX, drawY, w, h);
    }

    ctx.restore();
  }
}

async function main() {
  const stageImage = await loadImage("/stages/stage1/bg.png");

  const char1Idle = await loadFramesAuto("/chars/char1/idle");
  const char2Idle = await loadFramesAuto("/chars/char2/idle");

  const stage = new Stage({
    image: stageImage,
    x: 0,
    y: 0,
    scaleX: canvas.width / stageImage.width,
    scaleY: canvas.height / stageImage.height,
  });

  const p1 = new Fighter({
    frames: char1Idle,
    centerX: canvas.width / 2 - DISTANCE_FROM_CENTER,
    groundY: GROUND_Y,
    scale: 2.5,
    flip: false,
    frameDelay: 8,
    footOffsetY: P1_FOOT_OFFSET_Y,
  });

  const p2 = new Fighter({
    frames: char2Idle,
    centerX: canvas.width / 2 + DISTANCE_FROM_CENTER,
    groundY: GROUND_Y,
    scale: 2.5,
    flip: true,
    frameDelay: 8,
    footOffsetY: P2_FOOT_OFFSET_Y,
  });

  function loop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    stage.draw(ctx);

    p1.update();
    p2.update();

    p1.draw(ctx);
    p2.draw(ctx);

    if (DEBUG_FLOOR_LINE) {
      ctx.fillStyle = "red";
      ctx.fillRect(0, GROUND_Y, canvas.width, 2);
    }

    requestAnimationFrame(loop);
  }

  loop();
}

main().catch((error) => {
  console.error(error);

  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "red";
  ctx.font = "24px Arial";
  ctx.fillText("Error loading game files", 40, 80);

  ctx.fillStyle = "white";
  ctx.font = "16px Arial";
  ctx.fillText(error.message, 40, 120);
});
