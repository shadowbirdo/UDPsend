from logic import gen_vol

timetable1 = [
        {"time": "09:30", "rep": "30s", "vol": "15"},
        {"time": "10:30", "rep": "45s", "vol": "10"},
        {"time": "11:30", "rep": "60s", "vol": "5"}
    ]

timetable2 = [
        {"time": "10:30", "rep": "30s", "vol": "15"},
        {"time": "11:30", "rep": "45s", "vol": "10"},
        {"time": "09:30", "rep": "60s", "vol": "5"}
    ]


def test_vol_in_order():
    assert gen_vol(timetable1) == "V15-10-05"


def test_vol_not_order():
    assert gen_vol(timetable2) == "V05-15-10"

