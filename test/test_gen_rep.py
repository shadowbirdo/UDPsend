from logic import gen_rep

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


def test_rep_in_order():
    assert gen_rep(timetable1) == "T030-045-060"


def test_rep_not_order():
    assert gen_rep(timetable2) == "T060-030-045"
