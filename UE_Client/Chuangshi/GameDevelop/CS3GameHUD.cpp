// Fill out your copyright notice in the Description page of Project Settings.

#include "CS3GameHUD.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/MapManager.h"
#include "Manager/CfgManager.h"
#include "GameData/LevelHashMap.h"
#include "GameData/MinimapData.h"
#include "Actor/ServerCharacter.h"
#include "CS3Base/UIManager.h"
#include "Actor/NPC/NPCCharacter.h"
#include "Manager/QuestEntityVisibleManager.h"
#include "Manager/BuffEntityVisibleManager.h"
#include "Manager/LocalDataSaveManager.h"
#include "CS3GameInstance.h"
#include "Camera/PlayerCameraManager.h"
#include "Kismet/GameplayStatics.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Interface/Role/RoleTeamInterface.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Manager/GameStatus.h"
#include "Manager/VisibleManager.h"
#include "Actor/SpellBox/SpellBoxCharacter.h"
#include "Manager/CfgManager.h"
#include "GameData/TexturePath.h"
#include "Interface/Monster/MonsterInterface.h"
#include "Manager/ResourceManager.h"
#include "Blueprint/WidgetLayoutLibrary.h"
#include "KBEngine.h"
#include "Paths.h"
#include "Util/ImageLoader.h"
#include "Util/CS3Debug.h"
#include "Interface/StateInterface.h"
#include "Math/Color.h"
#include "CS3Base/GameObject.h"
#include "Engine/UserInterfaceSettings.h"

CONTROL_COMPILE_OPTIMIZE_START 

DECLARE_CYCLE_STAT(TEXT("DrawCharacterPoint"), STAT_DrawCharacterPoint, STATGROUP_ACS3GameHUD);
DECLARE_CYCLE_STAT(TEXT("DrawNPCPoint"), STAT_DrawNPCPoint, STATGROUP_ACS3GameHUD);
DECLARE_CYCLE_STAT(TEXT("DrawMonsterPoint"), STAT_DrawMonsterPoint, STATGROUP_ACS3GameHUD);
DECLARE_CYCLE_STAT(TEXT("DrawSpellBoxPoint"), STAT_DrawSpellBoxPoint, STATGROUP_ACS3GameHUD);
DECLARE_CYCLE_STAT(TEXT("DrawDropBoxPoint"), STAT_DrawDropBoxPoint, STATGROUP_ACS3GameHUD);
DECLARE_CYCLE_STAT(TEXT("DrawPlayerPoint"), STAT_DrawPlayerPoint, STATGROUP_ACS3GameHUD);
DECLARE_CYCLE_STAT(TEXT("DrawTeamMembersPoint"), STAT_DrawTeamMembersPoint, STATGROUP_ACS3GameHUD);
DECLARE_CYCLE_STAT(TEXT("DrawActorPointByMaterial"), STAT_DrawActorPointByMaterial, STATGROUP_ACS3GameHUD);
DECLARE_CYCLE_STAT(TEXT("DrawActorPointByTexture"), STAT_DrawActorPointByTexture, STATGROUP_ACS3GameHUD);

DECLARE_CYCLE_STAT(TEXT("AddDamageEffect"), STAT_AddDamageEffect, STATGROUP_ACS3GameHUD);
DECLARE_CYCLE_STAT(TEXT("DrawDamageEffect"), STAT_DrawDamageEffect, STATGROUP_ACS3GameHUD);
DECLARE_CYCLE_STAT(TEXT("AddSkillNameEffect"), STAT_AddSkillNameEffect, STATGROUP_ACS3GameHUD);
DECLARE_CYCLE_STAT(TEXT("DrawSkillNameEffect"), STAT_DrawSkillNameEffect, STATGROUP_ACS3GameHUD);

DECLARE_CYCLE_STAT(TEXT("IsYXWZSignCfg"), STAT_IsYXWZSignCfg, STATGROUP_ACS3GameHUD); 
DECLARE_CYCLE_STAT(TEXT("GetMonsterPointVisible"), STAT_GetMonsterPointVisible, STATGROUP_ACS3GameHUD);
DECLARE_CYCLE_STAT(TEXT("GetMonsterVisible"), STAT_GetMonsterVisible, STATGROUP_ACS3GameHUD);

DECLARE_CYCLE_STAT(TEXT("FindMonsterPointVisible"), STAT_FindMonsterPointVisible, STATGROUP_GetMonsterPointVisible_ResultCache);
DECLARE_CYCLE_STAT(TEXT("UpdateCache"), STAT_UpdateCache, STATGROUP_GetMonsterPointVisible_ResultCache);

void ACS3GameHUD::BeginPlay()
{
	Super::BeginPlay();
	UUECS3GameInstance* GameInstance = UUECS3GameInstance::Instance;
	if (!IsValid(GameInstance)) return;
	//添加RootUI到视口中
	AddRootUMG();
	InitHUDDatas();
	InitConfigData();
}

void ACS3GameHUD::InitHUDDatas()
{
	PlayerPointIcon = Cast<UTexture2D>(UGolbalBPFunctionLibrary::LoadObjectByAssetPath(PlayerPoint));
	GreenPointIcon = Cast<UTexture2D>(UGolbalBPFunctionLibrary::LoadObjectByAssetPath(GreenPoint));
	RedPointIcon = Cast<UTexture2D>(UGolbalBPFunctionLibrary::LoadObjectByAssetPath(RedPoint));
	TeamMemberPointIcon = Cast<UTexture2D>(UGolbalBPFunctionLibrary::LoadObjectByAssetPath(TeamMemberPoint));
	CameraRotationIcon = Cast<UTexture2D>(UGolbalBPFunctionLibrary::LoadObjectByAssetPath(CameraRotationImg));
	GreenPointMat = Cast<UMaterialInterface>(UGolbalBPFunctionLibrary::LoadObjectByAssetPath(GreenMatPoint));
	RedPointMat = Cast<UMaterialInterface>(UGolbalBPFunctionLibrary::LoadObjectByAssetPath(RedMatPoint));
	DropBoxPointIcon = Cast<UTexture2D>(UGolbalBPFunctionLibrary::LoadObjectByAssetPath(DropBoxPoint));
	MiniMapTexture = UGolbalBPFunctionLibrary::ImageLoader()->GetMiniMapTexture();
}

void ACS3GameHUD::BeginDestroy()
{
	MiniMapTexture = nullptr;
	PlayerPointIcon = nullptr;
	GreenPointIcon = nullptr;
	RedPointIcon = nullptr;
	TeamMemberPointIcon = nullptr;
	CameraRotationIcon = nullptr;
	GreenPointMat = nullptr;
	RedPointMat = nullptr;
	DropBoxPointIcon = nullptr;
	ClearConfigDatas();
	Super::BeginDestroy();
}

void ACS3GameHUD::PreInitializeComponents()
{
	//初始HUD动画效果
	{
		DamageEffectInfos_CircularArray.AddDefaulted(MaxDamageEffectCount);

		SkillNameEffectInfos_CircularArray.AddDefaulted(MaxSkillNameEffectCount);

		checkf(DamageNumIconsTable_Common->GetRowStruct()->IsChildOf(FCS3TexturePath::StaticStruct()), TEXT("ACS3GameHUD::BeginPlay() 失败! DamageNumIconsTable_Common为空或RowStruct不是FCS3TexturePath"));
		checkf(DamageNumIconsTable_Critical->GetRowStruct()->IsChildOf(FCS3TexturePath::StaticStruct()), TEXT("ACS3GameHUD::BeginPlay() 失败! DamageNumIconsTable_Critical为空或RowStruct不是FCS3TexturePath"));
		checkf(DamageNumIconsTable_LocalPlayerAreAttacked->GetRowStruct()->IsChildOf(FCS3TexturePath::StaticStruct()), TEXT("ACS3GameHUD::BeginPlay() 失败! DamageNumIconsTable_LocalPlayerAreAttacked为空或RowStruct不是FCS3TexturePath"));

		auto LoadNumIconsFun = [](FName Num, UDataTable* DamageNumIconsTable, TArray<FCanvasIcon, TInlineAllocator<10>>& DamageNumIcons)
		{
			FCS3TexturePath* CS3TexturePath = DamageNumIconsTable->FindRow<FCS3TexturePath>(Num, TEXT(""), false);
			checkf(CS3TexturePath != nullptr, TEXT("ACS3GameHUD::BeginPlay::LoadNumIconsFun 加载错误: 找不到RowName: %s"), *Num.ToString());
			if (IsValid(UUECS3GameInstance::Instance))
			{
				UTexture* Texture = (UTexture*)UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(CS3TexturePath->TexturePath, true); //伤害字资源永不释放
				checkf(Texture != nullptr, TEXT("ACS3GameHUD::BeginPlay::LoadNumIconsFun 加载错误: RowName:%s TexturePath.LoadSynchronous == nullptr"), *Num.ToString());
				DamageNumIcons.Emplace(UCanvas::MakeIcon(Texture));
			}
		};

		for (int Num = 0; Num < 10; ++Num)
		{
			FName RowName = *FString::FromInt(Num);

			LoadNumIconsFun(RowName, DamageNumIconsTable_Common, DamageNumIcons_Common);
			LoadNumIconsFun(RowName, DamageNumIconsTable_Critical, DamageNumIcons_Critical);
			LoadNumIconsFun(RowName, DamageNumIconsTable_LocalPlayerAreAttacked, DamageNumIcons_LocalPlayerAreAttacked);
		}
	}
}

void ACS3GameHUD::DrawHUD()
{
	DpiScale = UGolbalBPFunctionLibrary::GetViewportScale();
	Super::DrawHUD();
}

void ACS3GameHUD::SetMiniMapData()
{
	const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	UMapManager* MapManager = UGolbalBPFunctionLibrary::MapManager();
	FString tempMapScriptID = SpaceScriptID;
	if (IsValid(MapManager))
	{
		if (MapManager->IsPlaneSpace(SpaceScriptID))
		{
			//如果是位面，需要先获得对应大地图的scriptID
			tempMapScriptID = MapManager->GetRelatedMapScriptID(SpaceScriptID);
		}
	}
	//读HashMap表，根据表来加载关卡
	UCfgManager* CfgManager = UGolbalBPFunctionLibrary::CfgManager();
	if (!IsValid(CfgManager)) return;
	const UConfigTable* HashConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_LEVELMAP);
	const UConfigTable* MiniMapConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MINIMAP_DATA);
	if (IsValid(HashConfigTable) && IsValid(MiniMapConfigTable))
	{
		const FLEVEL_HASHMAP* LevelHashMap = HashConfigTable->GetRow<FLEVEL_HASHMAP>(tempMapScriptID);
		if (LevelHashMap != nullptr)
		{
			// 先之后SubStreamLevelName，为空再找LevelName（CST-11204）
			FName tempLevelName = LevelHashMap->SubStreamLevelName;
			bool UseSubStreamLevelName = false;
			if (!tempLevelName.IsNone())
			{
				FMINIMAP_DATA* MiniMapData = const_cast<FMINIMAP_DATA*>(MiniMapConfigTable->GetRow<FMINIMAP_DATA>(tempLevelName.ToString()));
				if (MiniMapData != nullptr)
				{
					UseSubStreamLevelName = true;
				}
			}
			if (UseSubStreamLevelName)
			{
				LevelName = tempLevelName.ToString();
			}
			else
			{
				tempLevelName = LevelHashMap->LevelName;
				if (tempLevelName.ToString().Contains(TEXT("|")))
				{
					//比如凤鸣南麓是由三个关卡组成HashMap表里面配的有下划线“L_FM_XYW|L_FMYW_DOWN|L_FMYW_UP”，而贴图名字不能命名下划线所以需修改
					LevelName = tempLevelName.ToString().Replace(TEXT("|"), TEXT("_"));
				}
				else
				{
					LevelName = tempLevelName.ToString();
				}
			}
			
			FMINIMAP_DATA* MiniMapData = const_cast<FMINIMAP_DATA*>(MiniMapConfigTable->GetRow<FMINIMAP_DATA>(tempLevelName));
			if (MiniMapData != nullptr)
			{
				UpdateMiniMapTexture(LevelName);
				LevelSize = MiniMapData->LevelSize;
				LevelOrign = MiniMapData->LevelOrign;
				MiniMapUISize = MiniMapData->MiniMapSize;
				IsShowMiniMap = MiniMapData->IsShowMiniMap;
				Rate = LevelSize.X / MiniMapUISize.X;
				SetViewDefaultScale(MiniMapData->ViewDefaultScale);
				return;
			}
		}
	}
	LevelName = TEXT("");
	IsShowMiniMap = false;
}

void ACS3GameHUD::SetViewDefaultScale(float DefaultScale)
{
	ViewDefaultScale = DefaultScale;
	MaxZoomScale = 1.0 / ViewDefaultScale;//最大放大到正常图片没有任何缩放的尺寸即1.0
	FVector2D MinZoom = MiniMapViewSize / MiniMapUISize;//最小缩到全地图不能再缩了
	MinZoomScale = FMath::Max(MinZoom.X, MinZoom.Y) / ViewDefaultScale;
	ZoomRate = DefaultScale;
	PerZoomRate = DefaultScale / 10.0f;
	MiniMapViewSizeTarget = MiniMapViewSize / ZoomRate;
}

void ACS3GameHUD::CalcMiniMapData()
{
	//获取玩家
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(PlayerActor))
	{
		//设置地图UI上玩家的点的像素坐标
		FVector PlayerLocation = PlayerActor->GetActorLocation();
		MiniMapPlayerPos.X = (PlayerLocation.X - LevelOrign.X) / Rate;
		MiniMapPlayerPos.Y = (PlayerLocation.Y - LevelOrign.Y) / Rate;
		
		//设置可视范围顶点像素坐标：在地图UI上小地图可视范围顶点像素坐标=MiniMapPlayerPos-1/2*MiniMapViewSizeTarget
		MiniMapViewOrigin = MiniMapPlayerPos - MiniMapViewSizeTarget / 2.0;
		MiniMapViewOrigin = FVector2D(FMath::Clamp(MiniMapViewOrigin.X, 0.0f,(MiniMapUISize.X - MiniMapViewSizeTarget.X)), FMath::Clamp(MiniMapViewOrigin.Y, 0.0f, (MiniMapUISize.Y - MiniMapViewSizeTarget.Y)));
		//设置小地图可视范围的原点在小地图的贴图MiniMapTexture上的UV坐标（0~1）：小地图可视范围顶点UV坐标=在地图UI上小地图可视范围顶点像素坐标/MiniMapTexture尺寸
		MiniMapViewOriginUV = MiniMapViewOrigin / MiniMapUISize;
	}
}

void ACS3GameHUD::ZoomIn()
{
	if (CanZoomScale(true))
	{
		ZoomRate = ZoomRate + PerZoomRate;
		MiniMapViewSizeTarget = MiniMapViewSize / ZoomRate;
	}
}

void ACS3GameHUD::ZoomOut()
{
	if (CanZoomScale(false))
	{
		ZoomRate = ZoomRate - PerZoomRate;
		MiniMapViewSizeTarget = MiniMapViewSize / ZoomRate;
	}
}

bool ACS3GameHUD::CanZoomScale(bool IsZoomIn)
{
	if (IsZoomIn)
	{
		return ZoomRate + PerZoomRate <= ViewDefaultScale * MaxZoomScale;
	}
	else
	{
		return ZoomRate - PerZoomRate >= ViewDefaultScale * MinZoomScale;
	}
}

FString ACS3GameHUD::GetZoomScale(bool IsZoomIn)
{
	FString OutZoomScale = TEXT("");
	float TempRate = ZoomRate / ViewDefaultScale;//当前放大或缩小倍数
	if (IsZoomIn)
	{
		TempRate += 0.1;
	}
	else
	{
		TempRate -= 0.1;
	}
	OutZoomScale = FString::Printf(TEXT("%0.1f"), TempRate);
	return OutZoomScale;
}
 
void ACS3GameHUD::DrawMiniMapTexture()
{
	float tempScreenX;
	float tempScreenY;
	float tempScreenW;
	float tempScreenH;
	float tempTextureU;
	float tempTextureV;
	float tempTextureUWidth;
	float tempTextureVHeight;
	GetMinimapXYHW(tempScreenX, tempScreenY, tempScreenW, tempScreenH, tempTextureU, tempTextureV, tempTextureUWidth, tempTextureVHeight);
	DrawTexture(MiniMapTexture, tempScreenX, tempScreenY, tempScreenW, tempScreenH, tempTextureU, tempTextureV, tempTextureUWidth, tempTextureVHeight);
	return;
}

void ACS3GameHUD::DrawMiniMapMaterial(UMaterialInterface* InMaterial)
{
	if (!IsValid(InMaterial)) return;
	float tempScreenX;
	float tempScreenY;
	float tempScreenW;
	float tempScreenH;
	float tempTextureU;
	float tempTextureV;
	float tempTextureUWidth;
	float tempTextureVHeight;
	GetMinimapXYHW(tempScreenX, tempScreenY, tempScreenW, tempScreenH, tempTextureU, tempTextureV, tempTextureUWidth, tempTextureVHeight);
	DrawMaterial(InMaterial, tempScreenX, tempScreenY, tempScreenW, tempScreenH, tempTextureU, tempTextureV, tempTextureUWidth, tempTextureVHeight);
}

void ACS3GameHUD::DrawPoint()
{
	AServerCharacter* PlayerActor;
	const TMap<int32, KBEngine::Entity*>* EntitiesMap;

	if ( !IsValid(UUECS3GameInstance::Instance) ||
		!IsValid(PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()) || 
		UUECS3GameInstance::pKBEApp == nullptr || 
		(EntitiesMap = UUECS3GameInstance::pKBEApp->Entities()) == nullptr )
	{
		return;
	}

	static TArray<AActor*> ActorList;
	ActorList.Reset();
	FVector2D tempViewLevelRange = MiniMapViewSizeTarget / 2.0 * Rate;;


	const FString NowSpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	static const FString SpaceScriptID = FString(TEXT("fu_ben_L_LMZC"));
	bool isLMZC = SpaceScriptID.Equals(NowSpaceScriptID);
	bool isZhenyingPVP = NowSpaceScriptID.Equals(TEXT("fu_ben_L_YCJMD_zhenyingPVP"));
	bool isYCJMD = NowSpaceScriptID.StartsWith(TEXT("fu_ben_L_YCJMD"))&&!isZhenyingPVP;
	MonsterPointVisible_ResultCache.UpdateCache();

	for (auto& Elem : *EntitiesMap)
	{
		KBEngine::Entity* Entity = Elem.Value;
		AActor* EntityActor;
		if ( Entity == nullptr || Entity->IsPlayer() || !IsValid(EntityActor = Entity->Actor()) )
		{
			continue;
		}

		FVector2D ActorPos = (FVector2D(EntityActor->GetActorLocation()) - LevelOrign) / Rate;//Actor像素位置
		FVector2D tempDis = ActorPos - MiniMapViewOrigin;//Actor距离小地图可视原点的像素距离
		if (tempDis.X > 0 && tempDis.X < MiniMapViewSizeTarget.X && tempDis.Y > 0 && tempDis.Y < MiniMapViewSizeTarget.Y)
		{
			//绘制各种点
			//这里continue是为了优化性能,不全部都执行
			//
			FVector PlayerPosition = PlayerActor->GetActorLocation();
			FVector ActorPosition = EntityActor->GetActorLocation();
			int Distance = FVector::Dist(ActorPosition, PlayerPosition);
			URoleTeamInterface* RoleTeamInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.RoleTeamInterface : nullptr;
			if (DrawMonsterPoint(EntityActor, PlayerActor) || 
				DrawNPCPoint(EntityActor, PlayerActor) || 
				DrawDropBoxPoint(EntityActor, PlayerActor) || 
				DrawSpellBoxPoint(EntityActor, PlayerActor)) continue;			
			if ((isLMZC && Distance <= 5000.0)||(isZhenyingPVP && Distance <= 10000.0))//更新灵脉战场
			{
				DrawCharacterPoint(EntityActor, PlayerActor);
			}
			if (IsValid(RoleTeamInterface))
			{
				bool bIsSameTeam = RoleTeamInterface->IsTeammate(Entity->ID());
				if (isYCJMD && Distance <= 5000.0&&!bIsSameTeam)//更新吃鸡战场非队友玩家标记
				{
					DrawCharacterPoint(EntityActor, PlayerActor);
				}
			}
		}
	}

	//绘制各种点
	DrawPlayerPoint(PlayerActor);
	DrawTeamMembersPoint();
	//DrawCameraPoint()  暂时不需要显示预留方法
}

void ACS3GameHUD::DrawLinkLine(const TArray<FVector2D>& LinkPoints)
{
	for(int startIdx = 0; startIdx < LinkPoints.Num()-1; ++startIdx)
	{
		int endIdx = startIdx + 1;
		if (endIdx <= LinkPoints.Num() - 1)
		{
			DrawOneLine(LinkPoints[startIdx], LinkPoints[endIdx]);
		}

	}
}

void ACS3GameHUD::DrawLineSegments(const TArray<FLineSegment>& LineSegments)
{
	for (int index = 0; index < LineSegments.Num(); index++)
	{
		FLineSegment LineSegment = LineSegments[index];
		FVector2D StartPoint = FVector2D(LineSegment.PointA.X, LineSegment.PointA.Y);
		FVector2D EndPoint = FVector2D(LineSegment.PointB.X, LineSegment.PointB.Y);
		DrawOneLine(StartPoint, EndPoint);
	}
}

void ACS3GameHUD::DrawOneLine(FVector2D PointA, FVector2D PointB)
{
	FVector2D StartPoint = (PointA - LevelOrign) / Rate;
	FVector2D EndPoint = (PointB - LevelOrign) / Rate;
	FVector2D StartPadding = (StartPoint - MiniMapViewOrigin)*ZoomRate;
	FVector2D EndStartPadding = (EndPoint - MiniMapViewOrigin)*ZoomRate;
	if (StartPadding.X > 0.0&&StartPadding.X < MiniMapViewSize.X && StartPadding.Y > StartPadding.Y / 2 && StartPadding.Y < MiniMapViewSize.Y
	&& EndStartPadding.X > 0.0 && EndStartPadding.X <MiniMapViewSize.X && EndStartPadding.Y > EndStartPadding.Y / 2 && EndStartPadding.Y < MiniMapViewSize.Y)
	{
		float StartX = ResX - (MiniMapUIPadding.X + MiniMapViewSize.X - StartPadding.X) * DpiScale;
		float StartY = (MiniMapUIPadding.Y + StartPadding.Y) * DpiScale;
		float EndX = ResX - (MiniMapUIPadding.X + MiniMapViewSize.X - EndStartPadding.X) * DpiScale;
		float EndY = (MiniMapUIPadding.Y + EndStartPadding.Y) * DpiScale;
		DrawLine(StartX, StartY, EndX, EndY, FLinearColor(255, 0, 0), 1.0);
	}

}

void ACS3GameHUD::DrawPlayerPoint(AServerCharacter* PlayerActor)
{
	SCOPE_CYCLE_COUNTER(STAT_DrawPlayerPoint);

	if ( !IsValid(PlayerPointIcon) ) return;
	int32 IconSizeX = PlayerPointIcon->GetSizeX();
	int32 IconSizeY = PlayerPointIcon->GetSizeY();
	FVector2D tempPadding = (MiniMapPlayerPos - MiniMapViewOrigin) * ZoomRate;
	float tempScreenX = ResX - (MiniMapUIPadding.X + MiniMapViewSize.X - tempPadding.X + IconSizeX /2) * DpiScale;
	float tempScreenY = (MiniMapUIPadding.Y + tempPadding.Y - IconSizeY / 2) * DpiScale;
	float tempScreenW = IconSizeX * DpiScale;
	float tempScreenH = IconSizeY * DpiScale;
	float tempRotation = 0.0;
	tempRotation = PlayerActor->GetActorRotation().Yaw + 135.0;
	DrawTexture(PlayerPointIcon, tempScreenX, tempScreenY, tempScreenW, tempScreenH, 0, 0, 1, 1, FLinearColor::White, BLEND_Translucent, 1.0, false, tempRotation, FVector2D(0.5,0.5));
}

void ACS3GameHUD::DrawActorPointByTexture(AActor* InActor, UTexture2D* InTexture)
{
	SCOPE_CYCLE_COUNTER(STAT_DrawActorPointByTexture);
	if (IsValid(InTexture) && IsValid(InActor))
	{
		float ScreenX = 0.0;
		float ScreenY = 0.0;
		float ScreenW = 0.0;
		float ScreenH = 0.0;
		if (GetActorPointXYHW(InActor, FVector2D((float)InTexture->GetSizeX(), (float)InTexture->GetSizeY()), ScreenX, ScreenY, ScreenW, ScreenH))
		{
			DrawTexture(InTexture, ScreenX, ScreenY, ScreenW, ScreenH, 0.0, 0.0, 1.0, 1.0);
		}
	}
}

void ACS3GameHUD::DrawActorPointByMaterial(AActor* InActor, UMaterialInterface* InMaterial, FVector2D InSize)
{
	SCOPE_CYCLE_COUNTER(STAT_DrawActorPointByMaterial);
	if (IsValid(InMaterial) && IsValid(InActor))
	{
		float ScreenX = 0.0;
		float ScreenY = 0.0;
		float ScreenW = 0.0;
		float ScreenH = 0.0;
		if (GetActorPointXYHW(InActor, InSize, ScreenX, ScreenY, ScreenW, ScreenH))
		{
			DrawMaterial(InMaterial, ScreenX, ScreenY, ScreenW, ScreenH, 0.0, 0.0, 1.0, 1.0);
		}
	}
}

bool ACS3GameHUD::DrawCharacterPoint(AActor* EntityActor, AServerCharacter* PlayerActor)
{
	SCOPE_CYCLE_COUNTER(STAT_DrawCharacterPoint);
	APlayerCharacter* Character = Cast<APlayerCharacter>(EntityActor);

	if (IsValid(Character) && Character->EntityId != PlayerActor->EntityId)
	{

		UStateInterface* StateInterface = Character->GetEntityInterface_Cache().StateInterface;
		if (IsValid(StateInterface) && StateInterface->HasEffectState(EFFECT_STATE::EFFECT_STATE_HIDE) && Character->QueryRelation(PlayerActor) == COMBAT_RELATION::COMBAT_RELATION_ENEMY)
		{
			return false;
		}
		int32 CharacterCamp = Character->GetFinalCamp();
		int32 PlayerCamp = PlayerActor->GetFinalCamp();
		if (CharacterCamp == PlayerCamp)
		{
			DrawActorPointByTexture(Character, GreenPointIcon);
		}
		else
		{
			DrawActorPointByTexture(Character, RedPointIcon);
		}
		return true;
	}
	return false;
}

bool ACS3GameHUD::DrawNPCPoint(AActor* EntityActor, AServerCharacter* PlayerActor)
{
	SCOPE_CYCLE_COUNTER(STAT_DrawNPCPoint);
	ANPCCharacter* NPC = Cast<ANPCCharacter>(EntityActor);
	if (IsValid(NPC) && GetNPCPointVisible(NPC))
	{
		//FString icon = UGolbalBPFunctionLibrary::GetFStringPropertyValue(NPC->EntityId, TEXT("iconTypeOnMap"));
		//int32 camp = UGolbalBPFunctionLibrary::GetIntPropertyValue(NPC->EntityId, TEXT("camp"));
		AServerCharacter* PlayerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
		if (NPC->QueryRelation(PlayerCharacter) == COMBAT_RELATION::COMBAT_RELATION_ENEMY)
		{
			DrawActorPointByTexture(NPC, RedPointIcon);
		}
		else
		{
			DrawActorPointByTexture(NPC, GreenPointIcon);
		}
		return true;
	}
	return false;
}

void ACS3GameHUD::DrawTeamMembersPoint()
{
	SCOPE_CYCLE_COUNTER(STAT_DrawTeamMembersPoint);

	ULocalDataSaveManager* LocalDataSaveManager = UGolbalBPFunctionLibrary::LocalDataSaveManager();
	if (IsValid(LocalDataSaveManager) && IsValid(LocalDataSaveManager->LocalUserSettingData))
	{
		if (LocalDataSaveManager->LocalUserSettingData->BaseSettingData.IsShowTeammate)
		{
			URoleTeamInterface* RoleTeamInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.RoleTeamInterface : nullptr;
			if (IsValid(RoleTeamInterface))
			{
				for (auto It = RoleTeamInterface->TeamPosMap.CreateConstIterator(); It; ++It)
				{
					if (It.Value().objectID != UGolbalBPFunctionLibrary::GetPlayerID())
					{
						float ScreenX = 0.0;
						float ScreenY = 0.0;
						float ScreenW = 0.0;
						float ScreenH = 0.0;
						if (GetPointXYHW(It.Value().position, FVector2D((float)TeamMemberPointIcon->GetSizeX(), (float)TeamMemberPointIcon->GetSizeY()), ScreenX, ScreenY, ScreenW, ScreenH))
						{
							DrawTexture(TeamMemberPointIcon, ScreenX, ScreenY, ScreenW, ScreenH, 0.0, 0.0, 1.0, 1.0);
						}
					}
				}
			}
		}
	}
}

bool ACS3GameHUD::DrawMonsterPoint(AActor* EntityActor, AServerCharacter* PlayerActor)
{
	SCOPE_CYCLE_COUNTER(STAT_DrawMonsterPoint);
	AMonsterCharacter* Monster = Cast<AMonsterCharacter>(EntityActor);
	if (IsValid(Monster) && MonsterPointVisible_ResultCache.FindMonsterPointVisible(*Monster, *PlayerActor))
	{
		FString ScriptID = UGolbalBPFunctionLibrary::GetFStringPropertyValue(Monster->EntityId, TEXT("scriptID"));
		bool IsFind = false;
		UTexture2D* YXWZIcon = IsYXWZSignCfg(ScriptID, IsFind);
		if (IsFind)
		{
			DrawActorPointByTexture(Monster, YXWZIcon);
		}
		else
		{
			bool IsEnemy = false;
			AServerCharacter* PlayerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
			if (Monster->QueryRelation(PlayerCharacter) == COMBAT_RELATION::COMBAT_RELATION_ENEMY)
			{
				IsEnemy = true;
			}
			if (Monster->isTwinkle)
			{
				if (IsEnemy)
				{
					DrawActorPointByMaterial(Monster,RedPointMat, FVector2D(28.0f, 28.0f));
				}
				else
				{
					DrawActorPointByMaterial(Monster, GreenPointMat, FVector2D(28.0f, 28.0f));
				}
			}
			else
			{
				if (IsEnemy)
				{
					DrawActorPointByTexture(Monster, RedPointIcon);
				}
				else
				{
					DrawActorPointByTexture(Monster, GreenPointIcon);
				}
			}
		}
		return true;
	}
	return false;
}

bool ACS3GameHUD::DrawSpellBoxPoint(AActor* EntityActor, AServerCharacter* PlayerActor)
{
	SCOPE_CYCLE_COUNTER(STAT_DrawSpellBoxPoint);
	ASpellBoxCharacter* SpellBox = Cast<ASpellBoxCharacter>(EntityActor);
	if (IsValid(SpellBox) && GetSpellBoxPointVisible(SpellBox))
	{
		const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
		if (SpaceScriptID == FString(TEXT("cycle_L_LQMG")))
		{
			UObject* Texture2DObj = UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(FSoftObjectPath(TEXT("Texture2D'/Game/Textures/UI/BigMap/T_ICON_chuansong03_Big_D.T_ICON_chuansong03_Big_D'")));
			if (Texture2DObj)
			{
				SpellBoxPointIcon = (UTexture2D*)Texture2DObj;
			}
		}
		else if(SpaceScriptID.StartsWith(TEXT("fu_ben_L_YCJMD")))
		{
			FString ScriptID = UGolbalBPFunctionLibrary::GetFStringPropertyValue(SpellBox->EntityId, TEXT("scriptID"));
			if(ScriptID == TEXT("40001039")|| ScriptID == TEXT("40000797"))
			{
				UObject* Texture2DObj = UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(FSoftObjectPath(TEXT("Texture2D'/Game/Textures/UI/BigMap/NPCMarks/T_Icon_YCJMD_chest.T_Icon_YCJMD_chest'")));
				if (Texture2DObj)
				{
					SpellBoxPointIcon = (UTexture2D*)Texture2DObj;
				}
			}
		}
		else
		{
			SpellBoxPointIcon = GreenPointIcon;
		}
		DrawActorPointByTexture(SpellBox, SpellBoxPointIcon);
		return true;
	}
	return false;
}

void ACS3GameHUD::DrawCameraPoint()
{
	if (!IsValid(CameraRotationIcon)) return;
	float tempScreenX = ResX - (MiniMapUIPadding * DpiScale).X - (MiniMapViewSize * DpiScale / 2).X - (CameraRotationIcon->GetSizeX() * DpiScale / 2);
	float tempScreenY = (MiniMapUIPadding * DpiScale).Y + (MiniMapViewSize * DpiScale / 2).Y - (CameraRotationIcon->GetSizeY() * DpiScale );
	float tempScreenW = CameraRotationIcon->GetSizeX() * DpiScale;
	float tempScreenH = CameraRotationIcon->GetSizeY() * DpiScale;
	float tempRotation = 0.0;
	UWorld* GameWorld = UUECS3GameInstance::Instance->GetWorld();
	if (GameWorld && IsValid(GameWorld))
	{
		APlayerCameraManager* PlayerCameraManager = UGameplayStatics::GetPlayerCameraManager(GameWorld, 0);
		if (PlayerCameraManager && IsValid(PlayerCameraManager))
		{
			tempRotation = PlayerCameraManager->GetCameraRotation().Pitch - 90;
		}
	}
	DrawTexture(PlayerPointIcon, tempScreenX, tempScreenY, tempScreenW, tempScreenH, 0, 0, 1, 1, FLinearColor::White, BLEND_Translucent, 1.0, false, tempRotation, FVector2D(0.5, 0.5));
}

bool ACS3GameHUD::DrawDropBoxPoint(AActor* EntityActor, AServerCharacter* PlayerActor)
{
	SCOPE_CYCLE_COUNTER(STAT_DrawDropBoxPoint);
	ADropBoxCharacter* DropBox = Cast<ADropBoxCharacter>(EntityActor);
	if (IsValid(DropBox) && GetDropBoxPointVisible(DropBox))
	{
		DrawActorPointByTexture(DropBox, DropBoxPointIcon);
		return true;
	}
	return false;
}

void ACS3GameHUD::AddRootUMG()
{
	UGUIManager* UIManager = UGolbalBPFunctionLibrary::GUIManager();
	if (IsValid(UIManager))
	{
		UIManager->ShowRootUI();
	}
}

void ACS3GameHUD::InitConfigData()
{
	//清空数据
	ClearConfigDatas();
	//读entity 任务可见性配置表
	UCfgManager* CfgManager = UGolbalBPFunctionLibrary::CfgManager();
	if (!IsValid(CfgManager)) return;
	//初始化entity 任务可见性配置表
	const UConfigTable* QuestEntityVisibleTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_QUEST_ENTITY_VISIBLE);
	if (IsValid(QuestEntityVisibleTable))
	{
		auto QuestTableRowMap = QuestEntityVisibleTable->GetBaseTable()->GetRowMap();
		for (auto Row : QuestTableRowMap)
		{
			FQEV_CFG_ROW_DATA* QuestVisibleData = (FQEV_CFG_ROW_DATA*)Row.Value;
			QuestEntityVisibleMap.Add(Row.Key, QuestVisibleData);
		}
	}

	//初始化entity BUFF可见性配置表
	const UConfigTable* BuffEntityVisibleTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_BUFF_ENTITY_VISIBLE);
	if (IsValid(BuffEntityVisibleTable))
	{
		auto BuffTableRowMap = BuffEntityVisibleTable->GetBaseTable()->GetRowMap();
		for (auto Row : BuffTableRowMap)
		{
			FBEV_CFG_ROW_DATA* BuffVisibleData = (FBEV_CFG_ROW_DATA*)Row.Value;
			BuffEntityVisibleMap.Add(Row.Key, BuffVisibleData);
		}
	}

	//英雄王座Entity标记图标配置表
	const UConfigTable* YXWZIconTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_YXWZ_SIGN_ICON_DATA);
	if (IsValid(YXWZIconTable))
	{
		auto YXWZSignTableRowMap = YXWZIconTable->GetBaseTable()->GetRowMap();
		for (auto Row : YXWZSignTableRowMap)
		{
			FSIGN_ICON_DATA* YXWZVisibleData = (FSIGN_ICON_DATA*)Row.Value;
			YXWZSignIconMap.Add(Row.Key, YXWZVisibleData);
		}
	}
}

void ACS3GameHUD::ClearConfigDatas()
{
	QuestEntityVisibleMap.Empty();
	BuffEntityVisibleMap.Empty();
	YXWZSignIconMap.Empty();
}

void ACS3GameHUD::AddDamageEffect(FVector WorldLocation, int32 DamageValue, bool IsCritical, bool IsParry, bool IsDodge, bool IsPlayer)
{
	SCOPE_CYCLE_COUNTER(STAT_AddDamageEffect);

	WorldLocation.Z += 50.f; //让伤害数字在头顶出现
	FVector ScreenPosition;
	if (UWidgetLayoutLibrary::ProjectWorldLocationToWidgetPositionWithDistance(GetOwningPlayerController(), WorldLocation, ScreenPosition)) // 不在屏幕中的不添加效果
	{
		const FVector2D ViewportSize = FVector2D(GEngine->GameViewport->Viewport->GetSizeXY());
		const float ViewportScale = GetDefault<UUserInterfaceSettings>(UUserInterfaceSettings::StaticClass())->GetDPIScaleBasedOnSize(FIntPoint(ViewportSize.X, ViewportSize.Y));
		ScreenPosition = FVector(ScreenPosition.X * ViewportScale, ScreenPosition.Y * ViewportScale, ScreenPosition.Z);

		DamageEffectInfo& newDamageEffect = DamageEffectInfos_CircularArray[NowAddIndex_DamageEffect];

		// 居中偏移
		switch (newDamageEffect.Type)
		{
		case DamageEffectInfo::EffectType::Common:
			static int32 NumIconWeight_Common = DamageNumIcons_Common[0].UL / 2.f;
			ScreenPosition.X += (log10(DamageValue) + 1) * NumIconWeight_Common - NumIconWeight_Common * 2;
			break;
		case DamageEffectInfo::EffectType::Critical:
			static int32 NumIconWeight_Critical = DamageNumIcons_Critical[0].UL / 2.f;
			ScreenPosition.X += ((log10(DamageValue) + 1) * NumIconWeight_Critical - NumIconWeight_Critical * 2) * 1.8f;
			break;
		case DamageEffectInfo::EffectType::LocalPlayerAreAttacked:
			static int32 NumIconWeight_LocalPlayerAreAttacked = DamageNumIcons_LocalPlayerAreAttacked[0].UL / 2.f;
			ScreenPosition.X += ((log10(DamageValue) + 1) * NumIconWeight_LocalPlayerAreAttacked - NumIconWeight_LocalPlayerAreAttacked * 2) * 1.2f;
			break;
		case DamageEffectInfo::EffectType::Dodge:
			static int32 DodgeOffset = DodgeIcon->GetSurfaceWidth() / 2.f;
			ScreenPosition.X -= DodgeOffset;
			break;
		case DamageEffectInfo::EffectType::Parry:
			static int32 ParryOffset = ParryIcon->GetSurfaceWidth() / 2.f;
			ScreenPosition.X -= ParryOffset;
			break;
		}

		newDamageEffect.ScreenPosition = ScreenPosition;
		newDamageEffect.DamageValue = DamageValue;
		newDamageEffect.AnimationTime = 0.0f;

		if (IsPlayer)
		{
			newDamageEffect.Type = DamageEffectInfo::EffectType::LocalPlayerAreAttacked;
		}
		else if (IsParry)
		{
			newDamageEffect.Type = DamageEffectInfo::EffectType::Parry;
		}
		else if (IsDodge)
		{
			newDamageEffect.Type = DamageEffectInfo::EffectType::Dodge;
		}
		else if (IsCritical)
		{
			newDamageEffect.Type = DamageEffectInfo::EffectType::Critical;
		}
		else
		{
			newDamageEffect.Type = DamageEffectInfo::EffectType::Common;
		}

		NowAddIndex_DamageEffect = (NowAddIndex_DamageEffect + 1) % MaxDamageEffectCount;
	}
}

void ACS3GameHUD::DrawDamageEffect()
{
	SCOPE_CYCLE_COUNTER(STAT_DrawDamageEffect);
	auto UpdateFloatingAnimationFun = [this](DamageEffectInfo& DamageEffect)
	{
		DamageEffect.ScreenPosition.Y -= RenderDelta * DamageEffect_FloatingSpeed;
		DamageEffect.AnimationTime += RenderDelta;
	};

	auto DrawTextFun = [this](const DamageEffectInfo& DamageEffect,const TArray<FCanvasIcon, TInlineAllocator<10>>& DamageNumIcons, float Scale)
	{
		Canvas->DrawColor = FColor::White;
		Canvas->DrawColor.A = DamageEffect.AnimationTime <= DamageEffect_StartTransparencyTime ? 255 : 
			(1.f - (DamageEffect.AnimationTime - DamageEffect_StartTransparencyTime) / DamageEffect_StartTransparencyDuration) * 255.f;

		int32 DamageValue = DamageEffect.DamageValue;
		int32 Index = 0;
		while (DamageValue > 0)
		{
			int Num = DamageValue % 10;

			const FCanvasIcon& NumIcon = DamageNumIcons[Num];
			Canvas->DrawIcon(NumIcon, DamageEffect.ScreenPosition.X - NumIcon.UL * Index, DamageEffect.ScreenPosition.Y, Scale);

			++Index;
			DamageValue = DamageValue / 10;
		}
	};

	auto DrawColorFun = [this](const DamageEffectInfo& DamageEffect, const FCanvasIcon& CanvasIcon)
	{
		Canvas->DrawColor = FColor::White;
		Canvas->DrawIcon(CanvasIcon, DamageEffect.ScreenPosition.X, DamageEffect.ScreenPosition.Y, 1.0f);
	};

	int32 Index = NowAddIndex_DamageEffect - 1;
	for (int i = 0; i < MaxDamageEffectCount; ++i)
	{
		Index = Index < 0 ? MaxDamageEffectCount - 1 : Index;
		DamageEffectInfo& NowInfo = DamageEffectInfos_CircularArray[Index];

		if (NowInfo.AnimationTime >= DamageEffect_Duration) break; //由于是倒着循环,从最新添加的效果开始循环,所以判断到一个持续时间不够后面的也一定不够

		// 绘制效果
		{
			switch (NowInfo.Type)
			{
			case DamageEffectInfo::EffectType::Common:
				DrawTextFun(NowInfo, DamageNumIcons_Common, 1.f);
				break;
			case DamageEffectInfo::EffectType::Critical:
				DrawTextFun(NowInfo, DamageNumIcons_Critical, 1.8f);
				break;
			case DamageEffectInfo::EffectType::LocalPlayerAreAttacked:
				DrawTextFun(NowInfo, DamageNumIcons_LocalPlayerAreAttacked, 1.2f);
				break;
			case DamageEffectInfo::EffectType::Dodge:
				DrawColorFun(NowInfo, UCanvas::MakeIcon(DodgeIcon));
				break;
			case DamageEffectInfo::EffectType::Parry:
				DrawColorFun(NowInfo, UCanvas::MakeIcon(ParryIcon));
				break;
			}

			UpdateFloatingAnimationFun(NowInfo);
		}

		--Index; //倒着循环
	}
}

void ACS3GameHUD::AddSkillNameEffect(FVector WorldLocation, const FString& SkillName, bool IsLocalPlayer)
{
	SCOPE_CYCLE_COUNTER(STAT_AddSkillNameEffect);

	FVector ScreenPosition;
	if (UWidgetLayoutLibrary::ProjectWorldLocationToWidgetPositionWithDistance(GetOwningPlayerController(), WorldLocation, ScreenPosition)) // 不在屏幕中的不添加效果
	{
		const FVector2D ViewportSize = FVector2D(GEngine->GameViewport->Viewport->GetSizeXY());
		const float ViewportScale = GetDefault<UUserInterfaceSettings>(UUserInterfaceSettings::StaticClass())->GetDPIScaleBasedOnSize(FIntPoint(ViewportSize.X, ViewportSize.Y));
		ScreenPosition = FVector(ScreenPosition.X * ViewportScale, ScreenPosition.Y * ViewportScale, ScreenPosition.Z);

		SkillNameEffectInfo& newSkillNameEffect = SkillNameEffectInfos_CircularArray[NowAddIndex_SkillNameEffect];

		ScreenPosition.X -= SkillName.Len() * 20; // 将文字居中

		newSkillNameEffect.ScreenPosition = ScreenPosition;
		newSkillNameEffect.SkillName = FText::FromString(SkillName);
		newSkillNameEffect.AnimationTime = 0.0f;

		if (IsLocalPlayer)
		{
			newSkillNameEffect.Type = SkillNameEffectInfo::EffectType::LocalPlayer;
		}
		else
		{
			newSkillNameEffect.Type = SkillNameEffectInfo::EffectType::Other;
		}

		NowAddIndex_SkillNameEffect = (NowAddIndex_SkillNameEffect + 1) % MaxSkillNameEffectCount;
	}
}

void ACS3GameHUD::DrawSkillNameEffect()
{
	SCOPE_CYCLE_COUNTER(STAT_DrawSkillNameEffect);
	auto UpdateFloatingAnimationFun = [this](SkillNameEffectInfo& SkillNameEffect)
	{
		if (SkillNameEffect.AnimationTime < SkillNameEffect_StopFloatingTime)
		{
			SkillNameEffect.ScreenPosition.Y -= RenderDelta * SkillNameEffect_FloatingSpeed;
		}
		SkillNameEffect.AnimationTime += RenderDelta;
	};

	SkillNameEffect_Font->LegacyFontSize = 28;
	FFontRenderInfo DamageFontRenderInfo;
	DamageFontRenderInfo.bEnableShadow = true;
	auto DrawTextFun = [this, DamageFontRenderInfo](const SkillNameEffectInfo& SkillNameEffect, const FColor& Color, float Scale)
	{
		Canvas->DrawColor = Color;
		Canvas->DrawText(SkillNameEffect_Font, SkillNameEffect.SkillName, SkillNameEffect.ScreenPosition.X, SkillNameEffect.ScreenPosition.Y, Scale, Scale, DamageFontRenderInfo);
	};

	int32 Index = NowAddIndex_SkillNameEffect - 1;
	for (int i = 0; i < MaxSkillNameEffectCount; ++i)
	{
		Index = Index < 0 ? MaxSkillNameEffectCount - 1 : Index;
		SkillNameEffectInfo& NowInfo = SkillNameEffectInfos_CircularArray[Index];

		if (NowInfo.AnimationTime >= SkillNameEffect_Duration) break; //由于是倒着循环,从最新添加的效果开始循环,所以判断到一个持续时间不够后面的也一定不够

		// 绘制效果
		{
			switch (NowInfo.Type)
			{
			case SkillNameEffectInfo::EffectType::LocalPlayer:
				DrawTextFun(NowInfo, FColor::Yellow, 1.f);
				break;
			case SkillNameEffectInfo::EffectType::Other:
				DrawTextFun(NowInfo, FColor::Red, 1.f);
				break;
			}

			UpdateFloatingAnimationFun(NowInfo);
		}

		--Index; //倒着循环
	}
}

void ACS3GameHUD::AddFightStateChangeEffect(FVector WorldLocation, bool IsEnterFight)
{
	FVector ScreenPosition;
	if (UWidgetLayoutLibrary::ProjectWorldLocationToWidgetPositionWithDistance(GetOwningPlayerController(), WorldLocation, ScreenPosition)) // 不在屏幕中的不添加效果
	{
		const FVector2D ViewportSize = FVector2D(GEngine->GameViewport->Viewport->GetSizeXY());
		const float ViewportScale = GetDefault<UUserInterfaceSettings>(UUserInterfaceSettings::StaticClass())->GetDPIScaleBasedOnSize(FIntPoint(ViewportSize.X, ViewportSize.Y));
		ScreenPosition = FVector(ScreenPosition.X * ViewportScale, ScreenPosition.Y * ViewportScale, ScreenPosition.Z);

		ScreenPosition.X -= 4 * 25; // 将文字居中

		NowFightStateChangeEffectInfo.AnimationTime = 0.f;
		NowFightStateChangeEffectInfo.ScreenPosition = ScreenPosition;
		NowFightStateChangeEffectInfo.Type = IsEnterFight ? FightStateChangeEffectInfo::EffectType::Enter : FightStateChangeEffectInfo::EffectType::Leave;
	}
}

void ACS3GameHUD::DrawFightStateChangeEffect()
{
	auto UpdateFloatingAnimationFun = [this](FightStateChangeEffectInfo& FightStateChangeEffect)
	{
		FightStateChangeEffect.ScreenPosition.Y -= RenderDelta * FightStateChangeEffect_FloatingSpeed;
		FightStateChangeEffect.AnimationTime += RenderDelta;
	};

	FightStateChangeEffect_Font->LegacyFontSize = 32;
	FFontRenderInfo DamageFontRenderInfo;
	DamageFontRenderInfo.bEnableShadow = true;
	auto DrawTextFun = [this, DamageFontRenderInfo](const FightStateChangeEffectInfo& FightStateChangeEffect, const FText& Text, const FColor& Color, float Scale)
	{
		Canvas->DrawColor = Color;
		Canvas->DrawText(FightStateChangeEffect_Font, Text, FightStateChangeEffect.ScreenPosition.X, FightStateChangeEffect.ScreenPosition.Y, Scale, Scale, DamageFontRenderInfo);
	};

	if (NowFightStateChangeEffectInfo.AnimationTime >= FightStateChangeEffect_Duration) return;

	// 绘制效果
	static FText EnterFightText = FText::FromString(TEXT("进入战斗"));
	static FText LeaveFightText = FText::FromString(TEXT("离开战斗"));

	switch (NowFightStateChangeEffectInfo.Type)
	{
	case FightStateChangeEffectInfo::EffectType::Enter:
		DrawTextFun(NowFightStateChangeEffectInfo, EnterFightText, FColor::Red, 1.f);
		break;
	case FightStateChangeEffectInfo::EffectType::Leave:
		DrawTextFun(NowFightStateChangeEffectInfo, LeaveFightText, FColor::Green, 1.f);
		break;
	}

	UpdateFloatingAnimationFun(NowFightStateChangeEffectInfo);
}

bool ACS3GameHUD::IsInQuestEntityVisibleCfg(const FString& scriptID)
{
	//判断entity脚本ID是否在 任务可见性配置表中
	return QuestEntityVisibleMap.Contains(FName(*scriptID));
}

bool ACS3GameHUD::IsInBuffEntityVisibleCfg(const FString& scriptID)
{
	//判断entity脚本ID是否在BUFF可见性配置表中
	return BuffEntityVisibleMap.Contains(FName(*scriptID));
}

UTexture2D* ACS3GameHUD::IsYXWZSignCfg(const FString& scriptID, bool& OutIsFind)
{
	SCOPE_CYCLE_COUNTER(STAT_IsYXWZSignCfg);
	//判断entity脚本ID是否在英雄王座Entity标记图标配置表中

	if (const auto YXWZIconData = YXWZSignIconMap.Find(FName(*scriptID)))
	{
		OutIsFind = true;
		UTexture2D* tempTexture = Cast<UTexture2D>(UGolbalBPFunctionLibrary::LoadObjectByAssetPath((*YXWZIconData)->Icon));
		return tempTexture;
	}

	OutIsFind = false;
	return nullptr;
}

bool ACS3GameHUD::GetNPCPointVisible(ANPCCharacter* InNPC)
{
	if (!IsValid(InNPC)) return false;
	int32 DisplayOnClient = UGolbalBPFunctionLibrary::GetIntPropertyValue(InNPC->EntityId, TEXT("displayOnClient"));
	switch (DisplayOnClient)
	{
	case 0://默认可见，可控制
	{
		ULocalDataSaveManager* LocalDataSaveManager = UGolbalBPFunctionLibrary::LocalDataSaveManager();
		if (IsValid(LocalDataSaveManager) && IsValid(LocalDataSaveManager->LocalUserSettingData))
		{
			if (LocalDataSaveManager->LocalUserSettingData->BaseSettingData.IsShowNPC)
			{
				return GetNPCVisible(InNPC);
			}
		}
		return false;
		break; 
	}
	case 1://强制可见，不可控
	{
		return GetNPCVisible(InNPC);
		break;
	}
	case 2://强制不可见，不可控
	{
		return false;
		break;
	}
	case 3://
	{
		return true;
		break;
	}
	default:
		return true;
	}
}

bool ACS3GameHUD::GetNPCVisible(ANPCCharacter* InNPC)
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		FString ScriptID = UGolbalBPFunctionLibrary::GetFStringPropertyValue(InNPC->EntityId, TEXT("scriptID"));
		if (IsInBuffEntityVisibleCfg(ScriptID))
		{
			//如果是在BUFF可见性配置表中
			UBuffEntityVisibleManager* BuffEntityVisibleManager = UUECS3GameInstance::Instance->BuffEntityVisibleManager;
			if (IsValid(BuffEntityVisibleManager))
			{
				return BuffEntityVisibleManager->GetVisibleTypeByScriptID(ScriptID) == VISIBLE_TYPE::VISIBLE_TYPE_BUFF_TRUE;
			}
		}
		if (IsInQuestEntityVisibleCfg(ScriptID))
		{
			//如果是在任务可见性配置表中
			UQuestEntityVisibleManager* QuestEntityVisibleManager = UUECS3GameInstance::Instance->QuestEntityVisibleManager;
			if (IsValid(QuestEntityVisibleManager))
			{
				return QuestEntityVisibleManager->GetEntityVisible(ScriptID) > 0;
			}
		}
		if (InNPC->HasFlag(ENTITY_FLAG::FLAG_UNVISIBLE))
		{
			//是否有不可见标志位
			return false;
		}
	}
	return true;
}

bool ACS3GameHUD::GetMonsterPointVisible(AMonsterCharacter* InMonster, AServerCharacter* PlayerActor)
{
	SCOPE_CYCLE_COUNTER(STAT_GetMonsterPointVisible);
	if (!IsValid(InMonster)) return false;
	int32 DisplayOnClient = UGolbalBPFunctionLibrary::GetIntPropertyValue(InMonster->EntityId, TEXT("displayOnClient"));
	switch (DisplayOnClient)
	{
	case 0://默认可见，可控制
	{
		ULocalDataSaveManager* LocalDataSaveManager = UGolbalBPFunctionLibrary::LocalDataSaveManager();
		if (IsValid(LocalDataSaveManager) && IsValid(LocalDataSaveManager->LocalUserSettingData))
		{
			if (LocalDataSaveManager->LocalUserSettingData->BaseSettingData.IsShowMonster)
			{
				return GetMonsterVisible(InMonster, PlayerActor);
			}
		}
		return false;
		break;
	}
	case 1://强制可见，不可控
	{
		return !(InMonster->HasFlag(ENTITY_FLAG::FLAG_UNVISIBLE));
		break;
	}
	case 2://强制不可见，不可控
	{
		return false;
		break;
	}
	case 3:
	{
		return true;
		break;
	}
	default:
		return true;
	}
}

bool ACS3GameHUD::GetMonsterVisible(AMonsterCharacter* InMonster, AServerCharacter* PlayerActor)
{
	SCOPE_CYCLE_COUNTER(STAT_GetMonsterVisible);
	if (IsValid(UUECS3GameInstance::Instance))
	{
		FString ScriptID = UGolbalBPFunctionLibrary::GetFStringPropertyValue(InMonster->EntityId, TEXT("scriptID"));
		if (IsInBuffEntityVisibleCfg(ScriptID))
		{
			//如果是在BUFF可见性配置表中
			UBuffEntityVisibleManager* BuffEntityVisibleManager = UUECS3GameInstance::Instance->BuffEntityVisibleManager;
			if (IsValid(BuffEntityVisibleManager))
			{
				return BuffEntityVisibleManager->GetVisibleTypeByScriptID(ScriptID) == VISIBLE_TYPE::VISIBLE_TYPE_BUFF_TRUE;
			}
		}
		if (IsInQuestEntityVisibleCfg(ScriptID))
		{
			//如果是在任务可见性配置表中
			UQuestEntityVisibleManager* QuestEntityVisibleManager = UUECS3GameInstance::Instance->QuestEntityVisibleManager;
			if (IsValid(QuestEntityVisibleManager))
			{
				return QuestEntityVisibleManager->GetEntityVisible(ScriptID) > 0;
			}
		}
		if (IsValid(InMonster))
		{
			UStateInterface* StateInterface = InMonster->GetEntityInterface_Cache().StateInterface;
			if (IsValid(StateInterface) && StateInterface->HasEffectState(EFFECT_STATE::EFFECT_STATE_HIDE) && InMonster->QueryRelation(PlayerActor) == COMBAT_RELATION::COMBAT_RELATION_ENEMY)
			{
				//隐身状态
				return false;
			}
			if (InMonster->HasFlag(ENTITY_FLAG::FLAG_UNVISIBLE))
			{
				//是否有不可见标志位
				return false;
			}
		}
		
	}
	return true;
}

bool ACS3GameHUD::GetSpellBoxPointVisible(ASpellBoxCharacter *InSpellBox)
{
	if (!IsValid(InSpellBox)) return false;
	int32 DisplayOnClient = UGolbalBPFunctionLibrary::GetIntPropertyValue(InSpellBox->EntityId, TEXT("displayOnClient"));
	switch (DisplayOnClient)
	{
	case 0://默认可见，可控制
	{
		//需先判断InSpellBox->StatusBox == 2才执行下面的，这个变量被定义到了蓝图了，以后再改
// 		if (InSpellBox->StatusBox == 2)
// 		{
// 			return GetSpellBoxVisible(InSpellBox);
// 		}
// 		return false;
// 		break;
		return GetSpellBoxVisible(InSpellBox);
		break;
	}
	case 1://强制可见，不可控
	{
		return GetSpellBoxVisible(InSpellBox);
		break;
	}
	case 2://强制不可见，不可控
	{
		return false;
		break;
	}
	case 3://
	{
		return true;
		break;
	}
	default:
		return false;
	}
}

bool ACS3GameHUD::GetSpellBoxVisible(ASpellBoxCharacter *InSpellBox)
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		FString ScriptID = UGolbalBPFunctionLibrary::GetFStringPropertyValue(InSpellBox->EntityId, TEXT("scriptID"));
		if (IsInBuffEntityVisibleCfg(ScriptID))
		{
			//如果是在BUFF可见性配置表中
			UBuffEntityVisibleManager* BuffEntityVisibleManager = UUECS3GameInstance::Instance->BuffEntityVisibleManager;
			if (IsValid(BuffEntityVisibleManager))
			{
				return BuffEntityVisibleManager->GetVisibleTypeByScriptID(ScriptID) == VISIBLE_TYPE::VISIBLE_TYPE_BUFF_TRUE;
			}
		}
		UVisibleManager* VisibleManager = UUECS3GameInstance::Instance->VisibleManager;
		if (IsValid(VisibleManager))
		{
			if (InSpellBox->HasFlag(ENTITY_FLAG::FLAG_CANT_SELECTED) || VisibleManager->GetModelVisibleStyle(InSpellBox) == VISIBLE_STYLE::VISIBLE_STYLE_FALSE)
			{
				return false;
			}
			else
			{
				return (ScriptID == TEXT("40001039") || ScriptID == TEXT("40000797"));
			}
		}
	}
	return false;
}

bool ACS3GameHUD::GetDropBoxPointVisible(ADropBoxCharacter* InDropBox)
{
	if (!IsValid(InDropBox)) return false;
	
	//判断DropBox在玩家客户端是否可见
	if (InDropBox->isVisible(uint64(UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("playerDBID")))))
	{
		int32 DisplayOnClient = UGolbalBPFunctionLibrary::GetIntPropertyValue(InDropBox->EntityId, TEXT("displayOnClient"));
		switch (DisplayOnClient)
		{
			case 0://默认不可见
			{
				return false;
				break;
			}
			case 1://可见
			{
				return true;
				break;
			}
			default:
				return false;
		}

	}
	return false;
}

bool ACS3GameHUD::GetActorPointXYHW(AActor* InActor, FVector2D TextureSize, float& ScreenX, float& ScreenY, float& ScreenW, float& ScreenH)
{
	if ( !IsValid(InActor)) return false;
	FVector ActorLocation = InActor->GetActorLocation();
	return GetPointXYHW(ActorLocation, TextureSize, ScreenX, ScreenY, ScreenW, ScreenH);
}

bool ACS3GameHUD::GetPointXYHW(FVector InPosition, FVector2D TextureSize, float& ScreenX, float& ScreenY, float& ScreenW, float& ScreenH)
{
	FVector2D ActorPos = (FVector2D(InPosition) - LevelOrign) / Rate;//Actor像素位置
	FVector2D tempDis = ActorPos - MiniMapViewOrigin;//Actor距离小地图可视原点的像素距离
	FVector2D tempPadding = tempDis * ZoomRate;
	if (tempPadding.X > TextureSize.X / 2 && tempPadding.X <(MiniMapViewSize.X - TextureSize.X / 2) && tempPadding.Y > TextureSize.Y / 2 && tempPadding.Y < (MiniMapViewSize.Y - TextureSize.Y / 2))
	{
		//绘制Actor点在游戏屏幕的像素位置
		ScreenX = ResX - (MiniMapUIPadding.X + MiniMapViewSize.X - tempPadding.X + TextureSize.X / 2) * DpiScale;
		ScreenY = (MiniMapUIPadding.Y + tempPadding.Y - TextureSize.X / 2) * DpiScale;
		ScreenW = TextureSize.X * DpiScale;
		ScreenH = TextureSize.Y * DpiScale;
		return true;
	}
	return false;
}

bool ACS3GameHUD::GetMinimapXYHW(float& ScreenX, float& ScreenY, float& ScreenW, float& ScreenH, float& TextureU, float& TextureV, float& TextureUWidth, float& TextureVHeight)
{
	ScreenX = ResX - (MiniMapUIPadding.X + MiniMapViewSize.X) * DpiScale;
	ScreenY = MiniMapUIPadding.Y * DpiScale;
	ScreenW = MiniMapViewSize.X * DpiScale;
	ScreenH = MiniMapViewSize.Y * DpiScale;
	TextureU = MiniMapViewOriginUV.X;
	TextureV = MiniMapViewOriginUV.Y;
	TextureUWidth = MiniMapViewSizeTarget.X / MiniMapUISize.X;
	TextureVHeight = MiniMapViewSizeTarget.Y / MiniMapUISize.Y ;
	return true;
}

void ACS3GameHUD::UpdateMiniMapTexture(const FString& InFileName)
{
	TWeakObjectPtr<ACS3GameHUD> DelayThisPtr(this);
	UGolbalBPFunctionLibrary::ImageLoader()->LoadMiniMapTexture(InFileName, FImageLoadCompleted::CreateLambda([DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			ACS3GameHUD* ThisPtr = DelayThisPtr.Get();
			if (IsValid(ThisPtr))
			{
				ThisPtr->MiniMapTexture = UGolbalBPFunctionLibrary::ImageLoader()->GetMiniMapTexture();
				ThisPtr->OnMiniMapLoadCompleted();
			}
		}
		UE_LOG(LogTemp, Error, TEXT("MiniMap Texture Load Completed."));
	}));
}

bool GetMonsterPointVisible_ResultCache::FindMonsterPointVisible(AMonsterCharacter& Monster, AServerCharacter& PlayerActor)
{
	SCOPE_CYCLE_COUNTER(STAT_FindMonsterPointVisible);
	if (bool* result1 = ResultCache_Map.Find(Monster.EntityId))
	{
		return *result1;
	}
	else
	{
		bool result2 = HUD.GetMonsterPointVisible(&Monster, &PlayerActor);
		ResultCache.Add(Monster.EntityId);
		ResultCache_Map.Add(Monster.EntityId, result2);
		return result2;
	}
}

void GetMonsterPointVisible_ResultCache::UpdateCache()
{
	SCOPE_CYCLE_COUNTER(STAT_UpdateCache);

	if (!IsValid(UUECS3GameInstance::Instance) && UUECS3GameInstance::pKBEApp == nullptr) return;

	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(PlayerActor)) return;

	bool isLoop = false;
	int32 NowUpdateCount = 0;
	int32 Length = ResultCache.Num();
	if (Length == 0) return;
	int32 i = (NowUpdateIndex + 1) % Length;
	
	for (; i < Length && NowUpdateCount < UpdateQuantity && !isLoop; ++i %= Length, ++NowUpdateCount)
	{
		if (i == NowUpdateIndex) isLoop = true;

		int32 entityId = ResultCache[i];
		auto entity = UGolbalBPFunctionLibrary::FindEntity(entityId);

		if (entity != nullptr && IsValid(entity->Actor()))
		{
			// 这里直接强转类型是因为流程上只会保存AMonsterCharacter
			ResultCache_Map[entityId] = HUD.GetMonsterPointVisible((AMonsterCharacter*)entity->Actor(), PlayerActor);
		}
		else
		{
			ResultCache.RemoveAt(i);
			ResultCache_Map.Remove(entityId);
			Length = ResultCache.Num();
			--i;
			if (i < 0)
			{
				i = 0;
				break;
			}
		}
	}
	NowUpdateIndex = i;
}

GetMonsterPointVisible_ResultCache::GetMonsterPointVisible_ResultCache(ACS3GameHUD& HUD) : HUD(HUD)
{
	ResultCache.Reserve(ExpectedSize);
	ResultCache_Map.Reserve(ExpectedSize);
}

CONTROL_COMPILE_OPTIMIZE_END