import pandas as pd
import plotly.express as px
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


def plot_vision_vs_rotvel(df):
    fig = px.scatter(
        df,
        x="vision", 
        y="rot_vel",
        color="species",                  
        animation_frame="frame",          
        range_x=[0, df['vision'].max()+10], 
        range_y=[0, df['rot_vel'].max()+2],
        title="Evolution of Robot Species Over Time",
    )


    fig.update_layout(
        xaxis_title="Vision",
        yaxis_title="Rotation Speed",
        legend_title="Species"
    )
    fig.show()

def plot_3d_vis_rot_vel(df):
    fig = px.scatter_3d(
        df,
        x="vision", 
        y="rot_vel",
        z="velocity",
        color="species",                  
        animation_frame="frame",          
        range_x=[0, df['vision'].max()+10], 
        range_y=[0, df['rot_vel'].max()+2],
        range_z=[0, df['velocity'].max()+2],
        title="3D Evolution of Robot Species Over Time",
    )


    fig.update_layout(
        xaxis_title="Vision",
        yaxis_title="Rotation Speed",
        legend_title="Species"
    )
    fig.show()

def plot_3d_rot_vel_fail_vel(df):
    fig = px.scatter_3d(
        df,
        x="rot_vel", 
        y="prob_fail_rot",
        z="velocity",
        color="species",                  
        animation_frame="frame",          
        range_x=[0, df['rot_vel'].max()+10], 
        range_y=[0, df['prob_fail_rot'].max()+2],
        range_z=[0, df['velocity'].max()+2],
        title="3D Evolution of Robot Species Over Time",
    )


    fig.update_layout(
        xaxis_title="Vision",
        yaxis_title="Rotation Speed",
        legend_title="Species"
    )
    fig.show()

def evolution_over_time():
    df = pd.read_csv('logs/play0/snapshot.csv')

    all_species_labels = []

    frames = sorted(df['frame'].unique())

    for frame in frames:
        frame_data = df[df['frame'] == frame][["velocity","rot_vel","vision","prob_fail_rot"]]

        genes_scaled = StandardScaler().fit_transform(frame_data)

        dbscan = DBSCAN(eps=0.7, min_samples=5) 

        species_labels = dbscan.fit_predict(genes_scaled)
        all_species_labels.append(species_labels)

        df.loc[df['frame'] == frame, 'species'] = species_labels

    

    plot_vision_vs_rotvel(df)
    plot_3d_rot_vel_fail_vel(df)
    plot_3d_vis_rot_vel(df)


evolution_over_time()