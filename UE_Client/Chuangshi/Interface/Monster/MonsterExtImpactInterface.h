#pragma once
#include "Interface/Monster/MonsterInterface.h"
#include "MonsterExtImpactInterface.generated.h"

/*
* 文件名称：MonsterExtImpactInterface.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-09-19
*/
UCLASS(BlueprintType)
class UMonsterExtImpactInterface : public UMonsterInterface
{
	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UMonsterExtImpactInterface();
	virtual ~UMonsterExtImpactInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterExtImpactInterface'"); } //获取蓝图对象路径

};

