import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn import tree

#visualización de la imagen
from tkinter import *
from PIL import Image, ImageTk,ImageDraw

from datetime import datetime

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Cuadro de mandos")

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
clusters = ["K-means - StandardScaler - K = 3","K-means - MinMaxScaler - K = 7","K-means - RobustScaler - K = 3","K-means - PowerTransformer - K = 6","Jerárquico - StandardScaler - K = 5","Jerárquico - MinMaxScaler - K = 5","Jerárquico - RobustScaler - K = 5","Jerárquico - PowerTransformer - K = 5"]
cluster = st.radio("Escoge el clustering",clusters)

dict_clusters = {"K-means - StandardScaler - K = 3":"../unsupervised_datasets/kmeans/static_defenses_ss_kmeans_without_outliers.csv",
                 "K-means - MinMaxScaler - K = 7":"../unsupervised_datasets/kmeans/static_defenses_mms_kmeans_without_outliers.csv",
                 "K-means - RobustScaler - K = 3":"../unsupervised_datasets/kmeans/static_defenses_rs_kmeans_without_outliers.csv",
                 "K-means - PowerTransformer - K = 6":"../unsupervised_datasets/kmeans/static_defenses_pt_h_without_outliers.csv",
                 "Jerárquico - StandardScaler - K = 5":"../unsupervised_datasets/hierarchical_k_130/static_defenses_ss_hierarchical_without_outliers.csv",
                 "Jerárquico - MinMaxScaler - K = 5":"../unsupervised_datasets/hierarchical_k_130/static_defenses_mms_hierarchical_without_outliers.csv",
                 "Jerárquico - RobustScaler - K = 5":"../unsupervised_datasets/hierarchical_k_130/static_defenses_rs_hierarchical_without_outliers.csv",
                 "Jerárquico - PowerTransformer - K = 5":"../unsupervised_datasets/hierarchical_k_130/static_defenses_pt_hierarchical_without_outliers.csv"
                 }

selected_cluster = pd.read_csv(dict_clusters[cluster],index_col=0)

number_clusters = selected_cluster["cluster"].unique()

number_clusters.sort()
st.markdown("Distribución de los clusters")
elements_clusters = ""
for c in number_clusters:
    elements_clusters += "__Númer de elementos Cluster{}__: ".format(str(c))+str(len(selected_cluster[selected_cluster["cluster"]==c]))+"  \n"
    #st.markdown("__Númer de elementos Cluster{}__: ".format(str(c))+str(len(selected_cluster[selected_cluster["cluster"]==c])))

st.markdown(elements_clusters)

option_cluster = st.selectbox("Escoge un cluster para poder visualizarla en profundidad",number_clusters)

st.markdown("Media de las variables")
st.markdown("__defensivelinezonePlayers__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["defensivelinezonePlayers"].mean())
            +"  \n__deepzonePlayers__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["deepzonePlayers"].mean())
            +"  \n__hookzonePlayers__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["hookzonePlayers"].mean())
            +"  \n__curlzonePlayers__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["curlzonePlayers"].mean())
            +"  \n__flatzonePlayers__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["flatzonePlayers"].mean())
            +"  \n__defenseArea__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["defenseArea"].mean())
            +"  \n__defenseAreaCoverDefenders__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["defenseAreaCoverDefenders"].mean())
            +"  \n__width__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["width"].mean())
            +"  \n__height__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["height"].mean())
            +"  \n__numberQBs__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["numberQBs"].mean())
            +"  \n__numberWRs__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["numberWRs"].mean())
            +"  \n__numberRBs__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["numberRBs"].mean())
            +"  \n__numberTEs__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["numberTEs"].mean())
            +"  \n__numberFBs__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["numberFBs"].mean())
            +"  \n__numberOffensivePlayersAnotherPosition__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["numberOffensivePlayersAnotherPosition"].mean())
            +"  \n__numberSafeties__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["numberSafeties"].mean())
            +"  \n__numberLBs__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["numberLBs"].mean())
            +"  \n__numberCBs__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["numberCBs"].mean())
            +"  \n__strongSide__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["strongSide"].mean())
            +"  \n__numberPlayersDefenseStrongSide__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["numberPlayersDefenseStrongSide"].mean())
            +"  \n__numberPlayersDefenseWeakSide__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["numberPlayersDefenseWeakSide"].mean())
            +"  \n__numberPlayersOffenseStrongSide__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["numberPlayersOffenseStrongSide"].mean())
            +"  \n__numberPlayersOffenseWeakSide__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["numberPlayersOffenseWeakSide"].mean())
            +"  \n__differenceOffenseVsDefenseWidth__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["differenceOffenseVsDefenseWidth"].mean())
            +"  \n__differenceOffenseVsDefenseStrongSide__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["differenceOffenseVsDefenseStrongSide"].mean())
            +"  \n__differenceOffenseVsDefenseWeakSide__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["differenceOffenseVsDefenseWeakSide"].mean())
            +"  \n__HeightByWeightDeep__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["HeightByWeightDeep"].mean())
            +"  \n__HeightByWeightHook__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["HeightByWeightHook"].mean())
            +"  \n__HeightByWeightCurl__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["HeightByWeightCurl"].mean())
            +"  \n__HeightByWeightFlat__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["HeightByWeightFlat"].mean())
            +"  \n__WeightByArea__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["WeightByArea"].mean())
            +"  \n__density__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["density"].mean())
            +"  \n__densityNoLine__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["densityNoLine"].mean())
            +"  \n__densityInsidePoints__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["densityInsidePoints"].mean())
            +"  \n__densityInsidePointsNoLine__: "+str(selected_cluster[selected_cluster["cluster"]==option_cluster]["densityInsidePointsNoLine"].mean())
            )


st.header("Evaluación de los jugadores")

players = pd.read_csv("../processed_data/clean/players.csv",index_col = 0)
summary = pd.read_csv("../notebooks_valorations/summary.csv",index_col=0)
summary_cp = summary.copy()

def changeGameClock(value,quarter):
    if quarter == 1:
        total_time = 3600
    elif quarter == 2:
        total_time = 2700
    elif quarter == 3:
        total_time = 1800
    elif quarter == 4:
        total_time = 900
    
    format = "%M:%S:%f"
    actual_time = datetime.strptime(value, format) - datetime.strptime("00:00:00",format)
    time = total_time - (900 - actual_time.total_seconds())
    return time


summary_cp["gameClock"] = summary_cp.apply(lambda x: changeGameClock(x["gameClock"],x["quarter"]),axis=1)
summary_cp.drop(["playerId","playId"],axis=1,inplace=True)


X_train, X_test, y_train, y_test = train_test_split(summary_cp.drop(["defenseValoration"],axis=1),summary_cp["defenseValoration"],test_size=0.3)


regressor = tree.DecisionTreeClassifier(criterion='entropy', min_samples_split = 65, 
                                  min_samples_leaf = 20, max_depth = 10, 
                                  class_weight={0:5.5,1:4.4})
regressor.fit( X = X_train, y = y_train)
y_pred = regressor.predict(X = X_test)
acc = accuracy_score(y_test, y_pred)
#print ('Acc', acc)



predict_proba = regressor.predict_proba(summary_cp.drop(["defenseValoration"],axis=1))[:,1]

summary["predict_proba"] = predict_proba - (1 - predict_proba)
predict_proba_sums = summary.groupby("playerId")["predict_proba"].sum()

valoration_players = {}
for player in predict_proba_sums.index:
    valoration_players[player] = predict_proba_sums[player]
    
valorations = dict(sorted(valoration_players.items(), key=lambda item: item[1],reverse=True))


st.subheader("Top 25 defensores")


    
positions = ["Todas las posiciones", "Linebackers","Cornerbacks","Safeties"]
position = st.selectbox("Escoge una posición para ver el ranking según posiciones",positions)

if position == "Cornerbacks":
    cont = 0
    for val in valorations:
        if players.loc[val]["position"] in ["CB","DB"]:
            cont +=1
            st.markdown(str(cont)+".- ("+str(val)+") __"+players.loc[val]["displayName"]+"__: "+str(round(valorations[val],2)))
            if cont == 25:
                break
elif position == "Todas las posiciones":
    cont = 0
    for val in valorations:
        cont +=1
        st.markdown(str(cont)+".-("+str(val)+") __"+players.loc[val]["displayName"]+"__: "+str(round(valorations[val],2))+" _"+players.loc[val]["position"]+"_")
        if cont == 25:
            break
elif position == "Linebackers":
    cont = 0
    for val in valorations:
        if players.loc[val]["position"] in ["LB","ILB","OLB","MLB"]:
            cont +=1
            st.markdown(str(cont)+".- ("+str(val)+") __"+players.loc[val]["displayName"]+"__: "+str(round(valorations[val],2))+" _"+players.loc[val]["position"]+"_")
            if cont == 25:
                break
elif position == "Safeties":
    cont = 0
    for val in valorations:
        if players.loc[val]["position"] in ["S","SS","FS"]:
            cont +=1
            st.markdown(str(cont)+".- ("+str(val)+") __"+players.loc[val]["displayName"]+"__: "+str(round(valorations[val],2))+" _"+players.loc[val]["position"]+"_")
            if cont == 25:
                break
