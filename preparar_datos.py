"""Descarga el volcado CSV de Jolpica F1 (sucesor de la API Ergast) y lo convierte al
formato de tablas Ergast / Kaggle que usa el notebook, para las temporadas 2018-2026.

Uso:  python preparar_datos.py
Salida: data_2018_2026/{results,races,drivers,constructors,driverStandings,constructorStandings,status}.csv

Los IDs numéricos de Jolpica no coinciden con los de Ergast, así que se remapean por la
referencia textual (p. ej. "leclerc" -> 844) para que funcionen DRIVER_C / TEAM_C.
"""
import io
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

URL = "https://api.jolpi.ca/data/dumps/download/delayed/?dump_type=csv"
AÑOS = (2018, 2026)
SALIDA = Path(__file__).parent / "data_2018_2026"

# IDs Ergast de pilotos y escuderías que no están en el dataset 1950-2017 de Kaggle.
# Desde 2025 (antonelli en adelante) y para audi/cadillac Ergast ya no existía: son IDs asignados por nosotros.
DRIVER_IDS = {
    "raikkonen": 8, "alonso": 4, "kubica": 9, "hamilton": 1, "vettel": 20, "grosjean": 154,
    "hulkenberg": 807, "perez": 815, "ricciardo": 817, "bottas": 822, "kevin_magnussen": 825,
    "kvyat": 826, "ericsson": 828, "sainz": 832, "max_verstappen": 830, "vandoorne": 838,
    "ocon": 839, "stroll": 840, "giovinazzi": 841, "gasly": 842, "brendon_hartley": 843,
    "leclerc": 844, "sirotkin": 845, "norris": 846, "russell": 847, "albon": 848, "latifi": 849,
    "pietro_fittipaldi": 850, "aitken": 851, "tsunoda": 852, "mazepin": 853, "mick_schumacher": 854,
    "zhou": 855, "de_vries": 856, "piastri": 857, "sargeant": 858, "lawson": 859, "bearman": 860,
    "colapinto": 861, "doohan": 862, "antonelli": 863, "bortoleto": 864, "hadjar": 865, "arvid_lindblad": 866,
}
TEAM_IDS = {
    "mclaren": 1, "williams": 3, "renault": 4, "toro_rosso": 5, "ferrari": 6, "red_bull": 9,
    "force_india": 10, "sauber": 15, "alfa": 51, "aston_martin": 117, "mercedes": 131, "haas": 210,
    "racing_point": 211, "alphatauri": 213, "alpine": 214, "rb": 215, "audi": 216, "cadillac": 217,
}


def main():
    req = urllib.request.Request(URL, headers={"User-Agent": "DuocML-EP2/1.0"})
    z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(req).read()))
    leer = lambda n: pd.read_csv(z.open(f"formula_one_{n}.csv"))

    season, rnd, session = leer("season"), leer("round"), leer("session")
    sentry, rentry, tdriver = leer("sessionentry"), leer("roundentry"), leer("teamdriver")
    driver, team = leer("driver"), leer("team")
    dchamp, tchamp = leer("driverchampionship"), leer("teamchampionship")

    rnd = rnd.merge(season[["id", "year"]].rename(columns={"id": "season_id"}), on="season_id")
    rnd = rnd[rnd["year"].between(*AÑOS) & (rnd["is_cancelled"] == "f")]
    drv_map = driver.set_index("id")["reference"].map(DRIVER_IDS).astype("Int64")
    team_map = team.set_index("id")["reference"].map(TEAM_IDS).astype("Int64")

    # --- races: una fila por Gran Premio (session tipo "R" = carrera principal) ---
    carreras = session[session["type"] == "R"][["id", "round_id"]].rename(columns={"id": "session_id"})
    races = rnd.rename(columns={"id": "raceId", "number": "round", "circuit_id": "circuitId"})
    races = races.merge(carreras, left_on="raceId", right_on="round_id").astype({"round": int})
    races[["raceId", "year", "round", "circuitId", "name", "date"]].sort_values("date").to_csv(SALIDA / "races.csv", index=False)

    # --- results ---
    res = (sentry.merge(races[["raceId", "session_id"]], on="session_id")
                 .merge(rentry.rename(columns={"id": "round_entry_id"}), on="round_entry_id")
                 .merge(tdriver.rename(columns={"id": "team_driver_id"}), on="team_driver_id"))
    status = pd.DataFrame({"status": sorted(res["detail"].fillna("Unknown").unique())})
    status.insert(0, "statusId", range(1, len(status) + 1))
    res = res.assign(
        resultId=res["id"], driverId=res["driver_id"].map(drv_map), constructorId=res["team_id"].map(team_map),
        grid=res["grid"].fillna(0).astype(int), positionOrder=res["position"].astype(int), laps=res["laps_completed"].astype("Int64"),
        position=res["position"].where(res["is_classified"] == "t").astype("Int64"),
        statusId=res["detail"].fillna("Unknown").map(status.set_index("status")["statusId"]),
    )
    assert res[["driverId", "constructorId"]].notna().all().all(), "piloto o equipo sin ID Ergast"
    res[["resultId", "raceId", "driverId", "constructorId", "grid", "position", "positionOrder",
         "points", "laps", "time", "statusId"]].to_csv(SALIDA / "results.csv", index=False)
    status.to_csv(SALIDA / "status.csv", index=False)

    # --- standings tras cada ronda (última sesión puntuable de la ronda: incluye sprints) ---
    def standings(ch, key_src, key, mapa):
        ch = ch[ch["year"].between(*AÑOS)]
        ch = ch[ch["session_number"] == ch.groupby(["year", "round_number"])["session_number"].transform("max")]
        ch = ch.merge(races[["raceId", "year", "round"]], left_on=["year", "round_number"], right_on=["year", "round"])
        return ch.assign(**{key: ch[key_src].map(mapa), "wins": ch["win_count"], "position": ch["position"].astype("Int64")})[["raceId", key, "points", "position", "wins"]]

    standings(dchamp, "driver_id", "driverId", drv_map).to_csv(SALIDA / "driverStandings.csv", index=False)
    standings(tchamp, "team_id", "constructorId", team_map).to_csv(SALIDA / "constructorStandings.csv", index=False)

    # --- maestros ---
    d = driver[driver.id.isin(res["driver_id"])].assign(driverId=lambda x: x["id"].map(drv_map))
    d.rename(columns={"reference": "driverRef", "date_of_birth": "dob", "abbreviation": "code", "wikipedia": "url"})[
        ["driverId", "driverRef", "code", "forename", "surname", "dob", "nationality", "url"]].to_csv(SALIDA / "drivers.csv", index=False)
    t = team[team.id.isin(res["team_id"])].assign(constructorId=lambda x: x["id"].map(team_map))
    t.rename(columns={"reference": "constructorRef", "wikipedia": "url"})[
        ["constructorId", "constructorRef", "name", "nationality", "url"]].to_csv(SALIDA / "constructors.csv", index=False)

    print(f"OK -> {SALIDA}  ({len(res)} resultados, {len(races)} carreras {AÑOS[0]}-{AÑOS[1]})")


if __name__ == "__main__":
    SALIDA.mkdir(exist_ok=True)
    main()
