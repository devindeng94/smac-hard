from ..scripts.s_3m.script import DecisionTreeScript as DTS_3m
from ..scripts.s_8m.script import DecisionTreeScript as DTS_8m
from ..scripts.s_8m.script_1 import DecisionTreeScript as DTS_8m_1
from ..scripts.s_8m.script_2 import DecisionTreeScript as DTS_8m_2
from ..scripts.s_27m.script import DecisionTreeScript as DTS_27m
from ..scripts.s_3s5z.script import DecisionTreeScript as DTS_3s5z
from ..scripts.s_3s5z.script_1 import DecisionTreeScript as DTS_3s5z_1
from ..scripts.s_3s_vs_5z.script import DecisionTreeScript as DTS_3s_vs_5z

from ..scripts.s_1c3s5z.script import DecisionTreeScript as DTS_1c3s5z
from ..scripts.s_1c3s5z.script_1 import DecisionTreeScript as DTS_1c3s5z_1


SCRIPT_DICT = {
    '3m': [DTS_3m],
    '8m': [DTS_8m, DTS_8m_1, DTS_8m_2],
    '5m_vs_6m': [DTS_8m, DTS_8m_1, DTS_8m_2],
    '8m_vs_9m': [DTS_8m, DTS_8m_1, DTS_8m_2],
    '10m_vs_11m': [DTS_8m, DTS_8m_1, DTS_8m_2],
    '25m': [DTS_27m],
    '27m_vs_30m': [DTS_27m],
    '3s5z': [DTS_3s5z, DTS_3s5z_1],
    '2s3z': [DTS_3s5z],
    '3s5z_vs_3s6z': [DTS_3s5z],
    '3s_vs_3z': [DTS_3s_vs_5z],
    '3s_vs_4z': [DTS_3s_vs_5z],
    '3s_vs_5z': [DTS_3s_vs_5z],
    '1c3s5z': [DTS_1c3s5z_1],
}