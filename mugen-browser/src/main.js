const canvas = document.getElementById("game");

if (!canvas) {
  throw new Error('Canvas with id="game" was not found.');
}

const ctx = canvas.getContext("2d");

if (!ctx) {
  throw new Error("Could not get 2D canvas context.");
}

ctx.imageSmoothingEnabled = false;

/*
  Auto-load character frames.

  Folder structure:

  src/assets/chars/p1/idle/
  src/assets/chars/p1/walk/

  src/assets/chars/p2/idle/
  src/assets/chars/p2/walk/
*/
const spriteModules = import.meta.glob(
  [
    "/src/assets/chars/*/idle/*.{png,jpg,jpeg,webp}",
    "/src/assets/chars/*/walk/*.{png,jpg,jpeg,webp}",
  ],
  {
    eager: true,
    query: "?url",
    import: "default",
  },
);

/*
  Auto-load stage frames.

  Folder structure:

  src/assets/stages/
    0.png
    1.png
    2.png

  If you only have one stage image, just put one image there.
*/
const stageModules = import.meta.glob(
  "/src/assets/stages/*.{png,jpg,jpeg,webp}",
  {
    eager: true,
    query: "?url",
    import: "default",
  },
);

const SCALE = 2.5;
const SPEED = 3.2;

/*
  Character ground position.
  Bigger number = characters lower.
*/
const START_FEET_Y = canvas.height - 20;

/*
  "cover" fills the canvas and may crop a little.
  "stretch" forces the full stage image to fit the canvas.
*/
const STAGE_DRAW_MODE = "cover";

const boundsCache = new WeakMap();
const pressedKeys = new Set();

let player1;
let player2;
let stage;

function naturalSort(a, b) {
  return a.localeCompare(b, undefined, {
    numeric: true,
    sensitivity: "base",
  });
}

function getCharacterFrameUrls(characterName, animationName) {
  const folder = `/src/assets/chars/${characterName}/${animationName}/`;

  return Object.entries(spriteModules)
    .filter(([path]) => path.startsWith(folder))
    .sort(([pathA], [pathB]) => naturalSort(pathA, pathB))
    .map(([, url]) => String(url));
}

function getStageFrameUrls() {
  return Object.entries(stageModules)
    .sort(([pathA], [pathB]) => naturalSort(pathA, pathB))
    .map(([, url]) => String(url));
}

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

async function loadAnimationFrames(characterName, animationName) {
  const urls = getCharacterFrameUrls(characterName, animationName);

  if (urls.length === 0) {
    throw new Error(
      `No frames found for ${characterName}/${animationName}. Check src/assets/chars/${characterName}/${animationName}/`,
    );
  }

  return Promise.all(urls.map(loadImage));
}

async function loadStage() {
  const urls = getStageFrameUrls();

  if (urls.length === 0) {
    throw new Error("No stage images found. Check src/assets/stages/");
  }

  const frames = await Promise.all(urls.map(loadImage));

  return {
    frames,
    frameIndex: 0,
    frameTimer: 0,
    animationSpeed: 10,
  };
}

function drawImageCover(img, x, y, width, height) {
  const imageRatio = img.width / img.height;
  const targetRatio = width / height;

  let sourceX = 0;
  let sourceY = 0;
  let sourceWidth = img.width;
  let sourceHeight = img.height;

  if (imageRatio > targetRatio) {
    sourceWidth = img.height * targetRatio;
    sourceX = (img.width - sourceWidth) / 2;
  } else {
    sourceHeight = img.width / targetRatio;
    sourceY = (img.height - sourceHeight) / 2;
  }

  ctx.drawImage(
    img,
    sourceX,
    sourceY,
    sourceWidth,
    sourceHeight,
    x,
    y,
    width,
    height,
  );
}

function updateStage() {
  if (stage.frames.length <= 1) {
    return;
  }

  stage.frameTimer++;

  if (stage.frameTimer >= stage.animationSpeed) {
    stage.frameTimer = 0;
    stage.frameIndex = (stage.frameIndex + 1) % stage.frames.length;
  }
}

function drawStage() {
  const img = stage.frames[stage.frameIndex];

  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  if (STAGE_DRAW_MODE === "stretch") {
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    return;
  }

  drawImageCover(img, 0, 0, canvas.width, canvas.height);
}

function getVisibleBounds(img) {
  if (boundsCache.has(img)) {
    return boundsCache.get(img);
  }

  const tempCanvas = document.createElement("canvas");
  const tempCtx = tempCanvas.getContext("2d");

  tempCanvas.width = img.width;
  tempCanvas.height = img.height;

  tempCtx.drawImage(img, 0, 0);

  const { data, width, height } = tempCtx.getImageData(
    0,
    0,
    tempCanvas.width,
    tempCanvas.height,
  );

  let minX = width;
  let minY = height;
  let maxX = 0;
  let maxY = 0;

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const alpha = data[(y * width + x) * 4 + 3];

      if (alpha > 0) {
        minX = Math.min(minX, x);
        minY = Math.min(minY, y);
        maxX = Math.max(maxX, x);
        maxY = Math.max(maxY, y);
      }
    }
  }

  const bounds =
    maxX < minX || maxY < minY
      ? {
          x: 0,
          y: 0,
          width: img.width,
          height: img.height,
        }
      : {
          x: minX,
          y: minY,
          width: maxX - minX + 1,
          height: maxY - minY + 1,
        };

  boundsCache.set(img, bounds);

  return bounds;
}

function createPlayer({ x, y, facing, idleFrames, walkFrames, keys }) {
  return {
    x,
    y,
    facing,

    idleFrames,
    walkFrames,

    keys,

    currentAnimation: "idle",
    previousAnimation: "idle",

    frameIndex: 0,
    frameTimer: 0,

    speed: SPEED,
    scale: SCALE,
  };
}

window.addEventListener("keydown", (event) => {
  pressedKeys.add(event.code);
  pressedKeys.add(event.key.toLowerCase());

  const gameKeys = [
    "KeyW",
    "KeyA",
    "KeyS",
    "KeyD",
    "Digit8",
    "Digit4",
    "Digit5",
    "Digit6",
    "Numpad8",
    "Numpad4",
    "Numpad5",
    "Numpad6",
  ];

  if (gameKeys.includes(event.code)) {
    event.preventDefault();
  }
});

window.addEventListener("keyup", (event) => {
  pressedKeys.delete(event.code);
  pressedKeys.delete(event.key.toLowerCase());
});

function isDown(...keys) {
  return keys.some((key) => pressedKeys.has(key));
}

function updatePlayer(player) {
  let dx = 0;

  /*
    Only horizontal movement.
    W/S and 8/5 are ignored for movement.
  */
  if (isDown(...player.keys.left)) {
    dx -= 1;
  }

  if (isDown(...player.keys.right)) {
    dx += 1;
  }

  const isMoving = dx !== 0;

  if (isMoving) {
    player.x += dx * player.speed;
    player.currentAnimation = "walk";

    if (dx < 0) {
      player.facing = -1;
    } else if (dx > 0) {
      player.facing = 1;
    }
  } else {
    player.currentAnimation = "idle";
  }

  if (player.currentAnimation !== player.previousAnimation) {
    player.frameIndex = 0;
    player.frameTimer = 0;
    player.previousAnimation = player.currentAnimation;
  }

  /*
    Lock player to the ground axis.
    This prevents walking up or down.
  */
  player.y = START_FEET_Y;

  /*
    Keep players inside the canvas horizontally.
  */
  player.x = Math.max(60, Math.min(canvas.width - 60, player.x));

  const frames =
    player.currentAnimation === "walk" ? player.walkFrames : player.idleFrames;

  const animationSpeed = player.currentAnimation === "walk" ? 7 : 12;

  player.frameTimer++;

  if (player.frameTimer >= animationSpeed) {
    player.frameTimer = 0;
    player.frameIndex = (player.frameIndex + 1) % frames.length;
  }
}

function drawPlayer(player) {
  const frames =
    player.currentAnimation === "walk" ? player.walkFrames : player.idleFrames;

  const img = frames[player.frameIndex % frames.length];
  const bounds = getVisibleBounds(img);

  const drawWidth = bounds.width * player.scale;
  const drawHeight = bounds.height * player.scale;

  const drawX = -drawWidth / 2;
  const drawY = -drawHeight;

  ctx.save();

  ctx.translate(player.x, player.y);

  if (player.facing === -1) {
    ctx.scale(-1, 1);
  }

  ctx.drawImage(
    img,
    bounds.x,
    bounds.y,
    bounds.width,
    bounds.height,
    drawX,
    drawY,
    drawWidth,
    drawHeight,
  );

  ctx.restore();
}

function gameLoop() {
  updateStage();
  drawStage();

  updatePlayer(player1);
  updatePlayer(player2);

  /*
    Draw lower character last.
    Since both are locked to same Y,
    this mostly keeps the code ready for future jump/crouch.
  */
  const players = [player1, player2].sort((a, b) => a.y - b.y);

  for (const player of players) {
    drawPlayer(player);
  }

  requestAnimationFrame(gameLoop);
}

async function startGame() {
  stage = await loadStage();

  const p1Idle = await loadAnimationFrames("p1", "idle");
  const p1Walk = await loadAnimationFrames("p1", "walk");

  const p2Idle = await loadAnimationFrames("p2", "idle");
  const p2Walk = await loadAnimationFrames("p2", "walk");

  player1 = createPlayer({
    x: canvas.width / 2 - 260,
    y: START_FEET_Y,
    facing: 1,
    idleFrames: p1Idle,
    walkFrames: p1Walk,
    keys: {
      up: ["KeyW", "w"],
      left: ["KeyA", "a"],
      down: ["KeyS", "s"],
      right: ["KeyD", "d"],
    },
  });

  player2 = createPlayer({
    x: canvas.width / 2 + 260,
    y: START_FEET_Y,
    facing: -1,
    idleFrames: p2Idle,
    walkFrames: p2Walk,
    keys: {
      up: ["Digit8", "Numpad8", "8"],
      left: ["Digit4", "Numpad4", "4"],
      down: ["Digit5", "Numpad5", "5"],
      right: ["Digit6", "Numpad6", "6"],
    },
  });

  requestAnimationFrame(gameLoop);
}

startGame().catch((error) => {
  console.error(error);
});
