from core.arbitrage.optimal_size import calculate_optimal_volume


def test_larger_pool_allows_larger_volume():
    shallow = {"bid_volume": 1.0, "ask_volume": 1.0}
    deep = {"bid_volume": 100.0, "ask_volume": 100.0}
    result_shallow = calculate_optimal_volume([shallow, shallow])
    result_deep = calculate_optimal_volume([deep, deep])
    assert result_deep > result_shallow


def test_volume_limited_by_smallest_leg():
    legs = [
        {"bid_volume": 10.0, "ask_volume": 10.0},
        {"bid_volume": 2.0, "ask_volume": 2.0},
        {"bid_volume": 50.0, "ask_volume": 50.0},
    ]
    result = calculate_optimal_volume(legs)
    assert result <= 2.0


def test_minimum_volume():
    legs = [{"bid_volume": 0.0, "ask_volume": 0.0}]
    result = calculate_optimal_volume(legs)
    assert result >= 0.001
