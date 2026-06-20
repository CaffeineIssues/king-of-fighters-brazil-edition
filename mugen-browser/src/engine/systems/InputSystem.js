export default class InputSystem {
  constructor() {
    this.keys = new Set();

    this.justPressed = new Set();

    window.addEventListener("keydown", (event) => {
      if (!this.keys.has(event.code)) {
        this.justPressed.add(event.code);
      }

      this.keys.add(event.code);
    });

    window.addEventListener("keyup", (event) => {
      this.keys.delete(event.code);
    });
  }

  isPressed(key) {
    return this.keys.has(key);
  }

  wasPressed(key) {
    return this.justPressed.has(key);
  }

  update() {
    this.justPressed.clear();
  }
}
