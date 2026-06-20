import SceneManager from "./managers/SceneManager";
import InputSystem from "./systems/InputSystem";

import MenuScene from "./scenes/MenuScene";
import GameContext from "./contexts/GameContext";

export default class Game {
  constructor(canvas) {
    if (!canvas) {
      throw new Error('Canvas with id="game" not found.');
    }

    this.canvas = canvas;

    this.ctx = canvas.getContext("2d");

    this.gameContext = new GameContext();

    if (!this.ctx) {
      throw new Error("Could not get 2D context.");
    }

    this.ctx.imageSmoothingEnabled = false;

    this.sceneManager = new SceneManager(this);

    this.inputSystem = new InputSystem();

    this.lastTime = 0;

    this.loop = this.loop.bind(this);
  }

  async start() {
    await this.sceneManager.push(MenuScene);

    requestAnimationFrame(this.loop);
  }

  loop(timestamp) {
    const delta = timestamp - this.lastTime;

    this.lastTime = timestamp;

    this.sceneManager.update(delta);

    this.sceneManager.draw(this.ctx);

    this.inputSystem.update();

    requestAnimationFrame(this.loop);
  }
}
