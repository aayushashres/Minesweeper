from os import getcwd
import random
path=os.getcwd()

SIZE=10
MINES=9

images={} #blank dictioanryto later store images
defaultImageSize = 52

class Tile():
    def __init__(self,r,c,v,s):
        self.r=r
        self.c=c
        self.v=v
        self.s=s
        self.imgsize=defaultImageSize
        
    def display(self):
        if self.s=="H": #H is hidden, U is uncovered
            #display the tile or hidden unless "H" has been switched to "U"
            image(images["H"], self.r*self.imgsize,self.c*self.imgsize)
        else:
            image(images[self.v], self.r*self.imgsize,self.c*self.imgsize)
            
    
            
        
        
        
class Minesweeper():
    def __init__(self,n,m):
        self.n=n
        self.m=m 
        self.board=[]
        self.gamestate="play"
        self.createboard()
        
    def createboard(self):
        for r in range(self.n):
            for c in range(self.n):
                self.board.append(Tile(r,c,0,"H")) #all tiles are hidden, default val=0 as no bombs assigned
                    
        bombcount=0
    
        while bombcount<self.m: #condition to ensure only m bombs are placed
            bombTile = random.choice(self.board)
            
            #assigning the bombs
            if bombTile.v!="B": #checking if the random place generated doesnt already have a bomb before creating a bomb
                bombTile.v="B"
                bombcount+=1
                
                #counting the number of bombs surrounding the tiles, adding 1 when a bomb is found in a neighbouring tile
                for n in [[-1,0],[1,0],[0,1],[0,-1],[-1,-1],[-1,1],[1,-1],[1,1]]:
                    neighbortile=self.gettile(bombTile.r+n[0], bombTile.c+n[1])
                    if neighbortile!=None and neighbortile.v!="B":
                        neighbortile.v+=1
                        
                
                
    def gettile(self,r,c):
        if r >=0 and r<self.n and c>=0 and c<self.n:
            return self.board[(self.n*r)+c]
        else:
            return None #meaning tile doesnt exist, like a corner tile
                        
    
    def displayboard(self):
        if self.gamestate=="play":
            for tile in self.board:
                tile.display()
       
        elif self.gamestate=="lose":
            for tile in self.board:
                if tile.v=="B": #uncover all bombs once lost
                    tile.s="U"
                tile.display()
                
               #Showing gameover image after game is lost 
               #imageMode Center used to use x,y coordinate as center and not the corner of image
            imageMode(CENTER)
            image(images["GO"], height//2,width//2)
            imageMode(CORNER)
        
        elif self.gamestate=="win":
            
            for tile in self.board:
                #if won, display all bombs
                if tile.v=="B":
                    tile.s="U"
                tile.display()
            
    def checkwin(self):
        win = True
        for tile in self.board:
            #win condition is when all excpet bombs are uncovered
            #so if anything except a bomb is hidden, win is false
            if tile.v!="B" and tile.s=="H":
                
                win = False

                
        if win:
            self.gamestate="win"
        
            
        

            

    
    
#SIZE can be varied on line 4, size is the dimensions of the square board
#MINES is the number of bombs , can be varied      
ms=Minesweeper(SIZE,MINES)

def setup():
    #the board size will be the number of tile times number of pixels of an image
    size(SIZE*defaultImageSize,SIZE*defaultImageSize)
    background(0)
    
    for i in range(9):
        #loading images of tile with value 0(blank tile), and 1 to 8, into the dictionary
        images[i]= loadImage(path+"/images/"+str(i)+".png")
    images["B"]=loadImage(path+"/images/"+"mine.png") #"B" key in dictionary has value of bomb image, H has hidden tile, and GO has the game over image
    images["H"]=loadImage(path+"/images/"+"tile.png")
    images["GO"]=loadImage(path+"/images/"+"gameover.png")
    
    
                
def draw():
    ms.checkwin()
    ms.displayboard()
    
def mouseClicked():
    
    #condition for a new game on click after game is either lost or won
    if ms.gamestate=="win" or ms.gamestate=="lose":
        ms.__init__(SIZE,MINES)
        return
        
    
    if ms.gamestate=="play":
    
        x=mouseX//defaultImageSize
        y=mouseY//defaultImageSize
        uncover(x,y)

    
    
def uncover(x,y):
    
    clickedtile=ms.gettile(x,y)
    if clickedtile is None or clickedtile.s=="U":
        return #no action if tile doesnt exist, or is already uncovered
    elif clickedtile.v!=0:
        clickedtile.s="U"
        if clickedtile.v=="B" and ms.gamestate!="win":
            
            #lose game if clicked on bomb
            ms.gamestate="lose"
        return
    else:
        clickedtile.s="U"
        #for a blank tile, recursively calling uncover to uncover all the neighboring tiles of 
        #a blank tile
        for n in [[-1,0],[1,0],[0,1],[0,-1],[-1,-1],[-1,1],[1,-1],[1,1]]:
            uncover(clickedtile.r+n[0],clickedtile.c+n[1])
        
        return



        
    
