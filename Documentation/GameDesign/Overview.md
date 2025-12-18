# Game Overview

> **Status**: Active Development  
> **Last Updated**: 2025-12-16

---

## Elevator Pitch

A 2D side-scrolling platformer-shooter where every healing choice hurts your companion and every boss was once human. Navigate surreal fantasy worlds, master magic-based combat, and face the emotional weight of mercy and sacrifice.

---

## Core Concept

Lament is a 2D platformer-shooter set in a dark fantasy world with Lynchian surrealist elements. Players control a magic-wielding protagonist who must fight through interconnected levels, each world culminating in a boss fight against beings who have lost their humanity and must be mercy-killed.

The game's central emotional hook revolves around your companion - a healer who follows you throughout your journey. When you call upon her healing abilities, it hurts her, draining her vitality to restore yours. This creates a constant moral tension: every mistake you make, every hit you take, forces you to choose between your survival and her suffering. Your fail state isn't just running out of health - it's watching her grow weaker because of your failures.

While the game presents a 3D art style for visual richness, all gameplay logic operates on a 2D plane, allowing for tight, focused platforming and combat mechanics reminiscent of classic side-scrollers but with modern presentation and emotional depth.

---

## Core Pillars

The fundamental design principles that guide all decisions:

1. **Emotional Consequences**: Every mechanical decision has emotional weight. Healing hurts your companion. Bosses were once human. Success means minimizing suffering, not just winning.

2. **Mastery Through Empathy**: The game rewards skillful play not with power, but with less harm. Players are motivated to improve not for their own glory, but to protect their companion from pain.

3. **Surreal Fantasy**: A world that blends dark fantasy aesthetics with dreamlike, Lynchian imagery. Reality is malleable, disturbing, and beautiful in equal measure.

4. **Tight Combat Flow**: Responsive platforming and shooting mechanics with magic-based abilities. Combat must feel good enough that players can achieve mastery and minimize damage taken.

---

## Target Audience

**Primary Audience**: Core gamers who appreciate narrative depth and emotional storytelling in action games

**Player Profile**:
- Age range: 18-35
- Gaming experience: Experienced with 2D action games, platformers, and indie titles with emotional narratives
- Interests: Games that combine tight mechanics with meaningful stories, dark fantasy aesthetics, surrealist art, games that explore themes of sacrifice and empathy

**Similar Games**:
- **Hollow Knight** - Tight 2D combat/platforming, dark fantasy world, melancholic tone
- **Celeste** - Precision platforming with emotional narrative, companion relationship
- **Blasphemous** - Dark fantasy 2D action, religious/surreal imagery, mercy/suffering themes
- **Hyper Light Drifter** - Beautiful 2D action, wordless storytelling, companion character
- **GRIS** - Emotional journey, artistic presentation, themes of pain and healing

---

## Genre & Style

**Genre**: 2D Side-Scrolling Platformer-Shooter

**Sub-genres/Tags**:
- Action Platformer
- Metroidvania-lite (world structure)
- Boss Rush elements
- Narrative-driven
- Dark Fantasy
- Emotional storytelling

**Art Style**: 3D rendered graphics with 2D gameplay perspective. Dark fantasy aesthetic with surrealist/Lynchian elements - beautiful but unsettling, mixing organic and dreamlike imagery.

**Tone**: Dark, melancholic, introspective. Emotionally heavy but with moments of beauty. Focuses on themes of sacrifice, mercy, loss of humanity, and the cost of survival.

---

## Key Features

1. **Companion Sacrifice System**: Your healer companion follows you and restores your health at the cost of her own vitality. Every healing decision carries emotional and mechanical weight.

2. **Mercy Kill Boss Fights**: Bosses are former humans who have lost their humanity. Each boss fight is a tragedy, not a triumph - you're ending their suffering, not celebrating victory.

3. **Magic-Based Combat**: Blend ranged shooting and melee attacks using magical abilities. Responsive, skill-based combat that rewards mastery.

4. **World-Based Level Structure**: Fight through multiple interconnected levels that form cohesive worlds, each ending in a boss encounter.

5. **Dual Fail State**: Die from taking too much damage OR from draining your companion completely. Both represent different kinds of failure.

6. **Surreal Fantasy World**: Lynchian atmosphere mixing fantasy elements with real-world objects in dreamlike, unsettling arrangements.

7. **2.5D Presentation**: 3D art and environments rendered from a 2D gameplay perspective, providing visual depth while maintaining tight platformer controls.

---

## Technical Overview

**Engine**: Unreal Engine 5.5

**Primary Language**: C++

**Target Platforms**: PC (primary), with potential for console ports

**Estimated Scope**: Solo/small team project, focused scope with deep mechanical and emotional systems

**Development Phase**: Pre-production / Setup

**Technical Approach**:
- 3D assets and rendering for visual richness
- 2D collision and movement logic for tight platformer feel
- Side-view camera locked to 2D plane
- Blueprint for rapid prototyping, C++ for core systems

---

## Development Roadmap

### Phase 1: Pre-production (Current)
- [x] Finalize core game concept
- [x] Create initial design documentation
- [x] Design core movement and platforming mechanics
- [ ] Prototype core movement and platforming
- [ ] Prototype basic shooting mechanics
- [ ] Establish visual art direction and test scenes
- [ ] Design companion following/healing system
- [ ] Create first boss concept (mechanics and narrative)

### Phase 2: Vertical Slice
- [ ] Single complete level with full gameplay loop
- [ ] Companion AI and healing system fully functional
- [ ] One complete boss fight with mercy-kill mechanics
- [ ] Core combat abilities implemented
- [ ] Art style established and consistent
- [ ] Basic UI for health, companion status, abilities

### Phase 3: Production
- [ ] Build out 3-5 complete worlds with multiple levels each
- [ ] Design and implement 3-5 unique boss fights
- [ ] Expand magic ability system
- [ ] Create enemy variety for each world
- [ ] Implement narrative beats and environmental storytelling
- [ ] Audio design and music integration

### Phase 4: Polish & Release
- [ ] Balance difficulty and companion healing economy
- [ ] Playtesting and iteration
- [ ] Performance optimization
- [ ] Final art pass and visual polish
- [ ] Narrative/emotional beat refinement
- [ ] Release preparation

---

## Key Differentiators

1. **Inverted Healing Cost**: Unlike most games where healing is a resource you manage selfishly, healing directly harms someone you care about. This flips the emotional framing of failure - you're not just bad at the game, you're hurting your companion.

2. **Empathy as Skill Motivation**: Most games motivate mastery through rewards (better gear, more power). Lament motivates mastery through empathy - getting better means protecting your companion from suffering.

3. **Tragedy Over Triumph**: Boss fights aren't epic victories but mercy killings. Each boss represents a fallen soul that must be put to rest. The emotional tone is somber, not celebratory.

4. **Mechanical-Narrative Fusion**: The companion healing system isn't just a story element or just a mechanic - it's both simultaneously. The mechanics create the emotional experience; the narrative gives the mechanics meaning.

5. **Lynchian Surrealism in Action Games**: While many indie games use surrealism in walking sims or puzzle games, Lament brings that aesthetic to fast-paced action platforming, creating a unique tonal blend.

---

## Core Gameplay Loop

**Micro Loop (Moment-to-Moment)**:
1. Platform through level geometry
2. Engage enemies with ranged/melee magic attacks
3. Take damage, must decide when to heal
4. Call companion to heal (hurting her in the process)
5. Repeat, trying to minimize damage taken

**Macro Loop (Level-to-Level)**:
1. Navigate through interconnected levels within a world
2. Fight through enemies and environmental challenges
3. Reach boss arena
4. Fight and mercy-kill boss (tragic, emotional climax)
5. Proceed to next world
6. Companion's condition reflects your accumulated failures

**Emotional Arc**:
- Start: Hopeful, exploratory
- Middle: Growing attachment to companion, guilt over healing
- Late: Desperate to protect companion, mastery-driven play
- Boss fights: Cathartic tragedy, somber victory

---

## Documentation Links

**Current Documentation**:
- [[Bosses/BossOverview|Boss Design]] - Mercy-kill mechanics, boss concepts, Lament cutscenes
- [[Systems/GameFeel|Game Feel]] - Visual/audio feedback techniques, juice and polish
- [[Mechanics/PlayerMovement|Player Movement]] - Movement mechanics, platforming, advanced techniques

**Future Documentation**:
- [[Mechanics/Combat|Combat System]] - Shooting, melee, magic abilities
- [[Systems/CompanionAI|Companion System]] - Following AI, healing mechanics
- [[Systems/HealthDamage|Health & Damage]] - Player/companion health, fail states
- [[Narrative/WorldBuilding|World & Lore]] - Setting, themes, surrealist elements
- [[Narrative/Companion|Companion Character]] - Identity, relationship, arc
- [[Technical/2D3DHybrid|2D/3D Architecture]] - How 3D art works with 2D logic

---

## Notes

**Inspirations**:
- **Lynchian aesthetics**: David Lynch films (especially Eraserhead, Twin Peaks) for surreal, dreamlike atmosphere
- **Dark Souls**: For mercy-killing themes (similar to Sif fight emotional impact)
- **Shadow of the Colossus**: Tragic boss fights, melancholic tone
- **ICO/The Last Guardian**: Companion protection mechanics
- **Hollow Knight**: Tight 2D combat in melancholic world

**Key Themes to Explore**:
- Sacrifice and empathy
- Loss of humanity
- The cost of survival
- Mercy vs. cruelty
- Guilt and responsibility
- Beauty in darkness

**Artistic Direction Notes**:
- Fantasy elements: Magic, mythical creatures, otherworldly architecture
- Real-world elements: Familiar objects in unfamiliar contexts (Lynchian touch)
- Color palette: Muted with strategic color accents, emphasis on atmosphere
- Environmental storytelling: Show don't tell, world speaks through visuals

---

## Success Criteria

**For the Player**:
- Mechanical: Complete levels while taking minimal damage
- Emotional: Feel genuine attachment to companion, guilt when healing
- Narrative: Experience boss fights as tragic mercy, not triumphant victories

**For the Project**:
- Create memorable emotional experience through mechanics
- Achieve tight, responsive platformer/shooter feel
- Successfully blend surrealist aesthetics with action gameplay
- Make players think about the cost of healing in games
