import pygame
from math import cos, pi, sin, atan, atan2
colors = {
  "1":(255,0,0),
  "2":(0,255,0),
  "3":(0,0,255)
}

wall1 = pygame.image.load('./wall1.png')
wall2 = pygame.image.load('./wall2.png')
wall3 = pygame.image.load('./wall3.png')
wall4 = pygame.image.load('./wall4.png')
wall5 = pygame.image.load('./wall5.png')

textures = {
  "1": wall1,
  "2": wall2,
  "3": wall3,
  "4": wall4,
  "5": wall5,
}

titlescreen = pygame.image.load('./title.png')
hudtext = pygame.image.load('./hud.png')
endscreen = pygame.image.load('./endscreen.png')
tmm = pygame.image.load('./10mm.png')
shotgun = pygame.image.load('./sg.png')

weapons = {
  1 : tmm,
  2 : shotgun
}
enemies = [
  {
    "x": 100,
    "y": 200,
    "texture": pygame.image.load('./sprite2.png')
  },
  {
    "x": 280,
    "y": 190,
    "texture": pygame.image.load('./sprite3.png')
  },
  {
    "x": 225,
    "y": 340,
    "texture": pygame.image.load('./sprite4.png')
  },
  {
    "x": 220,
    "y": 425,
    "texture": pygame.image.load('./sprite1.png')
  },
  {
    "x": 320,
    "y": 420,
    "texture": pygame.image.load('./sprite2.png')
  }
]
class Raycaster:
  def __init__(self, screen):
    _, _, self.width, self.height = screen.get_rect()
    self.screen = screen
    self.blocksize = 50
    self.map =[]
    self.texture_size = 128
    self.ray_distance = 1
    self.ratio = self.texture_size / self.blocksize
    self.halfheight = self.height / 2
    self.zbuffer = [-float('inf') for z in range(0, self.width)]
    self.hudsize_x = 500
    self.hudsize_y = 100
    self.hudratio = max(self.hudsize_x, self.hudsize_y)/max(self.width, self.height)
    self.titlesize = 500
    self.screenratio = self.titlesize/max(self.width,self.height)


    self.player = {
      "x": self.blocksize + 2.5,
      "y": self.blocksize + 2.5,
      "view_angle": pi/3,
      "fov": pi/3,
      "selected_weapon":1
    }

  def point(self, x, y, c):
    screen.set_at((x, y), c)

  def draw_rectangle(self, x, y, texture):
    for cx in range(x, x + self.blocksize):
      for cy in range(y, y + self.blocksize):
        tx = int((cx - x)*self.ratio)
        ty = int((cy - y)*self.ratio)
        c = texture.get_at((tx, ty))
        self.point(cx, cy, c)

  def draw_hud(self,x, y, hudtext):
    for cx in range(x, x+self.hudsize_x):
      for cy in range(y, y+self.hudsize_y):
        tx = int((cx - x)*self.hudratio)
        ty = int((cy - y)*self.hudratio)
        c = hudtext.get_at((tx, ty))
        self.point(cx, cy, c)

  def draw_weapon(self, weapon):
    x = 16
    y = 414
    weapon_x = 157
    weapon_y = 72
    for cx in range(x, x+weapon_x):
      for cy in range(y, y+weapon_y):
        tx = int((cx - x))
        ty = int((cy - y))
        
        c = weapon.get_at((tx, ty))
        if c != (152, 0, 136, 255):
          self.point(cx, cy, c)

  def draw_endscreen(self):
    for cx in range(0, self.width):
      for cy in range(0, self.height):
        tx = int((cx)*self.screenratio)
        ty = int((cy)*self.screenratio)
        c = endscreen.get_at((tx, ty))
        if c != (152, 0, 136, 255):
          self.point(cx, cy, c)


  def draw_titlescreen(self):
    for cx in range(0, self.width):
      for cy in range(0, self.height):
        tx = int((cx)*self.screenratio)
        ty = int((cy)*self.screenratio)
        c = titlescreen.get_at((tx, ty))
        self.point(cx, cy, c)

  def load_map(self, filename):
      with open(filename) as f:
          for line in f.readlines():
              self.map.append(line.replace("\n", ""))

  def cast_ray(self, ray_angle):
    d = 0
    while True:
      x = self.player["x"] + d * cos(ray_angle)
      y = self.player["y"] + d * sin(ray_angle)

      i = int(x/self.blocksize)
      j = int(y/self.blocksize)

      if self.map[j][i] != ' ':
        hitx = x - i*self.blocksize
        hity = y - j*self.blocksize

        if 1 < hitx < self.blocksize-1:
          maxhit = hitx
        else:
          maxhit = hity
        tx = int(maxhit * self.ratio)

        return d, self.map[j][i], tx
        break

      # self.point(int(x), int(y), (255, 255, 255))
      d += self.ray_distance

  def draw_stake(self, x, h, texture, tx):
    
    start = int(self.halfheight - h/2)
    end =  int(self.halfheight + h/2)

    for y in range(start, end):
      ty = int(((y - start)*self.texture_size)/(end - start))
      c = texture.get_at((tx,ty))
      self.point(x, y, c)

  def draw_sprite(self, sprite):
      sprite_a = atan2(sprite["y"] - self.player["y"], sprite["x"] - self.player["x"])  

      sprite_d = ((self.player["x"] - sprite["x"])**2 + (self.player["y"] - sprite["y"])**2)**0.5
      sprite_size = (self.width/sprite_d) * 50

      sprite_x = (sprite_a - self.player["view_angle"])*self.width/self.player["fov"] + self.halfheight - sprite_size/2
      sprite_y = self.halfheight - sprite_size/2

      sprite_x = int(sprite_x)
      sprite_y = int(sprite_y)
      sprite_size = int(sprite_size)

      ratio = self.texture_size/sprite_size
      for x in range(sprite_x, sprite_x + sprite_size):
        for y in range(sprite_y, sprite_y + sprite_size):
          if 0 < x < self.width:
            if self.zbuffer[x] >= sprite_d:
              tx = int((x - sprite_x) * ratio)
              ty = int((y - sprite_y) * ratio)
              c = sprite["texture"].get_at((tx, ty))
              if c != (152, 0, 136, 255):
                self.point(x, y, c)
                self.zbuffer[x] = sprite_d



  def trymove(self, amount, back=False):
    v_angle = self.player["view_angle"]
    d= self.cast_ray(v_angle)[0] if not back else self.cast_ray(v_angle+pi)[0]
    if d > amount:
      self.player["x"] += cos(v_angle)*amount * (-1 if back else 1)
      self.player["y"] += sin(v_angle)*amount * (-1 if back else 1)

  def render(self, screen=None):
    # for x in range(0, int(self.width), self.blocksize):
    #     for y in range(0, self.height, self.blocksize):
    #         i = int(x/self.blocksize)
    #         j = int(y/self.blocksize)
    #         # print(i,j)
    #         if self.map[j][i] != ' ':
    #             self.draw_rectangle(x, y, textures[self.map[j][i]])

    # self.point(10, 10, (255, 0, 0))
    if screen=="Title":
      self.draw_titlescreen()

    else:
      self.point(int(self.player["x"]), int(self.player["y"]), (255,255,255))

      for i in range(0,int(self.width)):
        view_angle = (self.player["view_angle"]) - self.player["fov"]/2 + i * self.player["fov"]/self.width
        d, c, tx = self.cast_ray(view_angle)
        x = i #+ int(self.width)
        h = int(self.width)/(d*cos(view_angle - self.player["view_angle"])) * 50
        self.zbuffer[i] = d

        c = textures[c]
        self.draw_stake(x,h,c, tx)

      for enemy in enemies:
        self.point(enemy["x"], enemy["y"], (255, 0, 0))
        self.draw_sprite(enemy)
      
      
      self.draw_hud(0, self.height-100, hudtext)
      self.draw_weapon(weapons[self.player["selected_weapon"]])

      if self.movement > 5 and not self.endscreen_disabled:
        self.draw_endscreen()
      self.point(10, 10, (255, 0, 0))
       

pygame.init()
screen = pygame.display.set_mode((500, 500),pygame.DOUBLEBUF|pygame.HWACCEL)
screen.set_alpha(None)
r = Raycaster(screen)
r.load_map("map2.txt")

# render loop
framelock = False
r.draw_titlescreen()
r.endscreen_disabled = False
pygame.display.flip()
r.movement = 0
while True:
  if framelock is False:
    screen.fill((0,0,0))
    if pygame.event.get() is not None :
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          exit(0)
        if e.type == pygame.KEYDOWN:
          if e.key == pygame.K_a:
            r.player["view_angle"] -= pi/10
          elif e.key == pygame.K_d:
            r.player["view_angle"] += pi/10
          elif e.key == pygame.K_UP:
            r.trymove(10)
          elif e.key == pygame.K_DOWN:
            r.trymove(10, True)
          elif e.key == pygame.K_1:
            r.player["selected_weapon"] = 1
          elif e.key == pygame.K_2:
            r.player["selected_weapon"] = 2
          elif e.key == pygame.K_LSHIFT:
            r.endscreen_disabled = True
          framelock = True
          r.render()
          pygame.display.update()
          framelock = False
          r.movement +=1
