from plugins.dex.uniswap_v2 import UniswapV2Adapter, calculate_price


def test_calculate_price():
    price = calculate_price(
        reserve0=1000 * 10**18,
        reserve1=2000000 * 10**6,
        decimals0=18,
        decimals1=6,
    )
    assert abs(price - 2000.0) < 0.01


def test_calculate_price_different_decimals():
    price = calculate_price(
        reserve0=1000 * 10**9,
        reserve1=500 * 10**6,
        decimals0=9,
        decimals1=6,
    )
    assert abs(price - 0.5) < 0.001
