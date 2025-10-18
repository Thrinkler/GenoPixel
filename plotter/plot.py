import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

import seaborn as sns

import numpy as np
import pandas as pd


msft = pd.read_csv('logs/play2/mean.csv')
time = range(len(msft))

def time_plot():
    plt.plot(time, msft['food_count'])
    plt.plot(time, msft['robots_count'])
    plt.plot(time, msft['avg_speed']*50)
    plt.plot(time, msft['avg_rot_vel']*50)
    plt.plot(time, msft['avg_vision']*5)
    plt.plot(time, msft['avg_fail_rot']*5)
    plt.legend(['Food Count', 'Robot Count', 'Avg Speed x50', 'Avg Rot Vel x50', 'Avg Vision x5', 'Avg Fail Rot x5'])
    plt.title('Time vs Robots characteristics and food count')
    plt.grid(True)
    plt.show()


def correlation_plot():
    corr_matrix = msft.corr()
    print(corr_matrix)
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Mapa de Calor de Correlaciones de la Simulación')
    plt.show()


def food_vs_robots_plot():
    
    plt.plot(msft['food_count'], msft['robots_count'])
    plt.xlabel('Food Count')
    plt.ylabel('Robot Count')
    plt.title('Food Count vs Robot Count')
    plt.grid(True)
    plt.show()

def robots_characteristics_vs_robots_plot():
    plt.plot(msft['avg_speed'], msft['robots_count'], label='Avg Speed vs Robot Count')
    plt.plot(msft['avg_rot_vel'], msft['robots_count'], label='Avg Rot Vel vs Robot Count')
    plt.plot(msft['avg_vision'], msft['robots_count'], label='Avg Vision vs Robot Count')
    plt.plot(msft['avg_fail_rot'], msft['robots_count'], label='Avg Fail Rot vs Robot Count')
    plt.xlabel('Robot Characteristics')
    plt.ylabel('Robot Count')
    plt.title('Robot Characteristics vs Robot Count')
    plt.legend()
    plt.grid(True)
    plt.show()


def speed_vs_rotvel():
    plt.plot(msft['avg_speed'], msft['avg_rot_vel'])
    plt.xlabel('Avg Speed')
    plt.ylabel('Avg Rot Vel')
    plt.title('Avg Speed vs Avg Rot Vel')
    plt.grid(True)
    plt.show()

def rotvel_vs_failrot():
    plt.plot(msft['avg_rot_vel'], msft['avg_fail_rot'])
    plt.xlabel('Avg Rot Vel')
    plt.ylabel('Avg Fail Rot')
    plt.title('Avg Rot Vel vs Avg Fail Rot')
    plt.grid(True)
    plt.show()

def vision_vs_failrot():
    plt.plot(msft['avg_vision'], msft['avg_fail_rot'])
    plt.xlabel('Avg Vision')
    plt.ylabel('Avg Fail Rot')
    plt.title('Avg Vision vs Avg Fail Rot')
    plt.grid(True)
    plt.show()

def speed_vs_vision():
    plt.plot(msft['avg_speed'], msft['avg_vision'])
    plt.xlabel('Avg Speed')
    plt.ylabel('Avg Vision')
    plt.title('Avg Speed vs Avg Vision')
    plt.grid(True)
    plt.show()



time_plot()
correlation_plot()
food_vs_robots_plot()
robots_characteristics_vs_robots_plot()
speed_vs_rotvel()
rotvel_vs_failrot()
vision_vs_failrot()
speed_vs_vision()