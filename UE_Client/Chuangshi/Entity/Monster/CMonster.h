#pragma once

#include "KBEngine.h"
#include "CoreMinimal.h"
#include "Entity/Monster/Monster.h"
#include "BehaviorTree/BehaviorTree.h"
#include "MonsterAI/MonsterAIEnum.h"
#include "Entity/Role/CS3Role.h"
#include "GameData/GameDeFine.h"
#include "GameData/ClientMonsterAIData.h"
#include "Skill/SkillBase/Skill.h"
#include "CS3Base/InterfaceDef.h"


/*
* 文件名称：CMonster.h
* 功能说明：
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2019-11-13
*/

/**
* 客户端控制怪物类型
*/
class CHUANGSHI_API CMonster : public Monster
{	typedef Monster Supper;
	KBE_DECLARE_ENTITY_MAP();
public:
	CMonster();
	~CMonster();

	const FCLIENT_MOSNTER_AI_DATA* MonsterAIData;

	void OnControlled(bool isControlled) override;

	void InitRemoteAttr(bool isRemote);
	float InitiativeRange() { return initiativeRange; }
	void InitiativeRange(float fRange) { initiativeRange = fRange; }

	float DistanceControler() { return distanceControler; }
	void DistanceControler(float fDis) { distanceControler = fDis; }

	UBehaviorTree* BehaviorTree() { return AIBTree; }
	void BehaviorTree(UBehaviorTree* br) { AIBTree = br; }

protected:
	virtual void __init__() override;
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

private:
	int32 controlEntityID;
	float initiativeRange; //主动攻击范围
	float distanceControler; //距离控制者最大的距离
	UBehaviorTree* AIBTree;

	//AI命令
	MONSTER_AI_COMMAND _controlCmd;
	KBEngine::FVariantArray _controlArgs;
	bool _isExeCmd;
	void InitCmd();
public:
	void ReciveControlCMD(MONSTER_AI_COMMAND cmd, KBEngine::FVariantArray args = KBEngine::FVariantArray());
	MONSTER_AI_COMMAND GetControlCmd() { return _controlCmd; }
	KBEngine::FVariantArray GetControlArgs() { return _controlArgs; }
	bool IsExeCmd() { return _isExeCmd; }
	void OverExeCmd() { _isExeCmd = true; }

	//判断是否是当前控制客户端
	bool IsControlClient();
	//获取当前控制角色
	CS3Role* GetControlRole();
	KBEngine::Entity* GetControlEntity();

	void ChangeCMonsterState(ENTITY_STATE NewState);
	
	void SoldierCmdFollowUpdate(FVector TargetPos, FVector CenterPos, FVector RelativePos, FRotator Rotation);
	void SoldierCmdFormationUpdate(MONSTER_AI_FORMATION formation, FVector TargetPos, FRotator Rotation);
	void SoldierCmdAttackUptate();
	

	TArray<int32> GroupSkills;
	int32 GroupSkillIndex;

	void InitGroupSkills(TArray<int32> Skills);
	int32 GetGroupSkillID();
	/*技能结束*/
	void onSkillEnd(USkill * skill, bool castResult);

DEF_INTERFACE_CONTENT()
};
