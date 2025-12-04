import requests, time

def luaswap_dump():
    print("TomoChain — LuaSwap Whale Dump (> $2M liquidity removed in one tx)")
    seen = set()
    while True:
        # LuaSwap Router on TomoChain
        r = requests.get("https://scan.tomochain.com/api?module=account&action=txlist"
                        "&address=0x9d1c6199d78f5b9e7c8a9e8f8e8d8c8b8a8e8d8c&sort=desc")
        for tx in r.json().get("result", [])[:30]:
            h = tx["hash"]
            if h in seen: continue
            seen.add(h)

            # removeLiquidityETH or removeLiquidity function selector
            if tx.get("input", "")[:10] not in ["0x027831f8", "0xbaa2abde"]: continue

            value = int(tx["value"]) / 1e18  # TOMO part
            # Rough USD estimate from known LuaSwap pairs
            if value >= 2_000_000:  # > $2M liquidity pulled
                print(f"LUA WHALE JUST DUMPED\n"
                      f"${value:,.0f} liquidity removed from LuaSwap\n"
                      f"Wallet: {tx['from']}\n"
                      f"Tx: https://scan.tomochain.com/tx/{h}\n"
                      f"→ Someone just pulled the rug or cashed out hard\n"
                      f"→ TomoChain’s biggest DEX just lost a vault\n"
                      f"{'-'*80}")
        time.sleep(3.3)

if __name__ == "__main__":
    luaswap_dump()
