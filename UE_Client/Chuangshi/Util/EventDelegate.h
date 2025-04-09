#pragma once
#include "CoreMinimal.h"
#include "CoreTypes.h"

/*
* 文件名称：EventDelegate.h
* 功能说明：一些公共得事件代理定义
* 文件作者：ranxuanwen
* 目前维护：yanjingxin
* 创建时间：2016-08-15
*/


//用于返回调用是否成功
DECLARE_DELEGATE_OneParam(FTraceCallback, bool);