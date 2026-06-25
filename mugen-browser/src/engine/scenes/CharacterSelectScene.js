import brazilMap from "../../assets/ui/brazil-map.png";
import StageSelectScene from "./StageSelectScene";

const characterDefinitions = import.meta.glob(
  "/src/assets/chars/*/definition.js",
  {
    eager: true,
    import: "default",
  },
);

const portraitModules = import.meta.glob("/src/assets/chars/*/portrait.*", {
  eager: true,
  query: "?url",
  import: "default",
});

const portraitBigModules = import.meta.glob(
  "/src/assets/chars/*/portrait_big.*",
  {
    eager: true,
    query: "?url",
    import: "default",
  },
);

export default class CharacterSelectScene {
  constructor(game) {
    this.game = game;
    this.game.audioSystem?.stopMusic();
    this.map = new Image();
    this.map.src = brazilMap;

    this.columns = 4;
    this.selectedIndex = 0;

    this.characters = Object.values(characterDefinitions).map((character) => {
      const portraitEntry = Object.entries(portraitModules).find(([path]) =>
        path.includes(`/chars/${character.id}/portrait.`),
      );

      const portraitBigEntry = Object.entries(portraitBigModules).find(
        ([path]) => path.includes(`/chars/${character.id}/portrait_big.`),
      );

      const portraitSrc = portraitEntry?.[1] ?? null;

      const portraitBigSrc = portraitBigEntry?.[1] ?? null;

      const portrait = portraitSrc ? new Image() : null;

      const portraitBig = portraitBigSrc ? new Image() : null;

      if (portrait) {
        portrait.src = portraitSrc;
      }

      if (portraitBig) {
        portraitBig.src = portraitBigSrc;
      }

      return {
        ...character,

        portrait,
        portraitBig,
      };
    });

    if (this.characters.length === 0) {
      throw new Error("No characters found in assets/chars");
    }
  }

  update() {
    const input = this.game.inputSystem;

    if (input.wasPressed("Escape") || input.wasPressed("F1")) {
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
      const selected = this.characters[this.selectedIndex];

      const ctx = this.game.gameContext;

      //ctx.setAvailableCharacters(this.characters.map((c) => c.id));
      ctx.setAvailableCharacters(["he_man", "mestre_thaynan"]);
      console.log(ctx.availableCharacters);

      ctx.setPlayer1(selected.id);

      this.game.sceneManager.push(StageSelectScene);
    }
  }

  draw(ctx) {
    const canvas = this.game.canvas;

    const W = canvas.width;
    const H = canvas.height;

    const selected = this.characters[this.selectedIndex];

    ctx.fillStyle = "#050505";
    ctx.fillRect(0, 0, W, H);

    ctx.textAlign = "left";
    ctx.textBaseline = "top";

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

      if (character.portrait && character.portrait.complete) {
        ctx.drawImage(
          character.portrait,
          x + 2,
          y + 2,
          portraitSize - 4,
          portraitSize - 4,
        );
      }
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
     * PIN
     */

    const pinX = mapX + (selected.mapX / 1000) * mapWidth;

    const pinY = mapY + (selected.mapY / 500) * mapHeight;

    const pulse = 6 + Math.sin(Date.now() * 0.01) * 2;

    ctx.beginPath();

    ctx.arc(pinX, pinY, pulse, 0, Math.PI * 2);

    ctx.fillStyle = "#FF0000";
    ctx.fill();

    /*
     * BIG PORTRAIT
     */

    const portraitX = 730;
    const portraitY = 320;

    const portraitWidth = 180;
    const portraitHeight = 180;

    ctx.fillStyle = "#222";

    ctx.fillRect(portraitX, portraitY, portraitWidth, portraitHeight);

    ctx.strokeStyle = "#FFD700";

    ctx.strokeRect(portraitX, portraitY, portraitWidth, portraitHeight);

    const image = selected.portraitBig || selected.portrait;

    if (image && image.complete) {
      ctx.drawImage(image, portraitX, portraitY, portraitWidth, portraitHeight);
    }

    /*
     * INFO
     */

    ctx.fillStyle = "#111";

    ctx.fillRect(40, 330, 650, 150);

    ctx.strokeStyle = "#666";

    ctx.strokeRect(40, 330, 650, 150);

    ctx.fillStyle = "#FFD700";

    ctx.font = "bold 22px Arial";

    ctx.fillText(selected.name, 55, 345);

    ctx.fillStyle = "#FFFFFF";

    ctx.font = "16px Arial";

    ctx.fillText(`Cidade: ${selected.city}`, 55, 385);

    ctx.fillText(`Estado: ${selected.state}`, 55, 410);

    ctx.fillText(`Estilo: ${selected.style}`, 55, 435);

    /*
     * FOOTER
     */

    ctx.fillStyle = "#999";

    ctx.font = "13px Arial";

    ctx.fillText("ARROWS SELECT | ENTER CONFIRM | ESC BACK", LEFT, H - 20);
  }
}
