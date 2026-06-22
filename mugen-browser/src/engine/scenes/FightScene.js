export default class FightScene {
  constructor(game) {
    this.game = game;

    this.ctx = game.ctx;
    this.canvas = game.canvas;

    this.context = game.gameContext;
    this.characters = game.characters;

    this.p1 = null;
    this.p2 = null;

    this.stage = null;
    this.started = false;

    // -----------------------------
    // HUD & ROUND STATE
    // -----------------------------
    this.roundTime = 99;
    this.timer = 0;
    this.lastTime = null;

    // Control sequence when a round finishes
    this.roundOver = false;
    this.roundOverTimer = 0;
    this.roundWinnerMessage = "";
    this.matchOver = false;

    // Track active collision intersections for debug styling
    this.p1HitActive = false;
    this.p2HitActive = false;
  }

  handleCollisions() {
    // Stop checking collisions if the round or match is over
    if (!this.started || this.roundOver || this.matchOver) return;

    this.p1HitActive = false;
    this.p2HitActive = false;

    const p1Boxes = this.getCharacterWorldBoxes(this.p1);
    const p2Boxes = this.getCharacterWorldBoxes(this.p2);

    this.p1.worldBoxes = p1Boxes;
    this.p2.worldBoxes = p2Boxes;

    if (!this.p1.hasHitCurrentAttack && p1Boxes.hitboxes.length > 0) {
      for (const hitbox of p1Boxes.hitboxes) {
        for (const hurtbox of p2Boxes.hurtboxes) {
          if (this.checkAABB(hitbox, hurtbox)) {
            this.p1HitActive = true;
            this.applyHit(this.p1, this.p2);
            break;
          }
        }
        if (this.p1.hasHitCurrentAttack) break;
      }
    }

    if (!this.p2.hasHitCurrentAttack && p2Boxes.hitboxes.length > 0) {
      for (const hitbox of p2Boxes.hitboxes) {
        for (const hurtbox of p1Boxes.hurtboxes) {
          if (this.checkAABB(hitbox, hurtbox)) {
            this.p2HitActive = true;
            this.applyHit(this.p2, this.p1);
            break;
          }
        }
        if (this.p2.hasHitCurrentAttack) break;
      }
    }
  }

  getCharacterWorldBoxes(character) {
    const def =
      character.definition.boxDefinitions?.[character.currentAnimation] ||
      character.definition.boxDefinitions?.["idle"];

    if (!def) return { hitboxes: [], hurtboxes: [] };

    const localHurtboxes =
      def.hurtboxes ||
      character.definition.boxDefinitions?.["idle"]?.hurtboxes ||
      [];
    const localHitboxes = def.hitboxes?.[character.frameIndex] || [];

    const convertToWorld = (box) => {
      const w = box.w * character.scale;
      const h = box.h * character.scale;
      const y = character.y + box.y * character.scale;
      let x = character.x + box.x * character.scale;

      if (character.facing === -1) {
        x = character.x - (box.x + box.w) * character.scale;
      }

      return { x, y, w, h };
    };

    return {
      hurtboxes: localHurtboxes.map(convertToWorld),
      hitboxes: localHitboxes.map(convertToWorld),
    };
  }

  checkAABB(rect1, rect2) {
    return (
      rect1.x < rect2.x + rect2.w &&
      rect1.x + rect1.w > rect2.x &&
      rect1.y < rect2.y + rect2.h &&
      rect1.y + rect1.h > rect2.y
    );
  }

  applyHit(attacker, defender) {
    attacker.hasHitCurrentAttack = true;

    let damage = 20;
    if (attacker.currentAnimation === "medium_punch") damage = 45;
    if (attacker.currentAnimation === "heavy_punch") damage = 80;

    defender.health = Math.max(0, defender.health - damage);

    // Yellow damage flash
    defender.damageFlashTimer = 250;

    // Play hurt animation
    if (defender.animations?.hurt) {
      defender.currentAnimation = "hurt";
      defender.frameIndex = 0;
      defender.frameTimer = 0;

      // Keeps player locked in hurt briefly
      defender.hitStunTimer = 350;
    } else {
      console.warn(`${defender.name} has no hurt animation loaded`);
    }

    console.log(
      `${attacker.name} struck ${defender.name} for ${damage} damage!`,
    );

    if (defender.health <= 0) {
      this.endRound();
    }
  }

  // --- HANDLE ROUND END LOGIC ---
  endRound() {
    if (this.roundOver) return;
    this.roundOver = true;
    this.roundOverTimer = performance.now();

    let roundWinner = null;

    if (this.p1.health === this.p2.health) {
      this.roundWinnerMessage = "DRAW";
    } else if (this.p1.health > this.p2.health) {
      this.roundWinnerMessage = `${this.p1.name} WINS`;
      this.context.p1RoundWins++;
      roundWinner = this.p1;
    } else {
      this.roundWinnerMessage = `${this.p2.name} WINS`;
      this.context.p2RoundWins++;
      roundWinner = this.p2;
    }

    // Best of 3 check (First to 2 wins)
    if (this.context.p1RoundWins === 2) {
      this.matchOver = true;
      this.context.winner = this.p1.name;
      this.roundWinnerMessage = `${this.p1.name} IS THE CHAMPION!`;
    } else if (this.context.p2RoundWins === 2) {
      this.matchOver = true;
      this.context.winner = this.p2.name;
      this.roundWinnerMessage = `${this.p2.name} IS THE CHAMPION!`;
    }
  }

  // --- RESET FOR NEXT ROUND ---
  setupNextRound() {
    const groundY = this.stage?.groundY ?? 520;

    // Safely increment round (defaults to 1 if it was somehow undefined)
    this.context.round = (this.context.round || 1) + 1;
    this.roundTime = 99;
    this.timer = 0;
    this.lastTime = performance.now();
    this.roundOver = false;

    // --- Reset P1 ---
    this.p1.x = this.canvas.width / 2 - 260;
    this.p1.y = groundY;
    this.p1.facing = 1;
    this.p1.health = this.p1.maxHealth || 100;
    this.p1.currentAnimation = "idle";
    this.p1.frameIndex = 0;
    this.p1.frameTimer = 0;
    this.p1.hasHitCurrentAttack = false;
    this.p1.hitStunTimer = 0;

    // --- Reset P2 ---
    this.p2.x = this.canvas.width / 2 + 260;
    this.p2.y = groundY;
    this.p2.facing = -1;
    this.p2.health = this.p2.maxHealth || 100;
    this.p2.currentAnimation = "idle";
    this.p2.frameIndex = 0;
    this.p2.frameTimer = 0;
    this.p2.hasHitCurrentAttack = false;
    this.p2.hitStunTimer = 0;
  }

  drawDebugBoxes(ctx) {
    const renderBoxes = (character, hurtColor, hitColor, isHitActive) => {
      if (!character.worldBoxes) return;

      // Check if this character is currently flashing from damage
      const isTakingDamage = character.damageFlashTimer > 0;

      ctx.lineWidth = 2;

      // Override the stroke and fill if taking damage
      ctx.strokeStyle = isTakingDamage ? "rgb(255, 255, 0)" : hurtColor;
      ctx.fillStyle = isTakingDamage ? "rgba(255, 255, 0, 0.4)" : "transparent";

      for (const box of character.worldBoxes.hurtboxes) {
        if (isTakingDamage) ctx.fillRect(box.x, box.y, box.w, box.h);
        ctx.strokeRect(box.x, box.y, box.w, box.h);
      }

      ctx.fillStyle = isHitActive ? "rgba(255, 234, 0, 0.6)" : hitColor;
      ctx.strokeStyle = isHitActive ? "rgb(255, 200, 0)" : "rgb(255, 0, 0)";

      for (const box of character.worldBoxes.hitboxes) {
        ctx.fillRect(box.x, box.y, box.w, box.h);
        ctx.strokeRect(box.x, box.y, box.w, box.h);
      }
    };

    renderBoxes(
      this.p1,
      "rgba(0, 150, 255, 0.8)",
      "rgba(255, 0, 0, 0.4)",
      this.p1HitActive,
    );
    renderBoxes(
      this.p2,
      "rgba(150, 0, 255, 0.8)",
      "rgba(255, 0, 0, 0.4)",
      this.p2HitActive,
    );
  }

  async init() {
    const ctx = this.context;

    // Reset match state
    ctx.p1RoundWins = 0;
    ctx.p2RoundWins = 0;
    ctx.round = 1;
    ctx.winner = null;

    this.stage = ctx.stage;
    const groundY = this.stage?.groundY ?? 520;

    if (!ctx.player1 || !ctx.player2) {
      throw new Error("FightScene: Missing player1 or player2 in GameContext");
    }

    this.p1 = await this.characters.loadCharacter(ctx.player1, {
      x: this.canvas.width / 2 - 260,
      y: groundY,
      facing: 1,
    });

    this.p2 = await this.characters.loadCharacter(ctx.player2, {
      x: this.canvas.width / 2 + 260,
      y: groundY,
      facing: -1,
    });

    this.started = true;
    console.log("FightScene ready:", ctx.player1, "vs", ctx.player2);
  }

  update() {
    const input = this.game.inputSystem;

    if (input.wasPressed("Escape")) {
      this.game.sceneManager.pop();
      return;
    }

    if (!this.started) return;

    const now = performance.now();

    // Calculate the time difference since the last frame
    const deltaTime = this.lastTime ? now - this.lastTime : 16;

    // Decrement the flash timer for both players
    if (this.p1.damageFlashTimer > 0) this.p1.damageFlashTimer -= deltaTime;
    if (this.p2.damageFlashTimer > 0) this.p2.damageFlashTimer -= deltaTime;

    // Hurt recovery / hit stun
    for (const player of [this.p1, this.p2]) {
      if (player.hitStunTimer > 0) {
        player.hitStunTimer -= deltaTime;

        if (player.hitStunTimer <= 0 && player.currentAnimation === "hurt") {
          player.currentAnimation = "idle";
          player.frameIndex = 0;
          player.frameTimer = 0;
          player.hitStunTimer = 0;
        }
      }
    }

    // -----------------------------
    // ROUND OVER DELAY SEQUENCE
    // -----------------------------
    if (this.roundOver) {
      // Pause for 3 seconds before moving to the next round or quitting
      if (now - this.roundOverTimer > 3000) {
        if (this.matchOver) {
          // --- CLEANUP BEFORE EXITING ---
          // 1. Paint the canvas black to erase the final frame
          if (this.ctx) {
            this.ctx.fillStyle = "#000";
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
          }

          // 2. Clear out the global characters so they don't render in the next scene
          if (typeof this.characters.clear === "function") {
            this.characters.clear();
          } else if (Array.isArray(this.characters.entities)) {
            this.characters.entities = [];
          }

          // 3. Nullify local references
          this.p1 = null;
          this.p2 = null;
          // -----------------------------------

          // Entire match finished: clear/exit scene
          this.game.sceneManager.pop();
          return;
        } else {
          this.setupNextRound();
        }
      }
      // Skip processing fighting inputs while frozen
      this.characters.update();
      return;
    }

    // -----------------------------
    // TIMER UPDATE
    // -----------------------------
    if (this.lastTime === null) this.lastTime = now;
    this.timer += now - this.lastTime;
    this.lastTime = now;

    if (this.timer >= 1000) {
      this.timer = 0;
      if (this.roundTime > 0) {
        this.roundTime--;
        if (this.roundTime === 0) {
          this.endRound(); // Time Out!
        }
      }
    }

    // -----------------------------
    // PLAYER 1 INPUT
    // -----------------------------
    let p1Moving = false;
    if (
      this.p1.currentAnimation === "idle" ||
      this.p1.currentAnimation === "walk"
    ) {
      if (input.isPressed?.("KeyA")) {
        this.p1.x -= this.p1.walkSpeed;
        this.p1.facing = -1;
        p1Moving = true;
      }
      if (input.isPressed?.("KeyD")) {
        this.p1.x += this.p1.walkSpeed;
        this.p1.facing = 1;
        p1Moving = true;
      }
      if (input.wasPressed?.("KeyJ") && this.p1.animations.light_punch) {
        this.p1.currentAnimation = "light_punch";
        this.p1.frameIndex = 0;
        this.p1.frameTimer = 0;
      } else if (
        input.wasPressed?.("KeyK") &&
        this.p1.animations.medium_punch
      ) {
        this.p1.currentAnimation = "medium_punch";
        this.p1.frameIndex = 0;
        this.p1.frameTimer = 0;
      } else if (input.wasPressed?.("KeyL") && this.p1.animations.heavy_punch) {
        this.p1.currentAnimation = "heavy_punch";
        this.p1.frameIndex = 0;
        this.p1.frameTimer = 0;
      } else {
        const targetAnim = p1Moving ? "walk" : "idle";
        if (this.p1.currentAnimation !== targetAnim) {
          this.p1.currentAnimation = targetAnim;
        }
      }
    }

    // -----------------------------
    // PLAYER 2 INPUT
    // -----------------------------
    let p2Moving = false;
    if (
      this.p2.currentAnimation === "idle" ||
      this.p2.currentAnimation === "walk"
    ) {
      if (input.isPressed?.("ArrowLeft")) {
        this.p2.x -= this.p2.walkSpeed;
        this.p2.facing = -1;
        p2Moving = true;
      }
      if (input.isPressed?.("ArrowRight")) {
        this.p2.x += this.p2.walkSpeed;
        this.p2.facing = 1;
        p2Moving = true;
      }
      if (input.wasPressed?.("Numpad1") && this.p2.animations.light_punch) {
        this.p2.currentAnimation = "light_punch";
        this.p2.frameIndex = 0;
        this.p2.frameTimer = 0;
      } else if (
        input.wasPressed?.("Numpad2") &&
        this.p2.animations.medium_punch
      ) {
        this.p2.currentAnimation = "medium_punch";
        this.p2.frameIndex = 0;
        this.p2.frameTimer = 0;
      } else if (
        input.wasPressed?.("Numpad3") &&
        this.p2.animations.heavy_punch
      ) {
        this.p2.currentAnimation = "heavy_punch";
        this.p2.frameIndex = 0;
        this.p2.frameTimer = 0;
      } else {
        const targetAnim = p2Moving ? "walk" : "idle";
        if (this.p2.currentAnimation !== targetAnim) {
          this.p2.currentAnimation = targetAnim;
        }
      }
    }

    // -----------------------------
    // PLAYER VS PLAYER BODY COLLISION
    // -----------------------------
    const minDistance = 70;
    const currentDist = this.p2.x - this.p1.x;

    if (Math.abs(currentDist) < minDistance) {
      const overlap = minDistance - Math.abs(currentDist);
      if (currentDist > 0) {
        this.p1.x -= overlap / 2;
        this.p2.x += overlap / 2;
      } else {
        this.p1.x += overlap / 2;
        this.p2.x -= overlap / 2;
      }
    }

    this.p1.x = Math.max(60, Math.min(this.canvas.width - 60, this.p1.x));
    this.p2.x = Math.max(60, Math.min(this.canvas.width - 60, this.p2.x));

    this.handleCollisions();
    this.characters.update();
  }

  draw(renderCtx) {
    const W = this.canvas.width;
    const H = this.canvas.height;

    if (!this.started) return;

    renderCtx.fillStyle = "#000";
    renderCtx.fillRect(0, 0, W, H);

    if (this.stage?.preview?.complete) {
      renderCtx.drawImage(this.stage.preview, 0, 0, W, H);
    }

    this.characters.draw(renderCtx);
    this.drawHUD(renderCtx);
    this.drawDebugBoxes(renderCtx);

    // --- RENDER ROUND WINNER ANNOUNCEMENT ---
    if (this.roundOver) {
      renderCtx.fillStyle = "rgba(0, 0, 0, 0.5)";
      renderCtx.fillRect(0, H / 2 - 50, W, 100);

      renderCtx.fillStyle = "#fff";
      renderCtx.font = "bold 38px Arial";
      renderCtx.textAlign = "center";
      renderCtx.fillText(this.roundWinnerMessage, W / 2, H / 2 + 12);
    }
  }

  drawHUD(ctx) {
    const W = this.canvas.width;
    const p1 = this.p1;
    const p2 = this.p2;

    // Back Bars
    ctx.fillStyle = "#222";
    ctx.fillRect(50, 20, 300, 18);
    ctx.fillRect(W - 350, 20, 300, 18);

    // Life Bars
    const p1Life = (p1.health / (p1.maxHealth || 100)) * 300;
    const p2Life = (p2.health / (p2.maxHealth || 100)) * 300;

    ctx.fillStyle = "#00ff66";
    ctx.fillRect(50, 20, p1Life, 18);
    ctx.fillRect(W - 350 + (300 - p2Life), 20, p2Life, 18);

    // Timer Text
    ctx.fillStyle = "#fff";
    ctx.font = "22px Arial";
    ctx.textAlign = "center";
    ctx.fillText(this.roundTime, W / 2, 35);

    // --- ROUND TRACKING VISUALS (Pips below health bars) ---
    ctx.font = "14px Arial";
    ctx.fillStyle = "#ffcc00";

    // P1 round win pips
    let p1Pips =
      (this.context.p1RoundWins >= 1 ? "⭐" : "⚫") +
      (this.context.p1RoundWins >= 2 ? " ⭐" : " ⚫");
    ctx.textAlign = "left";
    ctx.fillText(p1Pips, 50, 50);

    // P2 round win pips
    let p2Pips =
      (this.context.p2RoundWins >= 2 ? "⭐ " : "⚫ ") +
      (this.context.p2RoundWins >= 1 ? "⭐" : "⚫");
    ctx.textAlign = "right";
    ctx.fillText(p2Pips, W - 50, 50);

    // Round counter string
    ctx.fillStyle = "#fff";
    ctx.textAlign = "center";
    ctx.fillText(`ROUND ${this.context.round || 1}`, W / 2, 60);

    // Names
    ctx.font = "14px Arial";
    ctx.textAlign = "left";
    ctx.fillText(p1.name, 50, 75);

    ctx.textAlign = "right";
    ctx.fillText(p2.name, W - 50, 75);
  }
}
