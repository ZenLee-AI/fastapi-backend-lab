import asyncio
import time
import httpx

BASE = "http://127.0.0.1:8000"
N = 50

async def hit(client: httpx.AsyncClient, path: str) -> float:
    t0 = time.perf_counter()
    r = await client.get(f"{BASE}{path}")
    r.raise_for_status()
    return (time.perf_counter() - t0) * 1000

async def run(path: str):
    async with httpx.AsyncClient(timeout=30.0) as client:
        t0 = time.perf_counter()
        latencies = await asyncio.gather(*[hit(client, path) for _ in range(N)])
        total = (time.perf_counter() - t0) * 1000

    latencies_sorted = sorted(latencies)
    avg = sum(latencies) / len(latencies)
    p95 = latencies_sorted[int(0.95 * (len(latencies_sorted)-1))]

    print(f"\n== {path} ==")
    print(f"concurrency={N}")
    print(f"batch_total_ms={total:.2f}")
    print(f"avg_ms={avg:.2f}")
    print(f"p95_ms={p95:.2f}")
    print(f"min_ms={min(latencies):.2f} max_ms={max(latencies):.2f}")

async def main():
    await run("/io-blocking")
    await run("/io-async")
    await run("/io-bad-async")
    await run("/cpu-bound")
if __name__ == "__main__":
    asyncio.run(main())