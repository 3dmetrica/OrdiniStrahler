from collections import defaultdict
from qgis.PyQt.QtCore import QVariant
import sys
sys.setrecursionlimit(10000)

def trova(parte):
    trovati = [l for l in QgsProject.instance().mapLayers().values() if parte.lower() in l.name().lower()]
    if len(trovati) != 1:
        raise Exception("'%s': %d layer trovati. Nomi nel progetto: %s"
                        % (parte, len(trovati), [l.name() for l in QgsProject.instance().mapLayers().values()]))
    return trovati[0]

ret = trova('2ha_bacino')
dem = trova('DTM_terra')

def estremi(g):
    parti = g.asMultiPolyline() if g.isMultipart() else [g.asPolyline()]
    return parti[0][0], parti[-1][-1]

k = lambda p: (round(p.x(), 2), round(p.y(), 2))
feat = {f.id(): f for f in ret.getFeatures()}
lung = {i: f.geometry().length() for i, f in feat.items()}
adj = defaultdict(list)
for i, f in feat.items():
    a, b = map(k, estremi(f.geometry()))
    adj[a].append((i, b))
    adj[b].append((i, a))

quota = lambda n: dem.dataProvider().sample(QgsPointXY(*n), 1)[0]
sbocco = min((n for n, v in adj.items() if len(v) == 1), key=quota)

ordine, monte = {}, {}
def visita(nodo, via):
    figli = [visita(o, i) for i, o in adj[nodo] if i != via]
    if not figli:
        s, L = 1, 0
    else:
        oo = sorted((x[0] for x in figli), reverse=True)
        s = oo[0] + 1 if len(oo) > 1 and oo[0] == oo[1] else oo[0]
        L = max(x[1] for x in figli)
    if via is not None:
        L += lung[via]
        ordine[via], monte[via] = s, L
    return s, L
visita(sbocco, None)

asta, nodo, via = set(), sbocco, None
while True:
    figli = [(i, o) for i, o in adj[nodo] if i != via]
    if not figli:
        break
    via, nodo = max(figli, key=lambda x: monte[x[0]])
    asta.add(via)

pr = ret.dataProvider()
pr.addAttributes([QgsField(n, QVariant.Int) for n in ('strahler', 'asta_princ') if ret.fields().indexOf(n) < 0])
ret.updateFields()
iS, iA = ret.fields().indexOf('strahler'), ret.fields().indexOf('asta_princ')
pr.changeAttributeValues({i: {iS: ordine.get(i), iA: int(i in asta)} for i in feat})
ret.triggerRepaint()
print('sbocco a quota %.1f m; ordine massimo %d; asta principale %.2f km'
      % (quota(sbocco), max(ordine.values()), sum(lung[i] for i in asta) / 1000))