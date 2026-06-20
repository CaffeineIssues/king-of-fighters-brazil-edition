export default class GameContext {
  constructor() {
    this.reset();
  }

  reset() {
    this.player1 = null;
    this.player2 = null;

    this.stage = null;

    this.mode = "versus";

    this.round = 1;

    this.winner = null;
  }

  setPlayer1(character) {
    this.player1 = character;
  }

  setPlayer2(character) {
    this.player2 = character;
  }

  setStage(stage) {
    this.stage = stage;
  }

  setWinner(winner) {
    this.winner = winner;
  }
}
