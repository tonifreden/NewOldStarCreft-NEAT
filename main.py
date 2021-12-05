import pygame
import sys
import os
import neat
from player import Player
from entity import BGEntity
from enemy import Enemy

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT
)
'''
CONSTANTS
'''
WIDTH, HEIGHT = ((960, 720))
ADDENEMY = pygame.USEREVENT + 1
ADDENTITY = pygame.USEREVENT + 2

gen = 0

def draw_text(surface, text, size, pos, color):
    font = pygame.font.Font(pygame.font.match_font('Comic Sans MS'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = pos
    surface.blit(text_surface, text_rect)
    
def handle_events(all_sprites, enemies, entities):
    for event in pygame.event.get():
            
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == ADDENEMY:
            new_enemy = Enemy(WIDTH, HEIGHT)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)  
            
        elif event.type == ADDENTITY:
            new_entity = BGEntity(WIDTH, HEIGHT)
            entities.add(new_entity)
            all_sprites.add(new_entity)
    
def get_index(non_playables, players):
    distance_list = [sprite.rect.left + sprite.rect.width - players[0].rect.left for sprite in non_playables]
    return distance_list.index(min(i for i in distance_list if i >= 0))

def eval_genomes(genomes, config):
    global gen
    gen += 1

    pygame.init()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    pygame.time.set_timer(ADDENEMY, 1000)
    
    pygame.time.set_timer(ADDENTITY, 500)
    
    pygame.font.init()
    
    players = pygame.sprite.Group()
    genomes_list = []
    neural_networks = []

    for genome_id, genome in genomes:
        players.add(Player(WIDTH, HEIGHT))
        genome.fitness = 0
        genomes_list.append(genome)
        neural_network = neat.nn.FeedForwardNetwork.create(genome, config)
        neural_networks.append(neural_network)
    
    enemies = pygame.sprite.Group()
    entities = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(players)
    
    clock = pygame.time.Clock()
    max_points = 0
    
    while True and len(players) > 0:
        
        handle_events(all_sprites, enemies, entities)
                
        enemies.update()
        entities.update()
        
        screen.fill((0, 0, 0))

        if len(players.sprites()) > 0:
            max_points_alive = max([player.points for player in players.sprites()])
            if max_points_alive > max_points:
                max_points = max_points_alive
        
        draw_text(screen, "GENERATION:", 12, (0, 0), (255, 0, 0))
        draw_text(screen, str(gen - 1), 12, (100, 0), (255, 0, 0))
        draw_text(screen, "HIGHEST POINTS:", 12, (150, 0), (255, 0, 0))
        draw_text(screen, str(max_points), 12, (280, 0), (255, 0, 0))
        draw_text(screen, "GENOMES:", 12, (350, 0), (255, 0, 0))
        draw_text(screen, str(len(players)), 12, (430, 0), (255, 0, 0))
        
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if len(enemies.sprites()) > 0 and len(entities.sprites()) > 0:
            closest_enemy_index = get_index(enemies.sprites(), players.sprites())
            closest_entity_index = get_index(entities.sprites(), players.sprites())

            for index, player in enumerate(players.sprites()):
                genomes_list[index].fitness += 0.1 # each player gains 0.1 fitness for every frame they stay alive

                distance_y_top_from_enemy = player.rect.top - enemies.sprites()[closest_enemy_index].rect.bottom
                distance_y_bottom_from_enemy = enemies.sprites()[closest_enemy_index].rect.top - player.rect.bottom
                distance_y_top_from_entity = player.rect.top + entities.sprites()[closest_entity_index].rect.bottom
                distance_y_bottom_from_entity = player.rect.bottom + entities.sprites()[closest_entity_index].rect.top

                output = neural_networks[index].activate([distance_y_top_from_enemy, distance_y_bottom_from_enemy, distance_y_top_from_entity, distance_y_bottom_from_entity])

                if output[0] == -1:
                    player.move("down")
                elif output[0] == 1:
                    player.move("up")
        
            for enemy in enemies:
                for player in players:
                    if pygame.sprite.collide_rect(player, enemy):
                        genomes_list[players.sprites().index(player)].fitness -= 50
                        neural_networks.pop(players.sprites().index(player))
                        genomes_list.pop(players.sprites().index(player))
                        players.sprites().pop(players.sprites().index(player))
                        player.kill()

            for entity in entities:
                for player in players:
                    if pygame.sprite.collide_rect(player, entity):
                        if entity.image == "meteor":
                            player.points += 1
                            genomes_list[players.sprites().index(player)].fitness += 2
                        elif entity.image == "asteroid":
                            player.points += 2
                            genomes_list[players.sprites().index(player)].fitness += 4
                        elif entity.image == "planet":
                            player.points += 5
                            genomes_list[players.sprites().index(player)].fitness += 6
                        elif entity.image == "saturn":
                            player.points += 10
                            genomes_list[players.sprites().index(player)].fitness += 8
                        elif entity.image == "uranus":
                            player.points += 15
                            genomes_list[players.sprites().index(player)].fitness += 10
                        entity.kill()                    

        pygame.display.flip()
        
        clock.tick(30)
        
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    population.run(eval_genomes, 20)

    winner = stats.best_genome()

    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)