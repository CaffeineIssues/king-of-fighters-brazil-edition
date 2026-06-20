export default class AssetManager {
  constructor() {
    this.spriteModules = import.meta.glob(
      [
        "/src/assets/chars/*/idle/*.{png,jpg,jpeg,webp}",
        "/src/assets/chars/*/walk/*.{png,jpg,jpeg,webp}",
      ],
      {
        eager: true,
        query: "?url",
        import: "default",
      },
    );

    this.stageModules = import.meta.glob(
      "/src/assets/stages/*.{png,jpg,jpeg,webp}",
      {
        eager: true,
        query: "?url",
        import: "default",
      },
    );
  }

  naturalSort(a, b) {
    return a.localeCompare(a, undefined, {
      numeric: true,
      sensitivity: "base",
    });
  }

  loadImage(src) {
    return new Promise((resolve, reject) => {
      const img = new Image();

      img.onload = () => resolve(img);
      img.onerror = () => reject(new Error(`Could not load image: ${src}`));

      img.src = src;
    });
  }

  getCharacterFrameUrls(character, animation) {
    const folder = `/src/assets/chars/${character}/${animation}/`;

    return Object.entries(this.spriteModules)
      .filter(([path]) => path.startsWith(folder))
      .sort(([a], [b]) => this.naturalSort(a, b))
      .map(([, url]) => String(url));
  }

  async loadAnimationFrames(character, animation) {
    try {
      const urls = this.getCharacterFrameUrls(character, animation);

      if (!urls.length) {
        console.warn(`Missing ${character}/${animation}, using fallback`);

        const fallback = this.getCharacterFrameUrls("p1", animation);

        return Promise.all(fallback.map((u) => this.loadImage(u)));
      }

      return Promise.all(urls.map((u) => this.loadImage(u)));
    } catch (e) {
      console.error(e);
      return [];
    }
  }

  async loadStage() {
    const urls = Object.values(this.stageModules);

    if (!urls.length) {
      throw new Error("No stage images found");
    }

    const frames = await Promise.all(urls.map((u) => this.loadImage(u)));

    return {
      frames,
      frameIndex: 0,
      frameTimer: 0,
      animationSpeed: 10,
    };
  }
}
