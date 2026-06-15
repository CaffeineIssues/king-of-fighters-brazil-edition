# Roster Specifications

These sheets translate the example roster into serious SNK-era fighting game
characters. Each fighter is inspired by a public meme persona, but the design
goal is always "believable 1998 arcade combatant" first.

## Team Black Tiger

### Mestre Thaynan

**Nickname:** The Sidewalk Sifu  
**Age:** 58  
**Height:** 176 cm  
**Weight:** 63 kg  
**Fighting Style:** Black Tiger kung fu, prayer-guard counters, and improvised
street conditioning  
**Hometown:** Interior Brazil  
**Team:** Team Black Tiger  
**Archetype:** Technical Counter Fighter / Stance Specialist

#### Visual Reference Notes

The reference direction is a lean older martial artist with long center-parted
dark gray hair tied back, rectangular glasses, sharp cheekbones, and a wiry
frame. His primary costume is the navy track jacket with yellow sleeve stripes,
light Black Tiger Kung Fu shirt, dark loose pants, and black shoes from the
provided sprite sheet. The sleeveless black kung fu top can remain an alternate
palette or story costume, but the jacketed version is the production target.

For SNK translation, keep him realistic and intimidating rather than goofy:
slightly hunched posture, narrow shoulders, sinewy forearms, precise hand
shapes, and a calm stare over the glasses. His silhouette should be defined by
the prayer-guard hand position, long hair framing the face, and thin limbs that
snap into sudden tiger-claw strikes.

#### Visual Design

Mestre Thaynan wears a navy track jacket with yellow sleeve stripes over a light
Black Tiger shirt, dark straight-leg training pants, and worn black shoes. His
base palette is navy, muted gold, pale blue-white shirt tones, weathered skin
tones, and gray-brown hair highlights. The jacket hem and tied-back hair should
move during jumps, knockdowns, and heavy tiger-claw attacks.

Alternate palettes:

- Sleeveless black kung fu shirt with white vertical markings.
- Sepia training uniform for old martial arts film homage.
- Dark green shirt with gold tiger markings for boss-style arcade routes.

#### Story

Mestre Thaynan spent years training in public squares, quiet streets, and empty
courts where passersby mistook his drills for performance. After clips of his
unusual hand forms and sidewalk conditioning spread online, challengers began
arriving to test whether the old master was real. He enters the tournament to
settle the question with discipline: no spectacle, no excuses, only form.

#### Fighting Style

Thaynan controls rhythm rather than space. He uses patient footsies, stance
cancels, counter windows, and sudden tiger-claw bursts to punish opponents who
rush in carelessly. He has excellent anti-hop checks and strong close confirms,
but his walk speed is modest and he must read projectiles instead of overpowering
them.

Core strengths:

- Strong whiff punishes from far HP and command normals.
- Prayer Guard counters predictable mids and highs.
- Stance cancels create pressure ambiguity.
- High stun output on clean counter hits.

Core weaknesses:

- Low raw damage without counter hits or meter.
- Slow backward movement.
- Vulnerable to delayed lows if Prayer Guard is overused.
- Projectile matchups require careful hop timing and read-based movement.

#### Normal Attacks

- LP: Short vertical palm check from prayer guard.
- HP: Snapping tiger-claw rake, high counter-hit stun.
- LK: Low shin tap with the lead foot.
- HK: Lean side kick with long recovery but excellent reach.
- Close LP: Two-finger throat feint, fast pressure starter.
- Close HP: Double palm shock, special cancelable.
- Close LK: Knee brush into ankle tap.
- Close HK: Rising instep kick, close launcher on counter hit.
- Far LP: Glasses-level measuring palm.
- Far HP: Long tiger-claw swipe, primary whiff punish normal.
- Far LK: Quick toe poke to stop walk-ins.
- Far HK: Straight side kick that checks hops and long pokes.
- Crouch LP: Compact palm jab.
- Crouch HP: Upward crane palm, anti-air normal.
- Crouch LK: Low ankle tap.
- Crouch HK: Sliding leg sweep with poor block recovery.
- Jump LP: Downward palm tap.
- Jump HP: Two-hand chop, deep jump-in.
- Jump LK: Fast knee angle for air-to-air.
- Jump HK: Long heel drop, cross-up at close spacing.

#### Command Normals

- Forward + HP: Tiger Enters Gate. Advancing overhead claw, special cancelable
  only on hit.
- Down-Forward + LP: Sidewalk Needle. Low palm poke that links from crouch LP.
- Forward + LK: Old Step. Short hop step that avoids low pokes during early
  frames and can cancel into specials on landing.

#### Special Moves

- QCF + P: Black Tiger Palm. Short-range palm burst. LP is safe but lower
  damage; HP travels farther and wall-bounces on counter hit near the corner.
- DP + P: Crane Frames the Moon. Vertical palm anti-air with brief upper-body
  invulnerability. HP version has slower startup and more juggle reward.
- QCB + P: Prayer Guard. Counter stance. LP covers highs and mids, HP covers
  heavier strikes but loses to lows and throws.
- QCF + K: Sidewalk Step. Low-profile advancing step with LK stop, HK shoulder
  check, and hold-back retreat follow-ups.
- QCB + K: Brick Conditioning. Thaynan stamps the floor, creating a short
  shockwave at his feet. Useful for ending strings and stopping rolls.
- HCF + P: Sifu Grip. Close command grab that switches sides and leaves the
  opponent standing at frame advantage instead of causing heavy damage.

#### Super Moves

- QCF, QCF + P: Black Tiger Sequence. Rapid palm, claw, elbow, and heel series
  that carries to the corner.
- QCB, QCB + P: Perfect Prayer Reversal. Counter super that catches strikes,
  freezes the screen, adjusts his glasses, and returns a crushing palm.

#### MAX Super

- QCF, QCB + HP+HK: Mestre do Tigre Preto. Cinematic stance sequence: Thaynan
  assumes the prayer guard, parries three phantom attacks, pulls the opponent
  into a sidewalk training circle, and finishes with a focused tiger-claw palm
  that cracks the pavement.

#### Extra Content

- Intro: Stands in prayer guard, lowers one hand, and calmly adjusts his
  glasses without looking away.
- Reference Intro Variant: A broom handle and two training blocks are visible
  at his feet; he steps past them into fighting stance.
- Taunt: Demonstrates a slow hand form and says nothing. If completed, slightly
  increases stun dealt by the next counter hit.
- Victory A: Returns to prayer guard and bows with a tiny nod.
- Victory B: Puts on the navy jacket, turns away, and resumes walking like the
  fight was only training.
- Defeat: Drops to one knee, one palm on the pavement, glasses tilted but not
  broken.

#### Stage Suggestion

Praca do Mestre: a quiet Brazilian sidewalk and public square with mosaic
pavement, trees, a low wall, and simple training objects near the background.
The stage should evoke the second reference image without copying it literally.

#### MUGEN State Structure

- 1000: Black Tiger Palm
- 1100: Crane Frames the Moon
- 1200: Prayer Guard
- 1210: Prayer Guard Success
- 1300: Sidewalk Step
- 1310: Sidewalk Step Stop
- 1320: Sidewalk Step Shoulder
- 1330: Sidewalk Step Retreat
- 1400: Brick Conditioning
- 1500: Sifu Grip
- 2000: Black Tiger Sequence
- 2100: Perfect Prayer Reversal
- 3000: Mestre do Tigre Preto

#### Animation List

Prayer-guard idle, glasses adjustment, long-hair sway, walk with narrow steps,
Sidewalk Step low glide, tiger-claw far HP, Crane Frames the Moon anti-air,
Prayer Guard startup and success freeze, brick-stamp shockwave, command-grab
side switch, MAX super training-circle stance, bow victory, jacket victory.

#### AI Behavior

Thaynan AI should feel patient. At low levels it pokes with far LP, far LK, and
Black Tiger Palm. At mid levels it anti-airs hops with crouch HP or Crane Frames
the Moon, then uses Sidewalk Step to maintain pressure. At high levels it uses
Prayer Guard after observing repeated jump-ins or heavy buttons, but it should
not counter with impossible precision. Meter is reserved for confirmed close HP
routes or Perfect Prayer Reversal against obvious offense.

## Team Receba

### Luva de Pedreiro

**Nickname:** The Receba Striker  
**Age:** 22  
**Height:** 178 cm  
**Weight:** 78 kg  
**Fighting Style:** Football footwork with Muay Thai elbows and knees  
**Hometown:** Quijingue, Bahia  
**Team:** Team Receba  
**Archetype:** Rushdown Power Fighter

#### Visual Design

Luva has a short athletic haircut, expressive eyebrows, and a forward-leaning
stance. His outfit reads like a rural football prodigy upgraded into an SNK
hero: sleeveless training top, taped wrists, shin guards under loose shorts,
and worn football boots. Main colors are green, yellow, white, and dark navy,
with a single glove on his lead hand as the silhouette anchor.

#### Story

Invited to the tournament after his impossible trick shots go viral, Luva sees
the event as the ultimate field: every fight is a penalty kick, every round is
stoppage time, and every opponent is a defender between him and glory.

#### Fighting Style

Luva overwhelms opponents with fast forward movement, plus-on-block shoulder
pressure, and explosive kick confirms. He struggles when forced to block long
strings or chase airborne zoners.

#### Normal Attacks

- LP: Quick jab with glove hand.
- HP: Heavy overhand elbow, strong close-range cancel normal.
- LK: Low football tap kick, fast poke.
- HK: Long round kick with football follow-through.
- Close LP: Chest-level hook for pressure resets.
- Close HP: Clinch elbow, high hit stun.
- Close LK: Knee feint to shin kick.
- Close HK: Rising knee, combo starter.
- Far LP: Measuring jab.
- Far HP: Lunging straight punch, whiff punish tool.
- Far LK: Toe poke, longest light normal.
- Far HK: High instep kick, anti-hop button.
- Jump LP: Downward tap punch.
- Jump HP: Deep elbow drop.
- Jump LK: Fast knee.
- Jump HK: Flying football volley, cross-up capable.

#### Command Normals

- Forward + HP: Chest Trap. Advancing body check, special cancelable on hit.
- Forward + LK: Step-Over Low. Low-hitting feint kick.

#### Special Moves

- QCF + P: RECEBA Rush. Shoulder charge with LP/HP distance variants.
- DP + K: Bicycle Kick. Anti-air flip kick with juggle on counter hit.
- QCF + K: Goal Shot. Ground-skimming football projectile.
- QCB + P: Celebration Counter. Upper-body counter that launches on success.
- HCF + K: Corner Flag Dash. Fast run cancel that can stop, kick, or throw.

#### Super Moves

- QCF, QCF + P: Stadium Breaker. Multi-hit shoulder rush into goal shot.
- QCB, HCF + K: Hat-Trick Cyclone. Three rising football kicks.

#### MAX Super

- QCF, QCF + HP+HK: RECEBAAAAAA. Cinematic full-field dash, bicycle kick,
  crowd flash, and final power shot.

#### Extra Content

- Intro: Juggles a ball three times, traps it underfoot, points forward.
- Taunt: Shouts "Receba!" and gains a tiny amount of meter if uninterrupted.
- Victory A: Slides on one knee like a goal celebration.
- Victory B: Signs an invisible camera lens.
- Defeat: Sits back against the corner post, glove lowered.

#### Stage Suggestion

Favela Rooftop at sunset, with kites and rooftop spectators reacting to shots.

#### MUGEN State Structure

- 1000: RECEBA Rush
- 1050: Bicycle Kick
- 1100: Goal Shot
- 1150: Celebration Counter
- 1200: Corner Flag Dash
- 2000: Stadium Breaker
- 2100: Hat-Trick Cyclone
- 3000: RECEBAAAAAA

#### Animation List

Idle breathing with bouncing foot, run with football sprinter lean, dash stop,
step-over feint, glove shoulder impact, bicycle flip, goal shot windup,
counter pose, stadium flash, win slide.

#### AI Behavior

Aggressive AI prioritizes hop HK, low LK confirms, and RECEBA Rush spacing. At
level 6+, it baits reversals with Corner Flag Dash stops and spends meter only
after confirmed close HP or anti-air Bicycle Kick.

## Team Viral Sound

### Caneta Azul

**Nickname:** The Blue Verse  
**Age:** 49  
**Height:** 169 cm  
**Weight:** 72 kg  
**Fighting Style:** Mid-range zoning with rhythmic pressure  
**Hometown:** Sao Luis, Maranhao  
**Team:** Team Viral Sound  
**Archetype:** Mid-range Zoner

#### Visual Design

Caneta Azul wears a tailored blue jacket over a plain shirt, high-waisted dark
trousers, polished shoes, and a pen tucked like a sacred weapon. His hair is
simple and neat. The silhouette is defined by the raised pen hand and a
microphone-cable belt that sways during movement.

#### Story

After a mysterious pen begins turning chorus lines into visible energy, Caneta
Azul enters the tournament to prove that a simple melody can defeat fists,
fireballs, and entire crime syndicates.

#### Fighting Style

He controls horizontal space with ink waves, delayed chorus traps, and long pen
stabs. He has weaker reversal options and must pre-place notes to stop rushdown.

#### Normal Attacks

- LP: Short pen jab.
- HP: Wide ink-backed palm strike.
- LK: Shoe tap low.
- HK: Long front kick.
- Close LP: Microphone hand check.
- Close HP: Two-hit pen flourish.
- Close LK: Knee bump.
- Close HK: Rising shin kick.
- Far LP: Pointing poke.
- Far HP: Long pen thrust.
- Far LK: Low toe tap.
- Far HK: Mid-height stage kick.
- Jump LP: Quick pen swipe.
- Jump HP: Downward ink splash.
- Jump LK: Fast knee.
- Jump HK: Long boot kick.

#### Command Normals

- Forward + HP: Verse Accent. Slow overhead pen slash.
- Down-Forward + LP: Blue Signature. Low ink swipe, cancelable.

#### Special Moves

- QCF + P: Ink Blast. Blue projectile with LP/HP speed variants.
- QCB + P: Blue Wave. Slow advancing wave that controls hop space.
- QCF + K: Chorus Trap. Places a delayed musical note on the floor.
- DP + P: Pen Strike. Vertical anti-air stab with brief upper-body invuln.
- QCB + K: Refrain Step. Backstep that leaves a short-lived ink mark.

#### Super Moves

- QCF, QCF + P: Blue Verse Barrage. Multiple ink projectiles in rhythm.
- QCB, QCB + P: Lost Pen Lament. Trap detonation sequence around the opponent.

#### MAX Super

- QCF, QCF + HP+HK: Caneta Azul Symphony. Full-screen musical staff forms and
  launches the opponent through a chorus of blue ink blasts.

#### Extra Content

- Intro: Checks his pocket, finds the blue pen, nods with relief.
- Taunt: Sings one short bar and twirls the pen.
- Victory A: Signs an autograph in the air.
- Victory B: Conducts invisible backing vocals.
- Defeat: Searches the ground for the missing pen.

#### Stage Suggestion

Feira Livre, with fruit vendors and street musicians joining the rhythm.

#### MUGEN State Structure

- 1000: Ink Blast
- 1050: Blue Wave
- 1100: Chorus Trap
- 1150: Pen Strike
- 1200: Refrain Step
- 2000: Blue Verse Barrage
- 2100: Lost Pen Lament
- 3000: Caneta Azul Symphony

#### Animation List

Pen idle glint, jacket sway walk, lyric charge, projectile release, floor note
placement, anti-air thrust, conductor super stance, autograph victory.

#### AI Behavior

Zoning AI keeps one trap active, alternates LP Ink Blast and HP Blue Wave, and
anti-airs hops with Pen Strike. It retreats after blocked close strings unless
the opponent is trapped.

## Team Carnival

### Carreta Furacao Captain

**Nickname:** Parade Leader  
**Age:** 31  
**Height:** 181 cm  
**Weight:** 76 kg  
**Fighting Style:** Capoeira, acrobatics, and parade movement  
**Hometown:** Ribeirao Preto, Sao Paulo  
**Team:** Team Carnival  
**Archetype:** Mix-up Fighter

#### Visual Design

The Captain wears a parade-inspired commander jacket, flexible dance pants,
wrapped ankles, and bright gloves. Colors are red, gold, white, and deep
purple, muted to fit KOF shading. The silhouette uses a tall feathered shoulder
ornament on one side and exaggerated capoeira hand placement.

#### Story

The famous dance crew is hired as tournament entertainment, but the Captain
discovers the bracket has an empty slot. He signs up to prove that carnival
rhythm can break any defensive guard.

#### Fighting Style

The Captain attacks from shifting heights with rolls, flips, ambiguous jump
arcs, and confetti traps. His damage is moderate unless he forces corner
guessing sequences.

#### Normal Attacks

- LP: Quick glove jab.
- HP: Spinning backfist.
- LK: Low capoeira tap.
- HK: Long meia-lua kick.
- Close LP: Short palm bump.
- Close HP: Double backfist.
- Close LK: Knee check.
- Close HK: Handstand kick launcher.
- Far LP: Parade baton poke.
- Far HP: Wide arm sweep.
- Far LK: Low rhythm step.
- Far HK: Long spinning kick.
- Jump LP: Downward palm.
- Jump HP: Confetti elbow.
- Jump LK: Knee cross-up.
- Jump HK: Aerial crescent kick.

#### Command Normals

- Forward + LK: Samba Step. Advancing low profile kick.
- Forward + HP: Baton Feint. Overhead strike that can cancel into Parade Dash.

#### Special Moves

- QCF + P: Dance Rush. Rekka-style palm and kick sequence.
- QCB + K: Carnival Kick. Flip kick that changes side on HK version.
- QCF + K: Parade Dash. Run stance with strike, throw, or stop follow-ups.
- QCB + P: Confetti Bomb. Arcing delayed projectile.
- DP + K: Drumline Rise. Flashy anti-air handstand kick.

#### Super Moves

- QCF, QCF + K: Avenue Blender. Multi-angle capoeira rush.
- QCB, HCF + P: Float Crash. Confetti bomb into sliding command grab.

#### MAX Super

- QCF, QCF + HP+HK: Furacao Parade. The screen becomes a parade lane as the
  Captain calls dancers for a cinematic cross-up barrage.

#### Extra Content

- Intro: Marches in with two off-screen dancers, then sends them away.
- Taunt: Spins in place and tosses harmless confetti.
- Victory A: Leads a short parade march.
- Victory B: Handstand freeze into finger point.
- Defeat: Collapses into a seated dancer pose, breathing hard.

#### Stage Suggestion

Carnival Avenue with floats, dancers, barricades, and timed confetti bursts.

#### MUGEN State Structure

- 1000: Dance Rush 1
- 1010: Dance Rush 2
- 1020: Dance Rush Enders
- 1100: Carnival Kick
- 1150: Parade Dash
- 1200: Confetti Bomb
- 1250: Drumline Rise
- 2000: Avenue Blender
- 2100: Float Crash
- 3000: Furacao Parade

#### Animation List

Capoeira idle sway, dash dance, handstand launcher, confetti toss, parade run
stance, flip side switch, dancer call silhouettes, parade victory.

#### AI Behavior

Mix-up AI rotates between Samba Step lows, Baton Feint overheads, and throw
follow-ups from Parade Dash. Higher levels use Confetti Bomb to cover approach
instead of raw dash-ins.

## Team Away

### Gil Brother Away

**Nickname:** The Glitch Prophet  
**Age:** 45  
**Height:** 174 cm  
**Weight:** 70 kg  
**Fighting Style:** Counter fighting with reality-bending feints  
**Hometown:** Rio de Janeiro, Rio de Janeiro  
**Team:** Team Away  
**Archetype:** Technical Counter Fighter

#### Visual Design

Gil Brother Away wears a sharp but slightly mismatched suit: narrow tie, rolled
sleeves, dark shoes, and a jacket lining that flickers during specials. Hair is
messy but charismatic. His silhouette is defined by pointing gestures, a tilted
stance, and afterimage frames.

#### Story

Gil enters after claiming the tournament bracket itself is wrong. His goal is
not victory in the normal sense; he wants to redirect the timeline until every
opponent loses before they understand the joke.

#### Fighting Style

Gil punishes predictable offense. He has counters, teleports, clone feints, and
delayed hitboxes, but low raw damage when opponents force honest footsies.

#### Normal Attacks

- LP: Fast finger jab.
- HP: Suit-sleeve hook.
- LK: Low shoe tap.
- HK: Leaning side kick.
- Close LP: Collar jab.
- Close HP: Two-hit suit hook.
- Close LK: Knee tap.
- Close HK: Short launcher kick.
- Far LP: Pointing poke.
- Far HP: Long backhand.
- Far LK: Ankle kick.
- Far HK: Straight-leg kick.
- Jump LP: Finger point.
- Jump HP: Downward backhand.
- Jump LK: Quick knee.
- Jump HK: Sideways drop kick.

#### Command Normals

- Forward + HP: Away Slap. Slow advancing slap with high guard stun.
- Down-Forward + HK: Timeline Sweep. Sliding sweep with long recovery.

#### Special Moves

- QCB + P: Brother Counter. Parries strike levels based on button strength.
- QCF + K: Away Teleport. Short warp forward, back, or behind depending on K.
- QCF + P: Shadow Clone. Sends a delayed afterimage strike.
- DP + P: Reality Glitch. Anti-air burst that shifts Gil backward.
- HCB + K: Wrong Bracket. Low command feint that reverses spacing on hit.

#### Super Moves

- QCB, QCB + P: Brother Reversal. Counter super with cinematic timeline break.
- QCF, QCF + K: Glitch Rush. Teleport sequence with clone follow-ups.

#### MAX Super

- QCB, HCF + HP+HK: Brother Away Dimension. Gil traps the opponent in repeated
  false round starts before striking from behind.

#### Extra Content

- Intro: Walks in mid-sentence, notices the opponent, and adjusts his tie.
- Taunt: Points off-screen and says the fight is happening elsewhere.
- Victory A: Vanishes, reappears closer to camera, shrugs.
- Victory B: Fixes his cufflinks while a clone claps.
- Defeat: Attempts one last teleport and falls out of it.

#### Stage Suggestion

LAN House 1999, with CRT monitors briefly glitching during his supers.

#### MUGEN State Structure

- 1000: Brother Counter
- 1100: Away Teleport
- 1200: Shadow Clone
- 1300: Reality Glitch
- 1400: Wrong Bracket
- 2000: Brother Reversal
- 2100: Glitch Rush
- 3000: Brother Away Dimension

#### Animation List

Suit idle, pointing normals, flicker startup, counter freeze, warp smear,
clone dissolve, false KO flash, cufflink win pose.

#### AI Behavior

Counter AI waits at mid range and reacts to predictable specials with Brother
Counter. At high levels it uses Shadow Clone to cover teleports, but it should
avoid perfect counter reads below boss difficulty.

## Team Cosmic Folklore

### ET Bilu

**Nickname:** The Knowledge Seeker  
**Age:** Unknown  
**Height:** 150 cm  
**Weight:** Unknown  
**Fighting Style:** Alien technology and psychic misdirection  
**Hometown:** Unknown signal origin  
**Team:** Team Cosmic Folklore  
**Archetype:** Trickster

#### Visual Design

ET Bilu is not a rubber mascot. The SNK interpretation is a small, cloaked
humanoid with reflective eyes, thin limbs, and a compact UFO device floating
behind one shoulder. The palette uses muted silver, moss green, black, and
soft blue highlights.

#### Story

ET Bilu appears near the tournament to test humanity's "knowledge under
pressure." It treats every battle as a lesson and every super move as a lecture
with dangerous visual aids.

#### Fighting Style

Bilu creates awkward screen positions with warps, slow beams, hovering helpers,
and psychic pushback. It has low health and must avoid extended brawls.

#### Normal Attacks

- LP: Short psychic poke.
- HP: Long sleeve swipe.
- LK: Low shin tap.
- HK: Floating side kick.
- Close LP: Palm pulse.
- Close HP: Two-hand psychic burst.
- Close LK: Knee nudge.
- Close HK: Levitation kick.
- Far LP: Finger beam poke.
- Far HP: Staff-like arm swing.
- Far LK: Toe tap.
- Far HK: Long floating kick.
- Jump LP: Small air pulse.
- Jump HP: Cloak swipe.
- Jump LK: Fast knee.
- Jump HK: Hovering heel kick.

#### Command Normals

- Forward + LP: Seek Poke. Long-reaching finger beam, not special cancelable.
- Forward + HK: Orbit Heel. Hops forward over lows and strikes mid.

#### Special Moves

- QCF + P: Seek Knowledge Beam. Thin projectile that can be charged.
- QCB + P: UFO Summon. Floating helper fires after a delay.
- QCF + K: Warp Jump. Teleport hop with three landing distances.
- DP + P: Psychic Pulse. Defensive burst with short range.
- QCB + K: Gravity Step. Slow hover that alters jump arc.

#### Super Moves

- QCF, QCF + P: Knowledge Ray. Fast full-screen beam.
- QCB, QCB + K: Abduction Setup. UFO marker tracks and launches on contact.

#### MAX Super

- QCF, QCB + HP+HK: Cosmic Revelation. Bilu opens a star field, lectures the
  opponent with psychic glyphs, and detonates the UFO helper.

#### Extra Content

- Intro: Steps out from a cone of light and quietly raises one finger.
- Taunt: "Seek knowledge" gesture with a tiny meter gain on completion.
- Victory A: Floats upward into a beam.
- Victory B: UFO projects a diagram over the defeated opponent.
- Defeat: Cloak crumples while the UFO spins away.

#### Stage Suggestion

Beach Boardwalk at night as an alternate stage, with distant lights over the
ocean. The default story stage can be LAN House 1999 for folklore contrast.

#### MUGEN State Structure

- 1000: Seek Knowledge Beam
- 1100: UFO Summon
- 1200: Warp Jump
- 1300: Psychic Pulse
- 1400: Gravity Step
- 2000: Knowledge Ray
- 2100: Abduction Setup
- 3000: Cosmic Revelation

#### Animation List

Cloak idle, eye shine, beam charge, UFO helper spawn, warp afterimage, hover
loop, glyph super overlay, abduction victory.

#### AI Behavior

Trickster AI keeps the UFO helper active and uses Warp Jump only when covered.
At low health it prioritizes Psychic Pulse and Gravity Step retreats over raw
beam zoning.

## Team Stadium Legends

### Vampeta

**Nickname:** The Stadium Enforcer  
**Age:** 44  
**Height:** 182 cm  
**Weight:** 86 kg  
**Fighting Style:** Football wrestling and power grappling  
**Hometown:** Nazare, Bahia  
**Team:** Team Stadium Legends  
**Archetype:** Power Grappler

#### Visual Design

Vampeta has a veteran footballer's build: thick neck, heavy shoulders, and
relaxed confidence. He wears a retro training jacket tied at the waist, fitted
shorts, compression socks, and boots. Colors are dark green, black, white, and
gold. The silhouette emphasizes broad grappler arms and a low tackle stance.

#### Story

Tired of hearing that modern fighters lack grit, Vampeta enters to show that
old-school football contact is close enough to martial arts when the referee is
gone.

#### Fighting Style

Vampeta wants close range. He uses armored tackles, command grabs, and brutal
corner carry. He is slow and must read zoning carefully.

#### Normal Attacks

- LP: Short body jab.
- HP: Heavy hook.
- LK: Low boot poke.
- HK: Long veteran round kick.
- Close LP: Clinch punch.
- Close HP: Elbow crush.
- Close LK: Knee check.
- Close HK: Launcher knee.
- Far LP: Hand check.
- Far HP: Big lariat.
- Far LK: Low shin kick.
- Far HK: Heavy side kick.
- Jump LP: Short downward punch.
- Jump HP: Body splash punch.
- Jump LK: Knee drop.
- Jump HK: Heavy boot drop.

#### Command Normals

- Forward + HP: Captain's Lariat. Armored during late startup.
- Forward + LK: Stud Check. Low advancing kick, unsafe but long range.

#### Special Moves

- HCF + P: Stadium Slam. Command grab with HP damage variant.
- Charge Back, Forward + P: Shoulder Tackle. Armored horizontal rush.
- DP + P: Headbutt Rush. Anti-air headbutt sequence.
- HCB + K: Bicycle Grab. Catch-style anti-air throw.
- QCB + P: Veteran Guard. Brief armor stance with throw follow-up.

#### Super Moves

- HCB, HCB + P: Penalty Box Driver. Command grab super with corner carry.
- Charge Back, Forward, Back, Forward + P: Derby Collision. Full-screen tackle.

#### MAX Super

- HCB, HCB + HP+HK: Legendary Celebration. Cinematic command grab into stadium
  pile-on, final booted volley, and crowd roar.

#### Extra Content

- Intro: Rolls shoulders, laughs, and stamps both boots.
- Taunt: Offers the opponent a handshake, then pulls it back.
- Victory A: Raises both arms like a derby champion.
- Victory B: Sits on an invisible advertising board and grins.
- Defeat: Drops to one knee, frustrated but still talking.

#### Stage Suggestion

Interior Bar with old televisions showing football highlights, or a dedicated
Stadium Tunnel stage for boss routes.

#### MUGEN State Structure

- 1000: Stadium Slam
- 1100: Shoulder Tackle
- 1200: Headbutt Rush
- 1300: Bicycle Grab
- 1400: Veteran Guard
- 2000: Penalty Box Driver
- 2100: Derby Collision
- 3000: Legendary Celebration

#### Animation List

Heavy idle, tackle windup, armored shoulder contact, grab lift, anti-air catch,
bar TV crowd flash, command grab super slam, victory grin.

#### AI Behavior

Grappler AI advances behind Shoulder Tackle armor, uses crouch LK to force
stand-block hesitation, and only attempts Stadium Slam after blocked close HP
or jump-in pressure. Boss variants may read jumps with Bicycle Grab more often.

## Boss Variants

Bosses should keep the source character readable while exaggerating one design
axis. They are intended for arcade mode and should not be default competitive
selects unless separately balanced.

### Ultra Instinct Luva de Pedreiro

- Faster run speed and improved hop acceleration.
- Goal Shot becomes two-stage: ball feint, then delayed strike.
- MAX super gains a final wall bounce.
- Weakness: takes increased damage while whiffing RECEBA Rush.

### Cosmic ET Bilu

- UFO helper becomes permanent until hit.
- Knowledge Ray can angle upward or downward.
- Warp Jump gains one fake landing.
- Weakness: lowest stun resistance in the boss set.

### Chaos Gil Brother Away

- Shadow Clone stores one copied normal from the opponent's last attack.
- Brother Counter covers two attack levels but has longer recovery on whiff.
- MAX super starts with a fullscreen clock-stop flash.
- Weakness: low base damage outside counters.
