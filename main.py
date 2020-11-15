import sys
import pygame
from collections import deque

MEMORY = [0 for i in range(4096)]

FONT = [
    [0xF0, 0x90, 0x90, 0x90, 0xF0],  # 0
    [0x20, 0x60, 0x20, 0x20, 0x70],  # 1
    [0xF0, 0x10, 0xF0, 0x80, 0xF0],  # 2
    [0xF0, 0x10, 0xF0, 0x10, 0xF0],  # 3
    [0x90, 0x90, 0xF0, 0x10, 0x10],  # 4
    [0xF0, 0x80, 0xF0, 0x10, 0xF0],  # 5
    [0xF0, 0x80, 0xF0, 0x90, 0xF0],  # 6
    [0xF0, 0x10, 0x20, 0x40, 0x40],  # 7
    [0xF0, 0x90, 0xF0, 0x90, 0xF0],  # 8
    [0xF0, 0x90, 0xF0, 0x10, 0xF0],  # 9
    [0xF0, 0x90, 0xF0, 0x90, 0x90],  # A
    [0xE0, 0x90, 0xE0, 0x90, 0xE0],  # B
    [0xF0, 0x80, 0x80, 0x80, 0xF0],  # C
    [0xE0, 0x90, 0x90, 0x90, 0xE0],  # D
    [0xF0, 0x80, 0xF0, 0x80, 0xF0],  # E
    [0xF0, 0x80, 0xF0, 0x80, 0x80]   # F
]

KEYBOARD_MAPPING = {
    pygame.K_1:pygame.K_1,
    pygame.K_2:pygame.K_2,
    pygame.K_3:pygame.K_3,
    pygame.K_4:pygame.K_c,
    pygame.K_q:pygame.K_4,
    pygame.K_w:pygame.K_5,
    pygame.K_e:pygame.K_6,
    pygame.K_r:pygame.K_d,
    pygame.K_a:pygame.K_7,
    pygame.K_s:pygame.K_8,
    pygame.K_d:pygame.K_9,
    pygame.K_f:pygame.K_e,
    pygame.K_z:pygame.K_a,
    pygame.K_x:pygame.K_0,
    pygame.K_c:pygame.K_b,
    pygame.K_v:pygame.K_f,
}

class Display: 
    def __init__(self):
        self.pixels = [[0 for i in range(64)] for i in range(32)]
        self.__initialize_display()

    def __initialize_display(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 320))
        self.screen.fill((0, 0, 0))
        pygame.display.update()
        self.draw_pixels()

    def draw_pixels(self):
        for y, row in enumerate(self.pixels):
            for x, pixel in enumerate(row):
                rect = pygame.Rect(
                    x*10,
                    y*10,
                    10,
                    10
                )

                pygame.draw.rect(
                    surface=self.screen,
                    color=[pixel] * 3,
                    rect=rect
                )
        pygame.display.update()


class Chip8:
    def __init__(self):
        self.stack = deque()
        self.memory = MEMORY
        self.variable_registers = [0 for i in range(16)]
        self.PC = 0x0
        self.I = 0x0
        self.delay_timer = 60
        self.sound_timer = 60
        # load font in memory
        for index, char in enumerate(FONT):
            self.memory[80 + index] = char

        try:
            self.load_game(sys.argv[-1])
        except IndexError:
            raise Exception('Please provide the program path')

        print(self.memory)

    def load_game(self, game_path):
        with open(game_path, 'rb') as game_file:
            game = game_file.read()

        for index, byte in enumerate(game):
            self.memory[200 + index] = hex(byte)

    def start_game(self):
        self.display = Display()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    print(f'{KEYBOARD_MAPPING.get(event.key)} PRESSED')

chip8 = Chip8()
