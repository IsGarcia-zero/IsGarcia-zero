<p align="center">
  <img src="assets/banner.svg" width="100%" alt="Eduardo Hernández Vergara — cellular automata, emergence, slime molds. Lightweight spaceships from Conway's Game of Life fly around the name.">
</p>

### Hi, I'm Eduardo 👋

I'm into cellular automata: a grid, a handful of local rules, no one in charge, and somehow you get
gliders, chaos, traffic jams and a slime mold that solves mazes. I find that slightly unsettling and
I can't stop looking at it.

My thesis was exactly that: a *Physarum polycephalum* automaton that finds its way through caves and
catacombs. We presented it at CANDAR 2024 in Okinawa, and then I put it inside a robot with a LiDAR,
because a simulation alone didn't feel weird enough. 🦠

**[Open my CV](https://isgarcia-zero.github.io/)** · [English version](https://isgarcia-zero.github.io/?lang=en) ·
[LinkedIn](https://www.linkedin.com/in/eduardo-hernandez-vergara-369366246) ·
[eduardo.hernandezv@proton.me](mailto:eduardo.hernandezv@proton.me)

<img src="assets/rule30.svg" width="100%" alt="Rule 30 running from a random row, revealed line by line">

### 🧬 Automata I've raised

- **Physarum, the brainless co-author.** A 9-state automaton with memory per cell that traces routes
  through mazes, caves and real floor plans loaded with OpenCV. It started in SFML; in 2026 I ported it
  to Vulkan compute shaders and now it chews through 4000 × 4000 cells.
- **All 256 Wolfram rules,** with density plots, attractors, graphs and LaTeX reports written by the
  program itself, because I wanted to stare at every single one.
- **The Game of Life,** with configurable B/S rules, population charts and attractors exported to Graphviz.
- **Traffic as rule 184:** two streets, one intersection, cars that are just ones and zeros.
- **A small zoo on my CV:** Langton's ant, Brian's Brain, a cyclic automaton, Wireworld and rules 30, 90,
  110 and 184, all running live.

### 🎮 Play with my CV

It isn't a PDF: it's an F# app (Bolero + Blazor WebAssembly) wrapped around that zoo. Drop ants on
Langton's grid, select any text and rule 30 will run inside your selection, or type `life` anywhere
on the page and see what happens to it.

### 📌 Public projects

| | Repository | What it is |
| --- | --- | --- |
| 🦠 | [Physarum-Automata](https://github.com/Jessenox/Physarum-Automata) | Thesis simulation (co-authored): Physarum with cellular automata, C++, later Vulkan compute shaders |
| 🔺 | [cellularAutomataECARules](https://github.com/IsGarcia-zero/cellularAutomataECARules) | All 256 elementary rules: density, attractors, graphs, auto-generated LaTeX reports |
| 🛸 | [juegoDeLaVida](https://github.com/IsGarcia-zero/juegoDeLaVida) | Conway's Game of Life with configurable rules, population charts and attractors |
| 🚦 | [traficoControlECARules](https://github.com/IsGarcia-zero/traficoControlECARules) | An intersection where cars follow rule 184 |
| 🤖 | [Teoria-Computacional](https://github.com/IsGarcia-zero/Teoria-Computacional) | The rest of the automata family: DFA, NFA, pushdown automaton and a Turing machine |
| 🌐 | [cv-web-fs](https://github.com/IsGarcia-zero/cv-web-fs) | My CV in F# (Bolero, Blazor WebAssembly, MVU), with the automata lab inside |

### 💼 How I keep my cells fed

By day I'm a backend and cloud engineer. Go and Java microservices on AWS and NATS, deployed to
Kubernetes; apps that talk to hardware over BLE and USB in Avalonia, Flutter and F#. That work lives in
private repositories, and it's the reason the automata above get electricity.

### 🛠️ Stack

C++ · Vulkan · C# / .NET · F# · Go · Java · TypeScript · AWS · Kubernetes · NATS · Avalonia · Flutter

🗣️ Spanish (native) · English (B2) · Japanese (A2)

---

<img src="assets/glider.svg" width="32" align="left" alt="A glider">

<sub>Nothing above is hand-drawn: the banner is Conway's Game of Life (B3/S23), the strip is rule 30,
and this glider loops around a tiny torus forever. They come out of <a href="assets/automata.py">a small script</a> that runs the real rules.</sub>
