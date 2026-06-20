import FightScene from "./FightScene";

const stageDefinitions = import.meta.glob(
  "/src/assets/stages/*/definition.js",
  {
    eager: true,
    import: "default",
  },
);

const previewModules = import.meta.glob("/src/assets/stages/*/preview.*", {
  eager: true,
  query: "?url",
  import: "default",
});

export default class StageSelectScene {
  constructor(game) {
    this.game = game;
    this.selectedIndex = 0;

    this.stages = Object.values(stageDefinitions).map((stage) => {
      const previewEntry = Object.entries(previewModules).find(([path]) =>
        path.includes(`/stages/${stage.id}/preview.`),
      );

      const previewSrc = previewEntry?.[1] ?? null;
      const preview = previewSrc ? new Image() : null;

      if (preview) {
        preview.src = previewSrc;
      }

      return {
        ...stage,
        preview,
      };
    });
  }

  update() {
    const input = this.game.inputSystem;

    if (input.wasPressed("Escape")) {
      this.game.sceneManager.pop();
      return;
    }

    if (input.wasPressed("ArrowLeft")) {
      this.selectedIndex--;

      if (this.selectedIndex < 0) {
        this.selectedIndex = this.stages.length - 1;
      }
    }

    if (input.wasPressed("ArrowRight")) {
      this.selectedIndex++;

      if (this.selectedIndex >= this.stages.length) {
        this.selectedIndex = 0;
      }
    }

    if (input.wasPressed("Enter")) {
      const selected = this.stages[this.selectedIndex];

      console.log("Stage Selected:", selected);

      this.game.selectedStage = selected;

      // ✅ FIXED: pass class, NOT instance
      this.game.sceneManager.push(FightScene);
    }
  }

  draw(ctx) {
    const canvas = this.game.canvas;

    const W = canvas.width;
    const H = canvas.height;

    const stage = this.stages[this.selectedIndex];

    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, W, H);

    // HEADER
    ctx.fillStyle = "#FFD700";
    ctx.font = "bold 32px Arial";
    ctx.fillText("STAGE SELECT", 30, 20);

    // PREVIEW
    const previewX = 60;
    const previewY = 80;
    const previewW = 840;
    const previewH = 320;

    ctx.fillStyle = "#222";
    ctx.fillRect(previewX, previewY, previewW, previewH);

    if (stage.preview && stage.preview.complete) {
      ctx.drawImage(stage.preview, previewX, previewY, previewW, previewH);
    }

    ctx.strokeStyle = "#FFD700";
    ctx.lineWidth = 3;
    ctx.strokeRect(previewX, previewY, previewW, previewH);

    // INFO
    ctx.fillStyle = "#FFFFFF";
    ctx.font = "bold 26px Arial";
    ctx.fillText(stage.name, 60, 430);

    ctx.font = "18px Arial";
    ctx.fillText(`${stage.city} - ${stage.state}`, 60, 465);

    ctx.fillStyle = "#AAAAAA";
    ctx.fillText(stage.description || "", 60, 495);

    // SELECTOR
    ctx.fillStyle = "#FFD700";
    ctx.font = "18px Arial";
    ctx.fillText(`${this.selectedIndex + 1}/${this.stages.length}`, 860, 430);

    // FOOTER
    ctx.fillStyle = "#888";
    ctx.font = "14px Arial";
    ctx.fillText(
      "LEFT/RIGHT SELECT STAGE | ENTER CONFIRM | ESC BACK",
      30,
      H - 20,
    );
  }
}
