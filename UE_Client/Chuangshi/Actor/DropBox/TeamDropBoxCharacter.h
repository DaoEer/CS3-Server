#pragma once

#include "GameData/Shape/BaseShape.h"
#include "Engine/EngineTypes.h"
#include "DropBoxCharacter.h"
#include "TeamDropBoxCharacter.generated.h"

/*
* 文件名称：TeamDropBoxCharacter.h
* 功能说明：箱子Character
* 文件作者：qiurunan
* 目前维护：qiurunan
* 创建时间：2020-11-16
*/


DECLARE_DELEGATE_OneParam(FTeamDropBoxDelegate, bool);


/*
* 掉落箱子Character类
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API ATeamDropBoxCharacter :public ADropBoxCharacter
{
	GENERATED_BODY()

public:
	ATeamDropBoxCharacter();///<构造函数
	virtual void OnUnBindActorCallBack() override;
	virtual bool CanGossipWith_Implementation() override;
	virtual void GossipWith() override;///<重写GossipWith
	virtual TArray<UItemBase*> GetBoxItemList() override;
	virtual bool isVisible(const UINT64 &PlayerDBID)override;
		
protected:
	virtual void OnPlayerBeginOverlap_Implementation() override;
	virtual void OnPlayerEndOverlap_Implementation() override;

private:
	void ReqTeamDropBoxData();
	void OnClosedWnd();
};