################################################################################
import pygame
import random
import math
import mapHandling
from constants import *
from bitmapFont import BitmapFont
from mainClasses import *

def main():
	pygame.mixer.pre_init(0, 0, 1, 1024)
	pygame.init()
	Channels = []
  
	i = 0  
	while  i < SCHANNELS:
		Channels.append(pygame.mixer.Channel(i))
		i += 1
	timer = pygame.time.Clock()
	layers = []
	keys = 0
  
	i = 0
	while i < 3:
		layers.append(pygame.Surface((S_WIDTH, S_HEIGHT)))
		layers[i].set_colorkey((0, 0, 0))
		i += 1
        
	dispScreen = pygame.display.set_mode((S_WIDTH * S_SCALE, S_HEIGHT * S_SCALE))
	screen = pygame.Surface((S_WIDTH, S_HEIGHT))
	areaData = mapHandling.loadArea("test.div")
	pygame.display.set_caption(areaData['Name'])
	tileSet = []	
	tileSet.append(pygame.image.load(areaData['tSet']))
    
	for set in tileSet:
		set.set_colorkey((0, 0, 0))
	if areaData['Music'] != 'NONE':
		pygame.mixer.music.load(areaData['Music'])
		pygame.mixer.music.play(-1)
	
	Sounds = dict(beams=[pygame.mixer.Sound("nBeam.wav"),], \
	jump=pygame.mixer.Sound("Jump.wav"), spin=pygame.mixer.Sound("Spin.wav"), \
	ball=pygame.mixer.Sound("BallIn.wav"), stand=pygame.mixer.Sound("BallOut.wav"), \
	step=pygame.mixer.Sound("Step.wav"), land=pygame.mixer.Sound("Land.wav"), \
	missile=pygame.mixer.Sound("Missile.wav"), explode=pygame.mixer.Sound("Explode1.wav"),\
	charge=pygame.mixer.Sound("Charge.wav"), cLoop=pygame.mixer.Sound("ChargeLoop.wav"))
    
	playerSprite = pygame.image.load("playerL1.png")
	playerSprite.set_colorkey((0, 0, 0))
	ballSprite = pygame.image.load("ballL1.png")
	ballSprite.set_colorkey((0, 0, 0))
	BeamSprite = pygame.image.load("beam.png")
	BeamSprite.set_colorkey((0, 0, 0))
	ChargeSprite = pygame.image.load("charge.png")
	ChargeSprite.set_colorkey((0,0,0))
	MissileSprite = pygame.image.load("missile1.png")
	MissileSprite.set_colorkey((0, 0, 0))
    
	projectiles = []
	playerFrames = [
		playerSprite.subsurface(pygame.Rect(0, 32, 16, 16)),
		playerSprite.subsurface(pygame.Rect(16, 0, 16, 16)),
		playerSprite.subsurface(pygame.Rect(32, 0, 16, 16)),
		playerSprite.subsurface(pygame.Rect(48, 0, 16, 16)),
		playerSprite.subsurface(pygame.Rect(64, 0, 16, 16)),
		playerSprite.subsurface(pygame.Rect(80, 0, 16, 16)),
		playerSprite.subsurface(pygame.Rect(16, 16, 16, 16)),
		playerSprite.subsurface(pygame.Rect(32, 16, 16, 16)),
		playerSprite.subsurface(pygame.Rect(48, 16, 16, 16)),
		playerSprite.subsurface(pygame.Rect(64, 16, 16, 16)),
		playerSprite.subsurface(pygame.Rect(80, 16, 16, 16)),
		playerSprite.subsurface(pygame.Rect(16, 32, 16, 16)),
		playerSprite.subsurface(pygame.Rect(32, 32, 16, 16)),
		playerSprite.subsurface(pygame.Rect(48, 32, 16, 16)),
		playerSprite.subsurface(pygame.Rect(64, 32, 16, 16)),
		playerSprite.subsurface(pygame.Rect(80, 32, 16, 16)),
		playerSprite.subsurface(pygame.Rect(16, 48, 16, 16)),
		playerSprite.subsurface(pygame.Rect(32, 48, 16, 16)),
		playerSprite.subsurface(pygame.Rect(48, 48, 16, 16)),
		playerSprite.subsurface(pygame.Rect(64, 48, 16, 16)),
		playerSprite.subsurface(pygame.Rect(80, 48, 16, 16)),
		playerSprite.subsurface(pygame.Rect(96, 0, 16, 16)),
		playerSprite.subsurface(pygame.Rect(112, 0, 16, 16)),
		playerSprite.subsurface(pygame.Rect(128, 0, 16, 16)),
		playerSprite.subsurface(pygame.Rect(144, 0, 16, 16)),
		playerSprite.subsurface(pygame.Rect(80, 64, 16, 16)),
	]
    
	ballFrames = [
		ballSprite.subsurface(pygame.Rect(0, 0, 8, 8)),
		ballSprite.subsurface(pygame.Rect(8, 0, 8, 8)),
		ballSprite.subsurface(pygame.Rect(16, 0, 8, 8)),
		ballSprite.subsurface(pygame.Rect(24, 0, 8, 8)),
	]
    
	chargeFrames = [
        ChargeSprite.subsurface(pygame.Rect(0,0,8,8)),
        ChargeSprite.subsurface(pygame.Rect(8,0,8,8)),
        ChargeSprite.subsurface(pygame.Rect(16,0,8,8)),
        ChargeSprite.subsurface(pygame.Rect(24,0,8,8)),
        ChargeSprite.subsurface(pygame.Rect(32,0,8,8)),
        ChargeSprite.subsurface(pygame.Rect(40,0,8,8))
	]
    
	pData = PlayerData()
	roomElems = mapHandling.loadRoom("testRoom.crm")
	player = Player(64, 64, pData)
	player.setSoundData(Sounds, Channels)
	running = 1
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = 0
			if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					keys = keys ^ C_UP
					if event.type == pygame.KEYDOWN:
						player.KDOWN_up(keys, roomElems)
					else:
						player.KUP_up(keys)

				if event.key == pygame.K_DOWN:
					keys = keys ^ C_DOWN
					if event.type == pygame.KEYDOWN:
						player.KDOWN_down(keys)
					else:
						player.KUP_down(keys)
					
				if event.key == pygame.K_LEFT:
					keys = keys ^ C_LEFT
					if event.type == pygame.KEYDOWN:
						player.KDOWN_left(keys)
					else:
						player.KUP_left(keys)
						
				if event.key == pygame.K_RIGHT:
					keys = keys ^ C_RIGHT
					if event.type == pygame.KEYDOWN:
						player.KDOWN_right(keys)
					else:
						player.KUP_right(keys)
						
				if event.key == pygame.K_SPACE:
					keys = keys ^ C_JUMP
					if event.type == pygame.KEYDOWN:
						player.KDOWN_jump(keys, roomElems)
					else:
						player.KUP_jump(keys)
						
				if event.key == pygame.K_d:
					keys = keys ^ C_SHOOT
					if event.type == pygame.KEYDOWN:
						player.KDOWN_fire(keys, projectiles)
					else:
						player.KUP_fire(keys, projectiles)
						
				if event.key == pygame.K_a:
					keys = keys ^ C_SECOND
					if event.type == pygame.KEYDOWN:
						playerSprite = pygame.image.load("playerL1Select.png")
					else:
						playerSprite = pygame.image.load("playerL1.png")
					playerFrames = [
						playerSprite.subsurface(pygame.Rect(0, 32, 16, 16)),
						playerSprite.subsurface(pygame.Rect(16, 0, 16, 16)),
						playerSprite.subsurface(pygame.Rect(32, 0, 16, 16)),
						playerSprite.subsurface(pygame.Rect(48, 0, 16, 16)),
						playerSprite.subsurface(pygame.Rect(64, 0, 16, 16)),
						playerSprite.subsurface(pygame.Rect(80, 0, 16, 16)),
						playerSprite.subsurface(pygame.Rect(16, 16, 16, 16)),
						playerSprite.subsurface(pygame.Rect(32, 16, 16, 16)),
						playerSprite.subsurface(pygame.Rect(48, 16, 16, 16)),
						playerSprite.subsurface(pygame.Rect(64, 16, 16, 16)),
						playerSprite.subsurface(pygame.Rect(80, 16, 16, 16)),
						playerSprite.subsurface(pygame.Rect(16, 32, 16, 16)),
						playerSprite.subsurface(pygame.Rect(32, 32, 16, 16)),
						playerSprite.subsurface(pygame.Rect(48, 32, 16, 16)),
						playerSprite.subsurface(pygame.Rect(64, 32, 16, 16)),
						playerSprite.subsurface(pygame.Rect(80, 32, 16, 16)),
						playerSprite.subsurface(pygame.Rect(16, 48, 16, 16)),
						playerSprite.subsurface(pygame.Rect(32, 48, 16, 16)),
						playerSprite.subsurface(pygame.Rect(48, 48, 16, 16)),
						playerSprite.subsurface(pygame.Rect(64, 48, 16, 16)),
						playerSprite.subsurface(pygame.Rect(80, 48, 16, 16)),
						playerSprite.subsurface(pygame.Rect(96, 0, 16, 16)),
						playerSprite.subsurface(pygame.Rect(112, 0, 16, 16)),
						playerSprite.subsurface(pygame.Rect(128, 0, 16, 16)),
						playerSprite.subsurface(pygame.Rect(144, 0, 16, 16)),
						playerSprite.subsurface(pygame.Rect(80, 64, 16, 16)),
					]
					
				if event.key == pygame.K_w:
					keys = keys ^ C_DIAG
					if event.type == pygame.KEYDOWN:
						player.KDOWN_diag(keys)
					else:
						player.KUP_diag(keys)
						
				if event.key == pygame.K_LSHIFT:
					keys = keys ^ C_SELECT
				if event.key == pygame.K_r:
					keys = keys ^ C_PAUSE
	
		player.update(roomElems, keys)
		for shot in projectiles:
			collided = 0
			collided = shot.update(roomElems)
			if shot.x < -shot.offx or shot.x > S_WIDTH + shot.offx \
			or shot.y < -shot.offy or shot.y > S_HEIGHT + shot.offy \
			or collided:
				projectiles.remove(shot)
				if collided:
					if isinstance(shot, Missile):
						Channels[3].play(Sounds["explode"])
		
		# Drawing
		screen.fill((0, 0, 0))
		for layer in layers:
			layer.fill((0, 0, 0))
		
		# Draw blocks
		for block in roomElems["Blocks"]:
			tCount = 0
			for tile in block.tiles:
				layers[block.layer].blit(tileSet[block.tSet], \
				(block.x + (tCount % block.w) * 8, block.y + (tCount / block.w) * 8), \
				pygame.Rect(tile % 3 * 8, tile / 3 * 8, 8 , 8))
				tCount += 1
		
		# Draw projectiles
		for shot in projectiles:
			fX = F_NORMAL[0] + shot.dir * 8
			fY = F_NORMAL[1] + shot.dx * 8
			if isinstance(shot, Beam):
				screen.blit(BeamSprite, (shot.x - shot.offx, shot.y - shot.offy), \
				pygame.Rect(fX, fY, 8, 8))
			elif isinstance(shot, Missile):
				screen.blit(MissileSprite, (shot.x - shot.offx, shot.y - shot.offy), \
				pygame.Rect(fX, fY, 8, 8))
		
		# Draw the player
		if not player.blink:
			if player.state & BALL:
				if player.dx < 1:
					layers[0].blit(ballFrames[player.frame], \
					(player.x - player.offx, player.y - player.offy))
				else:
					layers[0].blit(pygame.transform.flip\
					(ballFrames[player.frame], 1, 0), \
					(player.x - player.offx, player.y - player.offy))
			else:
				if player.dx < 1:
					layers[0].blit(playerFrames[player.frame], \
					(player.x - player.offx, player.y - player.offy))
				else:
					layers[0].blit(pygame.transform.flip\
					(playerFrames[player.frame], 1, 0), \
					(player.x - player.offx, player.y - player.offy))
                    
        # Draw charge effect
				if player.charge > 0 and not player.state & SPIN:
					lx, ly = L_SHOT[player.dx][player.dir]
					lx = lx - 4 + player.x - player.offx
					ly = ly - 4 + player.y - player.offy
					
					frame = int((player.charge / 60.0) * 5)
					
					layers[0].blit(chargeFrames[frame], (lx, ly))
		
		for layer in layers:
			screen.blit(layer, (0, 0))
		
		dispScreen.blit(pygame.transform.scale(screen, \
		(S_WIDTH * S_SCALE, S_HEIGHT * S_SCALE)), (0, 0))
		pygame.display.flip()
		
		timer.tick(30)
		
	pygame.quit()
		
if __name__ == "__main__":
	main()