import pandas as pd


def generate_summary(trade_log: pd.DataFrame) -> dict:

    total = len(trade_log)

    wins = (trade_log["Points"] > 0).sum()
    losses = (trade_log["Points"] < 0).sum()
    flats = (trade_log["Points"] == 0).sum()

    gross_profit = trade_log.loc[
        trade_log["Points"] > 0,
        "Points"
    ].sum()

    gross_loss = trade_log.loc[
        trade_log["Points"] < 0,
        "Points"
    ].sum()

    net_points = trade_log["Points"].sum()

    avg_win = (
        gross_profit / wins
        if wins else 0
    )

    avg_loss = (
        gross_loss / losses
        if losses else 0
    )

    profit_factor = (
        gross_profit / abs(gross_loss)
        if gross_loss != 0 else 0
    )

    win_rate = (
        wins / (wins + losses) * 100
        if (wins + losses) else 0
    )

    return {
        "Total Trades": total,
        "Wins": wins,
        "Losses": losses,
        "Flats": flats,
        "Win Rate": round(win_rate, 2),
        "Gross Profit": round(gross_profit, 2),
        "Gross Loss": round(gross_loss, 2),
        "Net Points": round(net_points, 2),
        "Average Win": round(avg_win, 2),
        "Average Loss": round(avg_loss, 2),
        "Profit Factor": round(profit_factor, 2),
    }