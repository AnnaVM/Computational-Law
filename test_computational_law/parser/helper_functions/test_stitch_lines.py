from computational_law.parser.helper_functions.stitch_lines import stitching_lines


def test_stitching_lines():
    lst = [('text 0', True),('text 1', None)]
    expected_out = [('text 0 text 1', True)]
    assert stitching_lines(lst) == expected_out


    lst = [('text 0', True), ('text 1', None), ('text 2', False)]
    expected_out = [('text 0 text 1', True), ('text 2', False)]
    assert stitching_lines(lst) == expected_out


    lst = [('text 0', True), ('text 1', False), ('text 2', False)]
    expected_out = [('text 0', True), ('text 1', False), ('text 2', False)]
    assert stitching_lines(lst) == expected_out


    lst = [('text 0', True), ('text 1', False), ('text 2', True)]
    expected_out = [('text 0', True), ('text 1', False), ('text 2', True)]
    assert stitching_lines(lst) == expected_out


    lst = [('text 0', False), ('text 1', None), ('text 2', False)]
    expected_out = [('text 0 text 1', False) , ('text 2', False)]
    assert stitching_lines(lst) == expected_out


    lst = [('text 0', False), ('text 1', False), ('text 2', True)]
    expected_out = [('text 0', False), ('text 1', False), ('text 2', True)]
    assert stitching_lines(lst) == expected_out


    lst = [('text 0', False), ('text 1', False), ('text 2', False)]
    expected_out = [('text 0', False), ('text 1', False), ('text 2', False)]
    assert stitching_lines(lst) == expected_out

if __name__ == '__main__':
    test_stitching_lines()
