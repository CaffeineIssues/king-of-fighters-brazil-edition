import brazilMap from "../../assets/ui/brazil-map.png";

const characterDefinitions = import.meta.glob(
  "/src/assets/chars/*/definition.js",
  {
    eager: true,
    import: "default",
  },
);

export default class CharacterSelectScene {
  constructor(game) {
    this.game = game;

    this.map = new Image();
    this.map.src = brazilMap;

    this.columns = 4;
    this.selectedIndex = 0;

    this.characters = Object.values(characterDefinitions).sort((a, b) =>
      a.name.localeCompare(b.name),
    );
  }

  update() {
    const input = this.game.inputSystem;

    if (input.wasPressed("F1")) {
      this.game.sceneManager.pop();
      return;
    }

    if (input.wasPressed("ArrowLeft")) {
      this.selectedIndex--;

      if (this.selectedIndex < 0) {
        this.selectedIndex = this.characters.length - 1;
      }
    }

    if (input.wasPressed("ArrowRight")) {
      this.selectedIndex++;

      if (this.selectedIndex >= this.characters.length) {
        this.selectedIndex = 0;
      }
    }

    if (input.wasPressed("ArrowUp")) {
      this.selectedIndex -= this.columns;

      if (this.selectedIndex < 0) {
        this.selectedIndex = 0;
      }
    }

    if (input.wasPressed("ArrowDown")) {
      this.selectedIndex += this.columns;

      if (this.selectedIndex >= this.characters.length) {
        this.selectedIndex = this.characters.length - 1;
      }
    }

    if (input.wasPressed("Enter")) {
      console.log("Selected:", this.characters[this.selectedIndex]);
    }
  }

  draw(ctx) {
    const canvas = this.game.canvas;

    const W = canvas.width;
    const H = canvas.height;

    const selected = this.characters[this.selectedIndex];

    ctx.textAlign = "left";
    ctx.textBaseline = "top";

    ctx.fillStyle = "#050505";
    ctx.fillRect(0, 0, W, H);

    const LEFT = 40;

    /*
     * HEADER
     */

    ctx.fillStyle = "#FFD700";
    ctx.font = "bold 20px Arial";

    ctx.fillText("KING OF FIGHTERS", LEFT, 12);

    ctx.fillStyle = "#00AA44";

    ctx.fillText("BRAZIL EDITION", LEFT, 36);

    /*
     * GRID
     */

    const gridX = LEFT;
    const gridY = 80;

    const portraitSize = 50;
    const gap = 8;

    this.characters.forEach((character, index) => {
      const col = index % this.columns;

      const row = Math.floor(index / this.columns);

      const x = gridX + col * (portraitSize + gap);

      const y = gridY + row * (portraitSize + gap);

      ctx.fillStyle = index === this.selectedIndex ? "#FFD700" : "#444";

      ctx.fillRect(x, y, portraitSize, portraitSize);

      ctx.fillStyle = "#111";

      ctx.fillRect(x + 2, y + 2, portraitSize - 4, portraitSize - 4);

      ctx.fillStyle = "#fff";
      ctx.font = "10px Arial";

      ctx.fillText(String(index + 1), x + 20, y + 18);
    });

    /*
     * MAP
     */

    const mapX = 290;
    const mapY = 55;

    const mapWidth = 640;
    const mapHeight = 250;

    if (this.map.complete) {
      ctx.drawImage(this.map, mapX, mapY, mapWidth, mapHeight);
    }

    /*
     * DEBUG BORDER
     */

    ctx.strokeStyle = "#333";
    ctx.strokeRect(mapX, mapY, mapWidth, mapHeight);

    /*
     * PIN
     */

    const pinX = mapX + (selected.mapX / 1000) * mapWidth;

    const pinY = mapY + (selected.mapY / 500) * mapHeight;

    const pulse = 6 + Math.sin(Date.now() * 0.01) * 2;

    ctx.beginPath();

    ctx.arc(pinX, pinY, pulse, 0, Math.PI * 2);

    ctx.fillStyle = "#ff0000";
    ctx.fill();

    /*
     * INFO PANEL
     */

    const infoX = LEFT;
    const infoY = 330;

    const infoWidth = W - LEFT * 2;

    const infoHeight = 150;

    ctx.fillStyle = "#111";

    ctx.fillRect(infoX, infoY, infoWidth, infoHeight);

    ctx.strokeStyle = "#666";

    ctx.strokeRect(infoX, infoY, infoWidth, infoHeight);

    ctx.fillStyle = "#FFD700";
    ctx.font = "bold 22px Arial";

    ctx.fillText(selected.name, infoX + 15, infoY + 15);

    ctx.fillStyle = "#fff";
    ctx.font = "16px Arial";

    ctx.fillText(`Cidade: ${selected.city}`, infoX + 15, infoY + 55);

    ctx.fillText(`Estado: ${selected.state}`, infoX + 15, infoY + 80);

    ctx.fillText(`Estilo: ${selected.style}`, infoX + 15, infoY + 105);

    /*
     * FOOTER
     */

    ctx.fillStyle = "#999";
    ctx.font = "13px Arial";

    ctx.fillText("ARROWS SELECT | ENTER CONFIRM | ESC BACK", LEFT, H - 20);
  }
}
