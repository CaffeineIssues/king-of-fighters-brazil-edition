import CharacterSelectScene from "./CharacterSelectScene";

export default class MenuScene {
  constructor(game) {
    this.game = game;

    this.options = ["START GAME", "OPTIONS", "EXIT"];

    this.selected = 0;

    this.game.audioSystem?.playMusic("menu");
  }

  async init() {
    console.log("Menu loaded");
  }

  update() {
    const input = this.game.inputSystem;

    if (input.wasPressed("ArrowUp")) {
      this.selected--;

      if (this.selected < 0) {
        this.selected = this.options.length - 1;
      }
    }

    if (input.wasPressed("ArrowDown")) {
      this.selected++;

      if (this.selected >= this.options.length) {
        this.selected = 0;
      }
    }

    if (input.wasPressed("Enter")) {
      this.select();
    }
  }

  select() {
    const option = this.options[this.selected];

    switch (option) {
      case "START GAME":
        this.game.sceneManager.push(CharacterSelectScene);
        break;

      case "OPTIONS":
        console.log("Options not implemented yet");
        break;

      case "EXIT":
        console.log("Exit selected");
        break;
    }
  }

  draw(ctx) {
    const canvas = this.game.canvas;

    // Background
    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Title
    ctx.textAlign = "center";

    ctx.fillStyle = "#ffcc00";

    ctx.font = "bold 72px Arial";

    ctx.fillText("KING OF FIGHTERS", canvas.width / 2, 150);

    ctx.font = "bold 42px Arial";

    ctx.fillText("BRAZIL EDITION", canvas.width / 2, 210);

    // Menu
    ctx.font = "bold 32px Arial";

    this.options.forEach((option, index) => {
      const y = 340 + index * 60;

      const selected = index === this.selected;

      ctx.fillStyle = selected ? "#ffcc00" : "#ffffff";

      ctx.fillText(selected ? `▶ ${option}` : option, canvas.width / 2, y);
    });

    // Footer
    ctx.font = "16px Arial";

    ctx.fillStyle = "#888888";

    ctx.fillText(
      "↑ ↓ Navigate    ENTER Select",
      canvas.width / 2,
      canvas.height - 40,
    );
  }

  destroy() {
    console.log("Leaving menu");
  }
}
