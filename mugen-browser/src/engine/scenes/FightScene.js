export default class FightScene {
  constructor(game) {
    this.game = game;

    this.ctx = game.ctx;
    this.canvas = game.canvas;

    this.context = game.gameContext; // GameContext

    this.stage = null;

    this.player1 = null;
    this.player2 = null;

    this.started = false;
  }

  async init() {
    this.stage = this.context.stage;

    const p1Idle = await loadAnimationFrames("p1", "idle");
    const p1Walk = await loadAnimationFrames("p1", "walk");

    const p2Idle = await loadAnimationFrames("p2", "idle");
    const p2Walk = await loadAnimationFrames("p2", "walk");

    const stageFromSelect = this.context.stage;

    this.player1 = createPlayer({
      x: this.canvas.width / 2 - 260,
      y: START_FEET_Y,
      facing: 1,
      idleFrames: p1Idle,
      walkFrames: p1Walk,
      keys: {
        left: ["KeyA", "a"],
        right: ["KeyD", "d"],
      },
    });

    this.player2 = createPlayer({
      x: this.canvas.width / 2 + 260,
      y: START_FEET_Y,
      facing: -1,
      idleFrames: p2Idle,
      walkFrames: p2Walk,
      keys: {
        left: ["Digit4", "Numpad4", "4"],
        right: ["Digit6", "Numpad6", "6"],
      },
    });

    this.started = true;

    console.log("FightScene ready:", stageFromSelect);
  }

  update() {
    const input = this.game.inputSystem;

    if (input.wasPressed("Escape")) {
      this.game.sceneManager.pop();
      return;
    }

    if (!this.started) return;

    updateStage(this.stage);

    updatePlayer(this.player1, input);
    updatePlayer(this.player2, input);
  }

  draw(ctx) {
    const W = this.canvas.width;
    const H = this.canvas.height;

    if (!this.started) return;

    drawStage(ctx, this.stage, this.canvas);

    const players = [this.player1, this.player2].sort((a, b) => a.y - b.y);

    for (const p of players) {
      drawPlayer(ctx, p);
    }

    /*
      HUD minimal
    */
    ctx.fillStyle = "#FFD700";
    ctx.font = "16px Arial";
    ctx.fillText(
      `ROUND ${this.context.round} | MODE ${this.context.mode}`,
      20,
      30,
    );

    ctx.fillStyle = "#888";
    ctx.fillText("ESC = back", 20, H - 20);
  }
}
