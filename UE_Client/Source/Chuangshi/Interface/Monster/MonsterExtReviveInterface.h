#pragma once
#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtReviveInterface.generated.h"

/*
* 文件名称：MonsterExtReviveInterface.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-05-15
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterExtReviveInterface : public UMonsterInterface
{
	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtReviveInterface();
	~UMonsterExtReviveInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtReviveInterface'"); } //获取蓝图对象路径

};

