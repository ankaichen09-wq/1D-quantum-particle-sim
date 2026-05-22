import pygame as pg
import numpy as np
import time as pytime
import pygame.freetype


#window set up
pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()  

#----------------------
#drawing background UI
#---------------------

#region

measurement_surface = pg.Surface((1280, 720), pg.SRCALPHA)
measurement_surface.fill((0,0,0,0))

bg = pg.Surface((1280, 720), pg.SRCALPHA)
bg.fill((0,0,0,0))

prob_dens_border = [(100, 501),(900, 501), (900, 50), (100, 50)]
pg.draw.lines(bg, (83, 83, 83), True, prob_dens_border, 2)

cn_box = [(400, 545),(1250, 545), (1250, 700), (400, 700)]
pg.draw.lines(bg, (83, 83, 83), True, cn_box, 2)

info_box = [(1230, 50),(955, 50), (955, 210), (1230, 210)]
pg.draw.lines(bg, (83, 83, 83), True, info_box, 2)

precision_slider = [925, 340, 325, 7]
pg.draw.rect(bg, (185, 185, 185), precision_slider, 2, 2)
precision_slider_pos = 955
precision_slider_colour = (230, 234, 35)
precision_slider_pressed = False

time_slider = [925, 440, 325, 7]
pg.draw.rect(bg, (185, 185, 185), time_slider, 2, 2)
time_slider_pos = 1050
time_slider_colour = (230, 234, 35)
time_slider_pressed = False

measure_button = [(100, 545),(190, 545), (190, 580), (100, 580)]
pg.draw.lines(bg, (83, 83, 83), True, measure_button, 2)
measure_button_pressed = False
measure_button_colour = (255, 255, 255)

reset_button = [(210, 545),(270, 545), (270, 580), (210, 580)]
pg.draw.lines(bg, (83, 83, 83), True, reset_button, 2)
reset_button_pressed = False
reset_button_colour = (255, 255, 255)

initial_state_border = [(100, 590),(270, 590), (270, 700), (100, 700)]
pg.draw.lines(bg, (43, 43, 43), True, initial_state_border, 2)
initial_state_border_colour = (255, 255, 255)

temp_input_outline = [(153, 597),(203, 597), (203, 615), (153, 615)]
temp_input_outline_colour = (43, 43, 43)
pg.draw.lines(bg, temp_input_outline_colour, True, temp_input_outline, 2)

wl_input_outline = [(203, 620),(253, 620), (253, 640), (203, 640)]
wl_input_outline_colour = (43, 43, 43)
pg.draw.lines(bg, wl_input_outline_colour, True, wl_input_outline, 2)

mass_input_outline = [(153, 645),(203, 645), (203, 663), (153, 663)]
mass_input_outline_colour = (43, 43, 43)
pg.draw.lines(bg, mass_input_outline_colour, True, mass_input_outline, 2)

restart_button = [(105, 670),(180, 670), (180, 695), (105, 695)]
pg.draw.lines(bg, (83, 83, 83), True, restart_button, 2)
restart_button_pressed = False
restart_button_colour = (255, 255, 255)

#endregion

#================================================================================

#inital states
#region

time = 0
dt = 0.00013
well_length = 1
wl_input = str(well_length)
psi = np.zeros(550, dtype = complex)
x_values = np.linspace(0, well_length, 550)
max_pd = 9/well_length
Temp = 1
temp_input = str(Temp)
precision = 2
mass = 1
mass_input = str(mass)
q = 0
input_state = 0 #1= temp, 2 = wl, 3 = mass
debug_print = True
info_state = 0
#endregion


#text
#region

text_surface = pg.Surface((1280, 720))
text_surface.set_colorkey((0,0,0))
text_surface_r = pg.Surface((1280, 720))
text_surface_r.set_colorkey((0,0,0))
text_surface_r2 = pg.Surface((1280, 720))
text_surface_r2.set_colorkey((0,0,0))

font = pg.freetype.SysFont("calibri",30, bold=False)
s_font = pg.freetype.SysFont("calibri",23, bold=True)
xs_font = pg.freetype.SysFont("calibri",10, bold=False)
ms_font = pg.freetype.SysFont("calibri",19, bold=True)

font.render_to(text_surface, (1030, 360), "precision", (12, 11, 13))
font.render_to(text_surface, (1023, 460), "sim. speed", (12, 11, 13))
ms_font.render_to(text_surface, (430, 505), "well length", (12, 11, 13))
s_font.render_to(text_surface, (107, 558), "measure", (160, 26, 30))
s_font.render_to(text_surface, (218, 555), "reset", (160, 26, 30))
s_font.render_to(text_surface, (111, 676), "restart", (160, 26, 30))
ms_font.render_to(text_surface, (107, 600), "temp: ", (10, 10, 10))
ms_font.render_to(text_surface, (107, 623), "well length: ", (10, 10, 10))
ms_font.render_to(text_surface, (107, 650), "mass: ", (10, 10, 10))
font.render_to(text_surface, (350, 25), "Probability Density Window", (12, 11, 13))
font.render_to(text_surface, (1000, 25), "Cn^2 distribution", (12, 11, 13))
xs_font.render_to(text_surface, (955, 215), "n = 1", (12, 11, 13))
ms_font.render_to(text_surface, (1050, 215), "eigenstate", (12, 11, 13))
xs_font.render_to(text_surface, (1200, 215), "n = 200", (12, 11, 13))
ms_font.render_to(text_surface_r, (1083, 700), "relative probability", (12, 11, 13)) 
text_surface_vert = pg.transform.rotate(text_surface_r, 90)
ms_font.render_to(text_surface_r2, (1083, 700), "probability density", (12, 11, 13)) 
text_surface_vert2 = pg.transform.rotate(text_surface_r2, 90)
xs_font.render_to(text_surface, (70, 50), "p = 1 ↑", (12, 11, 13))
xs_font.render_to(text_surface, (76, 498), "p = 0", (12, 11, 13))
xs_font.render_to(text_surface, (100, 505), "x = 0", (12, 11, 13))
#endregion


#Cn finder based on temperature
def Cn_calc(Temp, mass, well_length):
    i = 0 
    cn_array = np.zeros(200, dtype = complex)
    for eigenstate in range(1, 201, 1):
        eigenenergy = (np.pi**2*eigenstate**2) / (2 * mass * well_length**2)
        cn = np.sqrt(eigenenergy)*np.exp(-eigenenergy/Temp) # boltzmann distribution
        if np.sum(cn_array) == 0 or cn / np.sum(cn_array) > 0.00001: # cuts off values with under .001% contribution
            cn_array[i] = cn
        else:
            pass 
        i += 1
    cns = cn_array/np.sqrt(np.sum(np.abs(cn_array)**2)) # normalised cns
    return cns

cns = Cn_calc(Temp, mass, well_length)


#Cn visualiser
Cn_max = np.abs(np.max(cns))**2
Cn_X_values = np.linspace(957,1228,200)
rendering_cns = 210 - (np.abs(cns)**2 * 140/Cn_max)
cn_points = list(zip(Cn_X_values,rendering_cns))
pg.draw.lines(screen,(40, 40, 40), False, cn_points, 3)

p_mean = np.sum(np.abs(cns)**2 * np.linspace(1*np.pi/well_length, 200*np.pi/well_length, 200))
p_mean2 = np.sum(np.abs(cns)**2 * np.linspace(1*np.pi/well_length, 200*np.pi/well_length, 200)**2)
std_p = np.sqrt(max(0,p_mean2))



#==================================================================
#====================GAME LOOP=====================================
#==================================================================

running = True
while running:

        screen.fill((255, 255, 255))
        measurement_surface.fill((0, 0, 0, 0))    
        screen.blit(text_surface, (0,0))
        screen.blit(text_surface_vert, (235,10))
        screen.blit(text_surface_vert2, (-620,160))

        #-------------------------------
        #----WAVEFUNCTION PRODUCTION----
        #-------------------------------


        #TDSE point gen
        if measure_button_pressed == False :
            psi = np.zeros(550, dtype = complex)
            i=0
            for eigenstate in range(1, 201, 1):
                y_values = cns[i] *(np.sqrt(2/well_length)*np.sin( (eigenstate*np.pi*x_values)/well_length ) * (np.exp((-1j * eigenstate**2 * np.pi**2 * time)/(2 * mass * well_length**2))))
                psi += y_values
                i += 1
       
            time = time + dt
       
        prob_dens = np.real( (psi)*np.conj(psi) )


        #std position                
        x_mean = np.trapezoid(prob_dens * x_values, x_values)/np.trapezoid(prob_dens, x_values)
        x_mean2 = np.trapezoid(prob_dens * x_values**2, x_values)/np.trapezoid(prob_dens, x_values)
        std_x = np.sqrt(x_mean2 - x_mean**2)

        #render TDSE prob density points
        #region
        stretch_factor = 800
        x_offset = 100
        height_factor = 40*well_length
        y_offset = 100
        x_value_render = (x_values*stretch_factor)/well_length + x_offset
        y_value_render = -1*prob_dens * height_factor + 500
        y_value_render[y_value_render < 50] = 50
        plot_points = list(zip(x_value_render,y_value_render))
        pg.draw.lines(screen,(0, 0, 0), False, plot_points, 4)
        #endregion    

        #=========================================

        for event in pg.event.get():
            mx, my = pg.mouse.get_pos()

            #------------------------------------
            #-----SLIDERS AND BUTTONS------------
            #------------------------------------
         
            #region
            #change slider colour on click
            if (mx-precision_slider_pos)**2 + (my-343)**2 <= (7)**2 and event.type == pg.MOUSEBUTTONDOWN:
               
                    precision_slider_pressed = True
                    precision_slider_colour = (155, 167, 17)

            #set mouse x pos to slider x pos
            if precision_slider_pressed == True and 930 <= mx <= 1255 :
                precision_slider_pos = round(mx/25,0) * 25 + 5
                precision = int(( (precision_slider_pos - 930)/325 ) * 13 + 1)
            elif precision_slider_pressed == True and mx < 930:
                precision_slider_pos = 930
                precision = int(( (precision_slider_pos - 930)/325 ) * 13 + 1)
            elif precision_slider_pressed == True and mx > 1255:
                precision_slider_pos = 1255
                precision = int(( (precision_slider_pos - 930)/325 ) * 13 + 1)


            #undo colour change on release
            if precision_slider_pressed == True and event.type == pg.MOUSEBUTTONUP:
                    precision_slider_pressed = False
                    precision_slider_colour = (230, 234, 35)
            #endregion
            #-------------------------------------------------
            #region
            if (mx-time_slider_pos)**2 + (my-443)**2 <= (7)**2 and event.type == pg.MOUSEBUTTONDOWN:
               
                    time_slider_pressed = True
                    time_slider_colour = (155, 167, 17)
                
            if time_slider_pressed == True and 930 <= mx <= 1255 :
                time_slider_pos = mx 
                dt = ((time_slider_pos - 930)/325)* 0.0002 
            elif time_slider_pressed == True and mx < 930:
                time_slider_pos = 930
                dt = ((time_slider_pos - 930)/325)* 0.0002 
            elif time_slider_pressed == True and mx > 1255:
                time_slider_pos = 1255
                dt = ((time_slider_pos - 930)/325)* 0.0002

            if time_slider_pressed == True and event.type == pg.MOUSEBUTTONUP:
                    time_slider_pressed = False
                    time_slider_colour = (230, 234, 35)
                
            #endregion
            #measurement
            if 100 < mx < 190 and 545 < my < 580 and event.type == pg.MOUSEBUTTONDOWN:
               
                    measure_button_pressed = True
                    measure_button_colour = (150, 150, 150)
                
                    i_2 = round(550/precision)
                    prob_list = []
                    start, end = 0, i_2
                    locations = np.linspace(1,precision,precision)
                    for section in range(0, precision, 1):
                        probability = np.trapezoid(prob_dens[start:end], x_values[start:end])
                        prob_list.append(probability)
                        start += i_2
                        end += i_2
                    n_prob_list = np.array(prob_list)/sum(prob_list)
                    location = int(np.random.choice(locations, p=n_prob_list)) # this is where the particle is after measurement
                
                    #zero out non positve result areas
                    psi[0:(location - 1)*i_2] = 0
                    psi[location*i_2: 551] = 0  

                    #apply drop off gradient
                    laser_profile =np.sin(np.linspace(0,1, len(psi[(location - 1)*i_2:location*i_2]))*np.pi)**0.8
                    psi[(location - 1)*i_2:location*i_2] = psi[(location - 1)*i_2:location*i_2] * laser_profile

                    #renormalise
                    prob_dens = np.real( (psi)*np.conj(psi) )
                    psi = psi * np.sqrt(1/ np.trapezoid(prob_dens,x_values))
                
                    #fourier the psi
                    F_cns_list = []
                    for mode in range(1, 201, 1):
                        F_cns = np.trapezoid(np.sqrt(2/well_length) * np.sin(np.pi * mode * x_values / well_length) * psi, x_values)
                        F_cns_list.append(F_cns)
                    cns = np.array(F_cns_list)

                    #renormalise
                    cns = cns / np.sqrt(np.sum(np.abs(cns)**2))

                    time = 0
                #update cn visualiser
                    Cn_max = np.max(np.abs(cns))**2
                    rendering_cns = 210 - (np.abs(cns)**2 * 140/Cn_max)
                    cn_points = list(zip(Cn_X_values,rendering_cns))

                    #std momentum                 
                    p_mean = np.sum(np.abs(cns)**2 * np.linspace(1*np.pi/well_length, 200*np.pi/well_length, 200))
                    p_mean2 = np.sum(np.abs(cns)**2 * np.linspace(1*np.pi/well_length, 200*np.pi/well_length, 200)**2)
                    std_p = np.sqrt(max(0,p_mean2))


            if measure_button_pressed == True and event.type == pg.MOUSEBUTTONUP:
                    measure_button_pressed = False
                    measure_button_colour = (255, 255, 255)
        
            #reset
            if 210 < mx < 270 and 545 < my < 580 and event.type == pg.MOUSEBUTTONDOWN:
               
                    reset_button_pressed = True
                    reset_button_colour = (150, 150, 150)
                    cns = Cn_calc(Temp, mass, well_length)
                    time = 0

                #update cn visualiser
                    Cn_max = np.max(np.abs(cns))**2
                    rendering_cns = 210 - (np.abs(cns)**2 * 140/Cn_max)
                    cn_points = list(zip(Cn_X_values,rendering_cns))

                    #std momentum                 
                    p_mean = np.sum(np.abs(cns)**2 * np.linspace(1*np.pi/well_length, 200*np.pi/well_length, 200))
                    p_mean2 = np.sum(np.abs(cns)**2 * np.linspace(1*np.pi/well_length, 200*np.pi/well_length, 200)**2)
                    std_p = np.sqrt(max(0,p_mean2))

            if reset_button_pressed == True and event.type == pg.MOUSEBUTTONUP:
                    reset_button_pressed = False
                    reset_button_colour = (255, 255, 255)
            
            #restart
            if 105 < mx < 180 and 670 < my < 695 and event.type == pg.MOUSEBUTTONDOWN:
                    restart_button_pressed = True
                    restart_button_colour = (150, 150, 150)
                    input_state = 0

                    if temp_input_outline_colour != (239,0,0) and wl_input_outline_colour != (239,0,0) and mass_input_outline_colour != (239,0,0):
                        Temp = int(temp_input)
                        well_length = int(wl_input)
                        x_values = np.linspace(0, well_length, 550)
                        mass = int(mass_input)
                        cns = Cn_calc(Temp, mass, well_length)
                        time = 0

                        #update cn visualiser
                        Cn_max = np.max(np.abs(cns))**2
                        rendering_cns = 210 - (np.abs(cns)**2 * 140/Cn_max)
                        cn_points = list(zip(Cn_X_values,rendering_cns))

                        #std momentum                 
                        p_mean = np.sum(np.abs(cns)**2 * np.linspace(1*np.pi/well_length, 200*np.pi/well_length, 200))
                        p_mean2 = np.sum(np.abs(cns)**2 * np.linspace(1*np.pi/well_length, 200*np.pi/well_length, 200)**2)
                        std_p = np.sqrt(max(0,p_mean2))

            if restart_button_pressed == True and event.type == pg.MOUSEBUTTONUP:
                    restart_button_pressed = False
                    restart_button_colour = (255, 255, 255)    
            #typing to change variables
            #region
            if 153 < mx < 203 and 597 < my < 615 and event.type == pg.MOUSEBUTTONDOWN:
                input_state = 1
                current_time = pg.time.get_ticks()         

            if event.type == pg.KEYDOWN and input_state == 1:
                if event.key == pg.K_BACKSPACE:
                    temp_input = temp_input[:-1]
                elif event.key == pg.K_RETURN:
                    input_state = 0
                elif event.unicode.isdigit() and len(temp_input) <= 3:
                    temp_input += event.unicode

            if 203 < mx < 253 and 620 < my < 640 and event.type == pg.MOUSEBUTTONDOWN:
                input_state = 2
                current_time = pg.time.get_ticks()         

            if event.type == pg.KEYDOWN and input_state == 2:
                if event.key == pg.K_BACKSPACE:
                    wl_input = wl_input[:-1]
                elif event.key == pg.K_RETURN:
                    input_state = 0
                elif event.unicode.isdigit() and len(wl_input) <= 3:
                    wl_input += event.unicode
          

            if 153 < mx < 203 and 645 < my < 663 and event.type == pg.MOUSEBUTTONDOWN:
                input_state = 3
                current_time = pg.time.get_ticks()         

            if event.type == pg.KEYDOWN and input_state == 3:
                if event.key == pg.K_BACKSPACE:
                    mass_input = mass_input[:-1]
                elif event.key == pg.K_RETURN:
                    input_state = 0
                elif event.unicode.isdigit() and len(mass_input) <= 3:
                    mass_input += event.unicode            
            #endregion
            #hover events
            #region
            if 340 < mx < 700 and 25 < my < 50: # prob dens window
                info_state = 1
            elif 1000 < mx < 1210 and 25 < my < 50: # Cn^2 dist
                info_state = 2
            elif 75 < mx < 100 and 200 < my < 370: # prob dens
                info_state = 3
            elif 930 < mx < 950 and 50 < my < 210: # relative prob
                info_state = 4
            elif 1040 < mx < 1140 and 212 < my < 230: # eigenstate
                info_state = 5
            elif 920 < mx < 1020 and 230 < my < 250: # sigma_x
                info_state = 6
            elif 920 < mx < 1020 and 280 < my < 310: # sigma_p
                info_state = 7
            elif 1070 < mx < 1260 and 260 < my < 290: # sigma_p*x
                info_state = 8
            elif 1020 < mx < 1160 and 360 < my < 380: # precision
                info_state = 9
            elif 1020 < mx < 1150 and 460 < my < 485: # sim speed
                info_state = 10
            elif 425 < mx < 525 and 503 < my < 520: # well length
                info_state = 11
            elif 100 < mx < 190 and 545 < my < 580: # measure
                info_state = 12
            elif 210 < mx < 270 and 545 < my < 580: # reset
                info_state = 13
            elif 100 < mx < 150 and 595 < my < 615: # temp
                info_state = 14
            elif 100 < mx < 200 and 620 < my < 640: # wl
                info_state = 15
            elif 100 < mx < 150 and 645 < my < 660: # mass
                info_state = 16
            elif 105 < mx < 180 and 670 < my < 695: # restart
                info_state = 17
            else:
                info_state = 0
            #endregion
            #===========================================================================================================

            if event.type == pg.QUIT:
                running = False


        #Drawing UI
        #region

        screen.blit(bg, (0, 0))

        pg.draw.circle(screen, precision_slider_colour, (precision_slider_pos, 343), 7, 0)
        pg.draw.circle(screen, (0, 0, 0), (precision_slider_pos, 343), 8, 1) 

        pg.draw.circle(screen, time_slider_colour, (time_slider_pos, 443), 7, 0)
        pg.draw.circle(screen, (0, 0, 0), (time_slider_pos, 443), 8, 1)

        pg.draw.rect(bg, measure_button_colour, [102,547,88,33], 2, 2)
        pg.draw.rect(bg, reset_button_colour, [212,547,58,33], 2, 2)
        pg.draw.rect(bg, restart_button_colour, [107,672,73,23], 2, 2)
        xs_font.render_to(text_surface, (880, 505), "x = " + str(well_length), (12, 11, 13))
        #endregion
    #error checking that inputs are not 0----------------------------------------------------
    #region
        if temp_input == '' or float(temp_input) == 0:
            temp_input_outline_colour = (239,0,0)
        elif float(temp_input) != Temp:
            temp_input_outline_colour = (0,143,200)
        else:
            temp_input_outline_colour = (43,43,43)

        if wl_input == '' or int(wl_input) == 0:
            wl_input_outline_colour = (239,0,0)
        elif int(wl_input) != well_length:
            wl_input_outline_colour = (0,143,200)
        else:
            wl_input_outline_colour = (43,43,43)

        if mass_input == '' or int(mass_input) == 0:
            mass_input_outline_colour = (239,0,0)
        elif int(mass_input) != mass:
            mass_input_outline_colour = (0,143,200)
        else:
            mass_input_outline_colour = (43,43,43)

        pg.draw.lines(bg, temp_input_outline_colour, True, temp_input_outline, 2)
        pg.draw.lines(bg, wl_input_outline_colour, True, wl_input_outline, 2)
        pg.draw.lines(bg, mass_input_outline_colour, True, mass_input_outline, 2)
    #endregion
    #---------------------------------------------------------------------------------------------
        #measurement, sigma xp, flickering bar
    #region
        if precision_slider_pressed == True: # measurement border indicator
            increment = round(800/precision)
            k=100+increment
            for line in range (1, int(precision), 1):
                pg.draw.line(screen, (158,158,158),(k, 51),(k, 500))
                k += increment

        if measure_button_pressed == True: # measurement result
            pg.draw.rect(measurement_surface, (30, 206, 0, 70), [101+(location-1)*(800/precision),52 ,(800/precision) ,449])

        pg.draw.lines(screen,(40, 40, 40), False, cn_points, 3)

        s_font.render_to(screen, (923, 235), "σx = " + str(round(std_x,3)), (12, 11, 13))
        s_font.render_to(screen, (923, 285), "σp = " + str(round(std_p,3)), (12, 11, 13))
        font.render_to(screen, (1083, 260),"σp*σx = " + str(round(std_p*std_x,3)), (12, 11, 13))

        if input_state == 1:
            flick_time = pg.time.get_ticks() - current_time
            if int((flick_time // 500)) % 2 == 0:
                pg.draw.line(screen, (158,158,158), (160 + 10*(len(temp_input)), 600), (160+ 10*(len(temp_input)), 612)) # flickering typing bar
        ms_font.render_to(screen, (160, 601), temp_input, (12, 11, 13))

        if input_state == 2:
            flick_time = pg.time.get_ticks() - current_time
            if int((flick_time // 500)) % 2 == 0:
                pg.draw.line(screen, (158,158,158), (210 + 10*(len(wl_input)), 624), (210+ 10*(len(wl_input)), 636)) 
        ms_font.render_to(screen, (210, 625), wl_input, (12, 11, 13))

        if input_state == 3:
            flick_time = pg.time.get_ticks() - current_time
            if int((flick_time // 500)) % 2 == 0:
                pg.draw.line(screen, (158,158,158), (160 + 10*(len(mass_input)), 648), (160+ 10*(len(mass_input)), 660))
        ms_font.render_to(screen, (160, 649), mass_input, (12, 11, 13))
    #endregion
        #simulator descriptions
        #region
        if info_state == 1:
            ms_font.render_to(screen, (405, 550), '• 1D quantum systems can be modelled as a wavefunction ψ(x,t) where x is a position in space and t is a ', (12, 11, 13))
            ms_font.render_to(screen, (405, 570), '   point in time.', (12, 11, 13))
            ms_font.render_to(screen, (405, 590), '• The output of this function gives a probability amplitude which when squared (ψ x ψ*) gives a probability', (12, 11, 13))
            ms_font.render_to(screen, (405, 610), '   density.', (12, 11, 13))
        elif info_state == 2:
            ms_font.render_to(screen, (405, 550), '• Each eigenstate has an associated coefficient. When the coefficient is squared, it represents the', (12, 11, 13))
            ms_font.render_to(screen, (405, 570), '   probability of that eigenstate\'s energy being measured.', (12, 11, 13))
            ms_font.render_to(screen, (405, 590), '• When a precise measurement is taken, on average the distribution shifts right, showing how the energy', (12, 11, 13))
            ms_font.render_to(screen, (405, 610), '   of the system has increased as a result.', (12, 11, 13))
            ms_font.render_to(screen, (405, 630), '• If the coefficient for n = 200 has any magnitude, the simulation may no longer be accurate as the ', (12, 11, 13))
            ms_font.render_to(screen, (405, 650), '   wavefunction can no longer be recontructed accurately (modes above 200 are not calculated).', (12, 11, 13))
        elif info_state == 3:
            ms_font.render_to(screen, (405, 550), '• The area under the curve between two points is equal to the probability of finding the particle there', (12, 11, 13))
            ms_font.render_to(screen, (405, 570), '   post measurement.', (12, 11, 13))
            ms_font.render_to(screen, (405, 590), '• Since the probability of finding the particle in the well is 100%, as the probability density wave ', (12, 11, 13))
            ms_font.render_to(screen, (405, 610), '   changes with time, the  total area will remain constant.', (12, 11, 13))
            ms_font.render_to(screen, (405, 630), '• The y axis scale is more representative of probability, not probability density, so \'p = 1 ↑\' represents', (12, 11, 13))
            ms_font.render_to(screen, (405, 650), '   how - the higher the peak, the higher the likelihood that the particle\'s position is to be measured there. ', (12, 11, 13))
        elif info_state == 4:
            ms_font.render_to(screen, (405, 550), '• The scaling of this axis is relative, so the highest value of Cn squared always sits at a consistent height, ', (12, 11, 13))
            ms_font.render_to(screen, (405, 570), '   with the other values height based around it.', (12, 11, 13))
        elif info_state == 5:
            ms_font.render_to(screen, (405, 550), '• When solving the spatial part of the Schrodinger equation for a well, the solution is a sine wave that', (12, 11, 13))
            ms_font.render_to(screen, (405, 570), '   must equal zero at the boundaries. sin(f(x)) = 0 only if f(x) equals some integer muliple of pi when ', (12, 11, 13))
            ms_font.render_to(screen, (405, 590), '   x = well length.', (12, 11, 13))
            ms_font.render_to(screen, (405, 610), '• Each multiple of pi is a valid solution, and each solution is called an eigenstate.', (12, 11, 13))
            ms_font.render_to(screen, (405, 630), '• Higher eigenstates (e.g. n = 50) require more energy to have a significant probability of being present.', (12, 11, 13))
        elif info_state == 6:
            ms_font.render_to(screen, (405, 550), '• σx is the standard deviation of the particles position. So σx is small when a narrow spike is formed and', (12, 11, 13))
            ms_font.render_to(screen, (405, 570), '   gets larger as the particle\'s superposition gets more spread out', (12, 11, 13))
        elif info_state == 7:
            ms_font.render_to(screen, (405, 550), '• σp is the standard deviation of the paricles momentum. Since the inside of the well has no potential', (12, 11, 13))
            ms_font.render_to(screen, (405, 570), '   the entirety of each eigenstates associated energy is kinetic, from which you can calculuate momentum.', (12, 11, 13))
            ms_font.render_to(screen, (405, 590), '• σp will be small if only a few eigenstates are largely present and in a small bundle, such as when', (12, 11, 13))
            ms_font.render_to(screen, (405, 610), '   Temp = 1, where only n = 1 and n = 2 are present', (12, 11, 13))
            ms_font.render_to(screen, (405, 630), '• σp must be large to observe a narrow spike in the probability density, as a wide array of eigenstates are', (12, 11, 13))
            ms_font.render_to(screen, (405, 650), '   needed (each with a significant coefficient contribution) to describe it.', (12, 11, 13))
        elif info_state == 8:
            ms_font.render_to(screen, (405, 550), '• σp*σx = RPC †/2 is the basis of Heisenberg\'s uncertainty principle. This simulation uses natural units', (12, 11, 13))
            ms_font.render_to(screen, (405, 570), '   where in this case RPC † = 1, therefore the absolute mimimum value observable is 0.5.', (12, 11, 13))
            ms_font.render_to(screen, (405, 590), '• This occurs since σp and σx are inversely proportional. A very disperse probability density like a sine', (12, 11, 13))
            ms_font.render_to(screen, (405, 610), '   wave requires few eigenstates to describe (using fourier analysis), whereas a very localised probability', (12, 11, 13))
            ms_font.render_to(screen, (405, 630), '   density will require many eigenstates to describe (also with fourier analysis).', (12, 11, 13))
            xs_font.render_to(screen, (405, 690), '† RPC stands for \'Reduced Planck\'s Constant\', aka h bar', (12, 11, 13))
        elif info_state == 9:
            ms_font.render_to(screen, (405, 550), '• Hold down the slider ball to see a preview of the measurement width.', (12, 11, 13))
            ms_font.render_to(screen, (405, 570), '• Precision ranges from the whole well to a fourteenth of the well length.', (12, 11, 13))
            ms_font.render_to(screen, (405, 590), '• While the well-wide measurment seems to \'cool\' the system down by removing the high energy', (12, 11, 13))
            ms_font.render_to(screen, (405, 610), '   eigenstates, this is a byproduct of the measurement shifting the wavefunction to exhibit a sin(x)^0.8', (12, 11, 13))
            ms_font.render_to(screen, (405, 630), '   shape, where fourier analysis results in only the first few eigenstates being needed to describe it. In', (12, 11, 13))
            ms_font.render_to(screen, (405, 650), '   reality this form of measurement is still injecting energy into the system.', (12, 11, 13))
        elif info_state == 10:
            ms_font.render_to(screen, (405, 550), '• Simulation speed slider can be set to the far left to freeze the simulation.', (12, 11, 13))
        elif info_state == 11:
            ms_font.render_to(screen, (405, 550), '• In real quantum systems, such as ion traps, the effective well length is in micrometers.', (12, 11, 13))
            ms_font.render_to(screen, (405, 570), '• In this simulation the length is unitless.', (12, 11, 13))
        elif info_state == 12:
            ms_font.render_to(screen, (405, 550), '• The measurement event integrates the curves area for the probability of the particle being in each', (12, 11, 13))
            ms_font.render_to(screen, (405, 570), '   division, and then the division the particle is in is randomly chosen based off of the probabilities.', (12, 11, 13))
            ms_font.render_to(screen, (405, 590), '• The measurement instrument can be thought of as a laser with a potential gradient of sin(x)^0.8, in the', (12, 11, 13))
            ms_font.render_to(screen, (405, 610), '   simulation the wavefunction is directly multiplied by the potential gradient, however a truer ', (12, 11, 13))
            ms_font.render_to(screen, (405, 630), '   simulation would set V(x) in the Schrodinger equation to sin(x)^0.8 and solve, though an analytical ', (12, 11, 13))
            ms_font.render_to(screen, (405, 650), '   solution would then become impossible. The multiplication method is accurate enough for the purposes', (12, 11, 13))
            ms_font.render_to(screen, (405, 667), '   of this simulation.', (12, 11, 13))
            ms_font.render_to(screen, (405, 685), '• To take rapid repeated measurements, you can use the scroll wheel.', (12, 11, 13))
        elif info_state == 13:
            ms_font.render_to(screen, (405, 550), '• Resets the Cn^2 distibution back to it\'s initial state pre-measurement and the time back to 0', (12, 11, 13))
        elif info_state == 14:
            ms_font.render_to(screen, (405, 550), '• With only a single particle in the system, temperature is somewhat trivial as it represents the average', (12, 11, 13))
            ms_font.render_to(screen, (405, 570), '   kinetic energy of mulitple particles. So in this setting it should just be viewed as a more intuitive metric', (12, 11, 13))
            ms_font.render_to(screen, (405, 590), '   for the intial energy in the system. ', (12, 11, 13))
            ms_font.render_to(screen, (405, 610), '• The temperature scale is a pseudo-kelvin scale in that temp = 0 is the absolute zero state.', (12, 11, 13))
        elif info_state == 15:
            ms_font.render_to(screen, (405, 550), '• Increasing well length decreases the energy requirement for each eigenstate as their corresponding', (12, 11, 13))
            ms_font.render_to(screen, (405, 570), '   wavefunctions, will be more spread out in a larger well. As a result the Cn^2 distribution shifts right,', (12, 11, 13))
            ms_font.render_to(screen, (405, 590), '   though no additional energy has been introduced into the system from this.', (12, 11, 13))
            ms_font.render_to(screen, (405, 610), '• Time period for events is proportional to the well length squared.', (12, 11, 13))
        elif info_state == 16:
            ms_font.render_to(screen, (405, 550), '• Increasing mass is directly proportionate to increasing time period between events.', (12, 11, 13))
            ms_font.render_to(screen, (405, 570), '• If you consider a proton or neutron as having a mass of 1, then it soon becomes evident why classical', (12, 11, 13))
            ms_font.render_to(screen, (405, 590), '   objects don\'t exhibit wave-like or quantum mechanical phenomena.', (12, 11, 13))
            ms_font.render_to(screen, (405, 610), '• A speck of dust would have a mass of 10^18 in this instance.', (12, 11, 13))
        elif info_state == 17:
            ms_font.render_to(screen, (405, 550), '• A red border around an input box means the input is invalid, usually due to the input being 0.', (12, 11, 13))
            ms_font.render_to(screen, (405, 570), '• A blue border means the displayed value is different to the value being used in the current simulation.', (12, 11, 13))
            ms_font.render_to(screen, (405, 590), '• Hitting the restart button restarts the simulation with the displayed values becoming the new variables', (12, 11, 13))
            ms_font.render_to(screen, (405, 610), '   used in the simulation.', (12, 11, 13))
        else:
            ms_font.render_to(screen, (405, 610), '', (12, 11, 13))
        #endregion
        #=========================================
        screen.blit(measurement_surface, (0,0))
        pg.display.flip()

pg.quit()
