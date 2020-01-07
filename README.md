# GK9.3.2 Middleware Engineering "High Availability"
David Langheiter  
[Task](./TASK.md)

### Umsetzung
#### Balancer
Liest die `config.yml` und parst sie. Warted danach auf Verdingunen und leitet sie auf den nächsten Server weiter.

Dies tut es mit 2 Threads. Einen für die Client -> Server kommunikation und einen für die Server -> Client
kommunikation.
```python
def connect_client(self, csocket, server):
    print("Client got connected to", server)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server.host, server.port))
    cs = Process(target=BalanceServer.client_to_server, args=(csocket,server_socket))
    sc = Process(target=BalanceServer.server_to_client, args=(csocket,server_socket))
    cs.start()
    sc.start()
```

### Verweundung und Erklärung
Meine Umsetzung besteht aus zwei Teilen.
#### Balancer
Dieser ist der Load-Balancer.
Mann kann diesen mit der `config.yml` configurieren.
Example config:
```yaml
port: 1880

balancers:
  ser2:
    host: localhost
    port: 1882
    weight: 2
```
Beschreibung:
* `port` ist der Port auf dem der Server horcht
* `balancers` Map an Servern. Wobei der key nur ein name ist
    * `host` Host dieses Servers
    * `port` Port dieses Servers
    * `weight` die Gewichtung dieses Servers. default: `1`

Der Server geht einfach die Liste nach entlang und schickt den Servern `weight` viele Anfragen
hintereinander und geht dann weiter. Wenn er beim letzten angekommen ist spring er wieder zum ersten.

#### Server
Usage:
```shell script
python server.py <name> <port>
```
Dies startet einen Server auf dem angegebenen Port und erlaubt unendlich verbindungen.
Bei einer Verbindung schickt der Server die Nachricht `Connected to server <name>`.
Bei weiteren nachrichten schikt der Server die Nachricht `ECHO <name>: <msg>`.

### Fragen

##### Verlgeichen Sie die verwendeten Load Balancing Methoden und stellen Sie diese gegenüber.
Hab nur einer verwendet.

Weighted Round-Robin: Besucht alle Services so wie round-robin. Kann aber z.B. bestimmte öfter
besuchen. Je nach gewichtung.

Least Connection: Es werden die Services bevorzugt welche die wenigsten Vrbindungen haben.

##### Was kann als Gewichtung bei Weighted Round Robin verwendet werden?
* Auslastung
* Künstlicher aufteilung (weight)
* Verfügbarkeit
* Offenen verbindungen

##### Warum stellt die "Hochverfügbarkeit" von IT Systemen in der heutigen Zeit eine sehr wichtige Eigenschaft dar?
Weil es wichtig ist dass informationen immer und in einer angemessenen Zeit verfügbar sind.
Um z.B. Bankgeschäfte zu tätigen. Und weil die Menschen davon ausgehen das es immer Funktionert.

##### Welche anderen Massnahmen neben einer Lastverteilung müssen getroffen werden, um die "Hochverfügbarkeit" sicher zu stellen?
* Überwachung
* Ausfallsicherheit
* Redundanz
* vorbeugende Wartungen

##### Was versteht man unter "Session Persistenz" und welche Schwierigkeiten ergeben sich damit?
Das die selbe Session immer zum selben Server geleitet wird, damit die Server nicht immer
nachschauen müssen ob die Session noch aktiv und welcher Nutzer hinter der Session liegt.
Das Problem dabei ist wenn ein Server zu viele Sessions zugewisen bekommt die langlebiger sind als
normal und damit villeicht überlastet wird.

##### Nennen Sie jeweils ein Beispiel, wo Session Persistenz notwendig bzw. nicht notwendig ist.
Notwending: wenn man Formulare ausfüllt und der Nutzer wichtig ist.
Nicht notwendig: Nicht Benutzer spezifische Daten. Docs, Info seiten, ...

##### Welcher Unterschied besteht zwischen einer "server-side" bzw "client-side" Lastverteilungslösung?
Server-Side:
Der Client verbindet sich mit einem Server und dieser leitet ihn über sich zu einem anderen ohne das dies der Client mitbekommt.

Client-Side:
Der Client kümmert sich um die Auswahl des Servers. Mit z.B. Pings um den am Schnellsten erreichbarsten Server zu finden.

##### Was versteht man unter dem "Mega-Proxy-Problem"?
Dies tritt bei Load Balancing mit hash Methoden auf. Das heißt dass wenn viel Traffic von einer bestimten Addressen Range
kommt wird diese immer dem selben Server zugewiesen und damit wird dieser überlastet.

### Sources
[Weighted-Round-Robin](https://www.researchgate.net/figure/Round-robin-scheduling-strategy-Weighted-Round-Robin-Load-Balancing-Weighted_fig3_274007923)  
[Session Persistence](https://www.varnish-software.com/glossary/what-is-session-persistence/)