// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Chuangshi.h"
#include "LoginSelectLevel.h"
#include "LoginLevel.generated.h"


/*
* 文件名称：LoginLevel.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：shuqingping
* 创建时间：2017-06-21
*/

class UBaseWindow;

UCLASS(BlueprintType)
class CHUANGSHI_API ALoginLevel : public ALoginSelectLevel
{
	GENERATED_BODY()

public:
	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

	virtual void OnLoadLevelFinished() override;
	virtual bool CheckLoginRun()override;		//是从登录进来的，还是直接在某关卡播放
	void StopMediaSkip();
private:
	void OnViewportResized(FViewport* InViewPort, uint32 Inval);
	void OpenLoginUI();

private:
	FDelegateHandle ViewportResizedHandle;
};
