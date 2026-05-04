import pygame, math

STYLES = ["CROSS","T-SHAPE","DOT","CIRCLE","SQUARE"]

class Sight:
    def __init__(self):
        self.on    = False
        self.style = 0
        self.size  = 10
        self.thick = 2
        self.gap   = 4
        self.dot   = True
        self.outline = True
        self.color = (0, 255, 80)

    def draw(self, surf, cx, cy):
        if not self.on: return
        s, t, g, c = self.size, self.thick, self.gap, self.color
        oc = (0,0,0)

        def L(x1,y1,x2,y2,col,w): pygame.draw.line(surf,col,(x1,y1),(x2,y2),w)
        def R(x,y,w,h,col): pygame.draw.rect(surf,col,(x,y,w,h))

        st = STYLES[self.style]
        if st == "CROSS":
            if self.outline:
                L(cx-s-g,cy,cx-g,cy,oc,t+2); L(cx+g,cy,cx+s+g,cy,oc,t+2)
                L(cx,cy-s-g,cx,cy-g,oc,t+2); L(cx,cy+g,cx,cy+s+g,oc,t+2)
            L(cx-s-g,cy,cx-g,cy,c,t); L(cx+g,cy,cx+s+g,cy,c,t)
            L(cx,cy-s-g,cx,cy-g,c,t); L(cx,cy+g,cx,cy+s+g,c,t)
        elif st == "T-SHAPE":
            if self.outline:
                L(cx-s-g,cy,cx-g,cy,oc,t+2); L(cx+g,cy,cx+s+g,cy,oc,t+2)
                L(cx,cy+g,cx,cy+s+g,oc,t+2)
            L(cx-s-g,cy,cx-g,cy,c,t); L(cx+g,cy,cx+s+g,cy,c,t)
            L(cx,cy+g,cx,cy+s+g,c,t)
        elif st == "DOT":
            r = max(2,t+1)
            if self.outline: pygame.draw.circle(surf,oc,(cx,cy),r+1)
            pygame.draw.circle(surf,c,(cx,cy),r)
        elif st == "CIRCLE":
            r = s+g
            if self.outline: pygame.draw.circle(surf,oc,(cx,cy),r+1,t+2)
            pygame.draw.circle(surf,c,(cx,cy),r,t)
        elif st == "SQUARE":
            h = s+g
            if self.outline: R(cx-h-1,cy-h-1,h*2+2,h*2+2,oc)
            R(cx-h,cy-t//2,h,t,c); R(cx,cy-t//2,h,t,c)
            R(cx-t//2,cy-h,t,h,c); R(cx-t//2,cy,t,h,c)

        if self.dot and st != "DOT":
            if self.outline: pygame.draw.circle(surf,oc,(cx,cy),t)
            pygame.draw.circle(surf,c,(cx,cy),max(1,t-1))
