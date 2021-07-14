import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#visualización de la imagen
from tkinter import *
from PIL import Image, ImageTk,ImageDraw

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Cuadro de comandos")

st.write("Aquí se puede visualizar el dataset transformado")

#Datasets
@st.cache
def load_data_transformed():
    data = pd.read_csv("../transformed_data/static_defenses.csv",index_col=1)
    data.drop(["Unnamed: 0"],axis=1,inplace=True)
    return data

@st.cache
def load_data_games():
    data = pd.read_csv("../raw_data/games.csv",index_col=0)
    return data

@st.cache
def load_data_plays():
    data = pd.read_csv("../processed_data/clean/plays.csv",index_col=1)
    data.drop(["Unnamed: 0"],axis=1,inplace=True)
    return data

@st.cache
def load_data_static():
    data = pd.read_csv("../processed_data/weeks_frame1/frame1_process/all_players_play.csv")
    return data

#Cargar datasets
data_load_state = st.text("Cargando los datasets...")
games = load_data_games()
plays = load_data_plays()
all_plays_static = load_data_static()
df = load_data_transformed()
data_load_state.text("¡Hecho! Se ha cargado correctamente todos los datasets.")


df

#Diccionario para los equipos
dict_teams = {"PHI":"Philadelphia Eagles","ATL":"Atlanta Falcons","CLE":"Cleveland Browns",
              "PIT":"Pittsburgh Steelers","IND":"Indianapolis Colts","CIN":"Cincinnati Bengals",
              "MIA":"Miami Dolphins","TEN":"Tennessee Titans","BAL":"Baltimore Ravens",
              "BUF":"Buffalo Bills","NE":"New England Patriots","HOU":"Houston Texans",
              "NYG":"New York Giants","JAX":"Jacksonville Jaguars","NO":"New Orleans Saints",
              "TB":"Tampa Bay Buccaneers","ARI":"Arizona Cardinals","WAS":"Washington Football Team",
              "CAR":"Carolina Panthers","DAL":"Dallas Cowboys","GB":"Green Bay Packers",
              "CHI":"Chicago Bears","DET":"Detroit Lions","NYJ":"New York Jets",
              "OAK":"Oakland Raiders","LA":"Los Angeles Rams","SEA":"Seattle Seahawks",
              "LAC":"Los Angels Chargers","SF":"San Francisco 49ers","KC":"Kansas City Chiefs","MIN":"Minnesota Vikings","DEN":"Denver Broncos"}

#st.write(len(dict_teams))

user_input_id = st.text_input("Introduce el id para ver el partido")

if user_input_id != "":
    try:
        selected_play = plays.loc[user_input_id]
        partsId = user_input_id.split(":")
        gameId = partsId[0]
        selected_game = games.loc[int(gameId)]
        selected_static = all_plays_static[all_plays_static["id"]==user_input_id]
        
        image = Image.open("../resources/empty_field.png")
        draw = ImageDraw.Draw(image)
        
        if selected_static["playDirection"].all() == "left":
            direction = -1
        else:
            direction = 1
        
        #canvas.create_line(,fill="yellow",width=3)
        draw.line([int(selected_play["absoluteYardlineNumber"])*10+(int(selected_play["yardsToGo"])*10*direction),0,int(selected_play["absoluteYardlineNumber"])*10+(int(selected_play["yardsToGo"])*10*direction),533], fill="yellow",width=3)
        draw.line([int(selected_play["absoluteYardlineNumber"])*10, 0, int(selected_play["absoluteYardlineNumber"])*10, 533], fill="blue",width=3)
        
        for index,row in selected_static.iterrows():
            x0 = row["x"]*10 - 6
            y0 = row["y"]*10 - 6
            x1 = row["x"]*10 + 6
            y1 = row["y"]*10 + 6
           
            
            if row["team"] == "home":
                draw.ellipse((x0, y0, x1, y1), fill = 'red', outline ='red')
                #pos = "home"
                #paint_player(canvas,int(row["x"])*10,533-int(row["y"])*10,pos,row["o"])
                #canvas.create_text(int(row["x"])*10,533-int(row["y"])*10,font=("Purisa",5),fill="white",text=int(row["jerseyNumber"]))
            elif row["team"] == "away": 
                draw.ellipse((x0, y0, x1, y1), fill = 'blue', outline ='blue')
                #pos = "away"
                #paint_player(canvas,int(row["x"])*10,533-int(row["y"])*10,pos,row["o"])
                #canvas.create_text(int(row["x"])*10,533-int(row["y"])*10,font=("Purisa",5),fill="white",text=int(row["jerseyNumber"]))
            elif row["displayName"] == "Football":
                x0 = row["x"]*10 - 3
                y0 = row["y"]*10 - 3
                x1 = row["x"]*10 + 3
                y1 = row["y"]*10 + 3
                draw.ellipse((x0, y0, x1, y1), fill = 'brown', outline ='brown')
                #paint_football(canvas,int(row["x"])*10,533-int(row["y"])*10)
        
        
        
        
        
        st.image(image)
        
        st.markdown("__Equipo local__: "+dict_teams[selected_game["homeTeamAbbr"]]
                 +"  \n__Equipo visitante__: "+dict_teams[selected_game["visitorTeamAbbr"]]
                 +"  \n__Marcador__: "+selected_game["homeTeamAbbr"] +" "+str(int(selected_play["preSnapHomeScore"]))+" - "+str(int(selected_play["preSnapVisitorScore"]))+" "+str(selected_game["visitorTeamAbbr"])
                 +"  \n__Equipo con la posesión__: "+selected_play["possessionTeam"]
                 +"  \n__Descripción de la jugada__: "+selected_play["playDescription"]
                 +"  \n__Yardas para avanzar__: " + str(int(selected_play["yardsToGo"]))
                 +"  \n__Cuarto__: " + str(int(selected_play["quarter"]))
                 +"  \n__Down__: " + str(int(selected_play["down"]))
                 +"  \n__Tiempo en el reloj__: "+selected_play["gameClock"]
                 +"  \n__Posición del balón__: Yarda "+str(int(selected_play["yardlineNumber"])) + " en el campo de " + selected_play["possessionTeam"]
                 +"  \n__Resultado de la jugada__: " + str(int(selected_play["offensePlayResult"])) + " yardas"
                )
    except Exception as e:
        print(e)
        st.write("La jugada introducida no existe")
    #selected_play

st.header("Información de las variables")
        
option = st.selectbox("Escoge una feature para poder visualizarla en profundidad",df.columns)
st.subheader("Diagrama de frecuencias de la variable "+option)

if option not in ["defenseArea","defenseAreaCoverDefenders","width","height","differenceOffenseVsDefenseWidth","HeightByWeightDeep","HeightByWeightHook","HeightByWeightCurl","HeightByWeightFlat","WeightByArea","density","densityNoLine","densityInsidePoints","densityInsidePointsNoLine"]:
    #st.bar_chart(df[option].value_counts())
    df[option].value_counts().plot(kind="bar")
    plt.show()
    st.pyplot()

else:
    #hist_values = np.histogram(df[option])[0]
    #st.bar_chart()
    df[option].hist().grid(False)
    plt.show()
    st.pyplot()
#st.bar_chart(df[option].hist())


st.markdown("__Valor mínimo__: "+str(df[option].min())
            +"  \n__Valor máximo__: "+str(df[option].max())
            +"  \n__Valor medio__: "+str(df[option].mean())
            +"  \n__Valor primer cuantil__: "+str(df[option].quantile(q=0.25))
            +"  \n__Valor mediana__: "+str(df[option].median())
            +"  \n__Valor tercer cuantil__: "+str(df[option].quantile(q=0.75))
            +"  \n__Valor desviación típica__: "+str(df[option].std())
            )

if option in ["defenseArea","defenseAreaCoverDefenders","width","height","differenceOffenseVsDefenseWidth","HeightByWeightDeep","HeightByWeightHook","HeightByWeightCurl","HeightByWeightFlat","WeightByArea","density","densityNoLine","densityInsidePoints","densityInsidePointsNoLine"]:
    st.subheader("Boxplot de la variable "+option)
    df[option].plot.box()
    plt.show()
    st.pyplot()
#if st.checkbox('Show raw data'):
    #st.write("hola")

st.header("Clustering")
