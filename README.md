# Sistemes distribuïts

## Pràctica 2: Exclusió mútua

### Objectiu de la pràctica

Implementar un algorisme distribuït que garanteixi l'exclusió mútua de l'accés a un fitxer compartit que estarà guardat al IBM COS.

### Resolució

Per realitzar la practica hem seguit l'esquema proporcionat a l'enunciat de la pràctica.

La nostra funció coordinadora mira si hi ha peticions d'escriptura al IBM COS cada x segons, agafa totes les peticions que hi hagin en aquell moment, les ordena i finalment les tracta, un cop les ha tractat totes, torna a mirar si n'hi han de noves, si és així repeteix el procés fins que ja no en troba cap, moment en el qual acaba la seva execució.

La funció esclava, el que fa es mirar cada x segons si en l'IBM COS hi ha el fitxer que li concedeix els permisos d'escriptura, si és així, accedeix al fitxer compartit, hi afegeix el seu identificador corresponent i acaba la seva execució

### Preguntes

**Many distributed algorithms such as the one proposed in this assignment require the use of a master or** **coordinator process. To what extent can such algorithms actually be considered distributed? Discuss**

Poden ser anomenats algoritmes distribuïts tot i que tenen un cert grau de centralització ja que normalment en aquest tipus d'algorismes hi ha un nombre elevat d'esclaus i un nombre reduït de coordinadors. 

Es pot disminuir el grau de centralització, augmentant el nombre de coordinadors.

**Now suppose that the master function crashes. Does this always violate the correctness of the algorithm? If** **not, under what circumstances does this happen? Is there any way to avoid the problem and make the system able to tolerate coordinator crashes? Discuss**

Si el coordinador deixes de funcionar justament després de concedir el permís d'escriptura, sense que tingues temps de esborrar la petició d'escriptura, al tornar a iniciar el procés ordinador, aquest veuria que te una petició d'escriptura que en realitat ja s'ha realitzat, això provocaria que el procés coordinador es quedes bloquejat esperant a que el fitxer result.txt fos actualitzat cosa que mai passaria degut a que el procés esclau ja ho ha fet.

El sistema podria ser segur si es pogués garantir que el procés coordinador tractara cada sol·licitud de manera atòmica, es a dir completant el total de la petició o fent un rollback d'aquesta, com si fos una transacció d'una base de dades SQL.

Una altre possible solució seria tenir més d'un procés coordinador al mateix temps, de manera que si un deixes de funcionar en algun moment l'altre el pogués substituir

**In the proposed algorithm, write permissions are granted in the order in which are requested, so no slave** **function waits forever (no starvation). If the master function chose the slaves functions randomly, then could slave functions suffer from starvation?**

Es podria donar el cas si el nombre de peticions fos extremadament gran o si les peticions arribessin més ràpidament del que es tracten

### Joc de proves

#### 10 slaves

master:         {3}{0}{7}{8}{5}{4}{2}{1}{6}{9}

result.txt:     {3}{0}{7}{8}{5}{4}{2}{1}{6}{9}

Els resultats son correctes

#### 50 slaves

master:         {34}{29}{48}{47}{40}{49}{42}{35}{44}{31}{17}{39}{41}{18}{38}{37}{45}{46}{43}{0}{11}{28}{5}{7}{21}{19}{26}{20}{9}{30}{33}{16}{13}{22}{23}{24}{8}{3}{27}{12}{10}{32}{4}{6}{36}{25}{15}{1}{2}{14}

result.txt:     {34}{29}{48}{47}{40}{49}{42}{35}{44}{31}{17}{39}{41}{18}{38}{37}{45}{46}{43}{0}{11}{28}{5}{7}{21}{19}{26}{20}{9}{30}{33}{16}{13}{22}{23}{24}{8}{3}{27}{12}{10}{32}{4}{6}{36}{25}{15}{1}{2}{14}

Els resultats son correctes

#### 100 slaves

master:         {2}{20}{54}{58}{49}{18}{24}{40}{4}{5}{12}{59}{0}{15}{10}{11}{9}{6}{56}{13}{28}{26}{36}{21}{17}{3}{14}{27}{37}{7}{44}{30}{1}{35}{42}{8}{39}{41}{22}{33}{32}{97}{91}{94}{81}{99}{46}{45}{16}{47}{23}{50}{43}{38}{19}{53}{29}{34}{67}{66}{51}{68}{76}{31}{57}{25}{48}{69}{55}{85}{96}{72}{83}{61}{60}{79}{70}{78}{89}{73}{75}{63}{65}{98}{52}{80}{62}{64}{74}{86}{93}{88}{71}{95}{82}{77}{92}{84}{87}{90}

result.txt:     {2}{20}{54}{58}{49}{18}{24}{40}{4}{5}{12}{59}{0}{15}{10}{11}{9}{6}{56}{13}{28}{26}{36}{21}{17}{3}{14}{27}{37}{7}{44}{30}{1}{35}{42}{8}{39}{41}{22}{33}{32}{97}{91}{94}{81}{99}{46}{45}{16}{47}{23}{50}{43}{38}{19}{53}{29}{34}{67}{66}{51}{68}{76}{31}{57}{25}{48}{69}{55}{85}{96}{72}{83}{61}{60}{79}{70}{78}{89}{73}{75}{63}{65}{98}{52}{80}{62}{64}{74}{86}{93}{88}{71}{95}{82}{77}{92}{84}{87}{90}

Els resultats son correctes

### Llibreries

#### Pywren

La llibreria que ens deixa interaccionar amb ibm cloud per a poder utilitzar cloud function de
manera més senzilla. Aquesta llibreria ens donarà accés a funcions com call_async() que serveix
per cridar la funció que desitgem en el cloud, map() que serveix per aplicar una funció a un
conjunt de dades de manera que cada conjunt aplica una vegada la funció, i per últim la única
funció no asíncrona get_result() que serveix per a esperar els resultats de les funcions cridades
de manera asíncrona.

#### Time

Per últim tenim time per a poder contar el temps d’execució per a tots els paràmetres utilitzats i guardar-los.

#### Re

Llibreria per tractar expressions regulars.

### Referències

*Llibreria pywren:*

https://github.com/pywren/pywren-ibm-cloud/

*Llibreria time:*

https://docs.python.org/3/library/time.html

*Llibreria re:*

https://docs.python.org/3/library/re.html

### Participants i feina feta

*Adrià Ribas Jaumà* 

*Nicolás Fadul Bonamusa* 

Ens hem repartit la feina equitativament. Si algú dels dos tenia cap problema ho resolíem entre els dos.

### Github

https://github.com/rayderone/Sistemes-Distribuits-2
