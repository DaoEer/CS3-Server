// Fill out your copyright notice in the Description page of Project Settings.

#include "Chuangshi.h"
#include "KBEngine.h"
#include "Entity/EntityDeclare.h"
#include "Entity/CSOLPersonality.h"
#include "Guis/CS3Styles.h"
#include "CS3Base/CS3Entity.h"

using namespace KBEngine;

KBEPersonality *g_KBEPersonality;

struct FCS3Tick : FTickableGameObject
{
	FCS3Tick() {};
	virtual void Tick(float DeltaTime)
	{
		if (UUECS3GameInstance::pKBEApp != nullptr)
		{
			UUECS3GameInstance::pKBEApp->Process();

		//	KBEngine::Event::processOutEvents();

			// 实际执行游戏逻辑,平滑消息处理
			CS3Entity_MessageSmoothing::Get().ProcessMessageQueue();
		}
	}
	virtual bool IsTickable() const { return true; };
	virtual bool IsTickableInEditor() const { return true; };
	virtual bool IsTickableWhenPaused() const { return true; };
	FORCEINLINE TStatId GetStatId() const
	{
		RETURN_QUICK_DECLARE_CYCLE_STAT(FCS3Tick, STATGROUP_Tickables);
	}

};

class FCS3GameModule : public FDefaultGameModuleImpl
{
	virtual void StartupModule() override
	{
		g_KBEPersonality = new CSOLPersonality();
		KBEPersonality::Register(g_KBEPersonality);

		EntityDeclare();
		s_cs3Tick = new FCS3Tick();

		FSlateStyleRegistry::UnRegisterSlateStyle(FCS3Styles::GetStyleSetName());
		FCS3Styles::Initialize();
	}

	virtual void ShutdownModule()
	{
		if (g_KBEPersonality)
		{
			KBEPersonality::Deregister();
			delete g_KBEPersonality;
		}
		FCS3Styles::Shutdown();
	}
	static FCS3Tick *s_cs3Tick;
};

FCS3Tick *FCS3GameModule::s_cs3Tick = NULL;

IMPLEMENT_PRIMARY_GAME_MODULE(FCS3GameModule, Chuangshi, "Chuangshi" );
