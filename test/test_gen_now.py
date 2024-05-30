from datetime import datetime
from logic import gen_now


def test_now():
    assert ''.join(filter(lambda x: x not in "D-", gen_now())) == datetime.now().strftime('%Y/%m/%d/%H/%M/%S')
