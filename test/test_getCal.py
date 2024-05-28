import pytest
import getCal


def test2024():
    testEne24 = getCal.Calendario(2024, 1)
    assert testEne24.send() == "C1FMXJVSDLMXJVSDLMXJVSDLMXJVSDLMX"

    testFeb24 = getCal.Calendario(2024, 2)
    assert testFeb24.send() == "C2JVSDLMXJVSDLMXJVSDLMXJVSDLMXJ--"

    testDic24 = getCal.Calendario(2024, 12)
    assert testDic24.send() == "CCDLMXJVSDLMXJVSDLMXJVSDLMFJVSDLM"

def test13():
    with pytest.raises(IndexError):
        test13 = getCal.Calendario(2024, 13)
        test13.send()