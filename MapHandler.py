import numpy as np
import os
import GraphicsController as GC

class World:

    def __init__(self, SaveFolder, ChunkSize = 5):
        self.SaveFolder = SaveFolder
        self.ChunkSize = ChunkSize

    def GetChunk(self, Pos):
        FileName = "Chunk_{}~{}.cf".format(*Pos)
        #print(FileName)
        
        if os.path.exists(FileName):
            Chunk = []
            with open(FileName,"r") as C:
                Row = C.readline()
                while Row:
                    Chunk.append(list(Row.strip("\n")))
                    Row = C.readline()
            return Chunk
                    
        else:
            C = self.GenerateChunk(Pos)
            self.SaveChunk(C,Pos)
            return C
    
    def SaveChunk(self, Chunk, Pos):
        FileName = "Chunk_{}~{}.cf".format(*Pos)
        with open(FileName,"w") as C:
            for Row in Chunk:
                C.write("".join(Row)+"\n")

    def GenerateChunk(self, Pos):
        Generator = GC.Renderer((self.ChunkSize,self.ChunkSize))

        for i in range(self.ChunkSize):
            for j in range(self.ChunkSize):
                Generator.DrawSprite([str(i+j) if i+j < 30 else " "],(i,j))
                
        return Generator.FrameBuffer
    
        print("Generated")

    def GetRegion(self,Pos):
        CurChunk = [Pos[0]//self.ChunkSize,Pos[1]//self.ChunkSize]

        #print(CurChunk)
        
        Chunks = []
        for y in range(-1,2):
            for x in range(-1,2):
                Chunks.append(self.GetChunk((CurChunk[0]+x,CurChunk[1]+y)))

        View = np.hstack(np.hstack(np.reshape(Chunks,(3,3,self.ChunkSize,self.ChunkSize))))


        ViewOffset = ((CurChunk[0]-1)*self.ChunkSize,(CurChunk[1]-1)*self.ChunkSize)
        
        return ViewOffset, View
                    

        

if __name__ == "__main__":
    A = World("Test")
    B = GC.Renderer((50,50))

    A.SaveChunk([["A"," "],[" "," "]],(-1,-1))

    #for y in range(1,-2,-1):
        #for x in range(-1,2):
            #A.SaveChunk(B.FrameBuffer,(x,y))

    B.DrawSprite(A.GetRegion((0,0)),(10,10))
    B.DrawScreen()
