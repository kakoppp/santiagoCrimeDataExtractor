# config/queries.py
# Pares (tipo_delito, término_de_búsqueda) para Google News RSS

crimeRadar: list[tuple[str, str]] = [
    # ── Robo Violento 
    ("Robo Violento", "robo asalto violento santiago chile"),
    ("Robo Violento", "asalto a mano armada santiago"),
    ("Robo Violento", "robo con violencia region metropolitana"),
    ("Robo Violento", "asaltaron víctima santiago chile"),

    # ── Portonazo 
    ("Portonazo", "portonazo santiago region metropolitana"),
    ("Portonazo", "portonazo detenidos chile"),
    ("Portonazo", "portonazo carabineros santiago"),

    # ── Encerrona 
    ("Encerrona", "encerrona santiago region metropolitana"),
    ("Encerrona", "encerrona vehiculo santiago chile"),
    ("Encerrona", "encerrona detenidos carabineros"),

    # ── Homicidio
    ("Homicidio", "homicidio balacera santiago chile"),
    ("Homicidio", "homicidio muerto baleado santiago"),
    ("Homicidio", "asesinato crimen santiago region metropolitana"),
    ("Homicidio", "balacera muertos heridos chile"),
    ("Homicidio", "homicidio investigacion PDI santiago"),

    # ── Robo Vehículo
    ("Robo Vehiculo", "robo vehiculo auto santiago chile"),
    ("Robo Vehiculo", "robo camioneta furgon santiago"),
    ("Robo Vehiculo", "auto robado recuperado santiago chile"),
    ("Robo Vehiculo", "hurto vehiculo carabineros region metropolitana"),

    # ── Violencia 
    ("Violencia", "violencia pelea agresion santiago chile"),
    ("Violencia", "riña lesiones graves santiago"),
    ("Violencia", "agresión golpes detenidos santiago chile"),
    ("Violencia", "violencia barrial santiago region metropolitana"),

    # ── Narcotráfico
    ("Narcotráfico", "narcotrafico droga decomiso santiago chile"),
    ("Narcotráfico", "incautacion droga cocaina marihuana santiago"),
    ("Narcotráfico", "banda narcotrafico desarticulada santiago"),
    ("Narcotráfico", "decomiso pasta base santiago region metropolitana"),
    ("Narcotráfico", "operacion antidroga PDI carabineros santiago"),

    # ── Robo General
    ("Robo General", "detenido robo hurto santiago region metropolitana"),
    ("Robo General", "robo local comercial santiago chile"),
    ("Robo General", "detenidos hurto feria santiago"),
    ("Robo General", "robo vivienda casa santiago chile"),
    ("Robo General", "sorprendido robando detenido santiago"),

    # ── Extorsión / Secuestro 
    ("Extorsión", "extorsion amenaza cobro santiago chile"),
    ("Extorsión", "secuestro extorsion region metropolitana"),
    ("Extorsión", "extorsionistas detenidos chile"),

    # ── Estafa
    ("Estafa", "estafa engaño victima santiago chile"),
    ("Estafa", "fraude bancario phishing santiago"),
    ("Estafa", "estafadores detenidos PDI santiago"),

    # ── VIF / Femicidio 
    ("VIF/Femicidio", "femicidio violencia intrafamiliar santiago chile"),
    ("VIF/Femicidio", "femicidio frustrado santiago region metropolitana"),
    ("VIF/Femicidio", "violencia intrafamiliar detenido santiago"),

    # ── Armas 
    ("Armas", "armas incautadas decomisadas santiago chile"),
    ("Armas", "porte arma detenido santiago region metropolitana"),
    ("Armas", "pistola fusil decomisado carabineros santiago"),

    # ── Seguridad General 
    ("Seguridad General", "carabineros detenidos santiago noche"),
    ("Seguridad General", "PDI operacion detenidos santiago"),
    ("Seguridad General", "formalizado imputado tribunal santiago chile"),
    ("Seguridad General", "fiscalia formalizacion delito santiago"),
]
