import SceneManager from "./managers/SceneManager";
import InputSystem from "./systems/InputSystem";
import AssetManager from "./managers/AssetManager";
import MenuScene from "./scenes/MenuScene";
import GameContext from "./contexts/GameContext";
import CharacterManager from "./managers/CharacterManager";
import AudioSystem from "./systems/AudioSystem";

import menuMusic from "../assets/audio/pulo_da_gaita_8bit.wav";

export default class Game {
  constructor(canvas) {
    if (!canvas) {
      throw new Error('Canvas with id="game" not found.');
    }

    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");

    if (!this.ctx) {
      throw new Error("Could not get 2D context.");
    }

    this.ctx.imageSmoothingEnabled = false;

    // -----------------------------
    // CORE CONTEXT
    // -----------------------------
    this.gameContext = new GameContext();

    // -----------------------------
    // SYSTEMS / MANAGERS
    // -----------------------------
    this.sceneManager = new SceneManager(this);
    this.inputSystem = new InputSystem();
    this.assets = new AssetManager();
    this.characters = new CharacterManager(this);

    // -----------------------------
    // AUDIO SYSTEM
    // -----------------------------
    this.audioSystem = new AudioSystem();

    this.audioSystem.registerMusic("menu", menuMusic, {
      loop: true,
      volume: 0.6,
    });

    // Important: unlocks audio after first key/click
    this.audioSystem.init();

    // -----------------------------
    // GAME LOOP
    // -----------------------------
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
