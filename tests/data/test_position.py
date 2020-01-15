""" Tests for the data.position module"""

# Third party imports
import pytest
import numpy as np

# Midgard imports
from midgard.data import position
from midgard.dev import exceptions


@pytest.fixture()
def pos(request):
    return request.getfixturevalue(request.param.__name__)


@pytest.fixture()
def posvel(request):
    return request.getfixturevalue(request.param.__name__)


@pytest.fixture()
def posdelta(request):
    return request.getfixturevalue(request.param.__name__)


@pytest.fixture()
def posveldelta(request):
    return request.getfixturevalue(request.param.__name__)


@pytest.fixture
def pos_trs_a():
    """"""
    return position.Position(np.random.random((5, 3)) * 6.3e6, system="trs")


@pytest.fixture
def pos_trs_s():
    """"""
    return position.Position(np.random.random((3,)) * 6.3e6, system="trs")


@pytest.fixture
def posvel_trs_a():
    """"""
    factor = np.array([2e8] * 3 + [1e3] * 3)
    return position.PosVel(np.random.random((5, 6)) * factor, system="trs")


@pytest.fixture
def posvel_trs_s():
    """"""
    factor = np.array([2e8] * 3 + [1e3] * 3)
    return position.PosVel(np.random.random((6,)) * factor, system="trs")


@pytest.fixture
def posveldelta_trs_a():
    """"""
    ref_pos = position.PosVel(np.random.random((5, 6)) * 6.3e6, system="trs")
    return position.PosVelDelta(np.random.random((5, 6)), system="trs", ref_pos=ref_pos)


@pytest.fixture
def posveldelta_trs_s():
    """"""
    ref_pos = position.PosVel(np.random.random((6,)) * 6.3e6, system="trs")
    return position.PosVelDelta(np.random.random((6,)), system="trs", ref_pos=ref_pos)


@pytest.fixture
def posdelta_trs_a():
    """"""
    ref_pos = position.Position(np.random.random((5, 3)) * 6.3e6, system="trs")
    return position.PositionDelta(np.random.random((5, 3)), system="trs", ref_pos=ref_pos)


@pytest.fixture
def posdelta_trs_s():
    """"""
    ref_pos = position.Position(np.random.random((3,)) * 6.3e6, system="trs")
    return position.PositionDelta(np.random.random((3,)), system="trs", ref_pos=ref_pos)


@pytest.mark.parametrize("pos", (pos_trs_a, pos_trs_s), indirect=True)
def test_pos_conversions(pos):
    systems = position.PositionArray.systems.keys()

    print(f"Testing systems {systems}")
    for system in systems:
        try:
            converted_pos = getattr(getattr(pos, system), pos.system)
            assert np.allclose(np.asarray(pos), np.asarray(converted_pos))
            print(f"pos.{system} == pos.{system}.{pos.system} OK")
        except exceptions.UnknownConversionError:
            print(f"Conversion from {pos.system} to {system} is not defined")


@pytest.mark.parametrize("posdelta", (posdelta_trs_a, posdelta_trs_s), indirect=True)
def test_posdelta_conversions(posdelta):
    systems = position.PositionDeltaArray.systems.keys()

    print(f"Testing systems {systems}")
    for system in systems:
        try:
            converted_pos = getattr(getattr(posdelta, system), posdelta.system)
            assert np.allclose(np.asarray(posdelta), np.asarray(converted_pos))
            print(f"posdelta.{system} == posdelta.{system}.{posdelta.system} OK")
        except exceptions.UnknownConversionError:
            print(f"Conversion from {posdelta.system} to {system} is not defined")


@pytest.mark.parametrize("posvel", (posvel_trs_a, posvel_trs_s), indirect=True)
def test_posvel_conversions(posvel):
    systems = position.PosVelArray.systems.keys()

    print(f"Testing systems {systems}")
    for system in systems:
        try:
            converted_pos = getattr(getattr(posvel, system), posvel.system)
            assert np.allclose(np.asarray(posvel), np.asarray(converted_pos))
            print(f"posvel.{system} == posvel.{system}.{posvel.system} OK")
        except exceptions.UnknownConversionError:
            print(f"Conversion from {posvel.system} to {system} is not defined")


@pytest.mark.parametrize("posveldelta", (posveldelta_trs_a, posveldelta_trs_s), indirect=True)
def test_posveldelta_conversions(posveldelta):
    systems = position.PosVelDeltaArray.systems.keys()

    print(f"Testing systems {systems}")
    for system in systems:
        try:
            converted_pos = getattr(getattr(posveldelta, system), posveldelta.system)
            assert np.allclose(np.asarray(posveldelta), np.asarray(converted_pos))
            print(f"posveldelta.{system} == posveldelta.{system}.{posveldelta.system} OK")
        except exceptions.UnknownConversionError:
            print(f"Conversion from {posveldelta.system} to {system} is not defined")


def test_slice_and_columns():
    """"""
    # Ny-Ålesund 1202462.5677   252734.4956  6237766.1746
    # Wettzell   4075539.6734   931735.4828  4801629.4955
    # Westford   1492404.5274 -4457266.5326  4296881.8189
    _other = position.Position([[1, 2, 3], [4, 5, 6], [7, 8, 9]], system="trs")
    _pos = position.Position(
        [
            [1_202_462.5677, 252_734.4956, 6_237_766.1746],
            [4_075_539.6734, 931_735.4828, 4_801_629.4955],
            [1_492_404.5274, -4_457_266.5326, 4_296_881.8189],
        ],
        system="trs",
        other=_other,
    )
    _posdelta = position.PositionDelta([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]], system="enu", ref_pos=_pos)

    assert np.equal(_pos.x, np.array([1_202_462.5677, 4_075_539.6734, 1_492_404.5274])).all()
    assert np.equal(_pos[0], np.array([1_202_462.5677, 252_734.4956, 6_237_766.1746])).all()
    assert np.equal(_pos[-1], np.array([1_492_404.5274, -4_457_266.5326, 4_296_881.8189])).all()
    assert np.equal(
        _pos[1:],
        np.array([[4_075_539.6734, 931_735.4828, 4_801_629.4955], [1_492_404.5274, -4_457_266.5326, 4_296_881.8189]]),
    ).all()
    assert np.equal(_pos[0].other, np.array([1, 2, 3])).all()
    assert np.equal(_pos[-1].other, np.array([7, 8, 9])).all()
    assert np.equal(_posdelta.east, np.array([0.1, 0.4, 0.7])).all()
    assert np.equal(_posdelta[1], np.array([0.4, 0.5, 0.6])).all()
    assert np.equal(_posdelta[1].ref_pos, np.array([4_075_539.6734, 931_735.4828, 4_801_629.4955])).all()
    assert np.equal(_posdelta[1].ref_pos.other, np.array([4, 5, 6])).all()
    assert np.equal(_pos[1:].other, np.array([[4, 5, 6], [7, 8, 9]])).all()
