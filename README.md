# My Exam Game 🎮

## **JOGO DE PLATAFORMA TESTE KODLAND**

**Versão Atual**: 2.0  
**Framework**: PgZero (Python Game Zero)  
**Compatibilidade**: Windows 11/10  

---

## **REQUISITOS**

### **1. BIBLIOTECAS PERMITIDAS**
- **pgzero**: Framework principal do jogo
- **math**: Cálculos matemáticos e física
- **random**: Geração de números aleatórios

### **2. MENU OBRIGATÓRIO**
Menu principal com navegação por teclado:
- **JOGAR**: Inicia o jogo
- **MÚSICA**: Liga/desliga música de fundo
- **SONS**: Liga/desliga efeitos sonoros
- **SAIR**: Fecha o jogo

### **3. SISTEMA DE SONS**

### **4. SPRITES ANIMADOS**

### **5. INIMIGOS**
- **BlueBird**: Voa horizontalmente
- **FireBall**: Movimento vertical 
- **Ghost**: Persegue o jogador se ele estiver na área de patrulha

### **6. PERSONAGEM JOGÁVEL**

### **7. FRAMEWORK PGZERO**

### **8. NOMES EM INGLÊS**

### **9. LÓGICA SEM BUGS**

### **10. CÓDIGO ÚNICO**

---

## 🎮 **COMO JOGAR**

### **Controles:**
- **↑↓←→ ou WASD**: Movimentar no menu / Mover personagem
- **ESPAÇO**: Pular
- **ENTER**: Confirmar seleção
- **ESC**: Voltar ao menu

### **Objetivos:**
- Atravesse os níveis evitando inimigos
- Colete power-ups e vidas
- Chegue ao portal para avançar
- Complete todos os desafios

### **Features:**
- Pule nos inimigos ou colete a estrela para derrotar os inimigos  
- Colete corações para recuperar a vida  
- Chegue no topo da torre para completar a demo.  

---

## 🚀 **EXECUTÁVEIS DISPONÍVEIS**

### **📦 Versão 2.0 (Recomendada)**
**Localização**: `dist/v2/`
- `My-Exam-Game-v2.exe` (52.7 MB)
- `README-v2.md` (Documentação)
- `Executar-Game-v2.bat` (Launcher)

### **📦 Versão 1.0**
**Localização**: `dist/`
- `MyExamGame.exe` (52 MB)

---

## 🔧 **ESPECIFICAÇÕES TÉCNICAS**

### **Arquitetura do Projeto:**
```
📁 My-Exam-gamePy/
├── 📄 Main.py                    # Arquivo principal
├── 📁 Scripts/
│   ├── 📁 Actors/               # Personagens e objetos
│   │   ├── Player.py            # Jogador principal
│   │   ├── Enemies.py           # Sistema de inimigos
│   │   └── PowerFruit.py        # Coletáveis
│   ├── 📁 Components/           # Componentes do jogo
│   │   ├── InputManager.py     # Controles
│   │   ├── Movement.py          # Física e movimento
│   │   └── CollisionManager.py # Detecção de colisões
│   ├── 📁 Scenes/              # Cenas do jogo
│   │   ├── Menu.py             # Menu principal
│   │   ├── Scene1.py           # Primeira fase
│   │   └── Scene2.py           # Segunda fase
│   └── 📁 Utils/               # Utilitários
│       └── SoundManager.py     # Gerenciador de sons
├── 📁 images/                   # Sprites e texturas
├── 📁 sounds/                   # Efeitos sonoros
├── 📁 music/                    # Trilha sonora
└── 📁 dist/                     # Executáveis
```

### **Engine e Performance:**
- **Framework**: PgZero 1.2+
- **Resolução**: 800x600 pixels
- **FPS**: 60 frames por segundo
- **Física**: Gravidade 800, Força do pulo 450
- **Otimização**: Sprites pré-carregados

---

## 📞 **INFORMAÇÕES**

**Desenvolvido para**: Teste de Certificação Python Tutor  
**Desenvolvido por**: Anna Beatryz C.  
**Data**: 04 Agosto 2025  
**Versão**: 2.0 (DEMO)  
**Status**: Aguadando aprovação  

---

