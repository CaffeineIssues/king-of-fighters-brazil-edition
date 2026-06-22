export default {
  id: "mestre_thaynan",

  name: "MESTRE THAYNAN",

  city: "TIANGUÁ",

  state: "CE",

  style: "Marrada do Bode",

  mapX: 780,
  mapY: 170,

  scale: 2.5,

  health: 1000,

  walkSpeed: 3.2,

  moves: {},

  boxDefinitions: {
    idle: {
      hurtboxes: [{ x: -20, y: -90, w: 40, h: 90 }],
    },
    walk: {
      hurtboxes: [{ x: -20, y: -90, w: 40, h: 90 }],
    },
    light_punch: {
      hurtboxes: [{ x: -20, y: -90, w: 40, h: 90 }],
      // Map hitboxes to the exact frameIndex they become active
      hitboxes: {
        1: [{ x: 15, y: -75, w: 30, h: 15 }], // Active only on frame index 1
      },
    },
    medium_punch: {
      hurtboxes: [{ x: -20, y: -90, w: 40, h: 90 }],
      hitboxes: {
        2: [{ x: 18, y: -70, w: 35, h: 18 }],
      },
    },
    heavy_punch: {
      hurtboxes: [{ x: -20, y: -90, w: 40, h: 90 }],
      hitboxes: {
        2: [{ x: 20, y: -65, w: 45, h: 20 }],
        3: [{ x: 20, y: -65, w: 45, h: 20 }],
      },
    },
  },
};
