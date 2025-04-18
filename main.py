#Coded by @prraygo

import pygame
import sys
import time
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("@prraygo")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font_size = 48
font = pygame.font.SysFont('Arial', font_size, bold=True)

lyrics = [
    "sudah terbiasa", #1
    "terjadi", #2
    "tantee", #3
    "teman datang", #4
    "ketika", #5
    "lagi", #6
    "butuh saja", #7
    "coba", #8
    "kalo", #9
    "lagi susah", #10
    "mereka semua", #11
    "menghilaaaangg~" #12
]

durations = [1.2, 1.1, 1.1, 1.1, 0.9, 0.9, 1.3, 0.8, 1.2, 1.7, 1.7, 6]

particles = []

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 8)
        self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        self.speed = random.uniform(1.0, 3.0)
        self.angle = random.uniform(0, 2 * math.pi)
        self.lifetime = random.uniform(0.5, 1.5)
        self.age = 0
        
    def update(self, dt):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.age += dt
        self.size = max(0, self.size - (dt * 3))
        
    def draw(self):
        if self.age < self.lifetime:
            alpha = 255 * (1 - self.age / self.lifetime)
            color = (self.color[0], self.color[1], self.color[2], int(alpha))
            s = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (int(self.size), int(self.size)), int(self.size))
            screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))
            return True
        return False

class LightEffect:
    def __init__(self):
        self.intensity = 0
        self.increasing = True
        
    def update(self, dt):
        if self.increasing:
            self.intensity += dt * 2
            if self.intensity > 1:
                self.intensity = 1
                self.increasing = False
        else:
            self.intensity -= dt * 2
            if self.intensity < 0:
                self.intensity = 0
                self.increasing = True
                
    def draw(self, center_x, center_y, radius):
        max_radius = radius * 2
        for r in range(10):
            size = max_radius * (1 - r/10) * self.intensity
            alpha = 100 * (1 - r/10) * self.intensity
            s = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 255, 255, int(alpha)), (int(size), int(size)), int(size))
            screen.blit(s, (int(center_x - size), int(center_y - size)))

def main():
    clock = pygame.time.Clock()
    light_effect = LightEffect()
    
    current_lyric_index = 0
    time_since_last_change = 0
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill(BLACK)
        
        time_since_last_change += dt
        if time_since_last_change >= durations[current_lyric_index]:
            time_since_last_change = 0
            current_lyric_index = (current_lyric_index + 1) % len(lyrics)
            
            center_x = WIDTH // 2
            center_y = HEIGHT // 2
            for _ in range(30):
                particles.append(Particle(center_x, center_y))
        
        progress = min(1.0, time_since_last_change / durations[current_lyric_index])
        current_lyric = lyrics[current_lyric_index]
        text_scale = 1.0 + 0.2 * math.sin(time_since_last_change * 10)
        shake_amount = 3 * (1.0 - progress) if progress < 0.3 else 0
        offset_x = random.uniform(-shake_amount, shake_amount)
        offset_y = random.uniform(-shake_amount, shake_amount)
        text_render = font.render(current_lyric, True, WHITE)
        text_width = text_render.get_width() * text_scale
        text_height = text_render.get_height() * text_scale
        scaled_text = pygame.transform.scale(text_render, (int(text_width), int(text_height)))
        text_x = WIDTH // 2 - text_width // 2 + offset_x
        text_y = HEIGHT // 2 - text_height // 2 + offset_y
        light_effect.update(dt)
        light_effect.draw(WIDTH // 2, HEIGHT // 2, max(text_width, text_height) / 1.5)
        
        if random.random() < 0.3:
            particles.append(Particle(text_x + random.randint(0, int(text_width)), 
                                     text_y + random.randint(0, int(text_height))))
        
        screen.blit(scaled_text, (text_x, text_y))
        
        for particle in particles[:]:
            particle.update(dt)
            if not particle.draw():
                particles.remove(particle)
        
        particles[:] = particles[-300:] if len(particles) > 300 else particles
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()