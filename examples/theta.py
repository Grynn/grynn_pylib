#!/usr/bin/env python3
"""Plot theta vs expiry for QQQ options."""

import matplotlib.pyplot as plt
import pandas as pd

from grynn_pylib.data_providers import yahoo_finance
import grynn_pylib.finance.options as options


def plot_theta_vs_expiry(ticker: str = "QQQ", strike_range: float = 0.05, rate: float = 0.05):
    """Plot theta vs expiry for options near ATM.

    Args:
        ticker: Ticker symbol (default: "QQQ")
        strike_range: Range around ATM as fraction (default: 0.05 = 5%)
        rate: Risk-free rate (default: 0.05 = 5%)
    """
    print(f"Fetching spot price for {ticker}...")
    spot, timestamp, currency, kind = yahoo_finance.get_spot_price(ticker)
    print(f"Spot price: {spot:.2f} {currency} ({kind})")

    print("\nFetching available expiration dates...")
    dates = yahoo_finance.get_available_dates(ticker)
    print(f"Found {len(dates)} expiration dates")

    # Limit to last 10 dates (long-dated options only)
    dates = dates[-10:]
    print(f"Using long-dated options: {dates[0]} to {dates[-1]}")

    # Filter strikes near ATM
    strike_min = spot * (1 - strike_range)
    strike_max = spot * (1 + strike_range)

    # Collect theta data for calls and puts
    call_data = []
    put_data = []

    for date_str in dates:
        print(f"\nProcessing {date_str}...")
        try:
            calls_df, puts_df, info = yahoo_finance.get_option_chain(ticker, date_str)

            # Filter for strikes near ATM
            calls_atm = calls_df.loc[calls_df["strike"].between(strike_min, strike_max)]
            puts_atm = puts_df.loc[puts_df["strike"].between(strike_min, strike_max)]

            # Calculate average theta for this expiry
            if len(calls_atm) > 0 and "dte" in calls_atm.columns and "iv" in calls_atm.columns:
                dte = calls_atm["dte"].iloc[0]
                for _, row in calls_atm.iterrows():
                    if row["iv"] > 0:
                        theta = options.bs_theta(
                            spot=spot,
                            strike=row["strike"],
                            time=dte / 365,
                            rate=rate,
                            volatility=row["iv"],
                            option_type="call",
                        )
                        call_data.append(
                            {"date": date_str, "dte": dte, "strike": row["strike"], "theta": theta, "iv": row["iv"]}
                        )

            if len(puts_atm) > 0 and "dte" in puts_atm.columns and "iv" in puts_atm.columns:
                dte = puts_atm["dte"].iloc[0]
                for _, row in puts_atm.iterrows():
                    if row["iv"] > 0:
                        theta = options.bs_theta(
                            spot=spot,
                            strike=row["strike"],
                            time=dte / 365,
                            rate=rate,
                            volatility=row["iv"],
                            option_type="put",
                        )
                        put_data.append(
                            {"date": date_str, "dte": dte, "strike": row["strike"], "theta": theta, "iv": row["iv"]}
                        )

        except Exception as e:
            print(f"Error processing {date_str}: {e}")
            continue

    # Convert to DataFrames
    call_df = pd.DataFrame(call_data)
    put_df = pd.DataFrame(put_data)

    if len(call_df) == 0 and len(put_df) == 0:
        print("No data collected. Cannot plot.")
        return

    # Create the plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Plot calls
    if len(call_df) > 0:
        # Group by DTE and calculate mean theta
        call_summary = call_df.groupby("dte").agg({"theta": ["mean", "std"], "strike": "count"}).reset_index()

        ax1.scatter(call_df["dte"], call_df["theta"], alpha=0.3, s=20, label="Individual options")
        ax1.plot(
            call_summary["dte"], call_summary["theta"]["mean"], "r-o", linewidth=2, markersize=8, label="Mean theta"
        )
        ax1.fill_between(
            call_summary["dte"],
            call_summary["theta"]["mean"] - call_summary["theta"]["std"],
            call_summary["theta"]["mean"] + call_summary["theta"]["std"],
            alpha=0.2,
            color="red",
            label="±1 std dev",
        )

    ax1.set_xlabel("Days to Expiry (DTE)")
    ax1.set_ylabel("Theta ($/day)")
    ax1.set_title(f"{ticker} Call Options: Theta vs Expiry (Strikes: {strike_min:.2f} - {strike_max:.2f})")
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.axhline(y=0, color="gray", linestyle="--", alpha=0.5)

    # Plot puts
    if len(put_df) > 0:
        # Group by DTE and calculate mean theta
        put_summary = put_df.groupby("dte").agg({"theta": ["mean", "std"], "strike": "count"}).reset_index()

        ax2.scatter(put_df["dte"], put_df["theta"], alpha=0.3, s=20, label="Individual options")
        ax2.plot(put_summary["dte"], put_summary["theta"]["mean"], "b-o", linewidth=2, markersize=8, label="Mean theta")
        ax2.fill_between(
            put_summary["dte"],
            put_summary["theta"]["mean"] - put_summary["theta"]["std"],
            put_summary["theta"]["mean"] + put_summary["theta"]["std"],
            alpha=0.2,
            color="blue",
            label="±1 std dev",
        )

    ax2.set_xlabel("Days to Expiry (DTE)")
    ax2.set_ylabel("Theta ($/day)")
    ax2.set_title(f"{ticker} Put Options: Theta vs Expiry (Strikes: {strike_min:.2f} - {strike_max:.2f})")
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.axhline(y=0, color="gray", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(f"{ticker}_theta_vs_expiry.png", dpi=150, bbox_inches="tight")
    print(f"\nPlot saved as {ticker}_theta_vs_expiry.png")
    plt.show()

    # Print summary statistics
    print(f"{'=' * 60}")
    print("SUMMARY STATISTICS")
    print(f"{'=' * 60}")
    if len(call_df) > 0:
        print("\nCALLS:")
        print(f"  Total options analyzed: {len(call_df)}")
        print(f"  Mean theta: {call_df['theta'].mean():.4f} $/day")
        print(f"  Std dev: {call_df['theta'].std():.4f} $/day")
        print(f"  Min theta: {call_df['theta'].min():.4f} $/day")
        print(f"  Max theta: {call_df['theta'].max():.4f} $/day")

    if len(put_df) > 0:
        print("\nPUTS:")
        print(f"  Total options analyzed: {len(put_df)}")
        print(f"  Mean theta: {put_df['theta'].mean():.4f} $/day")
        print(f"  Std dev: {put_df['theta'].std():.4f} $/day")
        print(f"  Min theta: {put_df['theta'].min():.4f} $/day")
        print(f"  Max theta: {put_df['theta'].max():.4f} $/day")


if __name__ == "__main__":
    plot_theta_vs_expiry(ticker="QQQ", strike_range=0.05, rate=0.05)
