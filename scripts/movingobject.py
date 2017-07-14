# Disciplina : Linguagens Formais e Automatos
# Aluno      : Pedro Henrique Oliveira Veloso
# Matricula  : 0002346

from maze import *;
from AFD import *;

class MovingObject:
    def __init__(self, speed, name):
        self.name = name;
        self.speed      = speed;
        self.direction  = "";
        self.sprite     = "images/" + name + "_r1.png";
        self.set_surface();
        self.rect       = self.surface.get_rect();

        self.upAnim     = ["images/" + name + "_u1.png", "images/" + name + "_u2.png"];
        self.downAnim   = ["images/" + name + "_d1.png", "images/" + name + "_d2.png"];
        self.leftAnim   = ["images/" + name + "_l1.png", "images/" + name + "_l2.png"];
        self.rightAnim  = ["images/" + name + "_r1.png", "images/" + name + "_r2.png"];
        self.animFrame  = 0;

        self.blocked    = "";

        # Automato que define o movimento do objeto:
        self.automato     = AFD();
        self.currentState = None; 

    def animate(self):
        if(self.direction == "UP"):
            self.sprite = self.upAnim[self.animFrame];
        elif(self.direction == "DOWN"):
            self.sprite = self.downAnim[self.animFrame];
        elif(self.direction == "LEFT"):
            self.sprite = self.leftAnim[self.animFrame];
        elif(self.direction == "RIGHT"):
            self.sprite = self.rightAnim[self.animFrame];

        self.set_surface();

    def set_surface(self):
        self.surface = pygame.image.load(self.sprite);

    def nextPos(self):
        rect = self.surface.get_rect();
        rect.x = self.rect.x;
        rect.y = self.rect.y;

        if(self.direction == "UP"):
            rect.y -= self.speed;
        elif(self.direction == "DOWN"):
            rect.y += self.speed;
        elif(self.direction == "LEFT"):
            rect.x -= self.speed;
        elif(self.direction == "RIGHT"):
            rect.x += self.speed;

        return rect;

    def update(self, maze):
        # Determina se havera colisao na proxima posicao:
        prect = self.nextPos();
        if(self.blocked == ""):
            for wall in maze.walls:
                if (prect.colliderect(wall)):
                    self.blocked = self.direction;

        # Movimenta:
        if(self.direction != self.blocked) & (self.direction == "UP"):
            self.rect.move_ip(0, -self.speed);
            self.blocked = "";
        elif(self.direction != self.blocked) & (self.direction == "DOWN"):
            self.rect.move_ip(0, self.speed);
            self.blocked = "";
        elif(self.direction != self.blocked) & (self.direction == "LEFT"):
            self.rect.move_ip(-self.speed, 0);
            self.blocked = "";
        elif(self.direction != self.blocked) & (self.direction == "RIGHT"):
            self.rect.move_ip(self.speed, 0);
            self.blocked = "";

        # Se nao houver colisao, anime o sprite:
        if(self.blocked == ""):
            self.animate();

            self.animFrame = self.animFrame + 1;
            if(self.animFrame >= len(self.upAnim)):
                self.animFrame = 0;

    def set_coord(self, x, y):
        self.rect.x = x;
        self.rect.y = y;