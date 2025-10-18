import pygame
import math
import random

from .settings import *

from . import food
from . import food_sorter

class Robot(pygame.sprite.Sprite):
    def __init__(self, id: int,x:int,y:int, food:list[food.Food],dict_food: food_sorter.FoodSorter, velocity=2.0, rot_vel=2.0, vision = 80, life = 500, prob_fail_rot =70) -> None:
        super().__init__() 
        self.id = id
        self.rect = pygame.Rect(x,y,ROBOTS_SIZE,ROBOTS_SIZE)
        self.color = pygame.Color(((50+int(abs(velocity)*20) if abs(velocity)*20 < 200 else 255),\
                                   (vision) if vision < 250 else 255,\
                                   (50+int(abs(rot_vel)*20) if abs(rot_vel)*20 < 200 else 255)))

        self.food = food
        self.dict_food = dict_food

        self.angle = random.uniform(0,2*math.pi)
        
        self.velocity = velocity
        self.rot_vel = rot_vel
        self.life = life
        self.vision = vision
        self.prob_fail_rot = prob_fail_rot

        self.timeout = False

        self.target_food = None

        self.food_eaten = 0
        self.food_to_reproduce = random.randint(2,5)



        self.food_to_reproduce = random.randint(2,5)
    
    
    def vector_to_food(self, food: food.Food):
        if food is None:
            return [random.randint(-1,1),random.randint(-1,1)]
        return [food.rect.x - self.rect.x, food.rect.y - self.rect.y]

    def find_closest_food(self,food_list: list[food.Food]):
        if self.target_food is not None:
            x,y = self.vector_to_food(self.target_food)
        closest_distance = math.inf

        
        self.target_food = None
        if len(food_list)==0:
            return

        for food in food_list:
            x,y = self.vector_to_food(food)
            if x**2 + y**2 < closest_distance:
                closest_distance = x**2 + y**2
                self.target_food = food


    def closest_food(self):
        close_food = []
        if (self.rect.x//self.dict_food.grid_size,self.rect.y//self.dict_food.grid_size) in self.dict_food.food_dic:
            close_food = close_food + self.dict_food.food_dic[(self.rect.x//self.dict_food.grid_size,self.rect.y//self.dict_food.grid_size)]

        for i in range(1,self.vision//(2*self.dict_food.grid_size)):
            if len(close_food) > 1:
                break
            for j in range(-i,i+1):
                y = i+(self.rect.y//self.dict_food.grid_size)
                x = j+(self.rect.x//self.dict_food.grid_size)
                if (x,y) in self.dict_food.food_dic:
                    close_food = close_food + self.dict_food.food_dic[(x,y)]

                y = -i+(self.rect.y//self.dict_food.grid_size)
                x = -j+(self.rect.x//self.dict_food.grid_size)
                if (x,y) in self.dict_food.food_dic:
                    close_food = close_food + self.dict_food.food_dic[(x,y)]

            for j in range(-i+1,i):
                y = j+(self.rect.y//self.dict_food.grid_size)
                x = i+(self.rect.x//self.dict_food.grid_size)
                if (x,y) in self.dict_food.food_dic:
                    close_food = close_food + self.dict_food.food_dic[(x,y)]

                y = -j+(self.rect.y//self.dict_food.grid_size)
                x = -i+(self.rect.x//self.dict_food.grid_size)
                if (x,y) in self.dict_food.food_dic:
                    close_food = close_food + self.dict_food.food_dic[(x,y)]

        self.find_closest_food(close_food)
    
    def close(self):
        if self.target_food is None:
            return 1
        
        dist = self.vector_to_food(self.target_food)
        distance = dist[0]**2 + dist[1]**2
        return distance/(self.vision**2*2) + 0.75 if self.vision> 0 else 1


    def angle_to_food(self, food):
        x,y = self.vector_to_food(food)

        if x**2 + y**2 > self.vision**2:
            return self.angle + math.pi/2 * random.randint(-10,10)*0.1
        
        return math.atan2(y,x)* (1 if random.randint(0,100) < self.prob_fail_rot else 0)
        
    def draw(self, surface, camera_offset=(0,0)):

        x1,y1 = self.rect.x+self.rect.width//2 ,self.rect.y+self.rect.width//2 
        x2, y2 = self.rect.x+self.rect.width//2+(math.cos(self.angle)*self.vision//2),self.rect.y+self.rect.width//2+(math.sin(self.angle)*self.vision//2)

        
        #pygame.draw.line(surface,pygame.color.Color(0,0,0),(x1,y1),(x2,y2))

        #pygame.draw.circle(surface, self.color, (self.rect.x+self.rect.width//2 - camera_offset[0],self.rect.y+self.rect.width//2 - camera_offset[1]), self.vision//2, width=0)
        pygame.draw.rect(surface, self.color, self.rect.move(-camera_offset[0], -camera_offset[1]), width=0)
        
        

    def wander(self):
        turn_strength = self.rot_vel*0.1
        self.change_angle(random.uniform(-turn_strength, turn_strength))

    def change_angle(self, angle):
        self.angle += angle

    def update(self):
        close = self.close()
        if len(self.food) > 0:
            self.closest_food()
        else:
            self.target_food = None
        
        if self.target_food is None:
            self.wander()
        else:
            self.move_to_food(self.target_food)
        
        move_angle = (math.cos(self.angle)*self.velocity*close,math.sin(self.angle)*self.velocity*close)
        
        self.rect.move_ip(move_angle if random.randint(0,100) < self.prob_fail_rot else (move_angle[0]*1.5, move_angle[1] *1.5))
        self.life -= random.randint(0,1)
        self.life -= 0.05*self.velocity * random.randint(0,1)
        self.life -= 0.05*self.rot_vel * random.randint(0,1)

        if self.life <= 0:
            self.timeout = True

        if self.food != []:
                if self.target_food is not None and self.rect.colliderect(self.target_food.rect):
                    self.food_eaten += 1
                    self.life += 50
                    self.dict_food.remove(self.target_food)
                    self.food.remove(self.target_food)

    def move_to_food(self, food):

        ang = self.angle_to_food(food)
        move_angle = ang - self.angle
        if move_angle > math.pi:
            move_angle -= 2 * math.pi
        elif move_angle < -math.pi:
            move_angle += 2 * math.pi

        distance_sq = self.vision**2
        if self.target_food is not None:
            dist_vector = self.vector_to_food(self.target_food)
            distance_sq = dist_vector[0]**2 + dist_vector[1]**2
        aggressiveness = 1.0 - (distance_sq / (self.vision**2 + 1e-6))
        g = max(0, min(100/ROBOTS_SIZE, aggressiveness))*1
        self.change_angle(move_angle*0.05 * self.rot_vel*g *0.6)

        return move_angle

        


        