#pragma once

#include "Interface/Monster/MonsterInterface.h"
#include "MonsterBuildingInterface.generated.h"

/*
* 文件名称：MonsterBuildingInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017-07-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UMonsterBuildingInterface : public UMonsterInterface
{
	GENERATED_BODY()
	typedef UMonsterInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
		
public:
	UMonsterBuildingInterface();
	~UMonsterBuildingInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterBuildingInterface'"); } //获取蓝图对象路径

};