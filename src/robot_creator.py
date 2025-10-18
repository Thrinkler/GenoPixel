import random
import pygame

from . import robot
from . import food
from . import create_files
from . import food_sorter

from .settings import *

class Creator:
    def __init__(self, numRobots, numFoods):
        self.file,self.snapshot = create_files.new_file()

        self.F = [food.Food(random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT),pygame.Color(0,255,0)) for _ in range(numFoods)]
        self.dic_F = food_sorter.FoodSorter(self.F)

        self.P = []
        for i in range(ROBOT_FIRST_SPECIES_COUNT):
            self.robot_species(numRobots//ROBOT_FIRST_SPECIES_COUNT)

        self.mutation_rate = MUTATION_RATE

        self.avg_velocity = 0
        self.avg_rot_vel = 0
        self.avg_vision = 0
        self.avg_fail_rot = 0
    

    def robot_species(self, n):
        species_vel =random.uniform(MIN_FIRST_VELOCITY,MAX_FIRST_VELOCITY)
        species_rot_vel = random.uniform(MIN_FIRST_ROT_VELOCITY,MAX_FIRST_ROT_VELOCITY)
        species_vision = random.randint(MIN_FIRST_VISION,MAX_FIRST_VISION)
        species_prob_fail_rot = random.randint(MIN_FIRST_FAIL_ROT,MAX_FIRST_FAIL_ROT)
        species_life = random.randint(MIN_LIFE,MAX_LIFE)

        self.P += [robot.Robot(i+len(self.P),random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT), self.F, self.dic_F, \
                    velocity=species_vel,
                    rot_vel=species_rot_vel,
                    vision=species_vision,
                    prob_fail_rot=species_prob_fail_rot,
                    life=species_life)
                    for i in range(n)]
                


    def update(self):

        self.avg_velocity = self.avg_velocity/len(self.P) if len(self.P) > 0 else 0
        self.avg_rot_vel = self.avg_rot_vel/len(self.P) if len(self.P) > 0 else 0
        self.avg_vision = self.avg_vision/len(self.P) if len(self.P) > 0 else 0
        self.avg_fail_rot = self.avg_fail_rot/len(self.P) if len(self.P) > 0 else 0

        if(self.avg_velocity > 0 or self.avg_rot_vel > 0 or self.avg_vision > 0 or self.avg_fail_rot > 0):
            self.file.write(str(len(self.F))+","+ str(len(self.P))+ "," + str(self.avg_velocity) + "," + str(self.avg_rot_vel) + "," + str(self.avg_vision) + "," + str(self.avg_fail_rot) + "\n")
        self.avg_velocity = 0
        self.avg_rot_vel = 0
        self.avg_vision = 0
        self.avg_fail_rot = 0

        if random.uniform(0, 1) > 1 - FOOD_SPAWN_RATE/100:
            self.F.append(food.Food(random.randint(0,1000),random.randint(0,800),pygame.Color(0,255,0)))
            self.dic_F.add(self.F[-1])

        for f in self.F[:]:
            if f.time > f.death_time:
                self.dic_F.remove(f)
                self.F.pop(self.F.index(f))
            if f.time > f.child_time and f.can_reproduce and len(self.F) < 10000:
                self.F.append(f.gen_new())
                self.dic_F.add(self.F[-1])
                f.time = 0

        for p in self.P[:]:

            self.avg_velocity += p.velocity
            self.avg_rot_vel += p.rot_vel
            self.avg_vision += p.vision
            self.avg_fail_rot += p.prob_fail_rot
            p.update()
            
            if p.food_eaten >= p.food_to_reproduce:
                self.P.append(robot.Robot(p.id,p.rect.x,p.rect.y, self.F,self.dic_F,\
                        velocity=p.velocity+(random.uniform(-1,1) if random.randint(0,10)< self.mutation_rate*10 else 0),\
                        rot_vel=p.rot_vel+(random.uniform(-1,1) if random.randint(0,10)< self.mutation_rate*10 else 0),\
                        vision=p.vision+(random.randint(-10,10) if random.randint(0,10)< self.mutation_rate*10 else 0), \
                        prob_fail_rot=p.prob_fail_rot+(random.randint(-10,10) if random.randint(0,10)< self.mutation_rate*10 else 0),\
                            life=random.randint(MIN_LIFE,MAX_LIFE)))

                p.food_eaten = 0
                p.food_to_reproduce += random.randint(2,5)

            if p.timeout:
                self.P.pop(self.P.index(p))
        

    def draw(self,surface, time = 0,camera_offset=[0,0,False]):
        self.update()
        for p in self.P:
            if(camera_offset[2]):
                s =[p.velocity,p.rot_vel,p.vision,p.prob_fail_rot]
                self.snapshot.write(str(time)+","+",".join([str(x) for x in s]) + "\n")
            p.draw(surface, camera_offset)
        for f in self.F:
            f.draw(surface, camera_offset)
        