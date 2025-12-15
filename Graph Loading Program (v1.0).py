import pygame
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import os
import subprocess

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "image")
rule_and_control = os.path.join(current_path, "information")

rule_and_control_path = os.path.join(rule_and_control, "explain.txt")
dragon = pygame.image.load(os.path.join(image_path, "dragon.png"))
dragon = pygame.transform.scale(dragon, (100, 100))
background = pygame.image.load(os.path.join(image_path, "background.png"))
background = pygame.transform.scale(background, (800, 600))

pygame.display.set_icon(dragon)

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("함수 그래프 그리기")

BLACK = (25, 25, 25)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY_RED = (200, 0, 0)
BUTTON_COLOR = (100, 150, 255)

font = pygame.font.SysFont("headliner", 20)
font_exp = pygame.font.SysFont("headliner", 15)

# 버튼 클래스 정의
class Button:
    def __init__(self, x, y, width, height, image, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image, (190, 65))  # 이미지 크기 조정
        self.text = text
        self.font = font
        self.text_surface = self.font.render(text, True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)  # 버튼 배경 이미지 그리기
        screen.blit(self.text_surface, self.text_rect)  # 텍스트 그리기

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# 그래프 그리기 함수
def draw_graph():
    # 임의의 함수 그래프 그리기 (sin 함수)
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)
    points = [(int(300 + xi * 100), int(200 - yi * 100)) for xi, yi in zip(x, y)]
    
    for i in range(len(points) - 1):
        pygame.draw.line(screen, (255, 0, 0), points[i], points[i + 1], 2)

# 이미지 로드
button_image = pygame.image.load(os.path.join(image_path, "button.png")) # 버튼 이미지 로드 (본인의 이미지로 교체)

# 버튼 생성
button = Button(50, 300, 200, 65, button_image, 'Draw Graph', font)

input_boxes = [pygame.Rect(120, 50 + i * 50, 140, 32) for i in range(4)]
colors = [pygame.Color('lightskyblue3') for _ in range(4)]
active = [False for _ in range(4)]
texts = ['' for _ in range(4)]

selected_function = 1
running = True
draw_graph = False

liner = font.render("선택: 일차함수 f(x) = ax + b", True, GRAY_RED)
quadraitc = font.render("선택: 이차함수 f(x) = ax² + bx + c", True, GRAY_RED)
cubic = font.render("선택: 삼차함수 f(x) = ax³ + bx² + cx + d", True, GRAY_RED)
rational = font.render("선택: 유리함수 f(x) = (ax + b) / (cx + d)", True, GRAY_RED)
radical = font.render("선택: 무리함수 f(x) = √(a(x + b)) + c", True, GRAY_RED)
inverse_liner = font.render("선택: 일차함수(역함수) f^-1(x) = ax + b", True, GRAY_RED)
inverse_rational = font.render("선택: 유리함수(역함수) f^-1(x) = (ax - b) / (cx - d", True, GRAY_RED)
inverse_radical = font.render("선택: 무리함수(역함수) f^-1(x) = √(a(x + b)) + c", True, GRAY_RED)

def draw_linear_function(a, b):
    x = np.linspace(-10, 10, 400)
    y = a * x + b

    plt.figure(figsize=(5, 4))
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.xticks(np.arange(-10, 11))
    plt.yticks(np.arange(-10, 11))
    plt.plot(x, y, label=f"y = {a}x + {b}", color='pink')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.title(f"Graph : y = {a}x + {b}", color='black')
    plt.xlabel("x")
    plt.ylabel("y")

    buf = BytesIO()
    plt.savefig(buf, format='PNG')
    buf.seek(0)
    plt.close()
    return pygame.image.load(buf)

def draw_quadratic_function(a, b, c):
    x = np.linspace(-10, 10, 400)
    y = a * x ** 2 + b * x + c

    plt.figure(figsize=(5, 4))
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.xticks(np.arange(-10, 11))
    plt.yticks(np.arange(-10, 11))
    plt.plot(x, y, label=f"y = {a}x² + {b}x + {c}", color='red')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.title(f"Graph : y = {a}x² + {b}x + {c}", color='black')
    plt.xlabel("x")
    plt.ylabel("y")

    buf = BytesIO()
    plt.savefig(buf, format='PNG')
    buf.seek(0)
    plt.close()
    return pygame.image.load(buf)

def draw_cubic_function(a, b, c, d):
    x = np.linspace(-10, 10, 400)
    y = a * x ** 3 + b * x ** 2 + c * x + d

    plt.figure(figsize=(5, 4))
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.xticks(np.arange(-10, 11))
    plt.yticks(np.arange(-10, 11))
    plt.plot(x, y, label=f"y = {a}x³ + {b}x² + {c}x + {d}", color='purple')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.title(f"Graph : y = {a}x³ + {b}x² + {c}x + {d}", color='black')
    plt.xlabel("x")
    plt.ylabel("y")

    buf = BytesIO()
    plt.savefig(buf, format='PNG')
    buf.seek(0)
    plt.close()
    return pygame.image.load(buf)

def draw_rational_function(a, b, c, d):
    x = np.linspace(-10, 10, 400)
    # 점근선 발생을 방지하기 위해 x 범위를 나눕니다.
    asymptote_x = -d / c if c != 0 else None
    x1 = x[x < asymptote_x] if asymptote_x is not None else x
    x2 = x[x > asymptote_x] if asymptote_x is not None else []

    plt.figure(figsize=(5, 4))
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.xticks(np.arange(-10, 11))
    plt.yticks(np.arange(-10, 11))

    # 첫 번째 구간 그래프
    if len(x1) > 0:
        y1 = (a * x1 + b) / (c * x1 + d)
        plt.plot(x1, y1, label=f"y = ({a}x + {b}) / ({c}x + {d})", color='blue')

    # 두 번째 구간 그래프
    if len(x2) > 0:
        y2 = (a * x2 + b) / (c * x2 + d)
        plt.plot(x2, y2, color='blue')

    # 기준선만 표시
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.title(f"Graph : y = ({a}x + {b}) / ({c}x + {d})", color='black')
    plt.xlabel("x")
    plt.ylabel("y")

    buf = BytesIO()
    plt.savefig(buf, format='PNG')
    buf.seek(0)
    plt.close()
    return pygame.image.load(buf)

def draw_radical_function(a, b, c):
    x = np.linspace(-10, 10, 400)
    x = x[x + b >= 0]
    y = np.sqrt(a * (x + b)) + c

    plt.figure(figsize=(5, 4))
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.xticks(np.arange(-10, 11))
    plt.yticks(np.arange(-10, 11))
    plt.plot(x, y, label=f"y = √({a}(x + {b})) + {c}", color='green')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.title(f"Graph : y = √({a}(x + {b})) + {c}", color='black')
    plt.xlabel("x")
    plt.ylabel("y")

    buf = BytesIO()
    plt.savefig(buf, format='PNG')
    buf.seek(0)
    plt.close()
    return pygame.image.load(buf)

def draw_inverse_linear_function(a, b):
    if a == 0:
        raise ValueError("a cannot be zero for a linear function.")
    x = np.linspace(-10, 10, 400)
    y = (x - b) / a

    plt.figure(figsize=(5, 4))
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.xticks(np.arange(-10, 11))
    plt.yticks(np.arange(-10, 11))
    plt.plot(x, y, label=f"y = (x - {b}) / {a}", color='pink')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.title(f"Graph : y = (x - {b}) / {a}", color='black')
    plt.xlabel("x")
    plt.ylabel("y")

    buf = BytesIO()
    plt.savefig(buf, format='PNG')
    buf.seek(0)
    plt.close()
    return pygame.image.load(buf)

def draw_inverse_rational_function(a, b, c, d):
    x = np.linspace(-10, 10, 1000)

    # 점근선 위치 (c * x - a = 0 => x = a/c)
    if c != 0:
        asymptote_x = a / c
    else:
        asymptote_x = None  # 점근선 없음

    # 그래프를 나눌 구간 설정
    if asymptote_x is not None:
        x_left = x[x < asymptote_x]  # 점근선 왼쪽
        x_right = x[x > asymptote_x]  # 점근선 오른쪽
    else:
        x_left = x
        x_right = np.array([])

    # 유효한 y 값 계산
    y_left = (b * x_left - d) / (c * x_left - a) if len(x_left) > 0 else []
    y_right = (b * x_right - d) / (c * x_right - a) if len(x_right) > 0 else []

    # 그래프 그리기
    plt.figure(figsize=(5, 4))
    if len(x_left) > 0:
        plt.plot(x_left, y_left, color='blue')
    if len(x_right) > 0:
        plt.plot(x_right, y_right, color='blue', label=f"y = ({d} * x - {b}) / ({a} * {c} * x)")
    plt.axhline(0, color='black', linewidth=0.5)  # x축
    plt.axvline(0, color='black', linewidth=0.5)  # y축
    # if asymptote_x is not None:
      #  plt.axvline(asymptote_x, color='red', linestyle='--', label=f"Asymptote: x = {asymptote_x:.2f}")

    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.grid(color='lightgray', linestyle='--', linewidth=0.5)
    plt.title(f"Graph : y = ({d} * x - {b}) / ({a} * {c} * x)", color="black")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.xticks(np.arange(-10, 11))
    plt.yticks(np.arange(-10, 11))

    # 그래프를 이미지로 저장
    buf = BytesIO()
    plt.savefig(buf, format='PNG')
    buf.seek(0)
    plt.close()
    return pygame.image.load(buf)

def draw_inverse_radical_function(a, b, c):
    x = np.linspace(-10, 10, 400)
    x = x[x >= c]
    y = (x - c) ** 2 / a - b

    plt.figure(figsize=(5, 4))
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.xticks(np.arange(-10, 11))
    plt.yticks(np.arange(-10, 11))
    plt.plot(x, y, label=f"y = ((x - {c})² / {a}) - {b}", color='green')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.title(f"Graph : y = ((x - {c})² / {a}) - {b}", color='black')
    plt.xlabel("x")
    plt.ylabel("y")

    buf = BytesIO()
    plt.savefig(buf, format='PNG')
    buf.seek(0)
    plt.close()
    return pygame.image.load(buf)

while running:

    for event in pygame.event.get():
        screen.blit(background, (0, 0))
        if event.type == pygame.QUIT:
            running = False
        if button.is_clicked(event):
            draw_graph = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, box in enumerate(input_boxes):
                if box.collidepoint(event.pos):
                    active[i] = True
                    for j in range(len(active)):
                        if j != i:
                            active[j] = False
            
                else:
                    active[i] = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                subprocess.run(["notepad.exe",rule_and_control_path])
            if any(active):
                for i, (is_active, text) in enumerate(zip(active, texts)):
                    if is_active:
                        if event.key == pygame.K_BACKSPACE:
                            texts[i] = text[:-1]
                        else:
                            texts[i] += event.unicode
             
            else:
                if event.key == pygame.K_1:
                    selected_function = 1
                    draw_graph = False
                elif event.key == pygame.K_2:
                    selected_function = 2
                    draw_graph = False
                elif event.key == pygame.K_3:
                    selected_function = 3
                    draw_graph = False
                elif event.key == pygame.K_4:
                    selected_function = 4
                    draw_graph = False
                elif event.key == pygame.K_5:
                    selected_function = 5
                    draw_graph = False
                elif event.key == pygame.K_6:
                    selected_function = 6
                    draw_graph = False
                elif event.key == pygame.K_7:
                    selected_function = 7
                    draw_graph = False
                elif event.key == pygame.K_8:
                    selected_function = 8
                    draw_graph = False

    for i, box in enumerate(input_boxes):
        if selected_function in [1, 6] and i < 2:
            pygame.draw.rect(screen, colors[i] if active[i] else pygame.Color('lightskyblue3'), box, 2)
        elif selected_function == 2 and i < 3:
            pygame.draw.rect(screen, colors[i] if active[i] else pygame.Color('lightskyblue3'), box, 2)
        elif selected_function in [3, 4, 7] and i < 4:
            pygame.draw.rect(screen, colors[i] if active[i] else pygame.Color('lightskyblue3'), box, 2)
        elif selected_function in [5, 8] and i < 3:
            pygame.draw.rect(screen, colors[i] if active[i] else pygame.Color('lightskyblue3'), box, 2)

    labels = ["a:", "b:", "c:", "d:"]
    for i, label in enumerate(labels):
        if (selected_function in [1,6] and i < 2) or (selected_function == 2 and i < 3) or (selected_function in [3, 4, 7] and i < 4) or (selected_function in [5, 8] and i < 3):
            screen.blit(font.render(label, True, BLACK), (50, 55 + i * 50))

    for i, text in enumerate(texts):
        if (selected_function in [1,6] and i < 2) or (selected_function == 2 and i < 3) or (selected_function in [3, 4, 7] and i < 4) or (selected_function in [5, 8] and i < 3):
            screen.blit(font.render(text, True, BLACK), (input_boxes[i].x + 5, input_boxes[i].y + 5))

    explanation1 = font_exp.render("1: 1차함수, 2: 2차함수, 3: 3차함수, 4: 유리함수, 5: 무리함수", True, BLACK)
    explanation2 = font_exp.render("6: 1차함수(역함수), 7: 유리함수(역함수), 8: 무리함수(역함수)", True, BLACK)
    screen.blit(explanation1, (50, HEIGHT - 75))
    screen.blit(explanation2, (50, HEIGHT - 50))

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_1:
            if not any(active):
                screen.blit(liner, (5, 10))
        if event.key == pygame.K_2:
            if not any(active):
                screen.blit(quadraitc, (5, 10))
        if event.key == pygame.K_3:
            if not any(active):
                screen.blit(cubic, (5, 10))
        if event.key == pygame.K_4:
            if not any(active):
                screen.blit(rational, (5, 10))
        if event.key == pygame.K_5:
            if not any(active):
                screen.blit(radical, (5, 10))
        if event.key == pygame.K_6:
            if not any(active):
                screen.blit(inverse_liner, (5, 10))
        if event.key == pygame.K_7:
            if not any(active):
                screen.blit(inverse_rational, (5, 10))
        if event.key == pygame.K_8:
            if not any(active):
                screen.blit(inverse_radical, (5, 10))

    if draw_graph:
        try:
            a = int(texts[0])
            b = int(texts[1])
            if selected_function == 1:
                graph = draw_linear_function(a, b)
            elif selected_function == 2:
                c = int(texts[2])
                graph = draw_quadratic_function(a, b, c)
            elif selected_function == 3:
                c = int(texts[2])
                d = int(texts[3])
                graph = draw_cubic_function(a, b, c, d)
            elif selected_function == 4:
                c = int(texts[2])
                d = int(texts[3])
                graph = draw_rational_function(a, b, c, d)
            elif selected_function == 5:
                c = int(texts[2])
                graph = draw_radical_function(a, b, c)
            elif selected_function == 6:
                graph = draw_inverse_linear_function(a, b)
            elif selected_function == 7:
                c = int(texts[2])
                d = int(texts[3])
                graph = draw_inverse_rational_function(a, b, c, d)
            elif selected_function == 8:
                c = int(texts[2])
                graph = draw_inverse_radical_function(a, b, c)
            screen.blit(graph, (300, 50))
        except ValueError:
            screen.blit(font.render("Invalid input", True, RED), (50, 500))

    button.draw(screen)

    pygame.display.flip()

pygame.quit()