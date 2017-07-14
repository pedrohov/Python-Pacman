# Disciplina : Linguagens Formais e Automatos
# Aluno      : Pedro Henrique Oliveira Veloso
# Matricula  : 0002346

import pygame as pygame;

class Wall:
    def __init__(self, x, y, name):
        self.sprite     = "images/block_" + name + ".png";
        self.surface    = pygame.image.load(self.sprite);
        self.rect       = self.surface.get_rect();
        self.rect.x     = x;
        self.rect.y     = y;

class Dot:
    def __init__(self, x, y):
        self.sprite     = "images/dot.png";
        self.surface    = pygame.image.load(self.sprite);
        self.rect       = self.surface.get_rect();
        self.rect.x     = x;
        self.rect.y     = y;
        self.points     = 10;

class Maze:
    def __init__(self):
        self.grid = [
            ["D" , "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],
            ["R" ,  2 , "R",  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 , "L",  2 ,  2 ,  2 ,  2 ,  2 ,  2 ,  2 , "R",  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 , "L",  2 , "L"],
            ["R" , "D","DR",  0 ,"CL","UD","TD","UD","CR",  0 ,"DL", "D", "D", "D", "D", "D", "D", "D","DR",  0 ,"CL","UD","TD","UD","CR",  0 ,"DL", "D", "L"],
            ["R" ,  0 ,  0 ,  0 ,  0 ,  0 ,"LR",  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,"LR",  0 ,  0 ,  0 ,  0 ,  0 , "L"],
            ["R" ,  0 ,"CL","UD","C4",  0 ,"CD",  0 ,"C3","UD","CR",  0 ,"CL","CR",  0 ,"CL","CR",  0 ,"CL","UD","C4",  0 ,"CD",  0 ,"C3","UD","CR",  0 , "L"],
            ["R" ,  0 ,  0 ,  0 ,"LR",  0 ,  0 ,  0 ,"LR",  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,"LR",  0 ,  0 ,  0 ,"LR",  0 ,  0 ,  0 , "L"],
            ["R" , "U","UR",  0 ,"CD",  0 ,"CU",  0 ,"CD",  0 , "C",  0 ,"UL","U2",  2 ,"U1","UR",  0 , "C",  0 ,"CD",  0 ,"CU",  0 ,"CD",  0 ,"UL", "U", "L"],
            ["R" ,  2 , "R",  0 ,  0 ,  0 ,"LR",  0 ,  0 ,  0 ,  0 ,  0 , "L",  2 ,  2 ,  2 , "R",  0 ,  0 ,  0 ,  0 ,  0 ,"LR",  0 ,  0 ,  0 , "L",  2 , "L"],
            ["R" , "D","DR",  0 ,"CU",  0 ,"CD",  0 ,"CU",  0 , "C",  0 ,"DL", "D", "D", "D","DR",  0 , "C",  0 ,"CU",  0 ,"CD",  0 ,"CU",  0 ,"DL", "D", "L"],
            ["R" ,  0 ,  0 ,  0 ,"LR",  0 ,  0 ,  0 ,"LR",  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,"LR",  0 ,  0 ,  0 ,"LR",  0 ,  0 ,  0 , "L"],
            ["R" ,  0 ,"CL","UD","C1",  0 ,"CU",  0 ,"C2","UD","CR",  0 ,"CL","CR",  0 ,"CL","CR",  0 ,"CL","UD","C1",  0 ,"CU",  0 ,"C2","UD","CR",  0 , "L"],
            ["R" ,  0 ,  0 ,  0 ,  0 ,  0 ,"LR",  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,"LR",  0 ,  0 ,  0 ,  0 ,  0 , "L"],
            ["R" , "U","UR",  0 ,"CL","UD","TU","UD","CR",  0 ,"UL", "U", "U", "U", "U", "U", "U", "U", "UR", 0 ,"CL","UD","TU","UD","CR",  0 ,"UL", "U", "L"],
            ["R" ,  2 , "R",  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 , "L",  2 ,  2 ,  2 ,  2 ,  2 ,  2 ,  2 , "R",  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 , "L",  2 , "L"],
            ["U" , "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U", "U"]
        ];

        self.rows = 15;
        self.cols = 29;

        self.playerIniX = 105;
        self.playerIniY = 35;

        self.ghostIniX  = 490;
        self.ghostIniY  = 245;

        self.walls      = [];
        self.dots       = [];
        self.totalDots  = 0;

    def reset_maze(self):
        # Coloca todas as dots novamente:
        x = 0;
        y = 0;

        for i in range(0, self.rows):
            for j in range(0, self.cols):
                if(self.grid[i][j] == 0):
                    self.dots.append(Dot(x + 12.5, y + 12.5));
                    self.totalDots += 1;
                x += 35;

            x = 0;
            y += 35;

    def create_maze(self):
        x = 0;
        y = 0;

        for i in range(0, self.rows):
            for j in range(0, self.cols):
                if(self.grid[i][j] == "C"):
                    self.walls.append(Wall(x, y, "CLOSED"));
                    x += 35;
                elif(self.grid[i][j] == "CL"):
                    self.walls.append(Wall(x, y, "CLOSEDL"));
                    x += 35;
                elif(self.grid[i][j] == "CR"):
                    self.walls.append(Wall(x, y, "CLOSEDR"));
                    x += 35;
                elif(self.grid[i][j] == "CU"):
                    self.walls.append(Wall(x, y, "CLOSEDU"));
                    x += 35;
                elif(self.grid[i][j] == "CD"):
                    self.walls.append(Wall(x, y, "CLOSEDD"));
                    x += 35;
                elif(self.grid[i][j] == "C1"):
                    self.walls.append(Wall(x, y, "C1"));
                    x += 35;
                elif(self.grid[i][j] == "C2"):
                    self.walls.append(Wall(x, y, "C2"));
                    x += 35;
                elif(self.grid[i][j] == "C3"):
                    self.walls.append(Wall(x, y, "C3"));
                    x += 35;
                elif(self.grid[i][j] == "C4"):
                    self.walls.append(Wall(x, y, "C4"));
                    x += 35;
                elif(self.grid[i][j] == "TD"):
                    self.walls.append(Wall(x, y, "TD"));
                    x += 35;
                elif(self.grid[i][j] == "TU"):
                    self.walls.append(Wall(x, y, "TU"));
                    x += 35;
                if(self.grid[i][j] == "D"):
                    self.walls.append(Wall(x, y, "DOWN"));
                    x += 35;
                elif(self.grid[i][j] == "U"):
                    self.walls.append(Wall(x, y, "UP"));
                    x += 35;
                elif(self.grid[i][j] == "U1"):
                    self.walls.append(Wall(x, y, "U1"));
                    x += 35;
                elif(self.grid[i][j] == "U2"):
                    self.walls.append(Wall(x, y, "U2"));
                    x += 35;
                elif(self.grid[i][j] == "L"):
                    self.walls.append(Wall(x, y, "LEFT"));
                    x += 35;
                elif(self.grid[i][j] == "R"):
                    self.walls.append(Wall(x, y, "RIGHT"));
                    x += 35;
                elif(self.grid[i][j] == "DR"):
                    self.walls.append(Wall(x, y, "DOWNRIGHT"));
                    x += 35;
                elif(self.grid[i][j] == "DL"):
                    self.walls.append(Wall(x, y, "DOWNLEFT"));
                    x += 35;
                elif(self.grid[i][j] == "UR"):
                    self.walls.append(Wall(x, y, "UPRIGHT"));
                    x += 35;
                elif(self.grid[i][j] == "UL"):
                    self.walls.append(Wall(x, y, "UPLEFT"));
                    x += 35;
                elif(self.grid[i][j] == "UD"):
                    self.walls.append(Wall(x, y, "UPDOWN"));
                    x += 35;
                elif(self.grid[i][j] == "LR"):
                    self.walls.append(Wall(x, y, "LEFTRIGHT"));
                    x += 35;
                elif(self.grid[i][j] == 1):
                    self.walls.append(Wall(x, y, ""));
                    x += 35;
                elif(self.grid[i][j] == 0):
                    self.dots.append(Dot(x + 12.5, y + 12.5));
                    self.totalDots += 1;
                    x += 35;
                elif(self.grid[i][j] == 2):
                    x += 35;

            # Atualiza as coordenadas:
            x = 0;
            y += 35;

    def draw_maze(self, screen):
        for i in self.walls:
            screen.blit(i.surface, (i.rect.x, i.rect.y)); 

        for i in self.dots:
            screen.blit(i.surface, (i.rect.x, i.rect.y)); 