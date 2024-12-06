from ..scripts.s_3m.script import DecisionTreeScript as DTS_3m
from ..scripts.s_8m.script import DecisionTreeScript as DTS_8m
from ..scripts.s_8m.script_1 import DecisionTreeScript as DTS_8m_1
from ..scripts.s_8m.script_2 import DecisionTreeScript as DTS_8m_2
from ..scripts.s_27m.script import DecisionTreeScript as DTS_27m
from ..scripts.s_3s5z.script import DecisionTreeScript as DTS_3s5z
from ..scripts.s_3s5z.script_1 import DecisionTreeScript as DTS_3s5z_1
from ..scripts.s_3s_vs_5z.script import DecisionTreeScript as DTS_3s_vs_5z

from .s_1c3s5z.script import DecisionTreeScript as DTS_1c3s5z
from .s_1c3s5z.script_d import DecisionTreeScript as DTS_1c3s5z_1
from .s_1c3s5z.script_m import DecisionTreeScript as DTS_1c3s5z_m

from .s_2m_vs_1z.script import DecisionTreeScript as DTS_2m_vs_1z
from .s_2s_vs_1sc.script import DecisionTreeScript as DTS_2s_vs_1sc

from ..scripts.s_so_many_baneling.script import DecisionTreeScript as DTS_so_many_baneling
from ..scripts.s_2c_vs_64zg.script import DecisionTreeScript as DTS_2c_vs_64zg

from .s_MMM.script import DecisionTreeScript as DTS_MMM
from .s_6h_vs_8z.script_hard import DecisionTreeScript as DTS_6h_vs_8z
from .s_corridor.script import DecisionTreeScript as DTS_corridor
from .s_bane_vs_bane.script import DecisionTreeScript as DTS_bane_vs_bane

SCRIPT_DICT = {

    '3m': [DTS_3m],
    '8m': [DTS_8m, DTS_8m_1, DTS_8m_2],
    '5m_vs_6m': [DTS_8m, DTS_8m_1, DTS_8m_2],
    '8m_vs_9m': [DTS_8m, DTS_8m_1, DTS_8m_2],
    '10m_vs_11m': [DTS_8m, DTS_8m_1, DTS_8m_2],
    '25m': [DTS_27m],
    '27m_vs_30m': [DTS_27m],
    '3s5z': [DTS_3s5z, DTS_3s5z_1],
    '2s3z': [DTS_3s5z, DTS_3s5z_1],
    '3s5z_vs_3s6z': [DTS_3s5z],
    '3s_vs_3z': [DTS_3s_vs_5z],
    '3s_vs_4z': [DTS_3s_vs_5z],
    '3s_vs_5z': [DTS_3s_vs_5z],
    '1c3s5z': [DTS_1c3s5z_m],
    '2m_vs_1z': [DTS_2m_vs_1z],
    '2s_vs_1sc': [DTS_2s_vs_1sc],
    'MMM': [DTS_MMM],
    'MMM2': [DTS_MMM],
    'so_many_baneling': [DTS_so_many_baneling],
    '6h_vs_8z': [DTS_6h_vs_8z],
    'corridor': [DTS_corridor],
    'bane_vs_bane': [DTS_bane_vs_bane],
    '2c_vs_64zg': [DTS_2c_vs_64zg]
}
