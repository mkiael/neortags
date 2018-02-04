from neortags import NvimWrapper


def test_get_current_pos(nvim_instance):
    wrapper = NvimWrapper(nvim_instance)

    nvim_instance.current.buffer[0] = "abcdefg"
    nvim_instance.call('cursor', 1, 4)

    assert ":1:4" == wrapper.get_current_pos()

