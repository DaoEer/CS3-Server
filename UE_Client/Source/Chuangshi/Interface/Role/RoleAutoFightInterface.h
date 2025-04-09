#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "RoleAutoFightInterface.generated.h"

/*
* 文件名称：RoleAutoFightInterface.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2017-12-18
*/

UCLASS(BlueprintType)
class CHUANGSHI_API URoleAutoFightInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleAutoFightInterface();
	~URoleAutoFightInterface();
	static FString GetName() { return TEXT("RoleAutoFightInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleAutoFightInterface.BP_RoleAutoFightInterface_C'"); } //获取蓝图对象路径

	///添加技能到自动战斗技能快捷栏
	void AddSkillOnList(int32 skillKey, int32 skillID);

	///移除技能通过自动战斗技能栏Key
	void RemoveSkillOnListByKey(int32 SkillKey);
	
};

