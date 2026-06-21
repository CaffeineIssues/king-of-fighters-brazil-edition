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

    // =========================================================
    // PLAYER 1
    // =========================================================
    let p1Moving = false;

    const p1CanAct =
      this.p1.currentAnimation === "idle" ||
      this.p1.currentAnimation === "walk";

    if (p1CanAct) {
      if (input.isPressed("KeyA")) {
        this.p1.x -= this.p1.walkSpeed;
        this.p1.facing = -1;
        p1Moving = true;
      }

      if (input.isPressed("KeyD")) {
        this.p1.x += this.p1.walkSpeed;
        this.p1.facing = 1;
        p1Moving = true;
      }

      if (input.wasPressed("KeyJ") && this.p1.animations.light_punch) {
        this.p1.currentAnimation = "light_punch";
        this.p1.frameIndex = 0;
        this.p1.frameTimer = 0;
      } else if (input.wasPressed("KeyK") && this.p1.animations.medium_punch) {
        this.p1.currentAnimation = "medium_punch";
        this.p1.frameIndex = 0;
        this.p1.frameTimer = 0;
      } else if (input.wasPressed("KeyL") && this.p1.animations.heavy_punch) {
        this.p1.currentAnimation = "heavy_punch";
        this.p1.frameIndex = 0;
        this.p1.frameTimer = 0;
      } else {
        this.p1.currentAnimation = p1Moving ? "walk" : "idle";
      }
    }

    // =========================================================
    // PLAYER 2
    // =========================================================
    let p2Moving = false;

    const p2CanAct =
      this.p2.currentAnimation === "idle" ||
      this.p2.currentAnimation === "walk";

    if (p2CanAct) {
      if (input.isPressed("ArrowLeft")) {
        this.p2.x -= this.p2.walkSpeed;
        this.p2.facing = -1;
        p2Moving = true;
      }

      if (input.isPressed("ArrowRight")) {
        this.p2.x += this.p2.walkSpeed;
        this.p2.facing = 1;
        p2Moving = true;
      }

      if (input.wasPressed("Numpad1") && this.p2.animations.light_punch) {
        this.p2.currentAnimation = "light_punch";
        this.p2.frameIndex = 0;
        this.p2.frameTimer = 0;
      } else if (
        input.wasPressed("Numpad2") &&
        this.p2.animations.medium_punch
      ) {
        this.p2.currentAnimation = "medium_punch";
        this.p2.frameIndex = 0;
        this.p2.frameTimer = 0;
      } else if (
        input.wasPressed("Numpad3") &&
        this.p2.animations.heavy_punch
      ) {
        this.p2.currentAnimation = "heavy_punch";
        this.p2.frameIndex = 0;
        this.p2.frameTimer = 0;
      } else {
        this.p2.currentAnimation = p2Moving ? "walk" : "idle";
      }
    }

    // =========================================================
    // KEEP INSIDE SCREEN
    // =========================================================
    const limitX = (p) => {
      p.x = Math.max(60, Math.min(this.canvas.width - 60, p.x));
    };

    limitX(this.p1);
    limitX(this.p2);

    // =========================================================
    // UPDATE ANIMATIONS
    // =========================================================
    this.characters.update();
  }

  draw(renderCtx) {
    const W = this.canvas.width;
    const H = this.canvas.height;

    if (!this.started) return;

    // background
    renderCtx.fillStyle = "#000";
    renderCtx.fillRect(0, 0, W, H);

    // stage
    if (this.stage?.preview?.complete) {
      renderCtx.drawImage(this.stage.preview, 0, 0, W, H);
    }

    // characters
    this.characters.draw(renderCtx);

    // HUD
    renderCtx.fillStyle = "#FFD700";
    renderCtx.font = "16px Arial";
    renderCtx.fillText(
      `ROUND ${this.context.round} | MODE ${this.context.mode}`,
      20,
      30,
    );

    renderCtx.fillStyle = "#888";
    renderCtx.fillText("P1: A D J K L", 20, H - 40);
    renderCtx.fillText("P2: ← → NUM1 NUM2 NUM3", 20, H - 20);
  }
}
