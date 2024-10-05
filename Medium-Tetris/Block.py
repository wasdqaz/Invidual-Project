from Setting import *

class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        super().__init__(group)
        
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft = (self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE))
    def horizontal_limit(self, x, data_field):
        if not 0 <= x < COLUMNS or data_field[int(self.pos.y)][x]:
            return True
        return False
    def rotate(self, pivot_pos):

        return pivot_pos + (self.pos - pivot_pos).rotate(90)
    def vertical_limit(self, y, data_field):
        if not y < ROWS:
            return True
        if y >= 0 and data_field[y][int(self.pos.x)]:
            return True
        return False
    
    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE
    
class Tetromino():
    def __init__(self, group, shape, generate, data_field):
        self.generate = generate
        self.data_field = data_field
        self.shape = shape 
        self.block_pos = TETROMINOS[self.shape]['shape']
        self.color = TETROMINOS[self.shape]['color']
        self.blocks = [Block(group, pos, self.color) for pos in self.block_pos]
    #collisions
    def next_horizontal_limit(self, amount):
        collisions = [block.horizontal_limit(int(block.pos.x + amount), self.data_field) for block in self.blocks]
        return True if any(collisions) else False
    
    def vertical_limit(self):
        collisions = [block.vertical_limit(int(block.pos.y + 1), self.data_field) for block in self.blocks]
        return True if any(collisions) else False
    
    def move_down(self):
        if not self.vertical_limit():
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                self.data_field[int(block.pos.y)][int(block.pos.x)] = block

            self.generate()
        
    def move_horizontal(self, amount):
        if not self.next_horizontal_limit(amount):
            for block in self.blocks:
                block.pos.x += amount
                
    def rotate(self):
        if self.shape != 'O':

            # 1. pivot point 
            pivot_pos = self.blocks[0].pos

            # 2. new block positions
            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

            # 3. collision check
            for pos in new_block_positions:
                # horizontal 
                if pos.x < 0 or pos.x >= COLUMNS:
                    return

                # field check -> collision with other pieces
                if self.data_field[int(pos.y)][int(pos.x)]:
                    return

                # vertical / floor check
                if pos.y > ROWS:
                    return

            # 4. implement new positions
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]