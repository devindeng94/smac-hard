import math
import platform
from ..unit_typeid import UnitTypeId

SYSTEM = platform.system()
BASE_UNIT_TYPE = 2005 if SYSTEM.lower() == 'windows' or SYSTEM.lower() == 'darwin' else 1970

MAP_UNITS_TYPES = {
    '10m_vs_11m': {
        'ally': [UnitTypeId.MARINE.value],
        'enemy': [BASE_UNIT_TYPE]
    },
    '1c3s5z':{
        'ally': [UnitTypeId.COLOSSUS.value, UnitTypeId.ZEALOT.value, UnitTypeId.STALKER.value],
        'enemy': [BASE_UNIT_TYPE, BASE_UNIT_TYPE+1, BASE_UNIT_TYPE+2]
    },
    '25m':{
        'ally': [UnitTypeId.MARINE.value],
        'enemy': [BASE_UNIT_TYPE]
    },
    '27m_vs_30m':{
        'ally': [UnitTypeId.MARINE.value],
        'enemy': [BASE_UNIT_TYPE]
    },
    '2c_vs_64zg':{
        'ally': [UnitTypeId.ZERGLING.value],
        'enemy': [BASE_UNIT_TYPE]
    },
    '2m_vs_1z':{
        'ally': [UnitTypeId.ZEALOT.value],
        'enemy': [BASE_UNIT_TYPE]
    },
    '2s3z':{
        'ally': [UnitTypeId.ZEALOT.value, UnitTypeId.STALKER.value],
        'enemy': [BASE_UNIT_TYPE, BASE_UNIT_TYPE+1]
    },
    '2s_vs_1sc':{
        'ally': [UnitTypeId.SPINECRAWLER.value],
        'enemy': [BASE_UNIT_TYPE, BASE_UNIT_TYPE+1]
    },
    '3m':{
        'ally': [UnitTypeId.MARINE.value],
        'enemy': [BASE_UNIT_TYPE]
    },
    '3s5z': {
        'ally': [UnitTypeId.STALKER.value, UnitTypeId.ZEALOT.value],
        'enemy': [BASE_UNIT_TYPE, BASE_UNIT_TYPE+1]
    },
    '5m_vs_6m':{
        'ally': [UnitTypeId.MARINE.value],
        'enemy': [BASE_UNIT_TYPE]
    },
    '6h_vs_8z':{
        'ally': [UnitTypeId.ZEALOT.value],
        'enemy': [BASE_UNIT_TYPE]
    },
    '8m':{
        'ally': [UnitTypeId.MARINE.value],
        'enemy': [BASE_UNIT_TYPE]
    },
    '8m_vs_9m':{
        'ally': [UnitTypeId.MARINE.value],
        'enemy': [BASE_UNIT_TYPE]
    },
    'bane_vs_bane':{
        'ally': [UnitTypeId.BANELING.value, UnitTypeId.ZERGLING.value],
        'enemy': [BASE_UNIT_TYPE, BASE_UNIT_TYPE+1]
    },
    'corridor':{
        'ally': [UnitTypeId.ZERGLING.value],
        'enemy': [BASE_UNIT_TYPE]
    },
    'MMM':{
        'ally': [UnitTypeId.MARINE.value, UnitTypeId.MARAUDER.value, UnitTypeId.MEDIVAC.value],
        'enemy': [BASE_UNIT_TYPE, BASE_UNIT_TYPE+1, BASE_UNIT_TYPE+2]
    },
    'MMM2':{
        'ally': [UnitTypeId.MARINE.value, UnitTypeId.MARAUDER.value, UnitTypeId.MEDIVAC.value],
        'enemy': [BASE_UNIT_TYPE, BASE_UNIT_TYPE+1, BASE_UNIT_TYPE+2]
    },
    'so_many_baneling':{
        'ally': [UnitTypeId.BANELING.value],
        'enemy': [BASE_UNIT_TYPE]
    },
    '3s_vs_3z':{
        'ally': [UnitTypeId.ZEALOT.value],
        'enemy': [BASE_UNIT_TYPE]
    },
    '3s_vs_4z':{
        'ally': [UnitTypeId.ZEALOT.value],
        'enemy': [BASE_UNIT_TYPE]
    },
    '3s_vs_5z':{
        'ally': [UnitTypeId.ZEALOT.value],
        'enemy': [BASE_UNIT_TYPE]
    },
    '3s5z_vs_3s6z':{
        'ally': [UnitTypeId.ZEALOT.value, UnitTypeId.STALKER.value],
        'enemy': [BASE_UNIT_TYPE, BASE_UNIT_TYPE+1]
    }
}



def find_by_tag(units, tag):

    for u in units:
        if u.tag == tag:
            return u
        
    return None

def center(units):

    x = [u.pos.x for u in units]
    y = [u.pos.y for u in units]
    return (sum(x) / len(x), sum(y)/len(y))

def init_unit(obs, cls):
    
    agents = [unit for unit in obs.observation.raw_data.units if unit.owner==2]
    enemies = [unit for unit in obs.observation.raw_data.units if unit.owner==1]
    
    for i, key in enumerate(cls.ally_list):
        setattr(cls, key, sorted([agent for agent in agents if agent.unit_type==MAP_UNITS_TYPES[cls.map_name]['ally'][i]], key=lambda u: u.tag))
        
    for i, key in enumerate(cls.enemy_list):
        setattr(cls, key, sorted([enemy for enemy in enemies if enemy.unit_type==MAP_UNITS_TYPES[cls.map_name]['enemy'][i]], key=lambda u: u.tag))
