from cmath import rect
from pickle import TRUE
import pygame as pg
import random
from settings import *
from spritescode import *

vec = pg.math.Vector2

class Game:
    def __init__(self):
        # janela e outros
        pg.init()
        pg.mixer.init()
        pg.font.init()
        pg.display.set_caption(titulo)
        pg.mouse.set_visible(False)

        self.tela = pg.display.set_mode((largura, altura))

        self.fonte = pg.font.Font('codigos/spritesimg/FONTE/REDENSEK.TTF',50) 
        self.fonte3 = pg.font.Font('codigos/spritesimg/FONTE/REDENSEK.TTF',80) 
        self.fonte2 = pg.font.Font('codigos/spritesimg/FONTE/REDENSEK.TTF',25)

        self.clock = pg.time.Clock()

        self.rodando = True

        self.var1 = 1
        self.var2 = 1
        self.var3 = 0

        self.vidas = 3
        self.dashes = 0

        self.bg = pg.image.load('codigos/spritesimg/BACKGROWND/Level_1.png').convert_alpha()
        self.bordas = pg.image.load('codigos/spritesimg/BACKGROWND/bordas.png').convert_alpha() 
        self.mapa = pg.image.load('codigos/spritesimg/ICONS/MAPA/mapas1.png').convert_alpha()
        self.mapa = pg.transform.scale(self.mapa, (60, 270))
        self.bg_e = pg.image.load('codigos/spritesimg/BACKGROWND/vazio.png').convert_alpha()
        self.icone = pg.image.load('codigos/spritesimg/ICONS/vida1.png').convert_alpha()
        self.icone = pg.transform.scale(self.icone,(32,32))
        pg.display.set_icon(self.icone)

        self.movelplataforma_lista = movelplataformas_lst1 
        self.projetil_lista = projetil_lst1 
        self.plat_lista = plataformas_lst1
        self.torre_lista = torre_lst1
        self.platvar_lista = platvar_lst1
        self.point_lista = pontos_lst1
        self.tramp_lista = trampolins_lst1
        self.spike_lista = espinhos_lst1
        self.pass_lista = passou_lst1

        self.jogador = Jogador(self)
        self.jogador_sp = pg.sprite.Group()
        self.jogador_sp.add(self.jogador)

        self.fase_atual = 1
        self.reload = False

        self.hp0_counter = 60
        self.hp0_counter_set = 0
        self.hp0_hold = 120

        self.pulinho = False

        self.emfase = False

        self.seg_d = 0
        self.d_segundos = 0
        self.segundos_u = 0
        self.segundos_u2 = -1
        self.segundos_d = 0
        self.minutos_u = 0
        self.minutos_d = 0
        self.horas = 0
        self.segundos_u_sv = 0
        self.segundos_d_sv = 0
        self.minutos_u_sv = 0
        self.minutos_d_sv = 0
        self.horas_sv = 0
        self.float_time2 = 0

        self.prox_fase_counter = 0

        self.pode_contar = False

        self.passou_sound = pg.mixer.Sound('codigos/spritesimg/SONS/Passou.wav')
        self.passou_sound.set_volume(0.1)

        self.hit_sound = pg.mixer.Sound('codigos/spritesimg/SONS/Hit.wav')
        self.hit_sound.set_volume(0.3)

        self.musica = pg.mixer.music.load('codigos/spritesimg/MUSICAS/Cenario1.mp3')
        pg.mixer.music.set_volume(0.05)
        pg.mixer.music.play(-1)
    def new(self):
        # Novo Jogo
        self.sprites_gp = pg.sprite.Group() # GRUPO GERAL

        self.plataformas_gp = pg.sprite.Group() # GRUPOS INDIVIDUAIS
        self.platvar_gp = pg.sprite.Group()
        self.movelplataforma_gp = pg.sprite.Group() 
        self.torres_gp = pg.sprite.Group()
        self.projetil_gp = pg.sprite.Group() 
        self.trampolins_gp = pg.sprite.Group()
        self.pontos2_gp = pg.sprite.Group()
        self.espinho_gp = pg.sprite.Group()
        self.vidas_gp = pg.sprite.Group()
        self.passou_gp = pg.sprite.Group() 

        self.hp1 = Vida1(self)
        self.hp2 = Vida2(self)
        self.hp3 = Vida3(self)

        self.sprites_gp.add(self.hp1)
        self.sprites_gp.add(self.hp2)
        self.sprites_gp.add(self.hp3)

        ##################################################################### CONSTRUÇÃO DE FASE
        
        self.plataformas_geral = []
        self.platvar_geral = []
        self.movelplat_geral = []
        self.projeteis_geral = []
        self.torres_geral = []
        self.trampolins_geral = []

        for plat in self.plat_lista:
            p = Plataforma(*plat)
            p2 = p.rect
            self.plataformas_geral.append(p2)
            self.plataformas_gp.add(p)
        
        for platvar in self.platvar_lista:
            p = PlataformaVar(*platvar)
            p2 = p.rect
            self.platvar_geral.append(p2)
            self.platvar_gp.add(p)

        for moveplat in self.movelplataforma_lista: 
            p = MovelPlataforma(*moveplat)
            self.movelplat_geral.append(p)
            self.movelplataforma_gp.add(p)

        for torre in self.torre_lista:
            p = Torre(*torre)
            p2 = p.rect
            self.torres_geral.append(p2)
            self.torres_gp.add(p)

        for proj in self.projetil_lista: 
            p = Projetil(*proj)
            self.projeteis_geral.append(p)
            self.projetil_gp.add(p)

        for ponto2 in self.point_lista:
            p = Ponto2(*ponto2)
            self.pontos2_gp.add(p)

        for tramp in self.tramp_lista:
            p = Trampolim(*tramp)
            self.trampolins_geral.append(p)            
            self.trampolins_gp.add(p)

        for esp in self.spike_lista:
            p = Espinho(*esp)
            self.espinho_gp.add(p)

        for pas in self.pass_lista:  
            p = Passou(*pas)
            self.passou_gp.add(p)


        self.run()

    def run(self):
        
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update

        ##################################################################### TIMER
        self.tempo = pg.time.get_ticks()
        if self.pode_contar:
            self.d_segundos = str((self.tempo - self.float_time2) // 10)


            if int(self.d_segundos) > 99:
                self.d_segundos = '0'
                self.float_time2 = self.tempo
                self.segundos_u2 += 1

            if self.segundos_u2 > 9:
                self.segundos_u2 = 0
                self.segundos_u = 0
                self.segundos_d += 1
            
            if self.segundos_d > 5:
                self.segundos_d = 0
                self.minutos_u += 1
            
            if self.minutos_u > 9:
                self.minutos_u = 0
                self.minutos_d += 1
            
            if self.minutos_d > 5:
                self.minutos_d = 0
                self.horas += 1
                
        if self.segundos_u2 >= self.segundos_u:
            self.segundos_u = self.segundos_u2

        if self.fase_atual == 10:
            self.pode_contar = False
            self.segundos_u_sv = str(self.segundos_u)
            self.segundos_d_sv = str(self.segundos_d)
            self.minutos_u_sv = str(self.minutos_u)
            self.minutos_d_sv = str(self.minutos_d)
            self.horas_sv = str(self.horas)

            self.tempo_jogo = self.horas_sv + ":" + self.minutos_d_sv + self.minutos_u_sv + ":" + self.segundos_d_sv + self.segundos_u_sv

            self.time = self.fonte3.render(self.tempo_jogo,False,(branco))
            self.time_rect = self.time.get_rect(center = (largura/2,(altura/2)-80))

            self.fim = self.fonte2.render('FECHE O JOGO APERTANDO ESC OU PULE DA TORRE PARA JOGAR DENOVO', False,(branco))
            self.fim_rect = self.fim.get_rect(center = (largura/2,(altura/2)-30))


        self.dseg = self.fonte2.render(str(self.d_segundos),False,(branco))
        self.dseg_rect = self.dseg.get_rect(topleft = (largura - 40,40))

        self.seg = self.fonte.render(str(self.segundos_u),False,(branco))
        self.seg_rect = self.seg.get_rect(topleft = (largura - 65,20))

        self.segd = self.fonte.render(str(self.segundos_d),False,(branco))
        self.segd_rect = self.segd.get_rect(topleft = (largura - 87,20))
        
        self.minu = self.fonte.render(f"{self.minutos_u}:",False,(branco))
        self.minu_rect = self.minu.get_rect(topleft = (largura - 118,20))
       
        self.mind = self.fonte.render(f"{self.minutos_d}",False,(branco))
        self.mind_rect = self.mind.get_rect(topleft = (largura - 140,20))
        
        self.hor = self.fonte.render(f"{self.horas}:",False,(branco))
        self.hor_rect = self.hor.get_rect(topleft = (largura - 171,20))

        #####################################################################

        if self.jogador.vel.y == 0: #pulo quantitativo
            self.pulinho = False

        self.hp0_counter += 1 


        self.dashes = self.jogador.dashes

        ##################################################################### COLISOES
        self.passou_c = pg.sprite.spritecollide(self.jogador, self.passou_gp, True) 
        self.tramp_c = pg.sprite.spritecollide(self.jogador, self.trampolins_gp, False)
        self.espinho_c = pg.sprite.spritecollide(self.jogador, self.espinho_gp, False)
        self.ponto_c = pg.sprite.spritecollide(self.jogador, self.pontos2_gp, False)
        self.projetil_c = pg.sprite.spritecollide(self.jogador,self.projetil_gp,False)

        for proj in self.projeteis_geral:
            if proj.hor == 1:
                if proj.dire == 1:
                    if proj.rect.left >= 928:
                        proj.rect.right = proj.spawn_x
                elif proj.dire == -1:
                    if proj.rect.right <= 351:
                        proj.rect.left = proj.spawn_x
            if proj.ver == 1:
                if proj.dire == 1:
                    if proj.rect.top >= altura:
                        proj.rect.bottom = proj.spawn_y
                elif proj.dire == -1:
                    if proj.rect.bottom <= 0:
                        proj.rect.top = proj.spawn_y
            for plat in self.plataformas_geral:
                if proj.rect.colliderect(plat):
                    if proj.hor == 1:
                        if proj.dire == 1:
                            if proj.rect.left >= plat.left:
                                proj.rect.right = proj.spawn_x
                        elif proj.dire == -1:
                            if proj.rect.right <= plat.right:
                                proj.rect.left = proj.spawn_x
                    elif proj.ver == 1:
                        if proj.dire == 1:
                            if proj.rect.top >= plat.top:
                                proj.rect.top = proj.spawn_y
                        elif proj.dire == -1:
                            if proj.rect.bottom <= plat.bottom:
                                proj.rect.bottom = proj.spawn_y

        #####################################################################
                            
        ##################################################################### FULLSCREEN
        if self.var3 == 1: 
            self.tela = pg.display.set_mode((largura, altura), pg.FULLSCREEN)

        elif self.var3 == 2:
            self.tela = pg.display.set_mode((largura, altura))
            self.var3 = 0
        #####################################################################

        self.keys = pg.key.get_pressed()

        self.sprites_gp.update()
        self.projetil_gp.update()
        self.movelplataforma_gp.update()
        self.jogador_sp.update()


        ##################################################################### MOVIMENTO TECLADO
        if self.var1 == 0 or self.keys[pg.K_LEFT]:
            self.jogador.move_L()
            self.var2 = 1
        if self.var2 == 0 or self.keys[pg.K_RIGHT]:
            self.jogador.move_R()
            self.var1 = 1
        #####################################################################

        ##################################################################### PASSAR DE FASE
        if self.passou_c or self.reload: 

            if self.emfase:
                self.fase_atual += 1
            
            if self.fase_atual == 4 or self.fase_atual == 7:
                self.vidas = 3

            if self.fase_atual > 10:
                self.musica = pg.mixer.music.load('codigos/spritesimg/MUSICAS/Cenario1.mp3')
                pg.mixer.music.set_volume(0.05)
                pg.mixer.music.play(-1)
                self.fase_atual = 1
                self.float_time2 = self.tempo
                self.d_segundos = 0
                self.segundos_d = 0
                self.segundos_u = 0
                self.segundos_u2 = -1
                self.minutos_d = 0
                self.minutos_u = 0
                self.horas = 0
                self.vidas = 3
                self.jogador.pos.x = 383 
                self.jogador.pos.y = 688



            self.fase = Fases(self.fase_atual,bg_lst[self.fase_atual],bg_extra_lst[self.fase_atual],spx_lst[self.fase_atual],spy_lst[self.fase_atual])


            self.jogador.pos.y = altura - 32
            if not(self.reload) and self.fase_atual != 1: 
                self.passou_sound.play()
                self.jogador.vel.y = -5
                if self.fase_atual == 4:
                    self.musica = pg.mixer.music.load('codigos/spritesimg/MUSICAS/Cenario2.mp3')
                    pg.mixer.music.set_volume(0.05)
                    pg.mixer.music.play(-1)
                if self.fase_atual == 7:
                    self.musica = pg.mixer.music.load('codigos/spritesimg/MUSICAS/Cenario3.wav')
                    pg.mixer.music.set_volume(0.1)
                    pg.mixer.music.play(-1)
                if self.fase_atual == 10:
                    self.musica = pg.mixer.music.load('codigos/spritesimg/MUSICAS/Final.mp3')
                    pg.mixer.music.set_volume(0.1)
                    pg.mixer.music.play(-1)
            self.jogador.nColisoes = 0
            self.hp0_counter = self.hp0_counter_set

            for i in range(9):
                exec(self.fase[i])
 
            self.bg = pg.image.load(self.fase[9]).convert_alpha()
            if self.fase[10] == "0":
                self.bg_e = self.bg_e = pg.image.load('codigos/spritesimg/BACKGROWND/vazio.png').convert_alpha()
            else:
                self.bg_e = pg.image.load(self.fase[10]).convert_alpha()
            self.mapa = pg.image.load(f'codigos/spritesimg/ICONS/MAPA/mapas{self.fase_atual}.png').convert_alpha()
            self.mapa = pg.transform.scale(self.mapa, (60, 270))

            exec(self.fase[11])
            exec(self.fase[12])

            if self.reload:
                self.vidas = 3
                self.jogador.pos.x = self.jogador.spawn_x
            
            self.reload = False

            self.emfase = False
            self.new()

        #####################################################################


        ##################################################################### DANO
        if self.espinho_c and self.jogador.recall_update == 10:
            self.hit_sound.play()
            self.jogador.recall_update = 0
            
            self.jogador.dashvel = 0
            self.jogador.vel.xy = (0,0)
            self.vidas -= 1
            if self.vidas != 0:
                self.jogador.pos.x = self.jogador.spawn_x
                self.jogador.pos.y = self.jogador.spawn_y
            self.hp1.rect.x = 20
            self.hp1.rect.y = 20
            self.hp2.rect.x = 55
            self.hp2.rect.y = 20
            self.hp3.rect.x = 90
            self.hp3.rect.y = 20
            self.hp0_counter = 119

            
        
            
        if self.projetil_c and self.jogador.recall_update == 10:
            self.hit_sound.play()
            self.jogador.recall_update = 0
            
            self.jogador.dashvel = 0
            self.jogador.vel.xy = (0,0)
            self.vidas -= 1
            if self.vidas != 0:
                self.jogador.pos.x = self.jogador.spawn_x
                self.jogador.pos.y = self.jogador.spawn_y
            
            self.hp1.rect.x = 20
            self.hp1.rect.y = 20
            self.hp2.rect.x = 55
            self.hp2.rect.y = 20
            self.hp3.rect.x = 90
            self.hp3.rect.y = 20
            self.hp0_counter = 119
        
        #####################################################################
        
        ##################################################################### ANIMAÇÃO DAS VIDAS
        if self.vidas == 3:

            if self.hp0_counter == self.hp0_hold:
                self.hp3.rect.y += 5
            if self.hp0_counter == self.hp0_hold + self.hp0_hold//2:
                self.hp2.rect.y += 5
            if self.hp0_counter == self.hp0_hold + 2*self.hp0_hold//2:
                self.hp1.rect.y += 5

            if self.hp0_counter == self.hp0_hold + 3*self.hp0_hold//2:
                self.hp3.rect.y -= 5
            if self.hp0_counter == self.hp0_hold + 4*self.hp0_hold//2:
                self.hp2.rect.y -= 5
            if self.hp0_counter == self.hp0_hold + 5*self.hp0_hold//2:
                self.hp1.rect.y -= 5
                self.hp0_counter = self.hp0_hold - self.hp0_hold//2
                self.hp0_counter_set = self.hp0_hold - self.hp0_hold//2
        
  

        if self.vidas == 2:
            self.hp3.image = pg.image.load('codigos/spritesimg/ICONS/vida2.png').convert_alpha()
            self.hp3.image = pg.transform.scale(self.hp3.image, (30, 30))

            if self.hp0_counter == self.hp0_hold:
                self.hp3.rect.y = 25
            if self.hp0_counter == self.hp0_hold + self.hp0_hold//4:
                self.hp2.rect.y += 5
            if self.hp0_counter == self.hp0_hold + 2*self.hp0_hold//4:
                self.hp1.rect.y += 5


            if self.hp0_counter == self.hp0_hold + 4*self.hp0_hold//4:
                self.hp2.rect.y -= 5
            if self.hp0_counter == self.hp0_hold + 5*self.hp0_hold//4:
                self.hp1.rect.y -= 5
                self.hp0_counter = self.hp0_hold - self.hp0_hold//4
                self.hp0_counter_set = self.hp0_hold - self.hp0_hold//4


            
        if self.vidas == 1:
            self.hp3.image = pg.image.load('codigos/spritesimg/ICONS/vida2.png').convert_alpha()
            self.hp3.image = pg.transform.scale(self.hp3.image, (30, 30))
            self.hp2.image = pg.image.load('codigos/spritesimg/ICONS/vida2.png').convert_alpha()
            self.hp2.image = pg.transform.scale(self.hp2.image, (30, 30))
        
            if self.hp0_counter == self.hp0_hold:
                self.hp3.rect.y = 25
            if self.hp0_counter == self.hp0_hold + self.hp0_hold//48:
                self.hp2.rect.y = 25
            if self.hp0_counter == self.hp0_hold + 2*self.hp0_hold//48:
                self.hp1.rect.y += 5


            if self.hp0_counter == self.hp0_hold + 5*self.hp0_hold//48:

                self.hp1.rect.y -= 5
                self.hp0_counter = self.hp0_hold - self.hp0_hold//48
           
                self.hp0_counter_set = self.hp0_hold - self.hp0_hold//48



            
        if self.vidas <= 0:
            # self.tela = pg.display.set_mode((largura, altura))
            self.hp3.image = pg.image.load('codigos/spritesimg/ICONS/vida2.png').convert_alpha()
            self.hp3.image = pg.transform.scale(self.hp3.image, (30, 30))
            self.hp2.image = pg.image.load('codigos/spritesimg/ICONS/vida2.png').convert_alpha()
            self.hp2.image = pg.transform.scale(self.hp2.image, (30, 30))
            self.hp1.image = pg.image.load('codigos/spritesimg/ICONS/vida2.png').convert_alpha()
            self.hp1.image = pg.transform.scale(self.hp1.image, (30, 30))

            self.vidas = 3
            if self.fase_atual < 4:
                self.fase_atual = 0
            elif self.fase_atual < 7:
                self.fase_atual = 3
            else:
                self.fase_atual = 6
            self.reload = True

    def events(self):
        # Game Loop - Eventos
        for evento in pg.event.get():
            # FECHAR JANELA
            ##################################################################### FECHAR JOGO
            if evento.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.rodando = False

            ##################################################################### BOTAO DOWN
            if evento.type == pg.JOYBUTTONDOWN:

                if evento.button == 0:  # A
                    self.jogador.pulo()

                if evento.button == 2:  # X
                    self.jogador.dash()

                if evento.button == 6: # SELECT
                    self.vidas = 3
                    self.new()

            ##################################################################### BOTAO UP
            if evento.type == pg.JOYBUTTONUP:

                if evento.button == 0 and self.pulinho:  # A
                    if self.jogador.vel.y < 0:
                        self.jogador.vel.y = 0


            ##################################################################### KEY DOWN
            if evento.type == pg.KEYDOWN:

                if evento.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.rodando = False

                if evento.key == pg.K_r:
                    self.vidas == 999

                if evento.key == pg.K_UP:
                    self.jogador.pulo()

                if evento.key == pg.K_z:
                    self.jogador.dash()

                if evento.key == pg.K_1:
                    self.var3 += 1

                if evento.key == pg.K_LEFT:
                    self.var1 = 0

                if evento.key == pg.K_RIGHT:
                    self.var2 = 0
            
            ##################################################################### KEY UP
            if evento.type == pg.KEYUP:

                if evento.key == pg.K_LEFT or evento.key == pg.K_RIGHT:
                    self.var1 = 1
                    self.var2 = 1
                    self.jogador.movendo = False

                if evento.key == pg.K_UP and self.pulinho:
                    if self.jogador.vel.y < 0:
                        self.jogador.vel.y = 0
            
            ##################################################################### SETINHAS
            if evento.type == pg.JOYHATMOTION: 
                if evento.value[0] == -1:
                    self.var1 = 0

                if evento.value[0] == 1:
                    self.var2 = 0

                if evento.value[0] == 0:
                    self.var1 = 1
                    self.var2 = 1
                    self.jogador.movendo = False

            ##################################################################### ANALOGICO
            if evento.type == pg.JOYAXISMOTION:

                if evento.axis == 0:
                    if evento.value > 0:
                        if evento.value > 0.8: self.jogador.movendo_factor = 1
                        else: self.jogador.movendo_factor = evento.value
                        self.var2 = 0 #MOVE_R

                    if evento.value < 0:
                        if evento.value < -0.8: self.jogador.movendo_factor = 1
                        else: self.jogador.movendo_factor = evento.value
                        self.var1 = 0 #MOVE_L

                    if -controle_zona < evento.value < controle_zona:
                        self.var1 = 1
                        self.var2 = 1
                        self.jogador.movendo = False
            
    def draw(self):
        # Game Loop - Representação

        self.tela.fill(preto)
        self.tela.blit(self.bg , [0,0])
        self.tela.blit(self.mapa,[20,altura - 20 - 270])

        ##################################################################### TIMER
        if self.fase_atual != 10:
            self.tela.blit(self.dseg,self.dseg_rect)
            self.tela.blit(self.seg,self.seg_rect)
            self.tela.blit(self.segd,self.segd_rect)
            self.tela.blit(self.minu,self.minu_rect)
            self.tela.blit(self.mind,self.mind_rect)
            self.tela.blit(self.hor,self.hor_rect)
        #####################################################################

        self.movelplataforma_gp.draw(self.tela)
        self.projetil_gp.draw(self.tela)
        self.tela.blit(self.bg_e,[0,0])
        self.sprites_gp.draw(self.tela)
        self.trampolins_gp.draw(self.tela)

        #####################################################################

        if self.fase_atual == 10:
            self.tela.blit(self.time,self.time_rect)
            self.tela.blit(self.fim,self.fim_rect)

        else:
            self.tela.blit(self.bordas, [0,0])

        #####################################################################

        self.jogador_sp.draw(self.tela)
        
       
        pg.display.flip()  # POR ULTIMO

g = Game()

while g.rodando:
    g.new()

pg.quit()