from ini_conf import MyIni

def test_get_ini():
    mi = MyIni()
    assert 'host' in mi.get_kakou()
    assert 'port' in mi.get_kakou()
    assert 'id_flag' in mi.get_kakou()
    assert 'city' in mi.get_kakou()
    assert 'host' in mi.get_union()
    assert 'port' in mi.get_union()

def test_set_id_flag():
    mi = MyIni()
    mi.set_id(709394)


if __name__ == "__main__":
    test_get_ini()
    test_set_id_flag()
