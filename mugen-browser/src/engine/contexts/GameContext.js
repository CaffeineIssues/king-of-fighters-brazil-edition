export default class GameContext {
  constructor() {
    this.reset();
  }

  reset() {
    this.player1 = null; // string id
    this.player2 = null; // string id

    this.stage = null;

    this.availableCharacters = [];
    console.log(this.availableCharacters);
    this.mode = "versus";
    this.round = 1;
    this.winner = null;
  }

  setStage(stage) {
    this.stage = stage;
  }

  setPlayer1(id) {
    this.player1 = id;
  }

  setPlayer2(id) {
    this.player2 = id;
  }

  setAvailableCharacters(list) {
    this.availableCharacters = list;
  }

  getRandomCharacter(exclude = []) {
    const pool = this.availableCharacters.filter((id) => !exclude.includes(id));

    if (pool.length === 0) return null;

    return pool[Math.floor(Math.random() * pool.length)];
  }
}
