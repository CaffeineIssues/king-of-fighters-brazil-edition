export default class SceneManager {
  constructor(game) {
    this.game = game;
    this.stack = [];
  }

  async push(SceneClass) {
    // Allow only constructor functions (classes)
    const scene = new SceneClass(this.game);

    this.stack.push(scene);

    if (scene.init) {
      await scene.init();
    }
  }

  async pop() {
    // Never remove the root scene
    if (this.stack.length <= 1) {
      return;
    }

    const scene = this.stack.pop();

    if (scene?.destroy) {
      await scene.destroy();
    }
  }

  async replace(SceneClass) {
    if (this.stack.length > 0) {
      const scene = this.stack.pop();

      if (scene?.destroy) {
        await scene.destroy();
      }
    }

    await this.push(SceneClass);
  }

  clear() {
    this.stack = [];
  }

  get currentScene() {
    return this.stack[this.stack.length - 1];
  }

  update(delta) {
    this.currentScene?.update?.(delta);
  }

  draw(ctx) {
    this.currentScene?.draw?.(ctx);
  }
}
