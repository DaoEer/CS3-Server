#pragma once
#include "Interface/NPC/NPCInterface.h"
#include "TongNPCInterface.generated.h"

/*
* 文件名称：TongNPCInterface.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2018-03-23
*/

/**
*帮会NPC接口类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTongNPCInterface: public UNPCInterface
{
	GENERATED_BODY()
	typedef UNPCInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UTongNPCInterface();
	~UTongNPCInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.TongNPCInterface'"); } //获取蓝图对象路径

};