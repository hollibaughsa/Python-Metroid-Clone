################################################################################
from constants import *

class Camera:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.w = S_WIDTH
		self.h = S_HEIGHT
		
	def update(self, track):
		return 0

class PlayerData:
	def __init__(self):
		self.inventory = 0
		self.power = 99
		self.missiles = 0
		self.supers = 0
		self.grenades = 0
		self.pbombs = 0
		self.beam = 0
		self.coolOff = 0
		self.maxPower = 99
		self.maxMissiles = 0
		self.maxSupers = 0
		self.maxGrenades = 0
		self.maxPbombs = 0
		self.bombCount = 0
		self.currentArea = 0

class Player:
	def __init__(self, x, y, data):
		self.x = x
		self.y = y
		self.data = data
		self.vx = 0.0
		self.vy = 0.0
		self.vxMax = 2
		self.vxMin = -2
		self.vyMax = 6
		self.vyMin = -4
		self.ax = 0.0
		self.ay = 0.0
		self.rect = NORMAL_RECT
		self.offx = NORMAL_OFFX
		self.offy = NORMAL_OFFY
		self.frame = 0
		self.mFrame = 0
		self.blink = 0
		self.charge = 0
		self.state = HIT | FROZEN
		self.freezeType = F_SPAWN
		self.invTime = 60
		self.dx = -1
		self.dir = 2
		self.airTime = 0
		self.sparkFlash = 0
		self.frameDel = FRAME_DELAY
		self.sounds = {}
		self.channels = []
		
	def update(self, world, keys):
		# Check if frozen
		if not self.state & FROZEN and self.dx >= 0:
			# Update animation frame
			if not self.frameDel:
				self.frameDel = FRAME_DELAY
				if not self.state & AIR and (keys & (C_LEFT | C_RIGHT)) \
				or self.state & (SPIN | BALL):
					self.mFrame += 1
					self.mFrame %= 4
					if not self.channels[1].get_busy() and \
					not self.state & (SPIN | BALL):
						self.channels[1].play(self.sounds["step"])
				else:
					self.mFrame = 0
			else:
				self.frameDel -= 1
			
			# Check charge status
			if keys & C_SHOOT and not (self.state & BALL or keys & C_SECOND):
				self.charge += 2
				if self.charge > 60:
					self.charge = 60
				if not self.channels[0].get_queue():
					self.channels[0].queue(self.sounds["cLoop"])
			else:
				self.sounds["charge"].stop()
				self.sounds["cLoop"].stop()
			
			# Decrement cool off timer
			if self.data.coolOff:
				self.data.coolOff -= 1
				
			# Calculate current frame
			if not (self.state & (SPIN | BALL | AIR) or self.airTime):
				self.frame = self.dir * 5 + self.mFrame + 1
			elif self.state & BALL:
				self.frame = self.mFrame
			elif self.state & SPIN:
				self.frame = 21 + self.mFrame
			else:
				self.frame = self.dir * 5 + 5
			
			# Check airTime for jumping. Apply gravity if zero
			if self.airTime > 0:
				self.airTime -= 1
				if self.airTime == 0:
					self.state = self.state | AIR
					self.ay = GRAVITY
			
			# Accelerate
			self.vx += self.ax		
			self.vy += self.ay
			
			# Keep velocities within apporpriate range
			if (self.state & AIR or self.airTime) and not self.state & SPIN:
				mvx = self.vxMax * 0.75
			else:
				mvx = self.vxMax
			
			if self.vx > mvx:
				self.vx = mvx
			elif self.vx < -mvx:
				self.vx = -mvx
				
			if self.vy > self.vyMax:
				self.vy = self.vyMax
			elif self.vy < self.vyMin:
				self.vy = self.vyMin
			
			# Check for ground
			if not self.state & AIR and not self.airTime:
				grounded = 0
				for block in world["Blocks"]:
					xMe = self.x - self.rect[0] / 2
					if xMe + self.rect[0] > block.x and \
					xMe < block.x + block.w * 8 and self.y == block.y:
						grounded = 1
						break
						
				if not grounded:
					self.state = self.state | AIR
					self.ay = GRAVITY
			
			collidedWith = 0
			
			# Move horizontally and check for collision
			self.x += self.vx
			for block in world["Blocks"]:
				if self.collide([block.x, block.y, block.w * 8, block.h * 8]):
					self.x -= self.vx
					self.vx = 0
					collidedWith = block
			
			# If collision occurred, move to point of collision
			if collidedWith:
				if self.x + self.rect[0] / 2 <= collidedWith.x:
					self.x = collidedWith.x - self.rect[0] / 2
				else:
					self.x = collidedWith.x + collidedWith.w * 8 + self.rect[0] / 2
			
			collidedWith = 0
			
			# Move vertically and check for collision
			self.y += self.vy
			for block in world["Blocks"]:
				if self.collide([block.x, block.y, block.w * 8, block.h * 8]):
					self.y -= self.vy
					self.vy = 0
					collidedWith = block
					
			# If collision occurred, move to point of collision
			if collidedWith:
				if self.y - self.rect[1] < collidedWith.y:
					self.y = collidedWith.y
					self.state = self.state ^ AIR
					self.channels[1].play(self.sounds["land"])
					if not keys & C_DIAG:
						if keys & C_UP:
							self.dir = 0
							if keys & (C_LEFT | C_RIGHT):
								self.dir = 1
						elif keys & C_DOWN:
							self.dir = 3
						else:
							self.dir = 2
							
					if self.state & SPIN:
						self.state = self.state ^ SPIN
						self.rect = NORMAL_RECT
						self.sounds["spin"].stop()
					
					self.ay = 0
					self.airTime = 0
				else:
					self.y = collidedWith.y + collidedWith.h * 8 + self.rect[1]
					
			# Apply friction
			if not self.state & AIR:
				if not self.dx and self.vx > 0:
					self.vx -= 0.15
				elif not self.dx and self.vx < 0:
					self.vx = 0
				elif self.dx and self.vx < 0:
					self.vx += 0.15
				elif self.dx and self.vx > 0:
					self.vx = 0
		
		# If hit, blink and update invincibility timer
		if self.state & HIT:
			self.invTime -= 1
			self.blink = self.blink ^ 1
			if self.invTime <= 0:
				self.state = self.state ^ HIT
				if self.freezeType == F_SPAWN:
					self.state = self.state ^ FROZEN
					self.freezeType = 0
					
	def KDOWN_right(self, keys):
		self.dx = 0
		if self.ax < 0.5:
			self.ax += 0.5
			
		if self.dir == 0:
			self.dir = 1
		elif self.dir == 4:
			self.dir = 3
		
	def KUP_right(self, keys):
		self.ax -= 0.5
		if not keys & C_DIAG:
			if keys & C_UP:
				self.dir = 0
			elif keys & C_DOWN and (self.state & AIR or self.airTime):
				self.dir = 4
	
	def KDOWN_left(self, keys):
		self.dx = 1
		if self.ax > -0.5:
			self.ax -= 0.5
			
		if self.dir == 0:
			self.dir = 1
		elif self.dir == 4:
			self.dir = 3
		
	def KUP_left(self, keys):
		self.ax += 0.5
		if not keys & C_DIAG:
			if keys & C_UP:
				self.dir = 0
			elif keys & C_DOWN and (self.state & AIR or self.airTime):
				self.dir = 4
		
	def KDOWN_up(self, keys, world):
		self.dir = 0
		
		if self.state & BALL:
			self.stand(world)				
		if keys & (C_DIAG | C_LEFT | C_RIGHT):
			self.dir = 1
		if self.state & SPIN:
			self.state = self.state ^ SPIN
			self.rect = NORMAL_RECT
			self.sounds["spin"].stop()
			
	def KUP_up(self, keys):
		if not keys & C_DIAG:
			self.dir = 2
			
	def KDOWN_down(self, keys):
		if not (self.state & AIR or self.airTime) or self.dir == 4:
			if not keys & (C_DIAG | C_LEFT | C_RIGHT) and not self.state & BALL:
				self.state = self.state | BALL
				self.offx = BALL_OFFX
				self.offy = BALL_OFFY
				self.rect = BALL_RECT
				self.y -= 8
				self.channels[2].play(self.sounds["ball"])
			else:
				self.dir = 3
				
		if self.state & SPIN:
			self.state = self.state ^ SPIN
			self.rect = NORMAL_RECT
			self.sounds["spin"].stop()
		if self.state & AIR or self.airTime:
			self.dir = 4
			if keys & (C_DIAG | C_LEFT | C_RIGHT):
				self.dir = 3
				
	def KUP_down(self, keys):
		if not(self.state & AIR or self.airTime) and not keys & C_DIAG:
			self.dir = 2
			
	def KDOWN_jump(self, keys, world):
		if self.state & BALL:
			self.stand(world)				
		else:
			if not self.state & AIR and not self.airTime:
				self.airTime = MAX_AIRTIME
				self.vy = self.vyMin
				if keys & (C_LEFT | C_RIGHT):
					self.state = self.state | SPIN
					self.rect = SPIN_RECT
					self.channels[1].play(self.sounds["spin"], -1)
				else:
					self.channels[1].play(self.sounds["jump"])
			else:
				self.state = self.state | SPIN
				self.rect = SPIN_RECT
				if not self.sounds["spin"].get_num_channels():
					self.channels[1].play(self.sounds["spin"], -1)
				if self.dx:
					self.vx = self.vxMin
				else:
					self.vx = self.vxMax
				
	def KUP_jump(self, keys):
		if self.airTime > 0:
			self.airTime = 0
			self.state = self.state | AIR
			self.ay = GRAVITY
			
	def KDOWN_fire(self, keys, projectiles):
		oX = self.x - self.offx
		oY = self.y - self.offy
		if not self.state & BALL and not self.data.coolOff:
			if self.state & SPIN:
				self.state = self.state ^ SPIN
				self.rect = NORMAL_RECT
				self.recalcAim(keys)
				self.sounds["spin"].stop()
			
			pX = oX + L_SHOT[self.dx][self.dir][0]
			pY = oY + L_SHOT[self.dx][self.dir][1]
			if keys & C_SECOND:
				projectiles.append(Missile(pX, pY, self.dx, self.dir, 0))
				self.channels[0].play(self.sounds["missile"])
			else:
				projectiles.append(Beam(pX, pY, self.dx, self.dir, self.data.beam))
				self.channels[0].play(self.sounds["beams"][0])
				self.channels[0].queue(self.sounds["charge"])
			self.data.coolOff = COOLOFF
		
			
	def KUP_fire(self, keys, projectiles):
		self.charge = 0
		return 0
			
	def KDOWN_diag(self, keys):
		if keys & C_DOWN:
			self.dir = 3
		else:
			self.dir = 1
		if self.state & SPIN:
			self.state = self.state ^ SPIN
			self.rect = NORMAL_RECT
			self.sounds["spin"].stop()
			
	def KUP_diag(self, keys):
		self.recalcAim(keys)
	
	def stand(self, world):
		clear = 1
		self.rect = (self.rect[0], NORMAL_RECT[1])
		for block in world["Blocks"]:
			if self.collide([block.x, block.y, block.w * 8, block.h * 8]):
				clear = 0
				self.rect = BALL_RECT
				break
				
		if clear:
			collidedWith = 0
			self.rect = NORMAL_RECT
			for block in world["Blocks"]:
				if self.collide([block.x, block.y, block.w * 8, block.h * 8]):
					collidedWith = block
			
			if collidedWith:
				oldx = self.x
				if self.x < collidedWith.x:
					self.x = collidedWith.x - self.rect[0] / 2
				else:
					self.x = collidedWith.x + collidedWith.w * 8 + self.rect[0] / 2
				
				for block in world["Blocks"]:
					if self.collide(\
					[block.x, block.y, block.w * 8, block.h * 8]):
						clear = 0
						self.rect = BALL_RECT
						self.x = oldx
						break
			if clear:
				self.state = self.state ^ BALL
				self.offx = NORMAL_OFFX
				self.offy = NORMAL_OFFY
				self.channels[2].play(self.sounds["stand"])
		
		return clear
	
	def recalcAim(self, keys):
		if keys & C_UP:
			self.dir = 0
			if keys & (C_LEFT | C_RIGHT):
				self.dir = 1
		elif keys & C_DOWN:
			self.dir = 4
			if keys & (C_LEFT | C_RIGHT) or \
			not (self.state & AIR or self.airTime):
				self.dir = 3
		else:
			self.dir = 2
	
	def collide(self, rect):
		xMe = self.x - self.rect[0] / 2
		yMe = self.y - self.rect[1]
		
		if xMe < rect[0] + rect[2] and xMe + self.rect[0] > rect[0] \
		and yMe < rect[1] + rect[3] and yMe + self.rect[1] > rect[1]:
			return 1
		else:
			return 0
	
	def setSoundData(self, sounds, channels):
		self.sounds = sounds
		self.channels = channels
	
	def destroy(self):
		return 0
		
class Entity:
	def __init__(self, x, y, health, freeze):
		self.x = x
		self.y = y
		self.health = health
		self.freeze = freeze
		self.coolOff = 0
		self.active = 0
		self.vx = 0
		self.vx = 0
		self.frame = 0
		
	def update(self):
		self.x += self.vx
		self.y += self.vy
		
	def collide(self, rect):
		return 0
		
	def destroy(self):
		return 0
		
class Projectile:
	def __init__(self, x, y, dx, dir, attributes, cDepth=0):
		self.x = x
		self.y = y
		self.offx = 4
		self.offy = 4
		self.dir = dir
		self.dx = dx
		self.attributes = attributes
		self.vx = 0
		self.vy = 0
		self.ax = 0
		self.ay = 0
		if dir == 0:
			self.vy = -5
		elif dir == 1:
			self.vy = -3
			self.vx = 3
		elif dir == 2:
			self.vx = 5
		elif dir == 3:
			self.vx = 3
			self.vy = 3
		elif dir == 4:
			self.vy = 5
			
		if dx:
			self.vx *= -1
		
	def update(self, world):
		self.x += self.vx
		self.y += self.vy
		self.vx += self.ax
		self.vy += self.ay
		
		collision = 0
		if not self.attributes & B_WAVE:
			for block in world["Blocks"]:
				if self.collide([block.x, block.y, block.w * 8, block.h * 8]):
					collision = 1
					break
				
		return collision
		
	def collide(self, rect):
		xMe = self.x - 2
		yMe = self.y - 2
		
		wMe = 4
		hMe = 4
		
		if xMe < rect[0] + rect[2] and xMe + wMe > rect[0] \
		and yMe < rect[1] + rect[3] and yMe + hMe > rect[1]:
			return 1
		else:
			return 0
		
	def destroy(self):
		return 0
		
class Beam(Projectile):
	def __init__(self, x, y, dx, dir, attributes, cDepth=0):
		Projectile.__init__(self, x, y, dx, dir, attributes, cDepth)
		
	def update(self, world):
		return Projectile.update(self, world)
		
	def collide(self, rect):
		return Projectile.collide(self, rect)
		
	def destroy(self):
		return 0
		
class Missile(Projectile):
	def __init__(self, x, y, dx, dir, attributes, cDepth=0):
		Projectile.__init__(self, x, y, dx, dir, attributes, cDepth)
		
	def update(self, world):
		return Projectile.update(self, world)
		
	def collide(self, rect):
		return Projectile.collide(self, rect)
		
	def destroy(self):
		return 0
	
class Block:
	def __init__(self, x, y, w, h, tiles, tSet, layer, attributes):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.tiles = tiles
		self.tSet = tSet
		self.layer = layer
		self.attributes = attributes
		self.ocpacity = 100
		active = 0
		destroyed = 0
		rTimer = 60
		fading = 0
		breaking = 0
		appearing = 0
		reforming = 0
		
	def destroy(self):
		destroying = 2
		
	def reform(self):
		reforming = 2
		
	def fade(self):
		fading = 4
		
	def appear(self):
		appearing = 4
		
	def update(self):
		if self.destroying > 0:
			self.destroying -= 1
			if self.destroying <= 0:
				self.destroyed = 1
				
		if self.destoryed:
			self.rTimer -= 1
			if self.rTimer <= 0:
				self.reform()
				
		if self.fading > 0:
			self.fading -= 1
			self.ocpacity -= 25
			if self.ocpacity < 0:
				self.ocpacity = 0
		
		if self.appearing > 0:
			self.appearing -= 1
			self.ocpacity += 25
			if self.ocpacity > 100:
				self.ocpacity = 100
				
class Door:
	def __init__(self, x, y, dest, type, dir):
		self.x = x
		self.y = y
		self.dest = dest
		self.type = type
		self.dir = dir
		self.opened = 0
		self.opening = 0
		self.closing = 0
		self.cTime = 0
		self.frame = 0
		
	def update(self):
		if self.opening > 0:
			frame += 1
			self.opening -= 1
			if self.opening <= 0:
				self.opened = 1
				self.cTime = 60
				
		if self.closing > 0:
			self.frame -= 1
			self.closing -= 1
			if self.closing <= 0:
				self.opened = 0
		
		if self.cTime > 0:
			self.cTime -= 1
			if self.cTime <= 0:
				self.close()
				
	def open(self):
		self.opening = 3
		
	def close(self):
		self.closing = 3
		
class Item:
	def __init__(self, x, y, type):
		self.x = x
		self.y = y
		self.type = type
		self.frame = frame
		self.life = 0
		self.active = 0
		self.collected = 0
		
	def update(self):
		self.frame += 1
		self.life -= 1
		
	def collect(self):
		self.collected = 1
		
class Bomb:
	def __init__(self, x, y, type):
		self.x = x
		self.y = y
		self.type = type
		self.time = 30
		self.frame = 0
		
	def update(self):
		self.time -= 1
		if self.time <= 0:
			self.explode()
		self.frame += 1
		
	def explode(self):
		return 0
		
class Elevator:
	def __init__(self, x, y, dir, dest):
		self.x = x
		self.y = y
		self.dir = dir
		self.dest = dest
		self.useable = 1
		self.moving = 0
		
	def use(self):
		self.moving = 1
		self.useable = 0