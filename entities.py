import random

class Entity:
    def __init__(self, x:int, y:int, name:str="None", health:int=1, attack_power:int=1, exp:int=0):
        self.x, self.y = x, y
        self.health:int = health
        self.name:str = name
        self.attack_power:int = attack_power
        self.exp:int = exp
        
class Enemy(Entity):
    def __init__(self, x:int, y:int, name:str="Bone", health:int=3, attack_power:int=1, exp:int=1, escape_rate:float=0.9, drop_items:dict={"やくそう":0.2}):
        super().__init__(x, y, name, health, attack_power, exp)
        self.escape_rate = escape_rate
        self.drop_items = drop_items

    def attack(self, player):
        player.health = max(0,player.health-self.attack_power)
        return [f"{self.name}の こうげき", f"{self.attack_power}ダメージをうけた！"]
    
    def drop(self):
        for k, rate in self.drop_items.items():
            if random.random() < rate:
                return Entity(self.x, self.y,k)