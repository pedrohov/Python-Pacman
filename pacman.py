# Disciplina : Linguagens Formais e Automatos
# Aluno      : Pedro Henrique Oliveira Veloso
# Matricula  : 0002346

# Alterar o caminho do sistema:
import sys;
sys.path.insert(0, 'scripts/');

# Importar classes:
from player import Player;
from ghost import *;

class Arbitro:
    # Inicializacao:
    def __init__(self):
        # Instancia o labirinto:
        self.maze = Maze();

        # Cria a tela:
        self._running   = True;
        self._screen    = None;
        self.weight     = self.maze.cols * 35;
        self.height     = self.maze.rows * 35 + 100;
        self.size       = self.weight, self.height;
        self.FPS        = pygame.time.Clock();

        # Instancia o Jogador:
        self.player = Player(5, 'pac');
        self.player.set_coord(self.maze.playerIniX, self.maze.playerIniY);

        # Instancia os Fantasmas:
        # x, y, speed, sprite
        self.red    = RedGhost(self.maze.ghostIniX, self.maze.ghostIniY, 5);
        self.blue   = BlueGhost(self.maze.ghostIniX, self.maze.ghostIniY, 5);
        self.pink   = PinkGhost(self.maze.ghostIniX, self.maze.ghostIniY, 5);
        self.orange = OrangeGhost(self.maze.ghostIniX, self.maze.ghostIniY, 5);

        # Exibir informacoes na tela:
        self.customFont = None;
        self.score      = None;
        self.message    = None;

        # Controlar fim do jogo:
        self.gameOver   = False;
 
    # Acontece apenas uma vez durante inicializacao:
    def on_init(self):
        # Inicializa o pygame:
        pygame.init();

        # Inicializa a fonte:
        pygame.font.init();
        self.customFont = pygame.font.SysFont('Arial', 20);

        # Cria a tela:
        self._screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF);
        pygame.display.set_caption("Pacman");

        # Informa que o jogo esta rodando:
        self._running = True;

        # Cria o labiritno:
        self.maze.create_maze();
 
    # Checa por eventos:
    def on_event(self, event):
        # Keyboard input:
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_ESCAPE):
                self._running = False;
            elif(event.key == pygame.K_UP):
                # Manda um sinal para o alfabeto do automato do jogador:
                self.player.currentState = self.player.automato.move(self.player.currentState, 'u');
                # Atualiza a imagem do jogador:
                self.player.set_surface();
            elif(event.key == pygame.K_DOWN):
                self.player.currentState = self.player.automato.move(self.player.currentState, 'd');
                self.player.set_surface();
            elif(event.key == pygame.K_LEFT):
                self.player.currentState = self.player.automato.move(self.player.currentState, 'l');
                self.player.set_surface();
            elif(event.key == pygame.K_RIGHT):
                self.player.currentState = self.player.automato.move(self.player.currentState, 'r');
                self.player.set_surface();
            elif(event.key == pygame.K_r) & (self.gameOver == True):
                # Posiciona o automato de todos os elementos moveis no estado inicial:
                self.player.currentState = self.player.automato.initial();
                self.red.currentState = self.red.automato.initial();
                self.blue.currentState = self.blue.automato.initial();
                self.pink.currentState = self.pink.automato.initial();
                self.orange.currentState = self.orange.automato.initial();

                # Reinicia o jogo:
                self.on_restart();

        if event.type == pygame.QUIT:
            self._running = False;

    # Atualiza os elementos do jogo:
    def on_loop(self):
        # Atualiza o jogador:
        self.player.update(self.maze);

        # Atualiza os fantasmas:
        self.red.update(self.player, self.maze);
        self.blue.update(self.maze);
        self.pink.update(self.maze);
        self.orange.update(self.player, self.maze);

        # Testa por colisoes entre jogador e fantasmas:
        if(self.player.rect.colliderect(self.red.rect)):
            self.gameOver = True;
        if(self.player.rect.colliderect(self.blue.rect)):
            self.gameOver = True;
        if(self.player.rect.colliderect(self.pink.rect)):
            self.gameOver = True;
        if(self.player.rect.colliderect(self.orange.rect)):
            self.gameOver = True;

        # Testa por vitoria do jogador:
        if(self.maze.totalDots == 0):
            self.gameOver = True;

    # Atualiza a tela:
    def on_render(self):
        # Limpa a tela:
        self._screen.fill((0, 0, 0));

        # Desenha o labirinto:
        self.maze.draw_maze(self._screen);

        # Desenha o jogador:
        self._screen.blit(self.player.surface, (self.player.rect.x, self.player.rect.y));
        
        # Desenha os fantasmas:
        self._screen.blit(self.red.surface, (self.red.rect.x, self.red.rect.y));
        self._screen.blit(self.blue.surface, (self.blue.rect.x, self.blue.rect.y));
        self._screen.blit(self.orange.surface, (self.orange.rect.x, self.orange.rect.y));
        self._screen.blit(self.pink.surface, (self.pink.rect.x, self.pink.rect.y));

        # Pontuacao e gameover:
        self.score = self.customFont.render("SCORE: " + str(self.player.score), False, (255, 255, 255));
        self._screen.blit(self.score, (70, self.maze.rows * 35 + (100 - 45) / 2));

        if(self.gameOver == True) & (self.maze.totalDots == 0):
            self.message = self.customFont.render("FASE COMPLETA", False, (255, 255, 255));
            self._screen.blit(self.message, (425, self.maze.rows * 35 + (100 - 60) / 2));
            self.message = self.customFont.render("'R' para recomecar", False, (255, 255, 255));
            self._screen.blit(self.message, (425, self.maze.rows * 35 + (100 - 60) / 2 + 30));
        elif(self.gameOver == True):
            self.message = self.customFont.render("GAME OVER", False, (255, 255, 255));
            self._screen.blit(self.message, (445, self.maze.rows * 35 + (100 - 60) / 2));
            self.message = self.customFont.render("'R' para recomecar", False, (255, 255, 255));
            self._screen.blit(self.message, (425, self.maze.rows * 35 + (100 - 60) / 2 + 30));

        # Atualiza a tela:
        pygame.display.flip();

    # Prepara para sair do jogo:
    def on_cleanup(self):
        pygame.quit();

    # Reiniciar o jogo apos gameover:
    def on_restart(self):
        # Reposiciona o Jogador:
        self.player = Player(5, 'pac');
        self.player.set_coord(self.maze.playerIniX, self.maze.playerIniY);

        # Reposiciona os Fantasmas:
        self.red    = RedGhost(self.maze.ghostIniX, self.maze.ghostIniY, 5);
        self.blue   = BlueGhost(self.maze.ghostIniX, self.maze.ghostIniY, 5);
        self.pink   = PinkGhost(self.maze.ghostIniX, self.maze.ghostIniY, 5);
        self.orange = OrangeGhost(self.maze.ghostIniX, self.maze.ghostIniY, 5);
        self.gameOver = False;

        self.maze.reset_maze();
 
    # Quando o jogo for chamado:
    def on_execute(self):
        if self.on_init() == False:
            self._running = False;
 
        # Loop enquanto o jogo rodar:
        while(self._running):

            for event in pygame.event.get():
                self.on_event(event);

            if(self.gameOver == False):
                self.on_loop();
                self.on_render();
                self.FPS.tick(30);

        self.on_cleanup();
 
if __name__ == "__main__" :
    jogo = Arbitro()
    jogo.on_execute()