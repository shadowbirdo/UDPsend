from logic import gen_time

timetable1 = [
        {'time': '09:30', 'rep': '30s', 'vol': '15'},
        {'time': '10:30', 'rep': '45s', 'vol': '10'},
        {'time': '11:30', 'rep': '60s', 'vol': '5'}
    ]

timetable2 = [
        {'time': '10:30', 'rep': '30s', 'vol': '15'},
        {'time': '11:30', 'rep': '45s', 'vol': '10'},
        {'time': '09:30', 'rep': '60s', 'vol': '5'}
    ]


def test_time_rows():
    assert gen_time(timetable1) == gen_time(timetable2)
    assert gen_time(timetable1)[0].startswith('H0930-1030-1130') and len(gen_time(timetable1)[0]) == 105
