import random
import pygame
from pygame.locals import *

# ウィンドウのサイズ
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# マップのセルのサイズと色
CELL_SIZE = 50
PLAYER_COLOR = (0, 255, 0)  # プレイヤーの色 (緑)
ENEMY_COLOR = (255, 165, 0)  # 敵の色 (オレンジ)
BOSS_COLOR = (255, 0, 0)  # ボスの色 (赤)
EMPTY_COLOR = (255, 255, 255)  # 空白セルの色 (白)

class Player:
    def __init__(self, x, y, game_map):
        self.x = x
        self.y = y
        self.health = 5
        self.max_health = 5
        self.attack_power = 1
        self.defense_power = 1
        self.level = 1
        self.experience = 0
        self.experience_to_level_up = 20
        self.game_map = game_map

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        # 移動先がマップ内かどうかをチェック
        if 0 <= new_x < len(self.game_map[0]) and 0 <= new_y < len(self.game_map):
            if self.game_map[new_y][new_x] == "-":
                # 移動先が空白の場合、プレイヤーを移動させる
                self.game_map[self.y][self.x] = "-"  # 元の位置を空白に戻す
                self.x = new_x
                self.y = new_y
                self.game_map[self.y][self.x] = "P"  # 移動後の位置にプレイヤーを表示
                self.encounter_enemy(self.x, self.y)  # 新しい位置に敵がいるかチェック
            elif self.game_map[new_y][new_x] == "E" or self.game_map[new_y][new_x] == "B":
                # 移動先に敵がいる場合、バトルを開始する
                self.encounter_enemy(new_x, new_y)
            else:
                print("You can't move there. Try again.")
        else:
            print("You can't move there. Try again.")


    def encounter_enemy(self, x, y):
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                print("Encountered an enemy!")
                self.battle(enemy)

    def attack(self, enemy):
        enemy.health -= self.attack_power

    def defend(self):
        self.defense_power = 2
        print("Player is defending. Defense power increased.")

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print("Player defeated! Game over.")
            self.game_over = True

    def gain_experience(self, experience):
        self.experience += experience
        if self.experience >= self.experience_to_level_up:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_health += 5
        self.health = self.max_health
        self.experience -= self.experience_to_level_up
        self.experience_to_level_up *= 2
        print("Player leveled up! HP increased and fully healed.")

class Enemy:
    def __init__(self, x, y, health=2, attack_power=1):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power

    def attack(self, player):
        if player.defense_power > 1:
            print("Player defended the attack!")
        else:
            player.take_damage(self.attack_power)

    def take_damage(self, damage):
        self.health -= damage

class Boss(Enemy):
    def __init__(self, x, y, health=5, attack_power=3):
        super().__init__(x, y, health, attack_power)

class Game:
    def __init__(self, map_size):
        self.map_size = map_size
        self.map = self.generate_map()
        self.player = Player(0, 0, self.map)
        self.enemies_positions = self.generate_enemies_positions()
        self.boss_position = random.choice(self.enemies_positions)
        self.enemies = self.generate_enemies()
        self.game_over = False
        pygame.init()
        # ゲームウィンドウの作成
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Battle Game')

        self.map[self.player.y][self.player.x] = "P"
        for enemy in self.enemies:
            self.map[enemy.y][enemy.x] = "E"
        self.map[self.boss_position[1]][self.boss_position[0]] = "B"  # ボスの位置をマップに反映
        
    def get_random_empty_position(self):
        while True:
            x = random.randint(0, self.map_size - 1)
            y = random.randint(0, self.map_size - 1)
            if self.map[y][x] == "-":
                return x, y

    def generate_enemies_positions(self):
        positions = []
        for _ in range(self.map_size - 1):  # ボスを除く敵の位置を生成
            x, y = self.get_random_empty_position()
            positions.append((x, y))
        return positions

    def generate_map(self):
        map = [["-" for _ in range(self.map_size)] for _ in range(self.map_size)]
        return map

    def generate_enemies_positions(self):
        positions = []
        for _ in range(self.map_size - 1):  # ボスを除く敵の位置を生成
            x, y = self.get_random_empty_position()
            positions.append((x, y))
        return positions

    def generate_enemies(self):
        enemies = []
        for position in self.enemies_positions:
            x, y = position
            if position == self.boss_position:
                enemy = Boss(x, y, 5, 5)  # BossのHP: 5, 攻撃力: 5
            else:
                enemy = Enemy(x, y, 2, 1)  # 通常の敵のHP: 2, 攻撃力: 1
            enemies.append(enemy)
        return enemies

    def print_map(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                cell_color = EMPTY_COLOR

                if self.player.x == x and self.player.y == y:
                    cell_color = PLAYER_COLOR
                elif (x, y) == self.boss_position:
                    cell_color = BOSS_COLOR
                else:
                    for enemy in self.enemies:
                        if enemy.x == x and enemy.y == y:
                            cell_color = ENEMY_COLOR
                            break

                pygame.draw.rect(self.window, cell_color, cell_rect)
        
        pygame.display.flip()

    def print_status(self):
        status_text = [
            f"HP: {self.player.health}/{self.player.max_health} ({self.player.experience}/{self.player.experience_to_level_up})",
            f"Lv: {self.player.level}"
        ]
        for i, text in enumerate(status_text):
            self.draw_text(text, 10, 10 + i * 30)

    def player_move(self, dx, dy):
        new_x = self.player.x + dx
        new_y = self.player.y + dy

        if (
            new_x >= 0
            and new_x < self.map_size
            and new_y >= 0
            and new_y < self.map_size
            and self.map[new_y][new_x] != "#"
        ):
            if self.map[new_y][new_x] == "E" or self.map[new_y][new_x] == "B":
                # 敵がいる場合、バトルを開始する
                self.encounter_enemy(new_x, new_y)
            else:
                self.map[self.player.y][self.player.x] = "."
                self.player.x = new_x
                self.player.y = new_y
                self.map[self.player.y][self.player.x] = "P"

    def encounter_enemy(self, x, y):
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                self.battle(enemy)

    def battle(self, enemy):
        self.current_enemy = enemy
        while self.player.health > 0 and enemy.health > 0:
            self.print_map()
            self.print_status()

            pygame.display.update()

            # プレイヤーのターン
            command_entered = False
            while not command_entered:
                self.handle_events()
                keys = pygame.key.get_pressed()
                if keys[K_a]:
                    self.player.attack(enemy)
                    command_entered = True
                if keys[K_d]:
                    self.player.defend()
                    command_entered = True

            # 敵のターン
            enemy.attack(self.player)

        if self.player.health <= 0:
            pygame.display.update()
            self.game_over = True
        else:
            self.player.gain_experience(10)
            self.enemies.remove(enemy)
            self.map[enemy.y][enemy.x] = "-"  # マップ上から敵を削除
            pygame.display.update()

    def draw_text(self, text, x, y, font_size=24, color=(0, 0, 0)):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.window.blit(text_surface, text_rect)

    def run_game(self):
        while not self.game_over:
            self.handle_events()
            self.print_map()
            pygame.display.update()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game_over = True

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.game_over = True
                if event.key == K_UP:
                    self.player_move(0, -1)
                if event.key == K_DOWN:
                    self.player_move(0, 1)
                if event.key == K_LEFT:
                    self.player_move(-1, 0)
                if event.key == K_RIGHT:
                    self.player_move(1, 0)
                if event.key == K_a:
                    self.player.attack(self.current_enemy)
                if event.key == K_d:
                    self.player.defend()

game = Game(10)  # 10x10のマップを作成
game.run_game()
