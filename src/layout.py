# -*- coding: utf-8 -*-
'''
Created on 11.05.2017

@author: dca

File containing plotting settings
'''

import numpy as np

copyright=u"\u00a9"
subtwo=u"\u2082"
suptwo=u"\u00B2"
celsius=u"\u00b0"+"C"
percent_sign=" "+u"\u0025"

rwth_blue=np.array([0., 84., 159.])/255
rwth_black=np.array([0., 0., 0.])/255
rwth_magenta=np.array([227., 0., 102.])/255
rwth_yellow=np.array([255., 237., 0.])/255
rwth_petrol=np.array([0., 97., 101.])/255
rwth_turquoise=np.array([0., 152., 161.])/255
rwth_green=np.array([87., 171., 39.])/255
rwth_maygreen=np.array([189., 205., 0.])/255
rwth_orange=np.array([246., 168., 0.])/255
rwth_red=np.array([204., 7., 30.])/255
rwth_bordeaux=np.array([161., 16., 53.])/255
rwth_violet=np.array([97., 33., 88.])/255
rwth_purple=np.array([122., 111., 172.])/255

rwth_blue_75 = np.array([64,127,183])/255.
rwth_blue_50 = np.array([142,186,229])/255.
rwth_blue_25 = np.array([199,221,242])/255.
rwth_blue_10 = np.array([232,241,250])/255.
rwth_black_75 = np.array([100,101,103])/255.
rwth_black_50 = np.array([156,158,159])/255.
rwth_black_25 = np.array([207,209,210])/255.
rwth_black_10 = np.array([236,237,237])/255.
rwth_magenta_75 = np.array([233,96,136])/255.
rwth_magenta_50 = np.array([241,158,177])/255.
rwth_magenta_25 = np.array([249,210,218])/255.
rwth_magenta_10 = np.array([253,238,240])/255.
rwth_yellow_75 = np.array([255,240,85])/255.
rwth_yellow_50 = np.array([255,245,155])/255.
rwth_yellow_25 = np.array([255,250,209])/255.
rwth_yellow_10 = np.array([255,253,238])/255.
rwth_petrol_75 = np.array([45,127,131])/255.
rwth_petrol_50 = np.array([125,164,167])/255.
rwth_petrol_25 = np.array([191,208,209])/255.
rwth_petrol_10 = np.array([230,236,236])/255.
rwth_turquoise_75 = np.array([0,177,183])/255.
rwth_turquoise_50 = np.array([137,204,207])/255.
rwth_turquoise_25 = np.array([202,231,231])/255.
rwth_turquoise_10 = np.array([235,246,246])/255.
rwth_green_75 = np.array([141,192,96])/255.
rwth_green_50 = np.array([184,214,152])/255.
rwth_green_25 = np.array([221,235,206])/255.
rwth_green_10 = np.array([242,247,236])/255.
rwth_maygreen_75 = np.array([208,217,92])/255.
rwth_maygreen_50 = np.array([224,230,154])/255.
rwth_maygreen_25 = np.array([240,243,208])/255.
rwth_maygreen_10 = np.array([249,250,237])/255.
rwth_orange_75 = np.array([250,190,80])/255.
rwth_orange_50 = np.array([253,212,143])/255.
rwth_orange_25 = np.array([254,234,201])/255.
rwth_orange_10 = np.array([255,247,234])/255.
rwth_red_75 = np.array([216,92,65])/255.
rwth_red_50 = np.array([230,150,121])/255.
rwth_red_25 = np.array([243,205,187])/255.
rwth_red_10 = np.array([250,235,227])/255.
rwth_bordeaux_75 = np.array([182,82,86])/255.
rwth_bordeaux_50 = np.array([205,139,135])/255.
rwth_bordeaux_25 = np.array([229,197,192])/255.
rwth_bordeaux_10 = np.array([245,232,229])/255.
rwth_violet_75 = np.array([131,78,117])/255.
rwth_violet_50 = np.array([168,133,158])/255.
rwth_violet_25 = np.array([210,192,205])/255.
rwth_violet_10 = np.array([237,229,234])/255.
rwth_purple_75 = np.array([155,145,193])/255.
rwth_purple_50 = np.array([188,181,215])/255.
rwth_purple_25 = np.array([222,218,235])/255.
rwth_purple_10 = np.array([242,240,247])/255.

rwth_main_colors=[rwth_blue, rwth_black, rwth_magenta,rwth_yellow,rwth_petrol,rwth_turquoise,rwth_green,rwth_maygreen,rwth_orange,rwth_red,rwth_bordeaux,rwth_violet,rwth_purple]
rwth_75_colors=[rwth_blue_75, rwth_black_75, rwth_magenta_75,rwth_yellow_75,rwth_petrol_75,rwth_turquoise_75,rwth_green_75,rwth_maygreen_75,rwth_orange_75,rwth_red_75,rwth_bordeaux_75,rwth_violet_75,rwth_purple]
rwth_50_colors=[rwth_blue_50, rwth_black_50, rwth_magenta_50,rwth_yellow_50,rwth_petrol_50,rwth_turquoise_50,rwth_green_50,rwth_maygreen_50,rwth_orange_50,rwth_red_50,rwth_bordeaux_50,rwth_violet_50,rwth_purple]
rwth_25_colors=[rwth_blue_25, rwth_black_25, rwth_magenta_25,rwth_yellow_25,rwth_petrol_25,rwth_turquoise_25,rwth_green_25,rwth_maygreen_25,rwth_orange_25,rwth_red_25,rwth_bordeaux_25,rwth_violet_25,rwth_purple]
rwth_10_colors=[rwth_blue_10, rwth_black_10, rwth_magenta_10,rwth_yellow_10,rwth_petrol_10,rwth_turquoise_10,rwth_green_10,rwth_maygreen_10,rwth_orange_10,rwth_red_10,rwth_bordeaux_10,rwth_violet_10,rwth_purple]

rwth_cold_hot=[rwth_purple, rwth_blue, rwth_blue_50, rwth_orange, rwth_red, rwth_bordeaux, rwth_violet]
fancy_colors=["r","Sienna","FireBrick","Red","OrangeRed","Tomato","DeepPink","Fuchsia","Magenta","MediumVioletRed","Crimson"]
greens_blues=["LimeGreen","ForestGreen","DarkGreen","LightSkyBlue","CornflowerBlue","DarkSlateBlue"]
rwth_greens_blues=[rwth_maygreen, rwth_green, rwth_petrol, rwth_blue_50, rwth_blue, rwth_purple]

wpg_markers=['s','^','o','h','+','x','s','p','*','d']


'''
lighter_colors_codes=[np.array([64., 127-183.])/255.,np.array([142-186-229.])/255.,np.array([199-221-242.])/255.,np.array([232-241-250.])/255.,np.array([100-101-103.])/255.,np.array([156-158-159.])/255.,np.array([207-209-210.])/255.,np.array([236-237-237.])/255.,np.array([233-96-136.])/255.,np.array([241-158-177.])/255.,np.array([249-210-218.])/255.,np.array([253-238-240.])/255.,np.array([255-240-85.])/255.,np.array([255-245-155.])/255.,np.array([255-250-209.])/255.,np.array([255-253-238.])/255.,np.array([45-127-131.])/255.,np.array([125-164-167.])/255.,np.array([191-208-209.])/255.,np.array([230-236-236.])/255.,np.array([0-177-183.])/255.,np.array([137-204-207.])/255.,np.array([202-231-231.])/255.,np.array([235-246-246.])/255.,np.array([141-192-96.])/255.,np.array([184-214-152.])/255.,np.array([221-235-206.])/255.,np.array([242-247-236.])/255.,np.array([208-217-92.])/255.,np.array([224-230-154.])/255.,np.array([240-243-208.])/255.,np.array([249-250-237.])/255.,np.array([250-190-80.])/255.,np.array([253-212-143.])/255.,np.array([254-234-201.])/255.,np.array([255-247-234.])/255.,np.array([216-92-65.])/255.,np.array([230-150-121.])/255.,np.array([243-205-187.])/255.,np.array([250-235-227.])/255.,np.array([182-82-86.])/255.,np.array([205-139-135.])/255.,np.array([229-197-192.])/255.,np.array([245-232-229.])/255.,np.array([131-78-117.])/255.,np.array([168-133-158.])/255.,np.array([210-192-205.])/255.,np.array([237-229-234.])/255.,np.array([155-145-193.])/255.,np.array([188-181-215.])/255.,np.array([222-218-235.])/255.,np.array([242-240-247.])/255.]

main_colors=['rwth_blue'',''rwth_black','rwth_magenta','rwth_yellow','rwth_petrol','rwth_turquoise','rwth_green','rwth_maygreen','rwth_orange','rwth_red','rwth_bordeaux','rwth_violet','rwth_purple']
shades=['_75','_50','_25','_10']
lighter_colors=[]

for mc in main_colors:
    for s in shades:
        print mc+s


print(lighter_colors)
'''
