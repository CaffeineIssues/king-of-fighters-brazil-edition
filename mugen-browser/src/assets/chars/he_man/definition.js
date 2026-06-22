export default {
  id: "he_man",

  name: "HE-MAN DO NORDESTE",

  city: "TIANGUÁ",

  state: "CE",

  style: "LAPADA SECA",

  mapX: 780,
  mapY: 170,

  scale: 2.5,

  health: 1000,

  walkSpeed: 3.2,

  moves: {},

  boxDefinitions: {
    idle: {
      hurtboxes: [{ x: -22, y: -110, w: 44, h: 110 }],
    },

    walk: {
      hurtboxes: [{ x: -22, y: -110, w: 44, h: 110 }],
    },

    light_punch: {
      // Same body/feet position as idle.
      // Slightly wider because the shoulder/arm extends forward.
      hurtboxes: [{ x: -22, y: -110, w: 46, h: 110 }],

      // If light_punch has only ONE image, use frame index 0.
      hitboxes: {
        0: [{ x: 30, y: -94, w: 38, h: 18 }],
      },
    },

    medium_punch: {
      hurtboxes: [{ x: -22, y: -110, w: 46, h: 110 }],

      hitboxes: {
        1: [{ x: 30, y: -94, w: 42, h: 20 }],
      },
    },

    heavy_punch: {
      hurtboxes: [{ x: -24, y: -110, w: 50, h: 110 }],

      hitboxes: {
        0: [{ x: 28, y: -96, w: 46, h: 22 }],
      },
    },
  },
};
