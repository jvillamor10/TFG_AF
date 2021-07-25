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

@st.cache
def load_data_all_selected_play(weekId):
    data = pd.read_csv("../processed_data/clean/week{}.csv".format(weekId))
    return data

#Cargar datasets
data_load_state = st.text("Cargando los datasets...")
games = load_data_games()
plays = load_data_plays()
all_plays_static = load_data_static()
df = load_data_transformed()
data_load_state.text("¡Hecho! Se ha cargado correctamente todos los datasets.")

def obtainOffenseTeam(playId):
    playIdParts = playId.split(":")
    gameId = playIdParts[0]
    visitorTeam = games.loc[int(gameId)]["visitorTeamAbbr"]
    homeTeam = games.loc[int(gameId)]["homeTeamAbbr"]
    possessionTeam = plays.loc[playId]["possessionTeam"]
    
    if possessionTeam == visitorTeam: #si equipo visitante tiene el balón, el equipo local es el que defiende
        value = "away"
    elif possessionTeam == homeTeam:
        value = "home"
    
    return value

def obtainDefenseTeam(playId):
    playIdParts = playId.split(":")
    gameId = playIdParts[0]
    visitorTeam = games.loc[int(gameId)]["visitorTeamAbbr"]
    homeTeam = games.loc[int(gameId)]["homeTeamAbbr"]
    possessionTeam = plays.loc[playId]["possessionTeam"]
    
    if possessionTeam == visitorTeam: #si equipo visitante tiene el balón, el equipo local es el que defiende
        value = "home"
    elif possessionTeam == homeTeam:
        value = "away"
    
    return value



df
st.markdown("Este conjunto de datos cuenta con "+str(len(df))+" registros y "+str(len(df.columns))+" columnas.")

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
st.header("Obtener información de una jugada determinada")

user_input_id = st.text_input("Introduce el id para ver el partido")
opciones_zonas = ["No","Sí"]
mostrar_zonas = st.radio("¿Mostrar zonas defensivas?",opciones_zonas)

if mostrar_zonas == "Sí":
    zone = True
elif mostrar_zonas == "No":
    zone = False



if user_input_id != "":
    try:
        partsId =user_input_id.split(":")
        weekId = partsId[2]
        all_selected_play = load_data_all_selected_play(weekId)
        frames_selected_play = all_selected_play[all_selected_play["id"]==user_input_id]
        frame = st.slider("Escoge el frame deseado:",1,int(max(frames_selected_play["frameId"].unique())))
        
        
        
        
        selected_play = plays.loc[user_input_id]
        partsId = user_input_id.split(":")
        gameId = partsId[0]
        selected_game = games.loc[int(gameId)]
        selected_static = all_plays_static[all_plays_static["id"]==user_input_id]
        selected_static = frames_selected_play[frames_selected_play["frameId"]==frame]
        
        image = Image.open("../resources/empty_field.png")
        draw = ImageDraw.Draw(image,"RGBA")
        
        if zone:
            los = selected_play["absoluteYardlineNumber"]*10
            playDirection = selected_static["playDirection"].values[0]
            yFootball = selected_static[(selected_static["displayName"]=="Football")]["y"].values[0] * 10
            
            if playDirection == "right":
                #print defensiveline zone
                #draw.rectangle(((100,0),(200,430)),fill="red")  #prueba
                if frame == 1:
                    draw.rectangle(((los, 533 -int(yFootball) + 70), (int(los)+15,533-int(yFootball)-70 )), fill=(0,0,0,180))
                deepzone = los + 150
                #print deep zone
                draw.rectangle(((int(deepzone), 0), (1200,533)), fill=(255,255,0,80))
                #print hook zone
                draw.rectangle(((int(los), 216), (int(deepzone),317)), fill=(0,255,0,80))
                #print curl zone                
                draw.rectangle(((int(los), 120), (int(deepzone), 216)), fill=(0,0,255,80))
                draw.rectangle(((int(los), 317), (int(deepzone), 413)), fill=(0,0,255,80))
                #print flat zone
                draw.rectangle(((int(los), 0), (int(deepzone), 120)), fill=(255,0,0,80))
                draw.rectangle(((int(los), 413), (int(deepzone), 533)), fill=(255,0,0,80))
                
            elif playDirection == "left":
                #print defensiveline zone
                #draw.rectangle(((100,0),(200,430)),fill="red")  #prueba
                if frame == 1:
                    draw.rectangle(((int(los) - 15, 533 - int(yFootball) - 70), (int(los),533- int(yFootball) + 70)), fill=(0,0,0,180))
                deepzone = los - 150
                #print deep zone
                draw.rectangle(((0,0), (int(deepzone), 533)), fill=(255,255,0,80))
                #print hook zone
                draw.rectangle(((int(deepzone),216), (int(los), 317)), fill=(0,255,0,80))
                #print curl zone                
                draw.rectangle(((int(deepzone), 120), (int(los), 216)), fill=(0,0,255,80))
                draw.rectangle(((int(deepzone), 317), (int(los), 413)), fill=(0,0,255,80))
                #print flat zone
                draw.rectangle(((int(deepzone), 0), (int(los), 120)), fill=(255,0,0,80))
                draw.rectangle(((int(deepzone), 413), (int(los), 533)), fill=(255,0,0,80))
                
        
        
        if selected_static["playDirection"].all() == "left":
            direction = -1
        else:
            direction = 1
        
        #canvas.create_line(,fill="yellow",width=3)
        draw.line([int(selected_play["absoluteYardlineNumber"])*10+(int(selected_play["yardsToGo"])*10*direction),0,int(selected_play["absoluteYardlineNumber"])*10+(int(selected_play["yardsToGo"])*10*direction),533], fill="yellow",width=3)
        draw.line([int(selected_play["absoluteYardlineNumber"])*10, 0, int(selected_play["absoluteYardlineNumber"])*10, 533], fill="blue",width=3)
        
        for index,row in selected_static.iterrows():
            x0 = row["x"]*10 - 6
            y0 = row["y"]*10 + 6
            x1 = row["x"]*10 + 6
            y1 = row["y"]*10 - 6
           
            
            if row["team"] == "home":
                draw.ellipse((x0,533- y0, x1,533- y1), fill = 'red', outline ='red')
                #pos = "home"
                #paint_player(canvas,int(row["x"])*10,533-int(row["y"])*10,pos,row["o"])
                #canvas.create_text(int(row["x"])*10,533-int(row["y"])*10,font=("Purisa",5),fill="white",text=int(row["jerseyNumber"]))
            elif row["team"] == "away": 
                draw.ellipse((x0, 533-y0, x1,533- y1), fill = 'blue', outline ='blue')
                #pos = "away"
                #paint_player(canvas,int(row["x"])*10,533-int(row["y"])*10,pos,row["o"])
                #canvas.create_text(int(row["x"])*10,533-int(row["y"])*10,font=("Purisa",5),fill="white",text=int(row["jerseyNumber"]))
            elif row["displayName"] == "Football":
                x0 = row["x"]*10 - 3
                y0 = row["y"]*10 + 3
                x1 = row["x"]*10 + 3
                y1 = row["y"]*10 - 3
                draw.ellipse((x0, 533-y0, x1, 533-y1), fill = 'brown', outline ='brown')
                #paint_football(canvas,int(row["x"])*10,533-int(row["y"])*10)
        
        
        
        
        st.subheader("Representación del campo en el frame "+str(frame))
        st.image(image)
        st.subheader("Información de la jugada")
        
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
        
        with st.beta_expander("Jugadores ofensivos"):
            offense = selected_static[selected_static["team"]==obtainOffenseTeam(user_input_id)]
            for index,row in offense.iterrows():
                st.markdown("("+str(row["nflId"])+") __"+row["displayName"]+"__ "+str(row["jerseyNumber"])+" " 
                            +str(row["position"])+" ("+str(row["x"])+","+str(row["y"])+")"
                            )
           
            
            
        
        with st.beta_expander("Jugadores defensivos"):
            defense = selected_static[selected_static["team"]==obtainDefenseTeam(user_input_id)]
            for index,row in defense.iterrows():
                st.markdown("("+str(row["nflId"])+") __"+row["displayName"]+"__ "+str(row["jerseyNumber"])+" " 
                            +str(row["position"])+" ("+str(row["x"])+","+str(row["y"])+")"
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
            +"  \n__Valor medio__: "+str(round(df[option].mean(),2))
            +"  \n__Valor primer cuantil__: "+str(round(df[option].quantile(q=0.25),2))
            +"  \n__Valor mediana__: "+str(round(df[option].median(),2))
            +"  \n__Valor tercer cuantil__: "+str(round(df[option].quantile(q=0.75),2))
            +"  \n__Valor desviación típica__: "+str(round(df[option].std(),2))
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

measures = ["Media","Mediana","Desviación típica"]
option_measure = st.selectbox("Escoge una medida para las variables",measures)

if option_measure == "Media":
    variables_cluster = []
    for column in selected_cluster[selected_cluster["cluster"]==option_cluster]:
        variables_cluster.append(selected_cluster[selected_cluster["cluster"]==option_cluster][column].mean())
elif option_measure == "Mediana":
    variables_cluster = []
    for column in selected_cluster[selected_cluster["cluster"]==option_cluster]:
        variables_cluster.append(selected_cluster[selected_cluster["cluster"]==option_cluster][column].median())
elif option_measure == "Desviación típica":
    variables_cluster = []
    for column in selected_cluster[selected_cluster["cluster"]==option_cluster]:
        variables_cluster.append(selected_cluster[selected_cluster["cluster"]==option_cluster][column].std())


st.markdown(option_measure+" de las variables")
st.markdown("__defensivelinezonePlayers__: "+str(round(variables_cluster[0],2))
            +"  \n__deepzonePlayers__: "+str(round(variables_cluster[1],2))
            +"  \n__hookzonePlayers__: "+str(round(variables_cluster[2],2))
            +"  \n__curlzonePlayers__: "+str(round(variables_cluster[3],2))
            +"  \n__flatzonePlayers__: "+str(round(variables_cluster[4],2))
            +"  \n__defenseArea__: "+str(round(variables_cluster[5],2))
            +"  \n__defenseAreaCoverDefenders__: "+str(round(variables_cluster[6],2))
            +"  \n__width__: "+str(round(variables_cluster[7],2))
            +"  \n__height__: "+str(round(variables_cluster[8],2))
            +"  \n__numberQBs__: "+str(round(variables_cluster[9],2))
            +"  \n__numberWRs__: "+str(round(variables_cluster[10],2))
            +"  \n__numberRBs__: "+str(round(variables_cluster[11],2))
            +"  \n__numberTEs__: "+str(round(variables_cluster[12],2))
            +"  \n__numberFBs__: "+str(round(variables_cluster[13],2))
            +"  \n__numberOffensivePlayersAnotherPosition__: "+str(round(variables_cluster[14],2))
            +"  \n__numberSafeties__: "+str(round(variables_cluster[15],2))
            +"  \n__numberLBs__: "+str(round(variables_cluster[16],2))
            +"  \n__numberCBs__: "+str(round(variables_cluster[17],2))
            +"  \n__strongSide__: "+str(round(variables_cluster[18],2))
            +"  \n__numberPlayersDefenseStrongSide__: "+str(round(variables_cluster[19],2))
            +"  \n__numberPlayersDefenseWeakSide__: "+str(round(variables_cluster[20],2))
            +"  \n__numberPlayersOffenseStrongSide__: "+str(round(variables_cluster[21],2))
            +"  \n__numberPlayersOffenseWeakSide__: "+str(round(variables_cluster[22],2))
            +"  \n__differenceOffenseVsDefenseWidth__: "+str(round(variables_cluster[23],2))
            +"  \n__differenceOffenseVsDefenseStrongSide__: "+str(round(variables_cluster[24],2))
            +"  \n__differenceOffenseVsDefenseWeakSide__: "+str(round(variables_cluster[25],2))
            +"  \n__HeightByWeightDeep__: "+str(round(variables_cluster[26],2))
            +"  \n__HeightByWeightHook__: "+str(round(variables_cluster[27],2))
            +"  \n__HeightByWeightCurl__: "+str(round(variables_cluster[28],2))
            +"  \n__HeightByWeightFlat__: "+str(round(variables_cluster[29],2))
            +"  \n__WeightByArea__: "+str(round(variables_cluster[30],2))
            +"  \n__density__: "+str(round(variables_cluster[31],2))
            +"  \n__densityNoLine__: "+str(round(variables_cluster[32],2))
            +"  \n__densityInsidePoints__: "+str(round(variables_cluster[33],2))
            +"  \n__densityInsidePointsNoLine__: "+str(round(variables_cluster[34],2))
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

number_tops = st.slider("Escoge el número de jugadores que quieres visualizar",0,100,25)

st.subheader("Top "+str(number_tops)+" defensores")


    
positions = ["Todas las posiciones", "Linebackers","Cornerbacks","Safeties"]
position = st.selectbox("Escoge una posición para ver el ranking según posiciones",positions)


if position == "Cornerbacks":
    cont = 0
    df = pd.DataFrame(columns=["Identificador","Nombre y apellidos","Valoración","Posición"])
    for val in valorations:
        if players.loc[val]["position"] in ["CB","DB"]:
            cont +=1
            new_row = {"Identificador":val,"Nombre y apellidos":players.loc[val]["displayName"],"Valoración":round(valorations[val],2),"Posición":players.loc[val]["position"]}
            df = df.append(new_row,ignore_index=True)
            if cont == number_tops:
                break
    df.index = np.arange(1, len(df)+1)
    st.table(df)
elif position == "Todas las posiciones":
    cont = 0
    df = pd.DataFrame(columns=["Identificador","Nombre y apellidos","Valoración","Posición"])
    for val in valorations:
        cont +=1
        new_row = {"Identificador":val,"Nombre y apellidos":players.loc[val]["displayName"],"Valoración":round(valorations[val],2),"Posición":players.loc[val]["position"]}
        df = df.append(new_row,ignore_index=True)
        if cont == number_tops:
            break
    df.index = np.arange(1, len(df)+1)
    st.table(df)
elif position == "Linebackers":
    cont = 0
    df = pd.DataFrame(columns=["Identificador","Nombre y apellidos","Valoración","Posición"])
    for val in valorations:
        if players.loc[val]["position"] in ["LB","ILB","OLB","MLB"]:
            cont +=1
            new_row = {"Identificador":val,"Nombre y apellidos":players.loc[val]["displayName"],"Valoración":round(valorations[val],2),"Posición":players.loc[val]["position"]}
            df = df.append(new_row,ignore_index=True)
            if cont == number_tops:
                break
    df.index = np.arange(1, len(df)+1)
    st.table(df)
elif position == "Safeties":
    cont = 0
    df = pd.DataFrame(columns=["Identificador","Nombre y apellidos","Valoración","Posición"])
    for val in valorations:
        if players.loc[val]["position"] in ["S","SS","FS"]:
            cont +=1
            new_row = {"Identificador":val,"Nombre y apellidos":players.loc[val]["displayName"],"Valoración":round(valorations[val],2),"Posición":players.loc[val]["position"]}
            df = df.append(new_row,ignore_index=True)
            if cont == number_tops:
                break
    df.index = np.arange(1, len(df)+1)
    st.table(df)
