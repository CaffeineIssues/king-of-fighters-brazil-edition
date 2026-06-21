const definitionModules = import.meta.glob(
  "/src/assets/chars/*/definition.js",
  {
    eager: true,
    import: "default",
  },
);

const spriteModules = import.meta.glob(
  "/src/assets/chars/**/*.{png,jpg,jpeg,webp}",
  {
    eager: true,
    query: "?url",
    import: "default",
  },
);

export default class CharacterManager {
  constructor(game) {
    this.game = game;

    this.characters = [];

    this.boundsCache = new WeakMap();
  }

  async loadCharacter(id, options = {}) {
    const definitionPath = `/src/assets/chars/${id}/definition.js`;

    const definition = definitionModules[definitionPath];

    if (!definition) {
      throw new Error(`Character definition not found: ${id}`);
    }

    const character = {
      id: definition.id,
      name: definition.name,

      definition,

      x: options.x ?? 0,
      y: options.y ?? 0,

      velocityX: 0,
      velocityY: 0,

      facing: options.facing ?? 1,

      health: definition.health ?? 1000,
      maxHealth: definition.health ?? 1000,

      power: 0,

      state: "idle",

      currentAnimation: "idle",
      previousAnimation: "idle",

      frameIndex: 0,
      frameTimer: 0,

      attacking: false,

      scale: definition.scale ?? 2.5,
      walkSpeed: definition.walkSpeed ?? 3.2,

      animations: {},

      moves: definition.moves ?? {},
    };

    await this.loadAnimations(character);

    this.characters.push(character);

    return character;
  }

  async loadAnimations(character) {
    const root = `/src/assets/chars/${character.id}/`;

    const groups = {};

    for (const [path, url] of Object.entries(spriteModules)) {
      if (!path.startsWith(root)) continue;

      const relative = path.replace(root, "");

      const parts = relative.split("/");

      if (parts.length < 2) continue;

      const animation = parts[0];

      groups[animation] ??= [];

      groups[animation].push(String(url));
    }

    for (const animation in groups) {
      groups[animation].sort();

      const images = await Promise.all(
        groups[animation].map((src) => this.loadImage(src)),
      );

      character.animations[animation] = images;
    }
  }

  loadImage(src) {
    return new Promise((resolve, reject) => {
      const img = new Image();

      img.onload = () => resolve(img);

      img.onerror = reject;

      img.src = src;
    });
  }

  update() {
    for (const character of this.characters) {
      this.updateCharacter(character);
    }
  }

  updateCharacter(character) {
    const frames =
      character.animations[character.currentAnimation] ??
      character.animations.idle ??
      [];

    if (frames.length === 0) {
      return;
    }

    if (character.currentAnimation !== character.previousAnimation) {
      character.frameIndex = 0;
      character.frameTimer = 0;
      character.previousAnimation = character.currentAnimation;
    }

    character.frameTimer++;

    let animationSpeed = 8;

    switch (character.currentAnimation) {
      case "walk":
        animationSpeed = 6;
        break;

      case "light_punch":
        animationSpeed = 4;
        break;

      case "medium_punch":
        animationSpeed = 4;
        break;

      case "heavy_punch":
        animationSpeed = 5;
        break;

      default:
        animationSpeed = 10;
    }

    if (character.frameTimer >= animationSpeed) {
      character.frameTimer = 0;

      character.frameIndex++;

      if (character.frameIndex >= frames.length) {
        const attackAnimations = ["light_punch", "medium_punch", "heavy_punch"];

        if (attackAnimations.includes(character.currentAnimation)) {
          character.currentAnimation = "idle";
          character.attacking = false;
          character.frameIndex = 0;
        } else {
          character.frameIndex = 0;
        }
      }
    }
  }

  playAnimation(character, animation) {
    if (!character.animations[animation]) {
      return false;
    }

    if (character.currentAnimation === animation) {
      return true;
    }

    character.currentAnimation = animation;
    character.frameIndex = 0;
    character.frameTimer = 0;

    return true;
  }

  lightPunch(character) {
    if (character.attacking) return;

    if (!character.animations.light_punch) return;

    character.attacking = true;

    this.playAnimation(character, "light_punch");
  }

  mediumPunch(character) {
    if (character.attacking) return;

    if (!character.animations.medium_punch) return;

    character.attacking = true;

    this.playAnimation(character, "medium_punch");
  }

  heavyPunch(character) {
    if (character.attacking) return;

    if (!character.animations.heavy_punch) return;

    character.attacking = true;

    this.playAnimation(character, "heavy_punch");
  }

  draw(ctx) {
    for (const character of this.characters) {
      this.drawCharacter(ctx, character);
    }
  }

  drawCharacter(ctx, character) {
    const frames =
      character.animations[character.currentAnimation] ??
      character.animations.idle;

    if (!frames || frames.length === 0) {
      return;
    }

    const img = frames[character.frameIndex % frames.length];

    const bounds = this.getVisibleBounds(img);

    const drawWidth = bounds.width * character.scale;
    const drawHeight = bounds.height * character.scale;

    const drawX = -drawWidth / 2;
    const drawY = -drawHeight;

    ctx.save();

    ctx.translate(character.x, character.y);

    if (character.facing === -1) {
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

  getVisibleBounds(img) {
    if (this.boundsCache.has(img)) {
      return this.boundsCache.get(img);
    }

    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");

    canvas.width = img.width;
    canvas.height = img.height;

    ctx.drawImage(img, 0, 0);

    const { data, width, height } = ctx.getImageData(
      0,
      0,
      canvas.width,
      canvas.height,
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
      maxX < minX
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

    this.boundsCache.set(img, bounds);

    return bounds;
  }

  getCharacter(id) {
    return this.characters.find((character) => character.id === id);
  }

  removeCharacter(id) {
    this.characters = this.characters.filter(
      (character) => character.id !== id,
    );
  }

  clear() {
    this.characters = [];
  }
}
