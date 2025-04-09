#pragma once
#include "CoreMinimal.h"

/*
* 文件名称：CS3Algorithms.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：hezhiming
* 创建时间：2017-08-17
*/

//计算两点间的定比分点坐标（三维）。知道两点(pos1,pos2)，求这两点所形成的直线上距离pos1一定距离(dst)的点。
//如果dst为正，则点的值以pos1为基础从pos1往pos2的方向前进，如果dst为负，则点的值以pos1为基础从pos2往pos1的方向前进。
FVector GetSepratePoint(const FVector& StartPoint, const FVector& EndPoint, float NeedDistance);

TArray<FVector> AnalysicsPathList(const TArray<FVector>& PathList, float MinDis);

