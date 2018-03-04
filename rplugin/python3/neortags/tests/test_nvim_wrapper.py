import pytest
import neovim
from neortags import NvimWrapper


def get_preview_window(nvim: neovim.Nvim):
    return next((windows for windows in nvim.windows if windows.options['previewwindow']), None)


@pytest.fixture
def nvim_wrapper(nvim_instance) -> NvimWrapper:
    yield NvimWrapper(nvim_instance)


def test_get_current_pos(nvim_instance, nvim_wrapper):
    nvim_instance.current.buffer[0] = "abcdefg"
    nvim_instance.call('cursor', 1, 4)

    assert ":1:4" == nvim_wrapper.get_current_pos()


def test_use_qf_false(nvim_instance, nvim_wrapper):
    assert nvim_wrapper.use_qf is False

    nvim_instance.command('let g:neortags_use_qf = 0')
    assert nvim_wrapper.use_qf is False

    nvim_instance.vars['neortags_use_qf'] = False
    assert nvim_wrapper.use_qf is False


def test_use_qf_true(nvim_instance, nvim_wrapper):
    nvim_instance.command('let g:neortags_use_qf = 1')
    assert nvim_wrapper.use_qf is True

    nvim_instance.command('let g:neortags_use_qf = 10')
    assert nvim_wrapper.use_qf is True

    nvim_instance.vars['neortags_use_qf'] = True
    assert nvim_wrapper.use_qf is True


def test_display_result_in_loc_list(nvim_instance, nvim_wrapper):
    # Arrange
    result = [
        "neortags/tests/testfile.cpp:10:9:     void print(const int value) const",
        "neortags/tests/testfile.cpp:20:10:    test1.print(1);",
        "neortags/tests/testfile.cpp:23:10:    test2.print(2);"
    ]

    # Act
    nvim_wrapper.display_in_qf_or_loclist(result)

    # Assert
    actual_result = nvim_instance.call("getloclist", 0)
    assert actual_result[0]['lnum'] == 10
    assert actual_result[0]['col'] == 9
    assert actual_result[0]['text'] == '    void print(const int value) const'
    assert actual_result[1]['lnum'] == 20
    assert actual_result[1]['col'] == 10
    assert actual_result[1]['text'] == '   test1.print(1);'
    assert actual_result[2]['lnum'] == 23
    assert actual_result[2]['col'] == 10


def test_display_result_in_qf(nvim_instance, nvim_wrapper):
    # Arrange
    nvim_instance.vars['neortags_use_qf'] = 1
    result = [
        "neortags/tests/testfile.cpp:10:9:     void print(const int value) const",
        "neortags/tests/testfile.cpp:20:10:    test1.print(1);",
        "neortags/tests/testfile.cpp:23:10:    test2.print(2);"
    ]

    # Act
    nvim_wrapper.display_in_qf_or_loclist(result)

    # Assert
    actual_result = nvim_instance.call("getqflist")
    assert actual_result[0]['lnum'] == 10
    assert actual_result[0]['col'] == 9
    assert actual_result[0]['text'] == '    void print(const int value) const'
    assert actual_result[1]['lnum'] == 20
    assert actual_result[1]['col'] == 10
    assert actual_result[1]['text'] == '   test1.print(1);'
    assert actual_result[2]['lnum'] == 23
    assert actual_result[2]['col'] == 10


def test_display_in_preview(nvim_instance, nvim_wrapper):
    # Act
    nvim_wrapper.display_in_preview("line1\nline2\n\nline4")

    # Assert
    preview_window = get_preview_window(nvim_instance)
    assert preview_window.buffer[:] == ["line1", "line2", "", "line4"]


def test_display_in_preview_does_nothing_if_empty_text(nvim_instance, nvim_wrapper):
    # Act
    nvim_wrapper.display_in_preview("")

    # Assert
    preview_window = get_preview_window(nvim_instance)
    assert preview_window is None, "Preview window should not be opened"
