import time
import machine
import neopixel
import random
import uasyncio as asyncio
from lets import *


num_pixels = 18
pin = machine.Pin(15, machine.Pin.OUT)
pixels = neopixel.NeoPixel(pin, num_pixels)

colors = (
    (255, 0, 0),  # Красный
    (255, 90, 0),  # Оранжевый
    (255, 255, 0),  # Желтый
    (0, 128, 0),  # Зеленый
    (0, 191, 255), # Голубой
    (0, 0, 255),  # Синий
    (148, 0, 255)  # Фиолетовый
)


def scale_color(color, led_brightness):
    """ Маштабирование цвета. """
    return tuple(int(channel * led_brightness) for channel in color)


def strip_clear():
    pixels.fill(0,0,0)
    pixels.write()


def fill_strip():
    """ Заполнение одним заданым цветом. """
    pixels.fill(scale_color((255, 0, 0), brightness))
    pixels.write()
    time.sleep(1)


        
def color_transition_effect(): 
    """ Циклическая смена цветов взятые из """
    for color in colors:
        pixels.fill(scale_color(color, brightness))
        pixels.write()
        time.sleep(1)


def rainbow_fade_effect():
    """ Еффект плавно переливающейся радуги. """

    def wheel(pos):
        """ Выполняет цветовой переход на основе позиции. """
        pos = 255 - pos
        if pos < 85:
            return (255 - pos * 3, 0, pos * 3)  # Переход от красного к зеленому
        elif pos < 170:
            pos -= 85
            return (0, pos * 3, 255 - pos * 3)  # Переход от зеленого к синему
        else:
            pos -= 170
            return (pos * 3, 255 - pos * 3, 0)  # Переход от синего к красному
        
    for j in range(256):
        for i in range (num_pixels):
            pixels[i] = scale_color(wheel((i + j) & 255), brightness)   # Вычисление цвета для текущего светодиода
        pixels.write()  
        time.sleep(0.02)
        


def random_flicker_effect(): 
    """ Включение случайного светодиода с задаными цветами в списке. """
    while True:
        random_led = random.randint(0, num_pixels - 1)
        random_color = random.randint(0, len(colors) - 1)
        pixels[random_led] = scale_color(colors[random_color], brightness)
        pixels.write()
        time.sleep(0.2)
    strip_clear()


def color_cycling_effect():
    """ Эффект циклически переключает цвета взятые из списка в светодиодной ленте. """
    for i in range(num_pixels):
        color = colors[i % len(colors)]
        pixels[i] = scale_color(color, brightness)
    pixels.write()
    time.sleep(1)


def strobe_effect():
    """ Эффект страбоскопа. """
    
    white_black = [(255,255,255), (0,0,0)]
    
    for color in white_black:
        pixels.fill(scale_color(color, 0.1))
        pixels.write()
        time.sleep(0.02)


def smooth_brightness_transit_effect():
    """ Эффект создает плавное изменение яркости. """
    s_brightness = 0.0
    flag = True
    color = random.choice(colors)
    
    while True:
        if flag:
            for _ in range(int(brightness * 1000)):
                s_brightness -= 0.001  # Уменьшен шаг изменения яркости
                pixels.fill(scale_color(color, s_brightness))
                pixels.write()
                if s_brightness < 0.0:
                    s_brightness = 0.0
                    color = random.choice(colors)
                    flag = False
                    break
                time.sleep(0.005)  # Уменьшена задержка для увеличения частоты обновления
        else:
            for _ in range(int(brightness * 1000)):
                s_brightness += 0.001  # Уменьшен шаг изменения яркости
                pixels.fill(scale_color(color, s_brightness))
                pixels.write()
                if s_brightness > brightness:
                    s_brightness = brightness
                    flag = True
                    break
                time.sleep(0.005)  # Уменьшена задержка для увеличения частоты обновления
                
                
def color_wave():
    """Cмена цвета волной справа налево и наоборот"""
    color = 0
    flag = True
    
    while True:
        forward = range(num_pixels) if flag else range(num_pixels - 1, -1, -1)        
        for i in forward:
            pixels[i] = scale_color(colors[color], brightness)
            pixels.write()
            time.sleep(0.025)
            
        flag = not flag
        color = (color + 1) % len(colors)
        
