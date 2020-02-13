import numpy as np
import Entity
import timeit

#where K = 1; M = 0.058; m = 0.045; V = 40, v = -50
#x = (sqrt(-m M ((m v + M V)^2 - 2 K (m + M))) + m M v + M^2 V)/(M (m + M))
# solve K = M*x^2/2 + m/2 * ((M/m)*(V-x)+v)^2

def normalize(vector):
    if not vector.any():
        raise ValueError("Cannot normalize vector equal to 0")
    return vector / np.sqrt(np.einsum('...i,...i', vector, vector))

def compareVecs(vectorA, vectorB):
    return np.dot(normalize(vectorA), normalize(vectorB))

def magnitude(vector):
    return np.sqrt(vector.dot(vector))

def onLine(point, line):
    
    if ((not point[0] <= max(line[0][0], line[1][0])) or
        (not point[0] >= min(line[0][0], line[1][0])) or
        (not point[1] <= max(line[0][1], line[1][1])) or
        (not point[1] >= min(line[0][1], line[1][1]))):
        
        return False

    return True

def orientation(pointA, pointB, pointC):
    return (pointB[1] - pointA[1]) * (pointC[0] - pointB[0]) - (pointB[0] - pointA[0]) * (pointC[1] - pointB[1])

def linesIntersect(lineA, lineB):

    o1 = orientation(lineA[0], lineA[1], lineB[0])
    o2 = orientation(lineA[0], lineA[1], lineB[1])
    o3 = orientation(lineB[0], lineB[1], lineA[0])
    o4 = orientation(lineB[0], lineB[1], lineA[1])

    if o1 != o2 and o3 != o4:
        return True
    elif o1 == 0 and onLine(lineB[0], lineA):
        return True
    elif o2 == 0 and onLine(lineB[1], lineA):
        return True
    elif o3 == 0 and onLine(lineA[0], lineB):
        return True
    elif o4 == 0 and onLine(lineA[1], lineB):
        return True

    return False

def raycastCollisionExists(entityA, entityB):
    ray = np.array((entityA.physicsPos, np.add(entityA.physicsPos,entityA.vel)))
    print("ray:",ray)

    position = entityB.physicsPos
    size = np.subtract(entityB.sprite.shape, 1)

    print("B:",size,position)

    bounds = [np.array((position, (position[0] + size[0], position[1]))), # upper bound
              np.array((position, (position[0], position[1] + size[1]))), # left bound
              np.array(((position[0], position[1] + size[1]), (position[0] + size[0], position[1] + size[1]))), # lower bound
              np.array(((position[0] + size[0], position[1]), (position[0] + size[0], position[1] + size[1])))] # right bound

    for bound in bounds:
        print("bound:",bound)
        if linesIntersect(bound, ray):
            print("intersects")
            return True

    return False
    
def checkEntityCollision(entityA,entityB):

    boundsIntersect = (entityA.physicsPos[0] < entityB.physicsPos[0] + entityB.sprite.shape[0] and
                       entityA.physicsPos[0] + entityA.sprite.shape[0] > entityB.physicsPos[0] and
                       entityA.physicsPos[1] < entityB.physicsPos[1] + entityB.sprite.shape[1] and
                       entityA.physicsPos[1] + entityA.sprite.shape[1] > entityB.physicsPos[1])

    
    if boundsIntersect and (entityA.vel.any() or entityB.vel.any()):
        
        # Because their bounding boxes are already colliding, the velocity of the faster entity will control whether they collide.
        # Draw a test vector from the faster entities position to the slower one. If the faster entities velocity is pointing closer than
        # perpendicular to the test vector and is greater or equal in magnitude to the test vector, the objects are colliding.
        
        if magnitude(entityA.vel) >= magnitude(entityB.vel):
            fastest = entityA
            slowest = entityB
        else:
            fastest = entityB
            slowest = entityA

        #minVelocity = np.subtract(slowest.pos, fastest.pos)

        # If the objects are inside each other, they must be colliding
        #if not minVelocity.any():
            #return True

        
        
        return raycastCollisionExists(fastest,slowest)
            
    return False

def calcCollision(firstEntity, secondEntity):
    
    if firstEntity.vel.any():
        entityA = firstEntity
        entityB = secondEntity
    elif secondEntity.vel.any():
        entityA = secondEntity
        entityB = firstEntity
    else:
        #raise RuntimeWarning("Attempted collision for stationary objects!")
        return

    # Calculate the kinetic energy in the system
    entityAKineticEnergy2x = np.multiply(entityA.mass,np.square(entityA.vel))
    entityBKineticEnergy2x = np.multiply(entityB.mass,np.square(entityB.vel))
    
    initialKineticEnergy = np.divide(np.add(entityAKineticEnergy2x,entityBKineticEnergy2x),2)

    # Calculate how energy will be absorbed by the two entities in the system
    tmpEntityARigidity = entityA.rigidity
    tmpEntityBRigidity = entityB.rigidity
    
    totalRigidity = tmpEntityARigidity + tmpEntityBRigidity

    if totalRigidity > 1:
        tmpEntityARigidity /= totalRigidity
        tmpEntityBRigidity /= totalRigidity

    # Calculate what the ending kinetic energy of the system will be after the collision
    finalKineticEnergy = np.multiply(initialKineticEnergy,(1 - tmpEntityARigidity - tmpEntityBRigidity))

    totalMomentum = np.add(np.multiply(entityA.mass, entityA.vel), np.multiply(entityB.mass, entityB.vel))
    totalMass = entityA.mass + entityB.mass

    # Check what kind of collision this is based on final KE
    if not finalKineticEnergy.any():
        
        # Calculate for inelastic collision
        aSolution = np.divide(totalMomentum,totalMass)
        bSolution = aSolution

    else:
        
        # Calculate for a partially elastic collision
        quadratic = np.divide(np.sqrt(np.multiply(-1 * entityA.mass * entityB.mass, np.subtract(np.square(totalMomentum), 2*finalKineticEnergy*totalMass))), entityA.mass * totalMass)
        fraction = np.divide(totalMomentum,totalMass)

        solutionsA = [np.add(fraction, quadratic),np.subtract(fraction, quadratic)]

        if magnitude(np.subtract(entityA.vel,solutionsA[0])) > magnitude(np.subtract(entityA.vel,solutionsA[1])):
            aSolution = solutionsA[0]
        else: 
            aSolution = solutionsA[1]
        
        #print("KE",finalKineticEnergy)
        #print("total momentum:",totalMomentum)
        #print("quadratic",quadratic)
        #print("EA:",entityA.vel)
        #print("sols:",solutionsA)
        #print(magnitude(np.subtract(entityA.vel,solutionsA[0])))
        #print(magnitude(np.subtract(entityA.vel,solutionsA[1])))
        #raise RuntimeError("Failed to compute collision for entities")

        bSolution = np.divide(np.subtract(totalMomentum,np.multiply(entityA.mass,aSolution)),entityB.mass)

    # Update entities accordingly
    
    
    entityA.absorbEnergy(tmpEntityARigidity * initialKineticEnergy)
    entityA.applyAcc(np.subtract(aSolution,entityA.vel))

    entityB.absorbEnergy(tmpEntityBRigidity * initialKineticEnergy)
    entityB.applyAcc(np.subtract(bSolution,entityB.vel))




def testCollision():
    A = Entity.Entity("A",(0,0),["A"],1)
    B = Entity.Entity("B",(1,0),["B"],1)

    A.vel = np.array([0,0])
    B.vel = np.array([-0.015,0])

    A.rigidity = 0
    B.rigidity = 0

    calcCollision(A,B)

    A.updatePhysics()
    B.updatePhysics()

    print(A.vel)
    print(B.vel)

def testRaycast():
    A = Entity.Entity("A",(0,0),np.array([["A","A"]]),1)
    B = Entity.Entity("B",(2,0),np.array([["B"]]),1)

    A.vel = np.array([0,0])
    B.vel = np.array([-1,1])

    print(raycastCollisionExists(B,A))

