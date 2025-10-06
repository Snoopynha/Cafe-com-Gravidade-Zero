# Stellar Legacy


![Version](https://img.shields.io/badge/Version-1.0.0-brightgreen)
![Language](https://img.shields.io/badge/Language-English-lightgrey)

You can run the project using a **`.bat`** file for convenience on Windows systems, or follow the steps below.

### Prerequisites
To run this project, you will need to have Python 3.10 or newer installed.

Go to https://www.python.org/downloads/ to download and install it.

Important (Windows): During installation, make sure to check the box that says "Add Python to PATH".

Installation Steps
Clone the Repository

Open your terminal or command prompt and run the following command to clone the project:

<pre>
git clone https://github.com/your-username/stellar-legacy.git
cd stellar-legacy </pre>

Alternative: If you don't have Git, you can download the project as a ZIP file. On the repository page, click Code > Download ZIP and extract the files. Then, navigate to the extracted folder in your terminal.

Create and Activate a Virtual Environment

It's good practice to use a virtual environment to isolate the project's dependencies.

Create the virtual environment
python -m venv venv
Now, activate the environment. The command varies depending on your operating system:

On Windows (PowerShell):

PowerShell

.\venv\Scripts\Activate.ps1
On macOS and Linux:


source venv/bin/activate
You will know the environment is active when you see (venv) at the beginning of your terminal line.

Install the Dependencies

With the virtual environment active, install the project's only dependency, Pygame:

<pre>

pip install pygame
Running the Game
After installation, run the game with the following command: </pre>

python core.py
The game window should open, and you'll be ready to start your mission!


### 1. Presentation

Imagine being a space engineer for just one minute. Sixty seconds to build a home in the stars. Sounds impossible? That is exactly the challenge of this game.

It is a single-player adventure where the clock is ticking, your imagination is alive, and every decision matters. From placing the airlock in the right spot to choosing where your astronauts will sleep, you are not just building a habitat; you are creating a tiny universe where people can live, work, and explore.

You start by picking your habitat. Perhaps the classic cylindrical module draws you in, solid and dependable, reminiscent of the International Space Station. Or maybe the hybrid "canister" habitat catches your eye, with its rigid base and inflatable upper floors, perfect for lunar or Martian surfaces. For those seeking a futuristic challenge, the expandable capsule packs a large living space into a compact launch configuration. Each choice is more than a design decision. It is a personality statement.

Once you have selected your stage, the real fun begins. Players are provided with a suite of items inspired by real space technologies: airlocks, exercise machines, research labs, and more. You drag, drop, and arrange each system, striving to make everything fit, work, and make sense. As the timer ticks down, you may find the medical station still missing. It is chaotic, yet rewarding, as the game balances strategy with playful improvisation.

The countdown drives the thrill, producing tension and excitement while allowing experimentation and discovery. Every session is a small story of triumph, failure, and the minor victories in between.

Stellar Legacy teaches without lecturing. Astronauts require exercise, sleep, and proper nutrition. The airlock is essential for extravehicular activities. Life support systems are critical. Every decision carries consequences, each serving as a mini-lesson wrapped in engaging gameplay.

Being single-player allows a focus on creativity without external pressure. You may plan meticulously or experiment wildly. Both approaches are valid. Every habitat you design tells a story, from compact efficiency in a small capsule to sprawling layouts in hybrid habitats. Every session unfolds a new narrative.

Now it is your turn. Step into this adventure and let your imagination take flight among the stars.

---

### 2. Game Overview

#### 2.1 Player Mode

* Single-player. The user assumes the role of a space habitat engineer.  
* Emphasis on individual creativity, strategy, and decision-making.  
* Every session presents a unique challenge, promoting iterative improvement and optimization.

#### 2.2 Core Components

The game is divided into two main sections:

1. Habitat Types – architectural structures and their operational characteristics.  
2. Item and Mission Impact Analysis – functional evaluation of systems, crew support, and operational efficiency.

---

### 3. Part 1: Habitat Types

#### 3.1 Cylindrical Metallic Habitat

**Reference:** Harmony Module, ISS  
**Description:** Rigid aluminum cylinder launched pre-pressurized with integrated systems.

**Advantages**

* Structurally robust for mounting external systems.  
* Ready-to-use, reducing setup time for crew.

**Disadvantages**

* Launch efficiency limited (1:1 volume ratio).  
* High cost for smaller rockets.

**Typical Mission Profile**

| Attribute | Specification |
|-----------|---------------|
| Location  | Low Earth Orbit or cislunar stations |
| Duration  | 6 months to multiple years |
| Crew      | 2–4 astronauts per module |

---

#### 3.2 Hybrid "Canister" Habitat

**Reference:** Artemis Surface Habitat  
**Description:** Combines a rigid metallic base with an inflatable multi-level upper section to maximize volume.

**Advantages**

* Maximized internal volume.  
* Stable base suitable for planetary surfaces.

**Disadvantages**

* Deployment complexity: requires inflation and outfitting.

**Typical Mission Profile**

| Attribute | Specification |
|-----------|---------------|
| Location  | Lunar or Martian surface |
| Duration  | 30–60+ days |
| Crew      | 2–4 astronauts |

---

#### 3.3 Expandable Capsule Habitat

**Reference:** BEAM (Bigelow Expandable Activity Module)  
**Description:** Launched compact and inflated in space. Multi-layer construction ensures protection against vacuum, radiation, and micrometeorites.

**Advantages**

* High launch-to-habitable volume ratio.  
* Lightweight and flexible.

**Disadvantages**

* External equipment installation is challenging.  
* Material may degrade over long durations.

**Typical Mission Profile**

| Attribute | Specification |
|-----------|---------------|
| Location  | Expansion modules or Mars transit/surface habitats |
| Duration  | Variable (depending on material resilience) |
| Crew      | 2–6 astronauts |

---

### 4. Part 2: Habitat Items and Mission Impact

#### 4.1 EVA Support

| Item | Function | Operational Impact |
|------|---------|------------------|
| EVA Zone (Airlock, Suitports) | Safe transition between habitat and vacuum | 1–2 units: basic EVA; multiple: redundancy; none: confined |
| EVA Computer Station | EVA planning and monitoring | One: functional baseline; Two: simultaneous management |

#### 4.2 Crew Health and Well-being

| Item | Function | Operational Impact |
|------|---------|------------------|
| Exercise Equipment | Prevents muscle/bone loss | Single: minimum; Two or more: redundancy |
| Hygiene Area & Waste Management | Maintains hygiene, health, morale | One: basic; Two: enhanced comfort for 4+ crew |
| Medical Area | Diagnostics, treatments, emergencies | Dedicated: essential; Multiuse: acceptable for short missions |

#### 4.3 Habitability and Daily Life

| Item | Function | Operational Impact |
|------|---------|------------------|
| Sleeping Quarters | Privacy, ventilation, acoustic isolation | Shared: <30 days; Private: >30 days |
| Galley & Wardroom | Meals, social interaction | One combined area: ideal; multiple: reduces cohesion |

#### 4.4 Operations and Work

| Item | Function | Operational Impact |
|------|---------|------------------|
| Computer Stations & Control Panels | Habitat operations | One: single point of failure; multiple: redundancy |
| Research Lab & ISPR Racks | Scientific experiments | Multiuse: functional; dedicated: maximizes output |
| Environmental Control & Life Support (ECLSS) | Air, water, temperature regulation | Open-loop: short missions; Regenerative: essential for long missions |

---

### 5. Structural Components

| Item | Function | Operational Impact |
|------|---------|------------------|
| Walls (Fixed or Retractable) | Define functional zones, airflow management | Few: open concept; Fixed: essential >30 days; Retractable: flexible reconfiguration |
| Storage Cabinets & ISPR Racks | Logistics and payload management | Few: disorganized; Multiple: efficient and scalable |


The ultimate question remains: can you construct a fully functional and realistic space habitat in just sixty seconds?

---

![Version](https://img.shields.io/badge/Version-1.0.0-brightgreen)
![Language](https://img.shields.io/badge/Language-Portuguese-lightgrey)



### 1. Apresentação

Imagine ser um engenheiro espacial por apenas um minuto. Sessenta segundos para construir um lar nas estrelas. Parece impossível? Esse é exatamente o desafio deste jogo.

É uma aventura para um jogador, onde o tempo está correndo, sua imaginação está ativa e cada decisão importa. Desde posicionar corretamente o airlock até escolher onde seus astronautas irão dormir, você não está apenas construindo um habitat; você está criando um pequeno universo onde as pessoas podem viver, trabalhar e explorar.

Você começa escolhendo seu habitat. Talvez o clássico módulo cilíndrico chame sua atenção, sólido e confiável, lembrando a Estação Espacial Internacional. Ou talvez o habitat híbrido "canister" desperte seu interesse, com sua base rígida e andares superiores infláveis, perfeito para a Lua ou Marte. E se você busca algo futurista, a cápsula expansível oferece muito espaço em um lançamento compacto. Cada escolha é mais que uma decisão de design. É uma afirmação de personalidade.

Uma vez selecionado o habitat, a diversão começa de verdade. O jogador recebe um conjunto de itens inspirados em tecnologias espaciais reais: airlocks, equipamentos de exercício, laboratórios de pesquisa e muito mais. Você arrasta, solta e organiza cada sistema, tentando fazer tudo caber, funcionar e fazer sentido. À medida que o tempo se esgota, você pode perceber que a estação médica ainda está faltando. É caótico, mas recompensador, já que o jogo equilibra estratégia com improvisação divertida.

A contagem regressiva aumenta a emoção, gerando tensão e entusiasmo enquanto permite experimentação e descoberta. Cada sessão é uma pequena história de triunfos, falhas e pequenas vitórias no meio do caminho.

Stellar Legacy ensina sem parecer uma aula. Astronautas precisam de exercícios, sono e alimentação adequada. O airlock é essencial para atividades extraveiculares. Sistemas de suporte à vida são críticos. Cada decisão tem consequências, cada consequência é uma mini-lição incorporada ao jogo.

Por ser para um jogador, o foco está na criatividade sem pressão externa. Você pode planejar meticulosamente ou experimentar de forma ousada. Ambas as abordagens são válidas. Cada habitat que você projeta conta uma história, desde a eficiência compacta de uma cápsula pequena até layouts expansivos em habitats híbridos. Cada sessão revela uma narrativa nova.

Agora é sua vez. Entre nessa aventura e deixe sua imaginação voar entre as estrelas.

---

### 2. Visão Geral do Jogo

#### 2.1 Modo do Jogador

* Um jogador. O usuário assume o papel de engenheiro de habitats espaciais.  
* Ênfase em criatividade, estratégia e tomada de decisão individual.  
* Cada sessão apresenta um desafio único, promovendo melhoria e otimização iterativa.

#### 2.2 Componentes Principais

O jogo é dividido em duas seções principais:

1. Tipos de Habitat – estruturas arquitetônicas e suas características operacionais.  
2. Itens e Análise de Impacto na Missão – avaliação funcional dos sistemas, suporte à tripulação e eficiência operacional.

---

### 3. Parte 1: Tipos de Habitat

#### 3.1 Habitat Cilíndrico Metálico

**Referência:** Módulo Harmony, ISS  
**Descrição:** Cilindro rígido de alumínio lançado pré-pressurizado com sistemas integrados.

**Vantagens**

* Estruturalmente robusto para suportar sistemas externos.  
* Pronto para uso, reduzindo o tempo de instalação para a tripulação.

**Desvantagens**

* Eficiência de lançamento limitada (relação 1:1 entre volume lançado e utilizável).  
* Custo elevado para foguetes menores.

**Perfil Típico da Missão**

| Atributo | Especificação |
|-----------|---------------|
| Localização | Órbita Terrestre Baixa ou estações cislunares |
| Duração | 6 meses a vários anos |
| Tripulação | 2–4 astronautas por módulo |

---

#### 3.2 Habitat Híbrido "Canister"

**Referência:** Habitat de Superfície Artemis  
**Descrição:** Combina base metálica rígida com seção inflável multi-nível para maximizar o volume.

**Vantagens**

* Maximiza o espaço interno.  
* Base estável adequada para superfícies planetárias.

**Desvantagens**

* Complexidade de implantação: requer inflação e montagem interna.

**Perfil Típico da Missão**

| Atributo | Especificação |
|-----------|---------------|
| Localização | Superfície Lunar ou Marciana |
| Duração | 30–60+ dias |
| Tripulação | 2–4 astronautas |

---

#### 3.3 Habitat Cápsula Expansível

**Referência:** BEAM (Bigelow Expandable Activity Module)  
**Descrição:** Lançado compacto e inflado no espaço. Construção multicamadas garante proteção contra vácuo, radiação e micrometeoritos.

**Vantagens**

* Alta relação entre volume habitável e volume lançado.  
* Leve e flexível.

**Desvantagens**

* Instalação de equipamentos externos é desafiadora.  
* Material pode degradar-se em longos períodos.

**Perfil Típico da Missão**

| Atributo | Especificação |
|-----------|---------------|
| Localização | Módulos de expansão ou habitats de trânsito/superfície em Marte |
| Duração | Variável (dependendo da durabilidade do material) |
| Tripulação | 2–6 astronautas |

---

### 4. Parte 2: Itens do Habitat e Impacto na Missão

#### 4.1 Suporte EVA

| Item | Função | Impacto Operacional |
|------|---------|------------------|
| Zona EVA (Airlock, Suitports) | Transição segura entre habitat e vácuo | 1–2 unidades: EVA básico; múltiplas: redundância; nenhuma: tripulação confinada |
| Estação de Computador EVA | Planejamento e monitoramento de EVA | Uma: base funcional; Duas: gerenciamento simultâneo |

#### 4.2 Saúde e Bem-estar da Tripulação

| Item | Função | Impacto Operacional |
|------|---------|------------------|
| Equipamento de Exercício | Previne perda muscular e óssea | Uma unidade: mínima; Duas ou mais: redundância |
| Área de Higiene & Gestão de Resíduos | Mantém higiene, saúde e moral | Uma: básica; Duas: conforto melhorado para 4+ tripulantes |
| Área Médica | Diagnósticos, tratamentos e emergências | Dedicada: essencial; Multiuso: aceitável para missões curtas |

#### 4.3 Habitabilidade e Vida Diária

| Item | Função | Impacto Operacional |
|------|---------|------------------|
| Quartos de Dormir | Privacidade, ventilação, isolamento acústico | Compartilhado: <30 dias; Privado: >30 dias |
| Cozinha & Sala de Refeições | Refeições e interação social | Área combinada: ideal; múltiplas: reduzem coesão |

#### 4.4 Operações e Trabalho

| Item | Função | Impacto Operacional |
|------|---------|------------------|
| Estações de Computador & Painéis de Controle | Operações do habitat | Uma: ponto único de falha; múltiplas: redundância |
| Laboratório de Pesquisa & Racks ISPR | Experimentos científicos | Multiuso: funcional; Dedicado: maximiza produção |
| Sistema de Controle Ambiental & Suporte à Vida (ECLSS) | Ar, água, temperatura | Circuito aberto: missões curtas; Regenerativo: essencial para missões longas |

---

### 5. Componentes Estruturais

| Item | Função | Impacto Operacional |
|------|---------|------------------|
| Paredes (Fixas ou Retráteis) | Definição de zonas e gestão de fluxo de ar | Poucas: conceito aberto; Fixas: essenciais >30 dias; Retráteis: reconfiguração flexível |
| Armários & Racks ISPR | Gestão de logística e cargas | Poucos: desorganizado; Múltiplos: eficiente e escalável |


A pergunta final permanece: você consegue construir um habitat espacial totalmente funcional e realista em apenas sessenta segundos?
