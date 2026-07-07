import json
from pathlib import Path
from threading import Lock

FILE = "dashboard/live_status.json"

LOCK = Lock()


def _read():

    Path("dashboard").mkdir(exist_ok=True)

    try:

        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return {}


def write_tick(symbol, ltp):

    with LOCK:

        data = _read()

        if symbol not in data:
            data[symbol] = {}

        data[symbol]["symbol"] = symbol
        data[symbol]["ltp"] = round(float(ltp), 2)

        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


def write_signal(symbol, last):

    with LOCK:

        data = _read()

        if symbol not in data:
            data[symbol] = {}

        data[symbol].update({

            "symbol": symbol,

            "time": str(last["datetime"]),

            "price": round(float(last["close"]), 2),

            "ema25": round(float(last["EMA25"]), 2),

            "alma10": round(float(last["ALMA10"]), 2),

            "mad_fl": int(last["MAD_FL"]),

            "bb_score": int(last["BB_SCORE"]),

            "score": int(last["SCORE"]),

            "final_score": int(last["FINAL_SCORE"]),

            "signal":
                "BUY"
                if int(last["FINAL_SCORE"]) == 1
                else "SELL"
                if int(last["FINAL_SCORE"]) == -1
                else "WAIT"

        })

        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)