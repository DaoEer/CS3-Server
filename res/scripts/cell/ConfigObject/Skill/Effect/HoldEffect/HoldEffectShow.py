# -*- coding: utf-8 -*-
"""
usage:
    Buff持有效果,onBegin 和 onEnd 必须成对存在，分别做buff添加和删除，增添的效果

attribute:
    pass

member function:
    pass

callback:
    pass

"""
import csdefine
from ConfigObject.Skill.Effect.HoldEffect.HoldEffect import HoldEffect

class HoldEffectShow(HoldEffect):
    """
    """
    def __init__(self):
        """
        """
        HoldEffect.__init__(self)

    def onBegin(self, effectData, receiver):
        """ """
        HoldEffect.onBegin(self, effectData, receiver)
        receiver.effectStateInc(csdefine.EFFECT_STATE_SHOW)

    def onEnd(self, effectData, receiver):
        """ """
        receiver.effectStateDec(csdefine.EFFECT_STATE_SHOW)
        HoldEffect.onEnd(self, effectData, receiver)



