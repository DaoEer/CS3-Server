#pragma once
#include "Interface/NPC/NPCInterface.h"
#include "NPCTortureInterface.generated.h"

/*
* 文件名称：NPCTortureInterface.h
* 功能说明：拷问副本特殊NPC
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-07-16
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UNPCTortureInterface : public UNPCInterface
{
	GENERATED_BODY()
	typedef UNPCInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UNPCTortureInterface();
	~UNPCTortureInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.NPCTortureInterface'"); } //获取蓝图对象路径

};