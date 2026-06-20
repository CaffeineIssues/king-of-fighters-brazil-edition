import Game from "./engine/Game";

const canvas = document.getElementById("game");

const game = new Game(canvas);

game.start();
