#pragma once

#include "DropBoxCharacter.h"
#include "GameData/Shape/BaseShape.h"
#include "Engine/EngineTypes.h"
#include "TongDropBoxCharacter.generated.h"

/*
* 文件名称：TongDropBoxCharacter.h
* 功能说明：箱子Character
* 文件作者：qiurunan
* 目前维护：qiurunan
* 创建时间：2020-11-16
*/


DECLARE_DELEGATE_OneParam(FTongDropBoxDelegate, bool);



/*
* 掉落箱子Character类
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API ATongDropBoxCharacter :public ADropBoxCharacter
{
	GENERATED_BODY()

public:
	ATongDropBoxCharacter();///<构造函数
	virtual void OnUnBindActorCallBack() override;
	virtual bool CanGossipWith_Implementation() override;
	virtual void GossipWith() override;///<重写GossipWith
	virtual UBaseShape* CreateSphereShape() override;
	///设置交互半径
	void SetInteractiveRadius(float InRadius);
	void SetCanGossip(float InCanGossip);

	/**
	*DropBox对某个玩家是否可见
	*
	*@param PlayerDBID 玩家DBID(UINT64)
	*
	*@return bool
	*/
	virtual bool isVisible(const UINT64 &PlayerDBID)override;
	virtual void ReSetOpenScen3DUI() { OpenScene3DUI = true; };

	virtual void FlyTargerOverEvent() override;

protected:
	virtual void OnPlayerBeginOverlap_Implementation() override;
	virtual void OnPlayerEndOverlap_Implementation() override;

private:
	void OnClosedWnd();

protected:
	float m_SphereRadius = 20.0f;///<圆形陷阱检测距离半径
	bool CanGossip;
};