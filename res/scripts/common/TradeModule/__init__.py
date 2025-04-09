# -*- coding: utf-8 -*-

import KBEDebug
from TradeModule import PayItems


def getInst( payType ):
	try:
		return PayItems.PayItemBase.PayItemBase.getClass( payType )
	except:
		KBEDebug.ERROR_MSG("Can not find payitem(%s) instance!"%payType)
		return None