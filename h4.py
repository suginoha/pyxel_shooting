import pyxel
import random
ri = random.randint
pyxel.init(256, 256, caption = "hour4", fps = 60)
pyxel.load("res.pyxres")
flow_no = 0 # 0:title 1:game 2:boss 3:over 5:ending
sx, sy, spd = 100, 200, 5
char = [(0,0,16), (16,0,16), (32,0,16), (48,0,8), (48,8,8), (56,0,8), (56,8,8),(0,32,32)]
move = ["123321","16663444","13","14443666944476662","8"]
md = [(0,0),(-1,1),(0,1),(1,1),(-1,0),(0,0),(1,0),(-1,-1),(0,-1),(1,-1)]
us = []
m_wait = 0
score = 0
energy = 10
end_msg = "   game over"
class Unit:
    def __init__(s, x, y, c, mt):s.x, s.y, s.c, s.mt, s.mc, s.hp = x, y, c, mt, 0, 1
    def draw(s):
    	u, v, sz = char[s.c]
    	if s.c<=6 and ri(0,2)==0:v += 16
    	pyxel.blt(s.x, s.y, 0, u, v, sz, sz, 0)
    def move(s):
        s.mc += 1
        if s.mc > 100000000:s.mc = 0
        st = move[s.mt]
        mp = (s.mc % (len(st)*20)) // 20
        dx, dy = md[int(st[mp])]
        s.x += dx
        s.y += dy
    def hit(s, m_pos):
        global score, sx, sy,energy
        u, v, sz = char[s.c]

        if s.c != 5:
            if sx-14 < s.x < sx + sz - 2 and sy-14 < s.y < sy + sz - 2:
                s.hp = 0
                energy -= 1
            else:
                for x, y in m_pos:
                    if x-6< s.x <x+sz-2 and y-6< s.y < y+sz-2:
                        s.hp -= 1
                        if s.hp==0: score += 100
                        return x, y
        return -99999, 0
def random_pat(list1):return list1[ri(0, len(list1)-1)]
def title():pyxel.text(90, 66, "   Our Forth", pyxel.frame_count % 16);pyxel.text(80, 200, "   - PRESS ENTER -", 13)
def game_over():
    global end_msg
    pyxel.text(70, 10, "      Our Forth "+str(score) , 12)
    pyxel.text(90, 66, end_msg, pyxel.frame_count % 16);pyxel.text(80, 200, "   - PRESS ENTER -", 13)
def mis_add():global us;us += [Unit(sx+4, sy-4, 5, 4)]
def mis_pos(us):
    r = []
    for u in us:
        if u.c == 5:
            r += [(u.x, u.y)]
    return r
def mis_cut(x, y):
    for u in us:
        if u.c == 5:
            if (u.x, u.y)==(x, y):u.hp = 0
def unit_off():
    l = len(us) - 1
    for n, u in enumerate(us[::-1]):
        if u.hp <= 0:
            del us[l - n]
def game_start():
    global flow_no, us,energy, end_msg, score
    end_msg = "   game over"
    us = []
    energy = 10
    flow_no = 1
    score = 0
    pyxel.playm(0, loop=False)
    for i in range(100):us += [Unit(ri(0,240), ri(-400,240), random_pat([1, 2, 7]), ri(0,3))]
def stage():
    global sx,sy,spd,us,score
    pyxel.blt(sx, sy, 0, 0, 0, 16, 16, 0)
    for u in us:
        u.move()
        u.draw()
    m_pos = mis_pos(us)
    for u in us:
        x, y = u.hit(m_pos)
        if x>-99999:
            mis_cut(x, y)
    unit_off()
    pyxel.text(10, 10, "Our Forth "+str(score) , 8)
    pyxel.text(110, 10, "O" * energy , 6)

def clear():
    global us, end_msg
    for u in us:
        if u.c != 5 and u.y > 0 and u.y < 256:return False
    end_msg = "all enemy clear."
    return True

def update():
    global sx, sy, spd, flow_no, m_wait, us
    m_wait -= 1
    if pyxel.btnp(pyxel.KEY_Q): pyxel.quit()
    if pyxel.btnp(pyxel.KEY_ENTER) and flow_no in [0, 3]:game_start()

    if flow_no == 1:
        if energy <=0 :pyxel.playm(1, loop=False); flow_no = 3
        if clear():pyxel.playm(3, loop=False); flow_no = 3
        if pyxel.btn(pyxel.KEY_LEFT): sx = max(0, sx-spd)
        if pyxel.btn(pyxel.KEY_RIGHT):sx = min(sx + spd, pyxel.width - 16)
        if pyxel.btn(pyxel.KEY_UP):   sy = max(0, sy-spd)
        if pyxel.btn(pyxel.KEY_DOWN): sy = min(sy + spd, pyxel.height - 16)
        if pyxel.btnp(pyxel.KEY_SPACE) and m_wait<=0:
            mis_add()
            m_wait = 30
            #pyxel.playm(1, loop=False); flow_no = 3
def draw():
    global flow_no
    pyxel.cls(0)
    if flow_no == 0: title()
    if flow_no == 1: stage()
    if flow_no == 3: game_over()
pyxel.playm(2, loop=False)
pyxel.run(update, draw)
