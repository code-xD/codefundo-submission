states = ["State1", "State2", "State3", "State4", "State5"]

city_dict = {
    'State1': ['State1City1', 'State1City2'],
    'State2': ['State2City1', 'State2City2', 'State2City3', 'State2City4'],
    'State3': ['State3City1', 'State3City2', 'State3City3', 'State3City4', 'State3City5', 'State3City6', ],
    'State4': ['State4City1', 'State4City2', 'State4City3', 'State4City4', 'State4City5', 'State4City6', 'State4City7', 'State4City8'],
    'State5': ['State5City1', 'State5City2', 'State5City3', 'State5City4', 'State5City5', 'State5City6', 'State5City7', 'State5City8', 'State5City9', 'State5City10', ]
}
district_dict = {
    'State1City1': ['State1State1City1District1', 'State1State1City1District2'],
    'State1City2': ['State1State1City2District1', 'State1State1City2District2', 'State1State1City2District3', 'State1State1City2District4'],
    'State2City1': ['State2State2City1District1', 'State2State2City1District2'],
    'State2City2': ['State2State2City2District1', 'State2State2City2District2', 'State2State2City2District3', 'State2State2City2District4'],
    'State2City3': ['State2State2City3District1', 'State2State2City3District2', 'State2State2City3District3', 'State2State2City3District4', 'State2State2City3District5', 'State2State2City3District6'],
    'State2City4': ['State2State2City4District1', 'State2State2City4District2', 'State2State2City4District3', 'State2State2City4District4', 'State2State2City4District5', 'State2State2City4District6', 'State2State2City4District7', 'State2State2City4District8'],
    'State3City1': ['State3State3City1District1', 'State3State3City1District2'],
    'State3City2': ['State3State3City2District1', 'State3State3City2District2', 'State3State3City2District3', 'State3State3City2District4'],
    'State3City3': ['State3State3City3District1', 'State3State3City3District2', 'State3State3City3District3', 'State3State3City3District4', 'State3State3City3District5', 'State3State3City3District6'],
    'State3City4': ['State3State3City4District1', 'State3State3City4District2', 'State3State3City4District3', 'State3State3City4District4', 'State3State3City4District5', 'State3State3City4District6', 'State3State3City4District7', 'State3State3City4District8'],
    'State3City5': ['State3State3City5District1', 'State3State3City5District2', 'State3State3City5District3', 'State3State3City5District4', 'State3State3City5District5', 'State3State3City5District6', 'State3State3City5District7', 'State3State3City5District8', 'State3State3City5District9', 'State3State3City5District10'],
    'State3City6': ['State3State3City6District1', 'State3State3City6District2', 'State3State3City6District3', 'State3State3City6District4', 'State3State3City6District5', 'State3State3City6District6', 'State3State3City6District7', 'State3State3City6District8', 'State3State3City6District9', 'State3State3City6District10', 'State3State3City6District11', 'State3State3City6District12'],
    'State4City1': ['State4State4City1District1', 'State4State4City1District2'],
    'State4City2': ['State4State4City2District1', 'State4State4City2District2', 'State4State4City2District3', 'State4State4City2District4'],
    'State4City3': ['State4State4City3District1', 'State4State4City3District2', 'State4State4City3District3', 'State4State4City3District4', 'State4State4City3District5', 'State4State4City3District6'],
    'State4City4': ['State4State4City4District1', 'State4State4City4District2', 'State4State4City4District3', 'State4State4City4District4', 'State4State4City4District5', 'State4State4City4District6', 'State4State4City4District7', 'State4State4City4District8'],
    'State4City5': ['State4State4City5District1', 'State4State4City5District2', 'State4State4City5District3', 'State4State4City5District4', 'State4State4City5District5', 'State4State4City5District6', 'State4State4City5District7', 'State4State4City5District8', 'State4State4City5District9', 'State4State4City5District10'],
    'State4City6': ['State4State4City6District1', 'State4State4City6District2', 'State4State4City6District3', 'State4State4City6District4', 'State4State4City6District5', 'State4State4City6District6', 'State4State4City6District7', 'State4State4City6District8', 'State4State4City6District9', 'State4State4City6District10', 'State4State4City6District11', 'State4State4City6District12'],
    'State4City7': ['State4State4City7District1', 'State4State4City7District2', 'State4State4City7District3', 'State4State4City7District4', 'State4State4City7District5', 'State4State4City7District6', 'State4State4City7District7', 'State4State4City7District8', 'State4State4City7District9', 'State4State4City7District10', 'State4State4City7District11', 'State4State4City7District12', 'State4State4City7District13', 'State4State4City7District14'],
    'State4City8': ['State4State4City8District1', 'State4State4City8District2', 'State4State4City8District3', 'State4State4City8District4', 'State4State4City8District5', 'State4State4City8District6', 'State4State4City8District7', 'State4State4City8District8', 'State4State4City8District9', 'State4State4City8District10', 'State4State4City8District11', 'State4State4City8District12', 'State4State4City8District13', 'State4State4City8District14', 'State4State4City8District15'],
    'State5City1': ['State5State5City1District1', 'State5State5City1District2'],
    'State5City2': ['State5State5City2District1', 'State5State5City2District2', 'State5State5City2District3', 'State5State5City2District4'],
    'State5City3': ['State5State5City3District1', 'State5State5City3District2', 'State5State5City3District3', 'State5State5City3District4', 'State5State5City3District5', 'State5State5City3District6'],
    'State5City4': ['State5State5City4District1', 'State5State5City4District2', 'State5State5City4District3', 'State5State5City4District4', 'State5State5City4District5', 'State5State5City4District6', 'State5State5City4District7', 'State5State5City4District8'],
    'State5City5': ['State5State5City5District1', 'State5State5City5District2', 'State5State5City5District3', 'State5State5City5District4', 'State5State5City5District5', 'State5State5City5District6', 'State5State5City5District7', 'State5State5City5District8', 'State5State5City5District9', 'State5State5City5District10'],
    'State5City6': ['State5State5City6District1', 'State5State5City6District2', 'State5State5City6District3', 'State5State5City6District4', 'State5State5City6District5', 'State5State5City6District6', 'State5State5City6District7', 'State5State5City6District8', 'State5State5City6District9', 'State5State5City6District10', 'State5State5City6District11', 'State5State5City6District12'],
    'State5City7': ['State5State5City7District1', 'State5State5City7District2', 'State5State5City7District3', 'State5State5City7District4', 'State5State5City7District5', 'State5State5City7District6', 'State5State5City7District7', 'State5State5City7District8', 'State5State5City7District9', 'State5State5City7District10', 'State5State5City7District11', 'State5State5City7District12', 'State5State5City7District13', 'State5State5City7District14'],
    'State5City8': ['State5State5City8District1', 'State5State5City8District2', 'State5State5City8District3', 'State5State5City8District4', 'State5State5City8District5', 'State5State5City8District6', 'State5State5City8District7', 'State5State5City8District8', 'State5State5City8District9', 'State5State5City8District10', 'State5State5City8District11', 'State5State5City8District12', 'State5State5City8District13', 'State5State5City8District14', 'State5State5City8District15'],
    'State5City9': ['State5State5City9District1', 'State5State5City9District2', 'State5State5City9District3', 'State5State5City9District4', 'State5State5City9District5', 'State5State5City9District6', 'State5State5City9District7', 'State5State5City9District8', 'State5State5City9District9', 'State5State5City9District10', 'State5State5City9District11', 'State5State5City9District12', 'State5State5City9District13', 'State5State5City9District14', 'State5State5City9District15'],
    'State5City10': ['State5City10District1', 'State5City10District2', 'State5City10District3', 'State5City10District4', 'State5City10District5', 'State5City10District6', 'State5City10District7', 'State5City10District8', 'State5City10District9', 'State5City10District10', 'State5City10District11', 'State5City10District12', 'State5City10District13', 'State5City10District14', 'State5City10District15']
}


def getcodes(state, city, district):
    s_code = states.index(state)
    c_code = city_dict[state].index(city)
    d_code = district_dict[city].index(district)
    return [s_code+1, c_code+1, d_code+1]
