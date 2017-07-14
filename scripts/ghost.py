# Disciplina : Linguagens Formais e Automatos
# Aluno      : Pedro Henrique Oliveira Veloso
# Matricula  : 0002346

from movingobject import *;
from random import randint;

class Ghost(MovingObject):
    def __init__(self, x, y, speed, name):
        MovingObject.__init__(self, speed, name);
        self.set_coord(x, y);

    def getPriorities(self, player):
        # Posicao do jogador em relacao ao fantasma,
        # Manda um sinal para o automato informando sua posicao.

        # Jogador esta no segundo quadrante:
        if((player.rect.x < self.rect.x) & (player.rect.y < self.rect.y)):
            self.currentState = self.automato.move(self.currentState, '1');

        # Jogador esta no primeiro quadrante em relacao ao fantasma:
        elif((player.rect.x >= self.rect.x) & (player.rect.y < self.rect.y)):
            self.currentState = self.automato.move(self.currentState, '2');

        # Jogador esta no terceiro quadrante:
        elif((player.rect.x < self.rect.x) & (player.rect.y >= self.rect.y)):
            self.currentState = self.automato.move(self.currentState, '3');

        # Jogador esta no quarto quadrante:
        elif((player.rect.x > self.rect.x) & (player.rect.y >= self.rect.y)):
            self.currentState = self.automato.move(self.currentState, '4');

    def getOpposingDir(self, direction):
        if(direction == "UP"):
            return "DOWN";
        elif(direction == "DOWN"):
            return "UP";
        elif(direction == "LEFT"):
            return "RIGHT";
        elif(direction == "RIGHT"):
            return "LEFT";

        return "";

    def randomDirection(self):
        newDir = randint(0, 3);
        if(newDir == 0):
            newDir = "UP";
        elif(newDir == 1):
            newDir = "DOWN";
        elif(newDir == 2):
            newDir = "LEFT";
        elif(newDir == 3):
            newDir = "RIGHT";

        return newDir;

    def availableDirections(self, maze):
        direction = [];

        rect = self.surface.get_rect();
        rect.x = self.rect.x;
        rect.y = self.rect.y;

        # Check UP:
        rect.y -= self.speed;
        able = True;
        for wall in maze.walls:
            if(rect.colliderect(wall)):
                able = False;

        if(able == True):
            direction.append("UP");

        # Check DOWN:
        rect.y = self.rect.y;
        rect.y += self.speed;
        able = True;
        for wall in maze.walls:
            if(rect.colliderect(wall)):
                able = False;

        if(able == True):
            direction.append("DOWN");

        # Check LEFT:
        rect.y = self.rect.y;
        rect.x -= self.speed;
        able = True;
        for wall in maze.walls:
            if(rect.colliderect(wall)):
                able = False;

        if(able == True):
            direction.append("LEFT");

        # Check RIGHT:
        rect.y = self.rect.y;
        rect.x = self.rect.x;
        rect.x -= self.speed;
        able = True;
        for wall in maze.walls:
            if(rect.colliderect(wall)):
                able = False;

        if(able == True):
            direction.append("RIGHT");

        return direction;

# O fantasma vermelho tentara seguir o pacman, automato 'perseguidor.jff':
class RedGhost(Ghost):
    def __init__(self, x, y, speed):
        Ghost.__init__(self, x, y, speed, "gr");
        self.priority = []; # Prioridade de direcoes.

        # Carrega o automato para controle de movimento:
        self.automato.load("../Pacman/automatos/perseguidor.jff");
        self.currentState = self.automato.initial();
        print("Fantasma vermelho:");
        print(self.automato);

    def update(self, player, maze):
        # Determina a prioridade de movimento de acordo om o estado atual:
        if(len(self.priority) == 0):
            self.getPriorities(player);
            if(self.currentState == 2):
                self.priority.append("UP");
                self.priority.append("LEFT");
            elif(self.currentState == 3):
                self.priority.append("UP");
                self.priority.append("RIGHT");
            elif(self.currentState == 4):
                self.priority.append("DOWN");
                self.priority.append("LEFT");
            elif(self.currentState == 5):
                self.priority.append("DOWN");
                self.priority.append("RIGHT");

        # Pega lista de movimentos possiveis:
        able = self.availableDirections(maze);

        # Escolhe uma direcao da lista de prioridades:
        prior = False;  # Indica se escolheu uma direcao das prioridades.
        for priority in self.priority:
            if(priority in able):
                self.direction = priority;
                self.priority.pop(self.priority.index(priority));
                prior = True;
                break;

        # Caso nao haja uma direcao favoravel, escolha outra aleatoria.
        # Pega nova direcao aleatoria:
        if((prior == False) & ((self.blocked != "") | (len(able) > 2))):
            newDir = self.randomDirection();

            while(newDir == self.blocked) & (newDir == self.getOpposingDir(self.blocked)):
                newDir = self.randomDirection();

            self.direction = newDir;
            self.blocked = "";
                    
        MovingObject.update(self, maze);

# O fantasma laranja tentara fujir do pacman, automato 'medroso.jff':
class OrangeGhost(Ghost):
    def __init__(self, x, y, speed):
        Ghost.__init__(self, x, y, speed, "go");
        self.priority = []; # Prioridade de direcoes.

        # Carrega o automato para controle de movimento:
        self.automato.load("../Pacman/automatos/medroso.jff");
        self.currentState = self.automato.initial();

    def update(self, player, maze):
        # Determina a prioridade de movimento de acordo om o estado atual:
        if(len(self.priority) == 0):
            self.getPriorities(player);
            if(self.currentState == 2):
                self.priority.append("UP");
                self.priority.append("LEFT");
            elif(self.currentState == 3):
                self.priority.append("UP");
                self.priority.append("RIGHT");
            elif(self.currentState == 4):
                self.priority.append("DOWN");
                self.priority.append("LEFT");
            elif(self.currentState == 5):
                self.priority.append("DOWN");
                self.priority.append("RIGHT");

        # Pega lista de movimentos possiveis:
        able = self.availableDirections(maze);

        # Escolhe uma direcao da lista de prioridades:
        prior = False;  # Indica se escolheu uma direcao das prioridades.
        for priority in self.priority:
            if(priority in able):
                self.direction = priority;
                self.priority.pop(self.priority.index(priority));
                prior = True;
                break;

        # Caso nao haja uma direcao favoravel, escolha outra aleatoria.
        # Pega nova direcao aleatoria:
        if((prior == False) & ((self.blocked != "") | (len(able) > 2))):
            newDir = self.randomDirection();

            while(newDir == self.blocked) & (newDir == self.getOpposingDir(self.blocked)):
                newDir = self.randomDirection();

            self.direction = newDir;
            self.blocked = "";
                    
        MovingObject.update(self, maze);

# O fantasma rosa anda em circulo sempre que possivel, automato 'circulo.jff':
class PinkGhost(Ghost):
    def __init__(self, x, y, speed):
        Ghost.__init__(self, x, y, speed, "gp");

        # Carrega o automato para controle de movimento:
        self.automato.load("../Pacman/automatos/circulo.jff");
        self.currentState = self.automato.initial();

        # Direcao inicial: 
        self.direction = "UP";

    def update(self, maze):
        # Se o fantasma encontrou uma parede
        # o fantasma recebe um sinal com a direcao em que foi bloqueado:
        if(self.blocked != ""):
            if(self.blocked == "UP"):
                self.currentState = self.automato.move(self.currentState, 'u');
                self.blocked = "";
            elif(self.blocked == "DOWN"):
                self.currentState = self.automato.move(self.currentState, 'd');
                self.blocked = "";
            elif(self.blocked == "LEFT"):
                self.currentState = self.automato.move(self.currentState, 'l');
                self.blocked = "";
            elif(self.blocked == "RIGHT"):
                self.currentState = self.automato.move(self.currentState, 'r');
                self.blocked = "";

        # Determina a nova direcao de acordo com o estado atual:
        if(self.currentState == 2):
            self.direction = "RIGHT";
        elif(self.currentState == 3):
            self.direction = "DOWN";
        elif(self.currentState == 4):
            self.direction = "LEFT";
        elif(self.currentState == 5):
            self.direction = "UP";

        # Atualiza a posicao do fantasma:
        MovingObject.update(self, maze);
             
# O fantasma azul anda aleatoriamente pelo labirinto, automato 'aleatorio.jff':
class BlueGhost(Ghost):
    def __init__(self, x, y, speed):
        Ghost.__init__(self, x, y, speed, "gb");

        # Carrega o automato para controle de movimento:
        self.automato.load("../Pacman/automatos/aleatorio.jff");
        self.currentState = self.automato.initial();

        # Direcao inicial: 
        self.direction = "UP";

    def update(self, maze):
        # Procura por movimentos disponiveis: 
        able = self.availableDirections(maze);

        # Se houver mais de dois movimentos,
        # o fantasma encontrou uma encruzilhada ou uma parede
        # o fantasma recebe um sinal 'e' para procurar uma nova direcao:
        if((self.blocked != "") | (len(able) > 2)):
            self.currentState = self.automato.move(self.currentState, 'e');
        
        # Caso contrario, o fantasma esta livre para mover:
        else:
            self.currentState = self.automato.move(self.currentState, 'l');

        # Pega nova direcao aleatoria:
        if(self.currentState == 3):
            newDir = self.randomDirection();

            while(newDir == self.blocked) & (newDir == self.getOpposingDir(self.blocked)):
                newDir = self.randomDirection();

            self.direction = newDir;
            self.blocked = "";
             
        # Atualiza a posicao do fantasma:
        MovingObject.update(self, maze);