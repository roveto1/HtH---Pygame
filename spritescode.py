from settings import *
import pygame as pg


vec = pg.math.Vector2


class Jogador(pg.sprite.Sprite):
    def __init__(self, game):
#Lista sprites andando
        self.imagem_direita = []
        self.imagem_direita_dash = []
        self.imagem_esquerda = []
        self.imagem_esquerda_dash = []
        self.index = 0
        self.counter = 0


        self.dash_img = True

        # Lista sprites parado
        self.imagem_idle_direita = []
        self.imagem_idle_direita_dash = []
        self.imagem_idle_esquerda = []
        self.imagem_idle_esquerda_dash = []
        self.indexidle = 0
        self.counteridle = 0

        #Sprite Dash
        self.img_dash_dir = pg.transform.scale(pg.image.load('codigos/spritesimg/JOGADOR/dash.png').convert_alpha(), (53, 24))
        self.img_dash_esq = pg.transform.flip(self.img_dash_dir, True,False)

        #Sprite Pulando/Caindo

        self.img_pulando_dir = pg.transform.scale(pg.image.load('codigos/spritesimg/JOGADOR/pulo1.png').convert_alpha(), (30, 35))
        self.img_pulando_dash_dir = pg.transform.scale(pg.image.load('codigos/spritesimg/JOGADOR/pulo_dash1.png').convert_alpha(), (30, 35))
        self.img_pulando_esq = pg.transform.flip(self.img_pulando_dir, True,False)
        self.img_pulando_dash_esq = pg.transform.flip(self.img_pulando_dash_dir, True,False)

        self.img_caindo_dir = pg.transform.scale(pg.image.load('codigos/spritesimg/JOGADOR/queda1.png').convert_alpha(), (30, 35))
        self.img_caindo_dash_dir = pg.transform.scale(pg.image.load('codigos/spritesimg/JOGADOR/queda_dash1.png').convert_alpha(), (30, 35))
        self.img_caindo_esq = pg.transform.flip(self.img_caindo_dir, True,False)
        self.img_caindo_dash_esq = pg.transform.flip(self.img_caindo_dash_dir, True,False)


        #Gerando as listas de sprites
        for num in range(1,5):
            #Arquivos andando
            img_direita = pg.image.load(f'codigos/spritesimg/JOGADOR/andando{num}.png').convert_alpha()
            img_direita = pg.transform.scale(img_direita,(30,40))
            img_esquerda = pg.transform.flip(img_direita, True,False)

            img_direita_dash = pg.image.load(f'codigos/spritesimg/JOGADOR/andando_dash{num}.png').convert_alpha()
            img_direita_dash = pg.transform.scale(img_direita_dash,(30,40))
            img_esquerda_dash = pg.transform.flip(img_direita_dash, True,False)

            self.imagem_direita.append(img_direita)
            self.imagem_esquerda.append(img_esquerda)
            self.imagem_direita_dash.append(img_direita_dash)
            self.imagem_esquerda_dash.append(img_esquerda_dash)

            #Arquivos idle
            img_idle_direita = pg.image.load(f'codigos/spritesimg/JOGADOR/idle{num}.png').convert_alpha()
            img_idle_direita = pg.transform.scale(img_idle_direita,(30,40))
            img_idle_esquerda = pg.transform.flip(img_idle_direita, True,False)
            
            img_idle_direita_dash = pg.image.load(f'codigos/spritesimg/JOGADOR/idle_dash{num}.png').convert_alpha()
            img_idle_direita_dash = pg.transform.scale(img_idle_direita_dash,(30,40))
            img_idle_esquerda_dash = pg.transform.flip(img_idle_direita_dash, True,False)

            self.imagem_idle_direita.append(img_idle_direita)
            self.imagem_idle_esquerda.append(img_idle_esquerda)
            self.imagem_idle_direita_dash.append(img_idle_direita_dash)
            self.imagem_idle_esquerda_dash.append(img_idle_esquerda_dash)

        #Sprite presente no jogador
        self.image = self.imagem_direita[self.index]
        self.largura = self.image.get_width()
        self.altura = self.image.get_height()
        self.rect = self.image.get_rect()
        self.direcao = 1
####################

        pg.sprite.Sprite.__init__(self)
        
        self.joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
        self.game = game
        self.rect.center = (largura / 2, altura / 2)
        self.pos = vec(383, 686)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.movendo = False
        self.mplat_ver = False
        self.dashes = 0
        self.dashow = 0
        self.dashvel = 0
        self.pular = 0
        self.float_mod = 0
        self.nColisoes1 = 0
        self.nColisoes2 = 0
        self.nColisoes3 = 0
        self.eColisoes1 = 0
        self.eColisoes2 = 0
        self.eColisoes3 = 0
        self.ratio = 0
        self.ratio2 = 0

        self.tramp = 0
        

        self.spawn_x = 363
        self.spawn_y = 686

        self.counter_tramp = 0
        self.counter_tramp_t = False

        self.recall_update = 0

        self.queda = 0

        self.trampolim_sound = pg.mixer.Sound('codigos/spritesimg/SONS/Trampolim.wav')
        self.trampolim_sound.set_volume(0.05)
        self.dash_sound = pg.mixer.Sound('codigos/spritesimg/SONS/Dash.wav')
        self.dash_sound.set_volume(0.05)
        self.pulo_sound = pg.mixer.Sound('codigos/spritesimg/SONS/Pulo.wav')
        self.pulo_sound.set_volume(0.1)

    def pulo(self):
        if self.game.fase_atual != 10:
            self.game.pode_contar = True
        self.rect.x += 1
        ponto_c = pg.sprite.spritecollide(self, self.game.pontos2_gp, False)
        self.rect.x -= 1
        if self.pular == 1 or ponto_c:
            self.pulo_sound.play()
            self.pular = 0
            self.game.pulinho = True
            self.vel.y = jogador_pulo
            if ponto_c:
                self.dashes = 1




    def dash(self):
        if self.game.fase_atual != 10:
            self.game.pode_contar = True
        if self.dashes > 0:
            self.dash_sound.play()
            self.float_mod = 0
            self.dashow = dash_duracao
            if self.direcao == 1:
                self.dashvel += jogador_dash
            if self.direcao == -1:
                self.dashvel += -jogador_dash
            self.dashes -= 1

    def move_L(self):
        if self.game.fase_atual != 10:
            self.game.pode_contar = True
        self.counter += 1 
        self.direcao = -1
        self.movendo = True
        self.vel.x = -jogador_velo
        

    def move_R(self):
        if self.game.fase_atual != 10:
            self.game.pode_contar = True
        self.counter += 1
        self.direcao = 1
        self.movendo = True
        self.vel.x = jogador_velo
        

    def update(self):

        if not(self.game.emfase):
            self.game.prox_fase_counter += 1
            if self.game.prox_fase_counter == 10:
                self.game.prox_fase_counter = 0
                self.game.emfase = True

        if self.recall_update < 10:
            self.recall_update += 1

        if self.counter_tramp_t:
            self.counter_tramp += 1
            if self.counter_tramp > 60:
                self.counter_tramp = 0
                self.counter_tramp_t = False

        if self.dashow != 0: self.dashow -= 1   
        self.acc = vec(0, jogador_grav)

        if self.dashvel != 0:
            self.vel.x = self.dashvel
            self.vel.y = 0
        
        if self.dashes > 0:
            self.dash_img = True
        else:
            self.dash_img = False

        
        
##########
 #Animação Andando
        self.tempo_andando = 10

        if self.counter > self.tempo_andando:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.imagem_direita):
                self.index = 0
            if self.dash_img:
                if self.direcao == 1:
                    self.image = self.imagem_direita[self.index]
                if self.direcao == -1:
                    self.image = self.imagem_esquerda[self.index]
            else:
                if self.direcao == 1:
                    self.image = self.imagem_direita[self.index]
                if self.direcao == -1:
                    self.image = self.imagem_esquerda[self.index]


    #Animação Parado
        self.tempo_parado = 10
        self.counteridle += 1

        if self.counteridle > self.tempo_parado:
            self.counteridle = 0
            self.indexidle += 1
            if self.indexidle >= len(self.imagem_idle_direita):
                self.indexidle = 0
            if self.dash_img:
                if self.direcao == 1 and not(self.movendo):
                    self.image = self.imagem_idle_direita[self.indexidle]
                if self.direcao == -1 and not(self.movendo):
                    self.image = self.imagem_idle_esquerda[self.indexidle]
            else:
                if self.direcao == 1 and not(self.movendo):
                    self.image = self.imagem_idle_direita[self.indexidle]
                if self.direcao == -1 and not(self.movendo):
                    self.image = self.imagem_idle_esquerda[self.indexidle]


    #Sprite Pulando
        if self.vel.y < 0:
            if self.dash_img:
                if self.direcao == 1:
                    self.image = self.img_pulando_dir
                if self.direcao == -1:
                    self.image = self.img_pulando_esq
            else:
                if self.direcao == 1:
                    self.image = self.img_pulando_dir
                if self.direcao == -1:
                    self.image = self.img_pulando_esq

        
    #dash
        if self.vel.x > jogador_velo:
            self.image = self.img_dash_dir

        if self.vel.x < -jogador_velo:
            self.image = self.img_dash_esq

    #COLISAO


        for tramp in self.game.trampolins_geral:
            self.ratio = self.rect.x + (self.vel.x*1.5), self.rect.y + 1, self.largura, self.altura - 1
            if tramp.rect.colliderect(self.ratio):
                self.trampolim_sound.play()
                self.dashow = 0
                self.float_mod = 0
                self.tramp = tramp
                if self.vel.y > 0:
                    self.vel.y = trampolim_vel #- (self.queda//25)
                else: self.vel.y = trampolim_vel
                self.dashes = 1
        
        for torre in self.game.torres_geral:
            self.eColisoes1 = 1
            self.ratio = self.rect.x + (self.vel.x*1.5), self.rect.y + 1, self.largura, self.altura - 1
            self.ratio2 = self.rect.x + 1, self.rect.y + self.vel.y + 1, self.largura - 2, self.altura
            if torre.colliderect(self.ratio):
                self.nColisoes1 = 0
                self.vel.x = 0

            elif torre.colliderect(self.ratio2):
                self.nColisoes1 = 0
                if self.vel.y < -1:
                    self.pos.y = torre.bottom + 40
                    self.vel.y = 0
                if self.vel.y > 0:
                    self.float_mod = 0
                    self.pos.y = torre.top
                    self.dashes = 1
                    self.vel.y = 0

            else:
                self.nColisoes1 = 1


            if self.vel.y == 0:
                self.pular = 1

            elif not(self.mplat_ver):
                self.pular = 0
            

        
        for plat in self.game.movelplat_geral:
            self.eColisoes2 = 1
            self.ratio = self.rect.x + (self.vel.x*1.5), self.rect.y + 3, self.largura, self.altura-10
            self.ratioL = self.rect.x + (self.vel.x*1.5), self.rect.y + 3, 2, self.altura-10
            self.ratioR = self.rect.x + (self.vel.x*1.5) + self.largura, self.rect.y + 3, 2, self.altura-10
            self.ratio2 = self.rect.x+7, self.rect.y + self.vel.y + abs(plat.velo_movendo), self.largura/2, self.altura
            if plat.rect.colliderect(self.ratio):
                self.nColisoes2 = 0
                self.vel.x = 0
                if plat.hor == 1:
                    if plat.rect.colliderect(self.ratioL):
                        self.pos.x = plat.rect.right + 15
                    if plat.rect.colliderect(self.ratioR):
                        self.pos.x = plat.rect.left - 15



            elif plat.rect.colliderect(self.ratio2):
                self.nColisoes2 = 0
                if self.vel.y < 0:
                    self.pos.y = plat.rect.bottom + 40
                    self.vel.y = 0
                if self.vel.y > 0:
                    self.pular = 1
                    self.pos.y = plat.rect.top
                    if plat.hor == 1:
                        if plat.value == 0:
                            self.vel.x += plat.velo_movendo
                        self.float_mod = plat.velo_movendo
                    if plat.ver == 1:
                        self.float_mod = 0
                        if plat.velo_movendo > 0:
                            self.vel.y = plat.velo_movendo - 1
                        else:
                            self.vel.y = 0
                        self.mplat_ver = True
                    else:
                        self.vel.y = 0
                        self.mplat_ver = False
                    self.dashes = 1

            else:
                self.mplat_ver = False
                self.nColisoes2 = 1
        
            #Sprite Caindo
        if self.vel.y > 1 and not(self.mplat_ver):
            if self.dash_img:
                if self.direcao == 1:
                    self.image = self.img_caindo_dir
                if self.direcao == -1:
                    self.image = self.img_caindo_esq
            else:
                if self.direcao == 1:
                    self.image = self.img_caindo_dir
                if self.direcao == -1:
                    self.image = self.img_caindo_esq

        for plat in self.game.plataformas_geral:
            self.eColisoes1 = 1
            self.ratio = self.rect.x + (self.vel.x*1.5), self.rect.y + 1, self.largura, self.altura - 1
            self.ratio2 = self.rect.x + 1, self.rect.y + self.vel.y + 1, self.largura - 2, self.altura
            if plat.colliderect(self.ratio):
                self.nColisoes1 = 0
                self.vel.x = 0

            elif plat.colliderect(self.ratio2):
                self.nColisoes1 = 0
                if self.vel.y < -1:
                    self.pos.y = plat.bottom + 40
                    self.vel.y = 0
                if self.vel.y > 0:
                    self.float_mod = 0
                    self.pos.y = plat.top
                    self.dashes = 1
                    self.vel.y = 0
                    self.pular = 1

            else:
                self.nColisoes1 = 1
                


        for plat in self.game.platvar_geral:
            self.eColisoes3 = 1
            self.ratio = self.rect.x + self.vel.x, self.rect.y + 3, self.largura, self.altura-10
            self.ratio2 = self.rect.x, self.rect.y + self.vel.y + 1 + 35, self.largura, self.altura - 35
            if plat.colliderect(self.ratio):
                pass


            elif plat.colliderect(self.ratio2):
                self.nColisoes3 = 0
                self.float_mod = 0
                if self.vel.y > 0:
                    self.pular = 1
                    self.pos.y = plat.top + 1
                    self.dashes = 1
                    self.vel.y = 0


            else:
                self.nColisoes3 = 1


        if self.dashvel == 0:
            self.vel.y += self.acc.y 
        
        if self.tramp != 0:
            self.tramp.image = pg.image.load('codigos/spritesimg/OBJETOS/trampolim2.png').convert_alpha()
            self.counter_tramp_t = True
            if self.counter_tramp == 60:
                self.tramp.image = pg.image.load('codigos/spritesimg/OBJETOS/trampolim1.png').convert_alpha()
                self.tramp = 0


        self.pos.y += self.vel.y

        self.pos.x += self.vel.x



        if self.dashow == 0: self.dashvel = 0
        

        if self.game.fase_atual != 10:
            if self.pos.x < 15 + 351:
                self.pos.x = 15 + 351
            if self.pos.x > 928 - 15:
                self.pos.x = 928 - 15
            if self.pos.y >= altura: self.pos.y = altura - 32
        
        if self.vel.y > 5: self.vel.y = 5

        if self.vel.y > 1:
            self.queda += 1
        else: self.queda = 0

        if self.queda >= 50:
            self.queda = 50

        self.rect.midbottom = self.pos

        self.nColisoes1 = 0
        self.nColisoes2 = 0
        self.nColisoes3 = 0
        self.eColisoes = 0
        self.vel.x = 0

class Plataforma(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(verde)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Torre(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(verde)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class PlataformaVar(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(verde)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ponto2(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((48 , 48))
        self.rect = self.image.get_rect()

        self.rect.x = x - 10
        self.rect.y = y - 10


class Trampolim(pg.sprite.Sprite):
    def __init__(self, x, y):

        self.imagem_trampolim = []
        self.index = 0
        self.counter = 0

        for num in range(1,3):

            #Arquivos Trampolim
            img_tramp = pg.image.load(f'codigos/spritesimg/OBJETOS/trampolim{num}.png').convert_alpha()
            img_tramp = pg.transform.scale(img_tramp,(32,26))

            self.imagem_trampolim.append(img_tramp)

        self.image = self.imagem_trampolim[self.index]
        self.rect = self.image.get_rect()

        pg.sprite.Sprite.__init__(self) 
        self.rect.x = x
        self.rect.y = y
       
        





class Espinho(pg.sprite.Sprite): #
    def __init__(self, x, y, w, h): #
        pg.sprite.Sprite.__init__(self)#
        self.image = pg.Surface((w, h))#
        self.image.fill(vermelho)#
        self.rect = self.image.get_rect()#
        self.rect.x = x#
        self.rect.y = y#

class Vida1(pg.sprite.Sprite): #
    def __init__(self, game): #
        pg.sprite.Sprite.__init__(self)#
        self.image = pg.image.load('codigos/spritesimg/ICONS/vida1.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()#
        self.rect.x = 20#
        self.rect.y = 20#


class Vida2(pg.sprite.Sprite): #
    def __init__(self, game): #
        pg.sprite.Sprite.__init__(self)#
        self.image = pg.image.load('codigos/spritesimg/ICONS/vida1.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()#
        self.rect.x = 55#
        self.rect.y = 20#

class Vida3(pg.sprite.Sprite): #
    def __init__(self, game): #
        pg.sprite.Sprite.__init__(self)#
        self.image = pg.image.load('codigos/spritesimg/ICONS/vida1.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()#
        self.rect.x = 90#
        self.rect.y = 20#


class Passou(pg.sprite.Sprite): #
    def __init__(self, x, y, w, h): #
        pg.sprite.Sprite.__init__(self)#
        self.image = pg.Surface((w, h))#
        self.image.fill(roxo)#
        self.rect = self.image.get_rect()#
        self.rect.x = x#
        self.rect.y = y#

class MovelPlataforma(pg.sprite.Sprite):
    def __init__(self,x,y,v,t,hor,ver,dire):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("codigos/spritesimg/OBJETOS/platmovel.png").convert_alpha()
        self.image = pg.transform.scale(self.image,(65,11))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velo_movendo = v
        self.tempo_movendo = 0
        self.range = t
        self.hor = hor
        self.ver = ver
        self.dire = dire
        self.value = 0

        self.velo_movendo *= self.dire
    
    def update(self):
        if self.value < 2:
            self.value += 1
        else:
            self.value = 0

        if self.value == 0:
            if self.hor == 1:
                self.rect.x += self.velo_movendo
            if self.ver == 1:
                self.rect.y += self.velo_movendo


        self.tempo_movendo += 1
        if abs(self.tempo_movendo) > self.range:
            self.velo_movendo *= -1
            self.tempo_movendo *= -1

class Projetil(pg.sprite.Sprite):
    def __init__(self,x,y,v,hor,ver,dire):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("codigos/spritesimg/ICONS/pelota.png").convert_alpha()
        self.image = pg.transform.scale(self.image,(8,8))
        self.rect = self.image.get_rect()

        self.spawn_x = x
        self.spawn_y = y

        self.x = x
        self.y = y

        self.rect.x = self.x
        self.rect.y = self.y
        self.velo_movendo = v
        self.hor = hor
        self.ver = ver
        self.dire = dire
        self.velo_movendo *= self.dire


    def update(self):
        self.rect.x += self.velo_movendo * self.hor
        self.rect.y += self.velo_movendo * self.ver
        if (self.rect.x < 0) or (self.rect.x > largura) or (self.rect.y > altura) or (self.rect.y < 0):
            self.rect.x = self.x
            self.rect.y = self.y
    

def Fases(num,bg,bg_e,spx,spy):

    lista_geral = []

    saida_plat = 'self.plat_lista'
    saida_torre = 'self.torre_lista'
    saida_point = 'self.point_lista'
    saida_tramp = 'self.tramp_lista'
    saida_spike = 'self.spike_lista'
    saida_platvar = 'self.platvar_lista'
    saida_pass = 'self.pass_lista'
    saida_projetil = 'self.projetil_lista'
    saida_movelplat = 'self.movelplataforma_lista'

    saida_jogsp_x = 'self.jogador.spawn_x'
    saida_jogsp_y = 'self.jogador.spawn_y'


    plat_lista = f"plataformas_lst{num}"
    torre_lista = f"torre_lst{num}"
    point_lista = f"pontos_lst{num}"
    tramp_lista = f"trampolins_lst{num}"
    spike_lista = f"espinhos_lst{num}"
    platvar_lista = f"platvar_lst{num}"
    pass_lista = f"passou_lst{num}"
    projetil_lista = f"projetil_lst{num}"
    movelplataforma_lista = f"movelplataformas_lst{num}" 

    jogsp_x = spx
    jogsp_y = spy

    background = bg
    background_e = bg_e

    template = "{} = {}"

    state_plat = template.format(saida_plat, plat_lista)
    state_torre = template.format(saida_torre, torre_lista)
    state_point = template.format(saida_point, point_lista)
    state_tramp = template.format(saida_tramp, tramp_lista)
    state_spike = template.format(saida_spike, spike_lista)
    state_platvar = template.format(saida_platvar, platvar_lista)
    state_pass = template.format(saida_pass, pass_lista)
    state_projetil = template.format(saida_projetil, projetil_lista)
    state_movelplataforma = template.format(saida_movelplat, movelplataforma_lista)
    state_jogsp_x = template.format(saida_jogsp_x, jogsp_x)
    state_jogsp_y = template.format(saida_jogsp_y, jogsp_y)


    lista_geral.append(state_plat)
    lista_geral.append(state_torre)
    lista_geral.append(state_point)
    lista_geral.append(state_tramp)
    lista_geral.append(state_spike)
    lista_geral.append(state_platvar)
    lista_geral.append(state_pass)
    lista_geral.append(state_projetil)
    lista_geral.append(state_movelplataforma)

    lista_geral.append(background)
    lista_geral.append(background_e)

    lista_geral.append(state_jogsp_x)
    lista_geral.append(state_jogsp_y)

    return lista_geral

