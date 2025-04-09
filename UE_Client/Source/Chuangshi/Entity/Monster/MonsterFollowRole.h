#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterFollowRole.h
* 功能说明：
* 文件作者：qiurunan
* 目前维护：qiurunan
* 创建时间：2019-10-30
*/

/**
* 跟随玩家
*/
class CHUANGSHI_API MonsterFollowRole : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterFollowRole();
	~MonsterFollowRole();

	FVector getNextPosition() { return nextPosition; }
	FVector getNextDirection() { return nextDirection; }

	void set_enemyID(const int32& newEnemyID, const int32& oldEnemyID);
	void set_curPosition(const FVector &newKbePos, const FVector& oldKbePos);
	void set_curDirection(const FVector &newKbeDir, const FVector& oldKbeDir);

private:
	void OnSetPosition(const FVector &unrealPos);
	void OnSetDirection(const FVector &unrealDir);
	void UpdateVolatileDataToServer(const FVector& pos, const FVector& dir);

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
	// 来自服务器：强制位置改变
	void OnPositionSet(const FVector &unrealPos);

	// 来自服务器：强制朝向改变
	void OnDirectionSet(const FVector &unrealDir);
private:
	FVector nextPosition;
	FVector nextDirection;
};
