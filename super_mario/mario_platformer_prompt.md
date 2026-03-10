# Prompt for Generating a Mario-Style Platformer Game (Single Python File)

---

## 1. Objective

Create a complete, polished, single-file Python application that implements a **2D side-scrolling platformer game** inspired by classic platform games such as *Super Mario Bros.*.

The game should be built using **Python 3** and the **Pygame** library, and the entire implementation must exist in **one single Python file** (e.g., `platformer_game.py`).

The goal is to create a smooth, visually clean, and enjoyable platform game that demonstrates physics, collision detection, and simple enemy behavior while remaining organized and readable.

---

## 2. Game Environment

### Window Configuration

- **Window size:** 800 × 600 pixels
- **Frame rate:** 60 FPS
- **Background color:** Sky blue

The game world contains:
- Ground platforms
- Floating platforms
- Enemies
- Collectible coins
- A goal flag at the end

> The level should be **larger than the screen width**, and the camera should **scroll horizontally** as the player moves.

---

## 3. Player Character

### Appearance

- Represent the player as a simple colored rectangle or sprite.
- **Suggested size:** 40 × 50 pixels
- **Color:** Red

### Player Controls

| Key | Action |
|-----|--------|
| Left Arrow / A | Move left |
| Right Arrow / D | Move right |
| Space | Jump |
| R | Restart game |

### Player Physics

The player must have realistic platformer physics:

- Gravity pulling the player downward
- Jump velocity when pressing jump
- Horizontal movement speed
- Collision with platforms
- Prevent player from passing through solid objects

**Example physics parameters:**

```python
gravity = 0.5
jump_strength = -10
move_speed = 5
```

> The player should only be able to jump **when standing on a platform or the ground**.

---

## 4. Platforms and Level Layout

Platforms are rectangular blocks that the player can stand on.

### Platform Design

- **Platform color:** Brown
- Platform sizes may vary
- Platforms must include:
  - A ground floor
  - Several floating platforms

### Example Level Layout

```
Ground floor across entire level
Floating platforms at different heights
```

**Level width example:**
```
Level width = 2000 pixels
```
> This requires a **camera scrolling system**.

---

## 5. Camera System

The camera should **follow the player horizontally**.

When the player moves:
- The world scrolls
- The player remains near the center of the screen

> Only **horizontal scrolling** is required.

---

## 6. Enemies

Add simple enemies inspired by the classic walking enemy from *Super Mario Bros.*.

### Enemy Behavior

- Enemies move **left and right**
- They **reverse direction** when hitting platform edges or walls
- **Enemy size:** 40 × 40 pixels
- **Color:** Dark Red

### Player Interaction

| Player Action | Result |
|---------------|--------|
| Jumps on top of an enemy | Enemy disappears + player gains score |
| Touches the enemy from the side | Player loses a life |

---

## 7. Coins (Collectibles)

Coins are collectible objects placed above platforms.

### Coin Properties

- **Shape:** Circle
- **Color:** Gold / Yellow
- **Size:** 10–12 pixels

### Behavior

When the player touches a coin:
- Coin disappears
- Score increases

```
coin_value = +10 points
```

---

## 8. Goal Flag

At the **far right of the level**, place a goal flag.

When the player reaches the flag:
- The game displays **"YOU WIN!"**
- Gameplay stops
- Player can press **R** to restart

---

## 9. Lives System

Player starts with:
```
lives = 3
```

**Player loses a life when:**
- Touching an enemy from the side
- Falling off the map

**When a life is lost:**
- Player respawns at the start

**If lives reach 0:**
```
GAME OVER
Press R to Restart
```

---

## 10. Score System

Score increases through:

| Action | Points |
|--------|--------|
| Collect coin | +10 |
| Defeat enemy | +20 |
| Reach flag | +100 |

> Score must be **displayed on the screen**.

---

## 11. User Interface

Display UI elements on the screen:

- **Top-left:** `Score: XXXX`
- **Top-right:** `Lives: X`
- **Messages when needed:**

```
YOU WIN!
GAME OVER
Press R to Restart
```

> Use a clean, readable font.

---

## 12. Graphics Style

Use simple but polished 2D graphics.

### Recommended Colors

| Element | Color |
|---------|-------|
| Background | Sky Blue |
| Platforms | Brown |
| Player | Red |
| Enemies | Dark Red |
| Coins | Yellow |
| Flag | Green |

### Visual Improvements

Add small visual enhancements such as:
- Platform outlines
- Coin shine
- Smooth animations if possible

---

## 13. Code Structure

All code must remain inside **one single Python file**.

The program should be organized using **classes**:

- `Player`
- `Platform`
- `Enemy`
- `Coin`
- `Game`

The `Game` class should manage:
- Initialization
- Input handling
- Game updates
- Collision detection
- Drawing
- Main game loop

---

## 14. Main Game Loop

The game loop should include:

```python
handle_input()
update_game_state()
handle_collisions()
draw_everything()
update_display()
```

> Running at **60 FPS**.

---

## 15. Restart Mechanism

Pressing **R** must:
- Reset score
- Reset lives
- Respawn enemies
- Respawn coins
- Reset player position
- Restart the game

---

## 16. Technical Requirements

- **Language:** Python 3
- **Library:** `pygame`
- Entire game contained in **one Python file**
- Code should be **clean, readable, and commented**
- Avoid unnecessary dependencies

**Game must run with:**
```bash
python platformer_game.py
```

---

## 17. Deliverable

Provide a complete, runnable Python file:

**`platformer_game.py`**

The file must implement:

- ✅ Player movement
- ✅ Gravity and jumping
- ✅ Scrolling camera
- ✅ Enemies
- ✅ Coins
- ✅ Platforms
- ✅ Scoring
- ✅ Lives
- ✅ Win and Game Over screens

> The result should be a **playable Mario-style platformer game in a single file**.
