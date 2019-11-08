from object_colors import Color


class TestBoth(object):
    def test_set_new_attributes(self):
        c = Color()
        c.set(text="blue")
        c.set(effect="bold")
        assert c.text == 4
        assert c.effect == 1
