import sys
import pygame
from collections import deque

MEMORY = [0 for i in range(4096)]

FONT = [
    0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
    0x20, 0x60, 0x20, 0x20, 0x70,  # 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
    0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
    0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
    0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
    0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
    0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
    0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
    0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
    0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
    0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
    0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
    0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
    0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
    0xF0, 0x80, 0xF0, 0x80, 0x80  # F
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
        self.pixels = [[False for i in range(32)] for i in range(64)]
        self.__initialize_display()

    def __initialize_display(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 320))
        self.screen.fill((0, 0, 0))
        pygame.display.update()
        self.draw_pixels()

    def draw_pixels(self):
        for x, row in enumerate(self.pixels):
            for y, pixel in enumerate(row):
                rect = pygame.Rect(
                    x*10,
                    y*10,
                    10,
                    10
                )

                pygame.draw.rect(
                    surface=self.screen,
                    color=[int(pixel)*255] * 3,
                    rect=rect
                )
        pygame.display.update()


class Chip8:
    def __init__(self):
        self.OPCODE_OPERATION_MAPPING = { 
            0x0:self.execute00E0,
            0x1:self.execute1NNN,
            0x6:self.execute6XNN,
            0x7:self.execute7XNN,
            0xa:self.executeANNN,
            0xd:self.executeDXYN
        }
        self.OPCODE_ARGS_MAPPING = {
            0x0: [],
            0x1: [self.get_nnn_from_instruction],
            0x6: [
                self.get_x_from_instruction,
                self.get_nn_from_instruction
            ],  
            0x7: [
                self.get_x_from_instruction,
                self.get_nn_from_instruction,
            ],
            0xa: [
                self.get_nnn_from_instruction
            ],
            0xd: [
                self.get_x_from_instruction,
                self.get_y_from_instruction,
                self.get_n_from_instruction
            ]
        }
        self.stack = deque()
        self.memory = MEMORY
        self.registers = [0 for i in range(16)]
        self.PC = 0x200
        self.I = 0x0
        self.delay_timer = 60
        self.sound_timer = 60
        # load font in memory
        for index, char in enumerate(FONT):
            self.memory[0x050 + index] = char

        try:
            self.load_game(sys.argv[-1])
        except IndexError:
            raise Exception('Please provide the program path')

    def load_game(self, game_path):
        with open(game_path, 'rb') as game_file:
            game = game_file.read()

        for index, byte in enumerate(game):
            self.memory[0x200 + index] = byte

    def fetch_instruction(self):
        first_half = self.memory[self.PC]
        second_half = self.memory[self.PC + 1]
        self.PC += 2

        full_instruction = (first_half << 8) | second_half
        return full_instruction

    def get_x_from_instruction(self, instruction):
        return (instruction & 0x0f00) >> 8

    def get_y_from_instruction(self, instruction):
        return (instruction & 0x00f0) >> 4

    def get_n_from_instruction(self, instruction):
        return (instruction & 0x000f)

    def get_nn_from_instruction(self, instruction):
        return (instruction & 0x00ff)

    def get_nnn_from_instruction(self, instruction):
        return (instruction & 0x0fff)

    def get_args(self, opcode, instruction):
        args = []
        for decode_arg in self.OPCODE_ARGS_MAPPING[opcode]:
            args.append(decode_arg(instruction))

        return args

    def decode_instruction(self, instruction):
        opcode = instruction >> 12

        try:
            operation = self.OPCODE_OPERATION_MAPPING[opcode]
            args = self.get_args(opcode, instruction)
        except KeyError:
            raise Exception('ops...')

        return operation, args

    def start_game(self):
        self.display = Display()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    print(f'{KEYBOARD_MAPPING.get(event.key)} PRESSED')

                current_instruction = self.fetch_instruction()
                instruction_function, args = self.decode_instruction(current_instruction)
                instruction_function(*args)

    def execute00E0(self):
        self.display.pixels = [[False for i in range(32)] for i in range(64)]
        self.display.draw_pixels()

    def execute1NNN(self, address):
        self.PC = address

    def execute6XNN(self, vx, value):
        self.registers[vx] = value

    def execute7XNN(self, vx, value):
        self.registers[vx] += value 

    def executeANNN(self, value):
       self.I = value

    def executeDXYN(self, vx, vy, rows):
        self.registers[0xf] = 0
        y = self.registers[vy] % 32

        for y_pos in range(rows):
            color = bin(self.memory[self.I + y_pos])[2:].zfill(8)
            x = self.registers[vx] % 64
            for sprite_color in color:
                sprite_color = bool(int(sprite_color))
                print(f'x{x}, y{y}')
                actual_color = self.display.pixels[x][y]

                if actual_color and sprite_color:
                    self.display.pixels[x][y] = False
                    self.registers[0xf] = 1
                elif sprite_color and not actual_color:
                    self.display.pixels[x][y] = True

                x += 1

                if x >= 63:
                    break
            y += 1

            if y >= 31:
                break

        self.display.draw_pixels()

chip8 = Chip8()
chip8.start_game()
