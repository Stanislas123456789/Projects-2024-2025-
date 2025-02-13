const story = [
    {
        text: "In a Victorian mansion's dimly lit gallery, an enigmatic portrait catches your eye. The brushstrokes seem to shimmer with an otherworldly quality...",
        background: "linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1618220671537-c819e3f1274a')",
        options: [
            { text: "Examine the portrait closer", next: 1 },
            { text: "Search the room", next: 2 }
        ]
    },
    {
        text: "As you approach, the portrait seems to change. The subject's features shift between youth and age, beauty and decay. A mystifying energy emanates from the canvas...",
        background: "linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1582561424760-0321d75e81fa')",
        options: [
            { text: "Touch the canvas", next: 3 },
            { text: "Step back", next: 2 }
        ]
    },
    {
        text: "The room holds many secrets. Antique furniture casts long shadows, and velvet curtains whisper with the evening breeze. A small desk catches your attention...",
        background: "linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1618219944342-824e40a13285')",
        options: [
            { text: "Examine the desk", next: 4 },
            { text: "Return to the portrait", next: 1 }
        ]
    },
    {
        text: "The moment your fingers brush the canvas, you feel a strange tingling sensation. The room begins to spin, colors blur together...",
        background: "linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1619472351888-f844a0b33875')",
        options: [
            { text: "Close your eyes", next: 5 },
            { text: "Try to step back", next: 4 }
        ]
    },
    {
        text: "In the desk drawer, you find an old letter. The handwriting is elegant, the ink slightly faded. It's signed by Oscar Wilde himself!",
        background: "linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1585258212873-91d745086fc3')",
        options: [
            { text: "Read the letter", next: 5 },
            { text: "Look for more clues", next: 3 }
        ]
    },
    {
        text: "The letter contains a magical secret - true love transcends time and appearance. As you realize this, the room fills with a warm, golden light...",
        background: "linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url('https://images.unsplash.com/photo-1518621736915-f3b1c41bfd00')",
        options: [
            { text: "Embrace the light", next: 6 },
            { text: "Start the mini-game", next: -1, action: 'startGame' }
        ]
    },
    {
        text: "The light envelops you, and a special message appears...",
        background: "linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url('https://images.unsplash.com/photo-1518621736915-f3b1c41bfd00')",
        options: [
            { text: "Read the message", next: 7 }
        ]
    },
    {
        text: "Je t'aime de tout mon coeur Camille... Marry me ?",
        background: "red",
        options: [],
        action: "showValentine"
    }
];

let currentStep = 0;
let gameStarted = false;

function updateStory() {
    const storyText = document.getElementById('storyText');
    const optionsContainer = document.getElementById('options');
    const backgroundLayer = document.getElementById('backgroundLayer');
    
    optionsContainer.innerHTML = '';
    
    // Update background
    if (story[currentStep].background) {
        backgroundLayer.style.backgroundImage = story[currentStep].background;
    }

    // Update text with fade effect
    storyText.style.opacity = 0;
    setTimeout(() => {
        storyText.innerText = story[currentStep].text;
        storyText.style.opacity = 1;
    }, 300);

    // Special valentine's action
    if (story[currentStep].action === "showValentine") {
        setTimeout(showValentinesMessage, 1000);
        return;
    }

    story[currentStep].options.forEach((option) => {
        const button = document.createElement('button');
        button.innerText = option.text;
        button.className = 'optionButton';
        button.onclick = () => {
            if (option.action === 'startGame') {
                startGame();
            } else {
                advanceStory(option.next);
            }
        };
        optionsContainer.appendChild(button);
    });
}

function showValentinesMessage() {
    const overlay = document.getElementById('valentinesOverlay');
    overlay.classList.remove('hidden');
    setTimeout(() => {
        overlay.classList.add('visible');
        createHeartRain();
    }, 100);
}

function createHeartRain() {
    const container = document.getElementById('valentinesOverlay');
    const heart = document.createElement('div');
    heart.innerHTML = '❤️';
    heart.className = 'falling-heart';
    heart.style.left = Math.random() * 100 + '%';
    heart.style.animationDuration = Math.random() * 3 + 2 + 's';
    container.appendChild(heart);

    heart.addEventListener('animationend', () => {
        heart.remove();
    });

    if (document.getElementById('valentinesOverlay').classList.contains('visible')) {
        setTimeout(createHeartRain, 100);
    }
}

function advanceStory(nextStep) {
    currentStep = nextStep;
    updateStory();
}

function startGame() {
    if (gameStarted) return;
    gameStarted = true;
    
    document.getElementById('gameContainer').style.display = 'none';
    const canvas = document.getElementById('gameCanvas');
    canvas.style.display = 'block';
    
    // Set canvas size to match window size
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    const ctx = canvas.getContext('2d');

    const player = {
        x: canvas.width / 2,
        y: canvas.height / 2,
        size: 20,
        speed: 5,
        color: '#4a90e2'
    };

    const keys = {};
    let score = 0;
    let gameOver = false;

    // Create collectibles
    const collectibles = Array(5).fill(null).map(() => ({
        x: Math.random() * (canvas.width - 20),
        y: Math.random() * (canvas.height - 20),
        size: 15,
        color: '#gold'
    }));

    window.addEventListener("keydown", (e) => keys[e.key] = true);
    window.addEventListener("keyup", (e) => keys[e.key] = false);

    function update() {
        if (gameOver) return;

        // Player movement
        if (keys["ArrowUp"] || keys["w"]) player.y -= player.speed;
        if (keys["ArrowDown"] || keys["s"]) player.y += player.speed;
        if (keys["ArrowLeft"] || keys["a"]) player.x -= player.speed;
        if (keys["ArrowRight"] || keys["d"]) player.x += player.speed;

        // Keep player in bounds
        player.x = Math.max(0, Math.min(canvas.width - player.size, player.x));
        player.y = Math.max(0, Math.min(canvas.height - player.size, player.y));

        // Check collectible collisions
        collectibles.forEach((collectible, index) => {
            if (collectible && checkCollision(player, collectible)) {
                collectibles[index] = null;
                score++;
                if (score >= 5) {
                    gameOver = true;
                    setTimeout(resetGame, 2000);
                }
            }
        });
    }

    function checkCollision(rect1, rect2) {
        return rect1.x < rect2.x + rect2.size &&
               rect1.x + rect1.size > rect2.x &&
               rect1.y < rect2.y + rect2.size &&
               rect1.y + rect1.size > rect2.y;
    }

    function draw() {
        // Clear canvas
        ctx.fillStyle = '#2d5a27';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Draw player
        ctx.fillStyle = player.color;
        ctx.fillRect(player.x, player.y, player.size, player.size);

        // Draw collectibles
        collectibles.forEach(collectible => {
            if (collectible) {
                ctx.fillStyle = collectible.color;
                ctx.fillRect(collectible.x, collectible.y, collectible.size, collectible.size);
            }
        });

        // Draw score
        ctx.fillStyle = 'white';
        ctx.font = '24px Lora';
        ctx.fillText(`Score: ${score}`, 20, 40);

        if (gameOver) {
            ctx.fillStyle = 'white';
            ctx.font = '48px Lora';
            ctx.textAlign = 'center';
            ctx.fillText('You Win!', canvas.width/2, canvas.height/2);
        }
    }

    function resetGame() {
        gameStarted = false;
        canvas.style.display = 'none';
        document.getElementById('gameContainer').style.display = 'block';
        advanceStory(0);
    }

    function gameLoop() {
        if (!gameStarted) return;
        update();
        draw();
        requestAnimationFrame(gameLoop);
    }

    gameLoop();
}

window.addEventListener('load', () => {
    updateStory();
});

// End of script.js

