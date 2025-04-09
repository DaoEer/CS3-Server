#pragma once
#include "Interface/NPC/NPCInterface.h"
#include "NPCExtMoveInterface.generated.h"

/*
* 文件名称：NPCExtMoveInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2017-09-30
*/

/**
*NPC欢乐鼎
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UNPCExtMoveInterface : public UNPCInterface
{
	GENERATED_BODY()
	typedef UNPCInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UNPCExtMoveInterface();
	~UNPCExtMoveInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.NPCExtMoveInterface'"); } //获取蓝图对象路径
};