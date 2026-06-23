export default class AudioSystem {
  constructor() {
    this.musicTracks = new Map();
    this.soundEffects = new Map();

    this.currentMusicId = null;
    this.currentMusic = null;

    this.musicVolume = 0.6;
    this.sfxVolume = 0.8;

    this.enabled = true;
    this.musicEnabled = true;
    this.sfxEnabled = true;

    this.pendingMusicId = null;
    this.pendingMusicOptions = null;

    this.unlocked = false;

    this.handleFirstInteraction = this.handleFirstInteraction.bind(this);
  }

  init() {
    window.addEventListener("pointerdown", this.handleFirstInteraction, {
      once: true,
    });

    window.addEventListener("keydown", this.handleFirstInteraction, {
      once: true,
    });
  }

  handleFirstInteraction() {
    this.unlocked = true;

    if (this.pendingMusicId) {
      this.playMusic(this.pendingMusicId, this.pendingMusicOptions || {});
    }
  }

  registerMusic(id, src, options = {}) {
    if (!id || !src) {
      console.warn("AudioSystem: registerMusic requires id and src");
      return;
    }

    const audio = new Audio(src);

    audio.loop = options.loop ?? true;
    audio.volume = options.volume ?? this.musicVolume;
    audio.preload = options.preload ?? "auto";

    this.musicTracks.set(id, audio);
  }

  registerSfx(id, src, options = {}) {
    if (!id || !src) {
      console.warn("AudioSystem: registerSfx requires id and src");
      return;
    }

    const audio = new Audio(src);

    audio.loop = options.loop ?? false;
    audio.volume = options.volume ?? this.sfxVolume;
    audio.preload = options.preload ?? "auto";

    this.soundEffects.set(id, audio);
  }

  async playMusic(id, options = {}) {
    if (!this.enabled || !this.musicEnabled) return;

    const audio = this.musicTracks.get(id);

    if (!audio) {
      console.warn(`AudioSystem: music "${id}" was not registered`);
      return;
    }

    this.pendingMusicId = id;
    this.pendingMusicOptions = options;

    // Avoid restarting same music when moving MenuScene -> CharacterSelectScene
    if (this.currentMusicId === id && this.currentMusic) {
      if (this.currentMusic.paused) {
        try {
          await this.currentMusic.play();
        } catch (error) {
          console.warn("AudioSystem: music blocked until interaction", error);
        }
      }

      return;
    }

    if (this.currentMusic) {
      this.currentMusic.pause();
      this.currentMusic.currentTime = 0;
    }

    this.currentMusicId = id;
    this.currentMusic = audio;

    audio.loop = options.loop ?? true;
    audio.volume = options.volume ?? this.musicVolume;

    try {
      await audio.play();
    } catch (error) {
      console.warn("AudioSystem: music blocked until user interaction", error);
    }
  }

  stopMusic() {
    if (!this.currentMusic) return;

    this.currentMusic.pause();
    this.currentMusic.currentTime = 0;

    this.currentMusic = null;
    this.currentMusicId = null;
    this.pendingMusicId = null;
    this.pendingMusicOptions = null;
  }

  pauseMusic() {
    if (!this.currentMusic) return;

    this.currentMusic.pause();
  }

  async resumeMusic() {
    if (!this.currentMusic) return;
    if (!this.enabled || !this.musicEnabled) return;

    try {
      await this.currentMusic.play();
    } catch (error) {
      console.warn("AudioSystem: could not resume music", error);
    }
  }

  playSfx(id, options = {}) {
    if (!this.enabled || !this.sfxEnabled) return;

    const baseAudio = this.soundEffects.get(id);

    if (!baseAudio) {
      console.warn(`AudioSystem: sfx "${id}" was not registered`);
      return;
    }

    // Clone so repeated hits can overlap
    const sfx = baseAudio.cloneNode();

    sfx.volume = options.volume ?? this.sfxVolume;
    sfx.loop = options.loop ?? false;

    sfx.play().catch((error) => {
      console.warn(`AudioSystem: could not play sfx "${id}"`, error);
    });
  }

  setMusicVolume(volume) {
    this.musicVolume = Math.max(0, Math.min(1, volume));

    for (const audio of this.musicTracks.values()) {
      audio.volume = this.musicVolume;
    }

    if (this.currentMusic) {
      this.currentMusic.volume = this.musicVolume;
    }
  }

  setSfxVolume(volume) {
    this.sfxVolume = Math.max(0, Math.min(1, volume));

    for (const audio of this.soundEffects.values()) {
      audio.volume = this.sfxVolume;
    }
  }

  muteAll() {
    this.enabled = false;

    if (this.currentMusic) {
      this.currentMusic.pause();
    }
  }

  unmuteAll() {
    this.enabled = true;

    if (this.currentMusic) {
      this.resumeMusic();
    } else if (this.pendingMusicId) {
      this.playMusic(this.pendingMusicId, this.pendingMusicOptions || {});
    }
  }

  muteMusic() {
    this.musicEnabled = false;

    if (this.currentMusic) {
      this.currentMusic.pause();
    }
  }

  unmuteMusic() {
    this.musicEnabled = true;

    if (this.currentMusic) {
      this.resumeMusic();
    } else if (this.pendingMusicId) {
      this.playMusic(this.pendingMusicId, this.pendingMusicOptions || {});
    }
  }

  muteSfx() {
    this.sfxEnabled = false;
  }

  unmuteSfx() {
    this.sfxEnabled = true;
  }

  destroy() {
    this.stopMusic();

    for (const audio of this.musicTracks.values()) {
      audio.pause();
      audio.src = "";
    }

    for (const audio of this.soundEffects.values()) {
      audio.pause();
      audio.src = "";
    }

    this.musicTracks.clear();
    this.soundEffects.clear();

    window.removeEventListener("pointerdown", this.handleFirstInteraction);
    window.removeEventListener("keydown", this.handleFirstInteraction);
  }
}
