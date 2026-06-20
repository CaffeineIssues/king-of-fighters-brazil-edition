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

    // -----------------------------
    // STAGE
    // -----------------------------
    this.stage = ctx.stage;

    const groundY = this.stage?.groundY ?? 520;

    if (!ctx.player1 || !ctx.player2) {
      throw new Error("FightScene: Missing player1 or player2 in GameContext");
    }

    // -----------------------------
    // CHARACTERS (IDs ONLY)
    // -----------------------------
    const p1Id = ctx.player1;
    const p2Id = ctx.player2;

    // -----------------------------
    // LOAD CHARACTERS
    // -----------------------------
    this.p1 = await this.characters.loadCharacter(p1Id, {
      x: this.canvas.width / 2 - 260,
      y: groundY,
      facing: 1,
    });

    this.p2 = await this.characters.loadCharacter(p2Id, {
      x: this.canvas.width / 2 + 260,
      y: groundY,
      facing: -1,
    });

    this.started = true;

    console.log("FightScene ready:", p1Id, "vs", p2Id);
  }

  update() {
    const input = this.game.inputSystem;

    if (input.wasPressed("Escape")) {
      this.game.sceneManager.pop();
      return;
    }

    if (!this.started) return;

    // -----------------------------
    // STAGE LOGIC (ONLY IF YOU WANT ANIMATION LATER)
    // -----------------------------
    // Currently NO updateStage needed (static stage system)

    // -----------------------------
    // PLAYER INPUT (TEMP SYSTEM)
    // -----------------------------
    if (input.isDown?.("KeyA")) this.p1.x -= this.p1.walkSpeed;
    if (input.isDown?.("KeyD")) this.p1.x += this.p1.walkSpeed;

    if (input.isDown?.("ArrowLeft")) this.p2.x -= this.p2.walkSpeed;
    if (input.isDown?.("ArrowRight")) this.p2.x += this.p2.walkSpeed;

    // -----------------------------
    // CHARACTER ANIMATIONS
    // -----------------------------
    this.characters.update();
  }

  draw(renderCtx) {
    const H = this.canvas.height;
    const W = this.canvas.width;

    if (!this.started) return;

    // -----------------------------
    // CLEAR SCREEN
    // -----------------------------
    renderCtx.fillStyle = "#000";
    renderCtx.fillRect(0, 0, W, H);

    // -----------------------------
    // STAGE DRAW (STATIC IMAGE OR FRAMES)
    // -----------------------------
    if (this.stage?.preview) {
      const img = this.stage.preview;

      if (img.complete) {
        renderCtx.drawImage(img, 0, 0, W, H);
      }
    }

    // -----------------------------
    // CHARACTERS DRAW
    // -----------------------------
    this.characters.draw(renderCtx);

    // -----------------------------
    // HUD
    // -----------------------------
    renderCtx.fillStyle = "#FFD700";
    renderCtx.font = "16px Arial";
    renderCtx.fillText(
      `ROUND ${this.context.round} | MODE ${this.context.mode}`,
      20,
      30,
    );

    renderCtx.fillStyle = "#888";
    renderCtx.fillText("ESC = back", 20, H - 20);
  }
}
