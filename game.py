import pygame
import random
import time
pygame.init()

size = 800

screen = pygame.display.set_mode([size, size])

running = True

fize = 10
am = int(size / fize)
dol = int(am / 7)

field = [[0 for i in range(am)] for j in range(am)]

clock = pygame.time.Clock()

for i in range(am):
    for j in range(am):
        field[i][j] = 1
for i in range(dol, am - dol):
    for j in range(dol, am - dol):
        field[i][j] = 0


def render_field(screen):
    for i in range(am):
        for j in range(am):
            if field[i][j] == 1:
                pygame.draw.rect(screen, (0, 240, 0), (j * fize, i * fize, fize, fize))
            elif field[i][j] == 2:
                pygame.draw.rect(screen, (240, 0, 0), (j * fize, i * fize, fize, fize))
            elif field[i][j] == 3:
                pygame.draw.rect(screen, (100, 0, 0), (j * fize, i * fize, fize, fize))
            elif field[i][j] == 4:
                pygame.draw.rect(screen, (50, 50, 200), (j * fize, i * fize, fize, fize))


pi = int(dol / 2)
pj = int(dol / 2)
si = 0
sj = 0

levels = [
    {"bs": [[30, 45], [50, 60]], "hs": [[1, 1], [-1, -1]]},
    {"bs": [[15, 15], [50, 50], [40, 30]], "hs": [[1, -1], [1, -1], [-1, -1]]},
    {"bs": [[20, 15], [50, 50], [40, 30]], "hs": [[-1, 1], [-1, 1], [-1, -1]]},
    {"bs": [[25, 10], [40, 25], [15, 35], [40, 40]], "hs": [[1, -1], [1, -1], [-1, 1], [1, 1]]}
]

#for i in range(10):
   # am = random.randint(4, 10)
   # levels.append({"bs": [[random.randint(15, 60), random.randint(15, 60)] for j in range(am)], "hs": [[random.randint(-1, 1), random.randint(-1, 1)] for j in range(am)]})

level = 0
lcom = [False, False]

ent = False
ext = False

field[pi][pj] = 2
c = -1

for i in levels[level]["bs"]:
    field[i[0]][i[1]] = 4

bs = levels[level]["bs"]
hs = levels[level]["hs"]
myfont = pygame.font.SysFont('Comic Sans MS', 30)

pygame.font.init()
cfr = 0
lost = False
won = False
while running:

    f = 0
    clock.tick(60)
    c += 1
    if c == 60:
        c = 0
    if cfr == 100:
        print(won, lost)

    if cfr <= 0 and won or lost:
        won = False
        lost = False
        bs = levels[level]["bs"]
        hs = levels[level]["hs"]

        for i in range(am):
            for j in range(am):
                field[i][j] = 1
        for i in range(dol, am - dol):
            for j in range(dol, am - dol):
                field[i][j] = 0

        pi = int(dol / 2)
        pj = int(dol / 2)
        si = 0
        sj = 0
        field[pi][pj] = 2


    if cfr > 0:
        cfr -= 1
        lostlab = myfont.render("You lost", False, (128, 0, 128))
        wonlab = myfont.render("You won", False, (128, 0, 128))
        levlab = myfont.render("Now playing: " + str(level + 1), False, (128, 0, 128))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))

        render_field(screen)

        screen.blit(score, (350, 0))
        if lost:
            screen.blit(lostlab, (350, 350))
        elif won:
            screen.blit(wonlab, (350, 350))

        screen.blit(levlab, (320, 400))
        if not won:
            lostlab = myfont.render("You lost", False, (128, 0, 128))
            screen.blit(lostlab, (350, 350))
        pygame.display.flip()
        continue

    levlab = myfont.render("Now playing: " + str(level + 1), False, (128, 0, 128))
    alab = myfont.render("You need to win - 70%", False, (128, 0, 128))

    for i in range(am):
        for j in range(am):
            if field[i][j] == 1:
                f += 1

    score = myfont.render(str(int((f / (am * am)) * 100)) + "%", False, (128, 0, 128))

    if f / (am * am) >= 0.7:
        lcom[level] = True
        won = True

    if lcom[level]:
        if level == len(lcom):
            running = False
        cfr = 100
        level += 1
        if lost:
            level -= 1
            lcom[level] = False
        bs = levels[level]["bs"]
        hs = levels[level]["hs"]


        for i in range(am):
            for j in range(am):
                field[i][j] = 1
        for i in range(dol, am - dol):
            for j in range(dol, am - dol):
                field[i][j] = 0

        pi = int(dol / 2)
        pj = int(dol / 2)
        si = 0
        sj = 0
        field[pi][pj] = 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and (si != -1 or not ent):
                si = 1
                sj = 0
            elif event.key == pygame.K_w and (si != 1 or not ent):
                si = -1
                sj = 0
            elif event.key == pygame.K_d  and (sj != -1 or not ent):
                si = 0
                sj = 1
            elif event.key == pygame.K_a  and (sj != 1 or not ent):
                si = 0
                sj = -1

    if c % 4 == 0:
        for i in range(len(bs)):
            bi = bs[i][0]
            bj = bs[i][1]
            hi = hs[i][0]
            hj = hs[i][1]
            field[bi][bj] = 0

            bs[i][0]  += hs[i][0]
            bs[i][1] += hs[i][1]

            if field[bs[i][0] ][bs[i][1]] == 1:
                bs[i][0]  -= hs[i][0]
                bs[i][1] -= hs[i][1]

                if hs[i][0] == 1 and hs[i][1] == 1:
                    hs[i][1] = -1
                elif hs[i][0] == 1 and hs[i][1] == -1:
                    hs[i][0] = -1
                elif hs[i][0] == -1 and hs[i][1] == 1:
                    hs[i][0] = 1
                elif hs[i][0] == -1 and hs[i][1] == -1:
                    hs[i][1] = 1

            if field[bs[i][0] ][bs[i][1]] == 3:
                lost = True
                cfr = 100
                print("lost")

            field[bs[i][0] ][bs[i][1]] = 4


    if c % 6 == 0:
        if field[pi][pj] == 0:
            field[pi][pj] = 3
        elif field[pi][pj] == 2:
            if ent and (abs(si) > 0 or abs(sj) > 0):
                field[pi][pj] = 3
            else:
                field[pi][pj] = 1
        elif field[pi][pj] == 1:
            field[pi][pj] = 1

        pi += si
        pj += sj

        if pi == am - 1:
            si = -1
            sj = 0
        elif pi == 0:
            si = 1
            sj = 0
        elif pj == 0:
            si = 0
            sj = 1
        elif pj == am - 1:
            si = 0
            sj = -1

        if field[pi][pj] == 0:
            ent = True
        if field[pi][pj] == 1 and ent:
            ext = True
        if field[pi][pj] == 3:
            lost = True
            cfr = 100
            print("here")
        if ent and ext:

            si = 0
            sj = 0
            ent = False
            ext = False

            comp = []

            vis = [[0 for j in range(am)] for i in range(am)]
            c = -1
            while True:
                c += 1
                comp.append([])
                q = []

                for i in range(am):
                    for j in range(am):
                        if field[i][j] == 0 and not vis[i][j]:
                            q.append((i, j))
                            break
                    if len(q) > 0:
                        break

                if len(q) == 0:
                    break

                while len(q) > 0:
                    f = q[0][:]
                    del q[0]

                    for i in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                        ti = (f[0] + i[0], f[1] + i[1])

                        if field[ti[0]][ti[1]] == field[f[0]][f[1]] and vis[ti[0]][ti[1]] == 0:
                            comp[c].append(ti)
                            vis[ti[0]][ti[1]] = 1
                            q.append(ti)
            comp.sort(key=lambda x: len(x))
            for i in range(len(comp) - 1):
                for j in comp[i]:
                    field[j[0]][j[1]] = 1
            for i in range(am):
                for j in range(am):
                    if field[i][j] == 3:
                        field[i][j] = 1

        field[pi][pj] = 2

    screen.fill((0, 0, 0))

    render_field(screen)

    screen.blit(score, (350, 0))

    screen.blit(levlab, (320, 700))
    screen.blit(alab, (320, 740))

    if lost:
        bs = levels[level]["bs"]
        hs = levels[level]["hs"]

        for i in range(am):
            for j in range(am):
                field[i][j] = 1
        for i in range(dol, am - dol):
            for j in range(dol, am - dol):
                field[i][j] = 0

        pi = int(dol / 2)
        pj = int(dol / 2)
        si = 0
        sj = 0
        field[pi][pj] = 2

    pygame.display.flip()

pygame.quit()