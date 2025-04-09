# -*- coding: utf-8 -*-

import datetime
from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()

from common import ActConf



@register.filter
def timestamp_format( value, arg = "" ):
	"""
	格式化时间戳
	"""
	try:
		t = datetime.datetime.fromtimestamp( value )
	except:
		return value
	
	if not arg:
		arg = settings.DATETIME_FORMAT
	
	result = t.strftime( arg )
	return result

@register.filter
def activity_type_2_name( value ):
	"""
	活动类型转換为名称
	"""
	if value in ActConf.TYPE2NAME:
		return mark_safe( ActConf.TYPE2NAME[value] )
	return value


