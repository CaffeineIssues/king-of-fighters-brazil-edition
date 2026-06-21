export default class FightScene {
  constructor(game) {
    this.game = game;

    this.ctx = game.ctx;
    this.canvas = game.canvas;

    this.context = game.gameContext;
    this.characters = game.characters;

    this.p1 = null;
    this.p2 = null;

    this.stage = null;
    this.started = false;

    // -----------------------------
    // HUD STATE
    // -----------------------------
    this.roundTime = 99;
    this.timer = 0;
    this.lastTime = null;
  }

  async init() {
    const ctx = this.context;

    this.stage = ctx.stage;

    const groundY = this.stage?.groundY ?? 520;

    if (!ctx.player1 || !ctx.player2) {
      throw new Error("FightScene: Missing player1 or player2 in GameContext");
    }

    this.p1 = await this.characters.loadCharacter(ctx.player1, {
      x: this.canvas.width / 2 - 260,
      y: groundY,
      facing: 1,
    });

    this.p2 = await this.characters.loadCharacter(ctx.player2, {
      x: this.canvas.width / 2 + 260,
      y: groundY,
      facing: -1,
    });

    this.started = true;

    console.log("FightScene ready:", ctx.player1, "vs", ctx.player2);
  }

  update() {
    const input = this.game.inputSystem;

    if (input.wasPressed("Escape")) {
      this.game.sceneManager.pop();
      return;
    }

    if (!this.started) return;

    // -----------------------------
    // TIMER UPDATE
    // -----------------------------
    const now = performance.now();

    if (this.lastTime === null) this.lastTime = now;

    this.timer += now - this.lastTime;
    this.lastTime = now;

    if (this.timer >= 1000) {
      this.timer = 0;

      if (this.roundTime > 0) {
        this.roundTime--;
      }
    }

    // -----------------------------
    // PLAYER 1
    // -----------------------------
    let p1Moving = false;

    if (
      this.p1.currentAnimation === "idle" ||
      this.p1.currentAnimation === "walk"
    ) {
      if (input.isPressed?.("KeyA")) {
        this.p1.x -= this.p1.walkSpeed;
        this.p1.facing = -1;
        p1Moving = true;
      }

      if (input.isPressed?.("KeyD")) {
        this.p1.x += this.p1.walkSpeed;
        this.p1.facing = 1;
        p1Moving = true;
      }

      if (input.wasPressed?.("KeyJ") && this.p1.animations.light_punch) {
        this.p1.currentAnimation = "light_punch";
        this.p1.frameIndex = 0;
        this.p1.frameTimer = 0;
      } else if (
        input.wasPressed?.("KeyK") &&
        this.p1.animations.medium_punch
      ) {
        this.p1.currentAnimation = "medium_punch";
        this.p1.frameIndex = 0;
        this.p1.frameTimer = 0;
      } else if (input.wasPressed?.("KeyL") && this.p1.animations.heavy_punch) {
        this.p1.currentAnimation = "heavy_punch";
        this.p1.frameIndex = 0;
        this.p1.frameTimer = 0;
      } else {
        this.p1.currentAnimation = p1Moving ? "walk" : "idle";
      }
    }

    // -----------------------------
    // PLAYER 2
    // -----------------------------
    let p2Moving = false;

    if (
      this.p2.currentAnimation === "idle" ||
      this.p2.currentAnimation === "walk"
    ) {
      if (input.isPressed?.("ArrowLeft")) {
        this.p2.x -= this.p2.walkSpeed;
        this.p2.facing = -1;
        p2Moving = true;
      }

      if (input.isPressed?.("ArrowRight")) {
        this.p2.x += this.p2.walkSpeed;
        this.p2.facing = 1;
        p2Moving = true;
      }

      if (input.wasPressed?.("Numpad1") && this.p2.animations.light_punch) {
        this.p2.currentAnimation = "light_punch";
        this.p2.frameIndex = 0;
        this.p2.frameTimer = 0;
      } else if (
        input.wasPressed?.("Numpad2") &&
        this.p2.animations.medium_punch
      ) {
        this.p2.currentAnimation = "medium_punch";
        this.p2.frameIndex = 0;
        this.p2.frameTimer = 0;
      } else if (
        input.wasPressed?.("Numpad3") &&
        this.p2.animations.heavy_punch
      ) {
        this.p2.currentAnimation = "heavy_punch";
        this.p2.frameIndex = 0;
        this.p2.frameTimer = 0;
      } else {
        this.p2.currentAnimation = p2Moving ? "walk" : "idle";
      }
    }

    // -----------------------------
    // SCREEN LIMITS
    // -----------------------------
    this.p1.x = Math.max(60, Math.min(this.canvas.width - 60, this.p1.x));
    this.p2.x = Math.max(60, Math.min(this.canvas.width - 60, this.p2.x));

    // -----------------------------
    // UPDATE CHARACTERS
    // -----------------------------
    this.characters.update();
  }

  draw(renderCtx) {
    const W = this.canvas.width;
    const H = this.canvas.height;

    if (!this.started) return;

    // -----------------------------
    // CLEAR
    // -----------------------------
    renderCtx.fillStyle = "#000";
    renderCtx.fillRect(0, 0, W, H);

    // -----------------------------
    // STAGE
    // -----------------------------
    if (this.stage?.preview?.complete) {
      renderCtx.drawImage(this.stage.preview, 0, 0, W, H);
    }

    // -----------------------------
    // CHARACTERS
    // -----------------------------
    this.characters.draw(renderCtx);

    // -----------------------------
    // HUD
    // -----------------------------
    this.drawHUD(renderCtx);
  }

  drawHUD(ctx) {
    const W = this.canvas.width;

    const p1 = this.p1;
    const p2 = this.p2;

    // -----------------------------
    // BACK BAR
    // -----------------------------
    ctx.fillStyle = "#222";
    ctx.fillRect(50, 20, 300, 18);
    ctx.fillRect(W - 350, 20, 300, 18);

    // -----------------------------
    // LIFE BAR
    // -----------------------------
    const p1Life = (p1.health / p1.maxHealth) * 300;
    const p2Life = (p2.health / p2.maxHealth) * 300;

    ctx.fillStyle = "#00ff66";
    ctx.fillRect(50, 20, p1Life, 18);

    ctx.fillStyle = "#00ff66";
    ctx.fillRect(W - 350, 20, p2Life, 18);

    // -----------------------------
    // TIMER
    // -----------------------------
    ctx.fillStyle = "#fff";
    ctx.font = "22px Arial";
    ctx.textAlign = "center";
    ctx.fillText(this.roundTime, W / 2, 35);

    // -----------------------------
    // NAMES
    // -----------------------------
    ctx.font = "14px Arial";
    ctx.textAlign = "left";
    ctx.fillText(p1.name, 50, 60);

    ctx.textAlign = "right";
    ctx.fillText(p2.name, W - 50, 60);
  }
}
