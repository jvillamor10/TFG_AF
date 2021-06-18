# TFG_AF

Cada jugada tiene el siguiente ID: gameId:playId:week

## Glosario de posiciones

### Posiciones ofensivas
* QB: Quarterback
* WR: Wide receiver
* RB: Running back
* TE: Tight end
* FB: Fullback
* HB: Halfback

### Posiciones defensivas
* SS: Strong safety
* FS: Free safety
* MLB: Middle linebacker
* CB: Cornerback
* LB: Linebacker
* OLB: Outside linebacker
* ILB: Inside linebacker
* DL: Defensive line
* DB: Defensive back
* NT: Nose tackle
* S: Safety
* DE: Defensive end
* DT: Defensive tackle

### Posiciones de equipos especiales
* P: Punter
* LS: Long snapper
* K: Kicker

### Sobre las posiciones de Special teams
Solo cuenta con tres, y han sido eliminadas todas las jugadas en las que aparezca al menos uno de estos tres (que son pocas, unas 10 o así). Básicamente son los jugadores encargados en realizar las jugadas de special teams,
como son un field goal (disparar a los palos), un kickoff (después de una anotación o al inicio del primer y tercer cuarto, se realiza este saque) o punts (alejar el balón de la zona actual para que el equipo rival obtenga la
posesión lo más lejano posible). 

Estas posiciones aparecen en estos datasets porque se realizan "trick plays", es decir, jugadas diseñadas para engañar al equipo defensor. Una vez que se llega al cuarto down, normalmente se inicia o bien el field goal o el
punt (siempre y cuando no se decida jugar el down). Estos equipos hacen creer al equipo defensor que van a realizar una de estas dos acciones, y al final acaban realizando un pase. Son jugadas que no aparecen en todos los
partidos, incluso no llegan a ocurrir todas las semanas, y no son de nuestra incumbencia en este estudio, ya que queremos estudiar las posiciones iniciales de los jugadores durante una defensa, esto no aporta ningún tipo de
información ya que son formaciones totalmente distintas.


## Glosario de formaciones ofensivas
* I_FORM: consiste en el QB, el FB y el HB colocados en una línea perpendicular a la líne de Scrimmage, en forma de I.
* SINGLEBACK: consiste en un único hombre, normalmente un HB, en el Backfield.
* SHOTGUN: el QB está a cinco yardas tras el Center.
* EMPTY: consiste en una formación sin ningún hombre más que el QB en el Backfield.
* PISTOL: variante de SHOTGUN. La diferencia es que el QB está una o dos yardas maś cerca del Center y que el RB se colooca justra tras él.
* WILDCAT: sitúa al QB en uno de los laterales, como si fuese un WR, y el RB recibe el Snap.
* JUMBO: no cuenta con WR, utiliza tres TE y dos RB o viceversa.
