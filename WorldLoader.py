import numpy as np
import os
import pickle

import Entity

class MapLoader:

    def __init__(self, saveFolder, chunkSize = 200, loadRange = 100):
        
        self.saveFolder = saveFolder
        self.chunkSize = chunkSize
        self.loadRange = loadRange
        
        self.currentEntities = []
        self.savedChunks = None

    def getEntities(self, pos):
        chunkPos = [pos[0]//self.chunkSize,pos[1]//self.chunkSize]
        
        chunkPath = self.saveFolder+"\\World\\Chunk_{}~{}".format(*chunkPos)
        
        entities = []
        
        if not os.path.exists(chunkPath):
            self.generateChunk(pos)
        
        for file in os.listdir(chunkPath+"\\Entities"):
            if file.endswith("pkl"):
                with open(chunkPath+"\\Entities\\"+file,"rb") as entity:
                    entities.append(pickle.load(entity))
        
        return entities

    def getChunk(self, pos):
        chunkPos = [pos[0]//self.chunkSize,pos[1]//self.chunkSize]
        
        chunkPath = self.saveFolder+"\\World\\Chunk_{}~{}.pkl".format(*chunkPos)
        
        if not os.path.exists(chunkPath):
            self.generateChunk(pos)

        with open(chunkPath, "rb") as file:
            chunk = pickle.load(file)
        
        return chunk

    def saveChunk(self, chunk):
        chunkPath = self.saveFolder+"\\World\\Chunk_{}~{}.pkl".format(*chunk.location)

        with open(chunkPath,"wb") as file:
            pickle.dump(chunk, file, protocol = pickle.HIGHEST_PROTOCOL)

    def getChunks(self, pos):
        chunkPos = (pos[0]//self.chunkSize,pos[1]//self.chunkSize)

        topLeft = [float("inf"),float("inf")]

        nearChunks = []
        
        for y in range(-1,2):
            for x in range(-1,2):
                chunkX = (chunkPos[0]+x)*self.chunkSize
                chunkY = (chunkPos[1]+y)*self.chunkSize
                
                deltaX = pos[0] - max(chunkX, min(pos[0], chunkX + self.chunkSize))
                deltaY = pos[1] - max(chunkY, min(pos[1], chunkY + self.chunkSize))

                if (deltaX**2 + deltaY**2) < (self.loadRange**2):
                    
                    nearChunks.append(self.getChunk((chunkX,chunkY)))
                    topLeft[0] = min(topLeft[0],chunkX)
                    topLeft[1] = min(topLeft[1],chunkY)

        chunkEntities = [chunk.entities for chunk in nearChunks]
        allEntities = []
        for entities in chunkEntities:
            allEntities.extend(entities)
                
        return allEntities, topLeft
        
    def saveEntities(self, entities, pos):
        chunkPath = self.saveFolder+"\\World\\Chunk_{}~{}".format(*[pos[0]//self.chunkSize,pos[1]//self.chunkSize])
        
        for entity in entities:
            with open(chunkPath+entity.fileName+".pkl","wb") as file:
                pickle.dump(entity, file, protocol = pickle.HIGHEST_PROTOCOL)

    
    def generateChunk(self, pos):
        chunkPos = [pos[0]//self.chunkSize,pos[1]//self.chunkSize]

        chunkPath = self.saveFolder+"\\World\\Chunk_{}~{}.pkl".format(*chunkPos)


        if os.path.exists(chunkPath):
            return
        else:
            with open(chunkPath, "wb") as file:
                self.saveChunk(Chunk(chunkPos,[Entity.Entity("Test",pos,[[65,65,65],[65,65,65]])]))
            

        #entities = [Entity.Entity("TestEntity",(chunkPos[0]*self.chunkSize,chunkPos[1]*self.chunkSize),[[65,65],[65,65]])]
        
        #for entity in entities:
            #with open(chunkPath+"\\Entities\\"+entity.fileName+".pkl","wb") as file:
                #pickle.dump(entity, file, protocol = pickle.HIGHEST_PROTOCOL)




class Chunk:

    def __init__(self, location, entities = []):

        self.location = location
        self.entities = entities

    def addEntities(self, entities):

        self.entities.extend(entities)

    def removeEntities(self, entities):

        for entity in entities:
            if entity in self.entities:
                del self.entities[self.entities.index(entity)]




      
