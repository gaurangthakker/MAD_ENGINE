async function loadData() {

    try {

        const response = await fetch(
        "https://mad-engine.onrender.com/api/live?t=" + Date.now(),
            {
                cache: "no-store"
            }
        );

        const json = await response.json();

        // ================= BTC =================

        if (json.BTCUSDT) {

            const d = json.BTCUSDT;

            document.getElementById("symbol").innerHTML = d.symbol;

            document.getElementById("price").innerHTML =
                Number(d.ltp || d.price).toFixed(2);

            document.getElementById("ema").innerHTML =
                d.ema25 ?? "-";

            document.getElementById("alma").innerHTML =
                d.alma10 ?? "-";

            document.getElementById("mad").innerHTML =
                d.mad_fl ?? "-";

            document.getElementById("bb").innerHTML =
                d.bb_score ?? "-";

            document.getElementById("score").innerHTML =
                d.score ?? "-";

            document.getElementById("final").innerHTML =
                d.final_score ?? "-";

            document.getElementById("update").innerHTML =
                d.time ?? "-";

            let s = document.getElementById("signal");

            s.innerHTML = d.signal ?? "WAIT";

            s.className = "signal";

            if (d.signal == "BUY")
                s.classList.add("buy");

            else if (d.signal == "SELL")
                s.classList.add("sell");

            else
                s.classList.add("wait");
        }

        // ================= ETH =================

        if (json.ETHUSDT) {

            const e = json.ETHUSDT;

            document.getElementById("symbol2").innerHTML = e.symbol;

            document.getElementById("price2").innerHTML =
                Number(e.ltp || e.price).toFixed(2);

            document.getElementById("ema2").innerHTML =
                e.ema25 ?? "-";

            document.getElementById("alma2").innerHTML =
                e.alma10 ?? "-";

            document.getElementById("mad2").innerHTML =
                e.mad_fl ?? "-";

            document.getElementById("bb2").innerHTML =
                e.bb_score ?? "-";

            document.getElementById("score2").innerHTML =
                e.score ?? "-";

            document.getElementById("final2").innerHTML =
                e.final_score ?? "-";

            document.getElementById("update2").innerHTML =
                e.time ?? "-";

            let s2 = document.getElementById("signal2");

            s2.innerHTML = e.signal ?? "WAIT";

            s2.className = "signal";

            if (e.signal == "BUY")
                s2.classList.add("buy");

            else if (e.signal == "SELL")
                s2.classList.add("sell");

            else
                s2.classList.add("wait");
        }

    }

    catch (err) {

        console.log(err);

    }

}

// Live Clock
function updateClock() {

    const now = new Date();

    const h = String(now.getHours()).padStart(2, "0");
    const m = String(now.getMinutes()).padStart(2, "0");
    const s = String(now.getSeconds()).padStart(2, "0");

    document.getElementById("time").innerHTML =
        `${h}:${m}:${s}`;
}

updateClock();
loadData();

setInterval(updateClock, 1000);
setInterval(loadData, 250);