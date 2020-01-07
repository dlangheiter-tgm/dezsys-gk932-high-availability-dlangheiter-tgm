# GK9.3.2 Middleware Engineering "High Availability"
David Langheiter  
[Task](./TASK.md)

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