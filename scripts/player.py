# Disciplina : Linguagens Formais e Automatos
# Aluno      : Pedro Henrique Oliveira Veloso
# Matricula  : 0002346

from movingobject import *;

class Player(MovingObject):
    def __init__(self, speed, name):
        # Instancia um novo objeto movel:
        MovingObject.__init__(self, speed, name);

        # Pontuacao:
        self.score = 0;

        # Animacoes:
        self.upAnim     = ["images/" + name + "_c.png", "images/" + name + "_u1.png", "images/" + name + "_u2.png"];
        self.downAnim   = ["images/" + name + "_c.png", "images/" + name + "_d1.png", "images/" + name + "_d2.png"];
        self.leftAnim   = ["images/" + name + "_c.png", "images/" + name + "_l1.png", "images/" + name + "_l2.png"];
        self.rightAnim  = ["images/" + name + "_c.png", "images/" + name + "_r1.png", "images/" + name + "_r2.png"];

        # Carrega o automato para controle de movimento:
        self.automato.load("../Pacman/automatos/pacman.jff");
        self.currentState = self.automato.initial();

    def getDots(self, maze):
        # Coletar dots:
        for dot in maze.dots:
            if(self.rect.colliderect(dot.rect)):
                self.score += dot.points;
                maze.totalDots -= 1;
                maze.dots.pop(maze.dots.index(dot));
                break;

    def update(self, maze):
        # Determina a direcao de acordo com o estado atual:
        if(self.currentState == None):
            self.direction = "";
        elif(self.currentState == 2):
            self.direction = "UP";
        elif(self.currentState == 3):
            self.direction = "RIGHT";
        elif(self.currentState == 4):
            self.direction = "DOWN";
        elif(self.currentState == 5):
            self.direction = "LEFT";

        MovingObject.update(self, maze);
        self.getDots(maze);