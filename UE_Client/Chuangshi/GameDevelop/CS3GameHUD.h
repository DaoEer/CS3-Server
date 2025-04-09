// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "GameData/BigMapData.h"
#include "Engine/Texture2D.h"
#include "Actor/NPC/NPCCharacter.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Actor/SpellBox/SpellBoxCharacter.h"
#include "Materials/MaterialInterface.h"
#include "GameData/QuestEntityVisibleData.h"
#include "GameData/BuffEntityVisibleData.h"
#include "Containers/CircularQueue.h"
#include "Engine/Canvas.h"
#include "Actor/DropBox/DropBoxCharacter.h"
#include "UObject/ConstructorHelpers.h"
#include "CS3GameHUD.generated.h"

/*
* 文件名称：CS3GameHUD.h
* 功能说明：
* 文件作者：liyuxia
* 目前维护：liyuxia
* 创建时间：2019-01-02
*/

DECLARE_STATS_GROUP(TEXT("ACS3GameHUD"), STATGROUP_ACS3GameHUD, STATCAT_Advanced);
DECLARE_STATS_GROUP(TEXT("GetMonsterPointVisible_ResultCache"), STATGROUP_GetMonsterPointVisible_ResultCache, STATCAT_Advanced);

class ACS3GameHUD;
class UFont;
struct FCanvasIcon;

struct DamageEffectInfo
{
	// 伤害效果动画参数
#define DamageEffect_FloatingSpeed 350.f			// 每秒上浮像素
#define DamageEffect_Duration 0.6f					// 效果持续时间
#define DamageEffect_StartTransparencyTime 0.3f		// 伤害效果出现多久后开始透明
#define DamageEffect_StartTransparencyDuration (DamageEffect_Duration - DamageEffect_StartTransparencyTime)

	enum EffectType : uint8
	{
		//普通NowInfo
		Common,
		//暴击
		Critical,
		// 闪避
		Dodge,
		//招架
		Parry,
		//本地玩家受到攻击
		LocalPlayerAreAttacked,
	};

	FVector ScreenPosition;
	int32 DamageValue;
	float AnimationTime = DamageEffect_Duration;
	EffectType Type;
};

struct SkillNameEffectInfo
{
	// 技能名称效果动画参数
#define SkillNameEffect_FloatingSpeed 150.f				// 每秒上浮像素
#define SkillNameEffect_StopFloatingTime 1.f			// 多少秒后停止上浮
#define SkillNameEffect_Duration 1.5f					// 效果持续时间

	enum EffectType : uint8
	{
		// 本地玩家释放的技能
		LocalPlayer,
		// 其他对象释放的技能
		Other,
	};

	FVector ScreenPosition;
	FText SkillName;
	float AnimationTime = SkillNameEffect_Duration;
	EffectType Type;
};

struct FightStateChangeEffectInfo
{
	// 进入/退出 战斗效果动画参数
#define FightStateChangeEffect_FloatingSpeed 200.f			// 每秒上浮像素
#define FightStateChangeEffect_Duration 1.f					// 效果持续时间

	enum EffectType : uint8
	{
		// 开始战斗
		Enter,
		// 离开战斗
		Leave,
	};

	FVector ScreenPosition;
	float AnimationTime = FightStateChangeEffect_Duration;
	EffectType Type;
};

// ACS3GameHUD::GetMonsterPointVisible在500个怪物的情况下消耗太高了,所以这里对结果缓存,会导致可见性查询的结果延迟 CST-9937
struct GetMonsterPointVisible_ResultCache
{
private:
	// Array用于分帧更新结果 [entityID, ...]
	TArray<int32> ResultCache;
	// Map用于查询
	TMap<int32, bool> ResultCache_Map;

	const int32 ExpectedSize = 1000;
	//每帧更新缓存数量
	const int32 UpdateQuantity = 10;

	ACS3GameHUD& HUD;

	int32 NowUpdateIndex = 0;

public:
	bool FindMonsterPointVisible(AMonsterCharacter& Monster, AServerCharacter& PlayerActor);

	void UpdateCache();

	GetMonsterPointVisible_ResultCache(ACS3GameHUD& HUD);
};

//线段结构体
USTRUCT(BlueprintType, Blueprintable)
struct CHUANGSHI_API FLineSegment
{
	GENERATED_USTRUCT_BODY();
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CS3GameHUD|MiniMap")
		FVector2D PointA = FVector2D(0.0, 0.0);
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CS3GameHUD|MiniMap")
		FVector2D PointB = FVector2D(0.0, 0.0);
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CS3GameHUD|MiniMap")
		int32 LineSate = 0;
};

UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API ACS3GameHUD : public AHUD
{
	GENERATED_BODY()

	friend struct GetMonsterPointVisible_ResultCache;
public:
	virtual void PreInitializeComponents() override;
	virtual void DrawHUD() override;
	//BlueprintCallable，设置小地图数据
	UFUNCTION(BlueprintCallable, Category = "CS3GameHUD|MiniMap")
		void SetMiniMapData();
	//设置小地图可视范围的默认缩放倍数
	void SetViewDefaultScale(float DefaultScale);
	//BlueprintCallable，计算小地图数据并设置变量
	UFUNCTION(BlueprintCallable, Category = "CS3GameHUD|MiniMap")
		void CalcMiniMapData();
	//BlueprintCallable，小地图放大
	UFUNCTION(BlueprintCallable, Category = "CS3GameHUD|MiniMap")
		void ZoomIn();
	//BlueprintCallable，小地图缩小
	UFUNCTION(BlueprintCallable, Category = "CS3GameHUD|MiniMap")
		void ZoomOut();
	
	//判断地图是否可放大缩小
	UFUNCTION(BlueprintPure, Category = "CS3GameHUD|MiniMap")
		bool CanZoomScale(bool IsZoomIn);

	/**
	*BlueprintPure,获得地图可放大缩小倍数（用于显示放大缩小按钮Tips，注意：和实际缩放尺寸是不一样的）
	*
	*@param	IsZoomIn True：放大，False：缩小
	*
	*@return 输出可放大缩小倍数
	*/
	UFUNCTION(BlueprintPure, Category = "CS3GameHUD|MiniMap")
		FString GetZoomScale(bool IsZoomIn);
	//获得小地图可视范围原点像素坐标
	UFUNCTION(BlueprintPure, Category = "CS3GameHUD|MiniMap")
	FVector2D GetMiniMapViewOrigin() { return MiniMapViewOrigin; };

	//绘制小地图纹理贴图
	UFUNCTION(BlueprintCallable, Category = "CS3GameHUD|MiniMap")
		void DrawMiniMapTexture();
	//绘制小地图纹理通过材质
	UFUNCTION(BlueprintCallable, Category = "CS3GameHUD|MiniMap")
		void DrawMiniMapMaterial(UMaterialInterface* InMaterial);
	//绘制所有Point
	UFUNCTION(BlueprintCallable, Category = "CS3GameHUD|MiniMap")
		void DrawPoint();
	//绘制连线
	UFUNCTION(BlueprintCallable, Category = "CS3GameHUD|MiniMap")
		void DrawLinkLine(const TArray<FVector2D>& LinkPoints);
	//绘制多线段
	UFUNCTION(BlueprintCallable, Category = "CS3GameHUD|MiniMap")
		void DrawLineSegments(const TArray<FLineSegment>& SegmentPoints);

	//小地图加载完成
	UFUNCTION(BlueprintImplementableEvent, Category = "CS3GameHUD|MiniMap")
		void OnMiniMapLoadCompleted();

private:
	//绘制玩家自己点的纹理贴图
	void DrawPlayerPoint(AServerCharacter* PlayerActor);
	//绘制Actor点的图片材质
	void DrawActorPointByTexture(AActor* InActor, UTexture2D* InTexture);
	//绘制Actor点的材质
	void DrawActorPointByMaterial(AActor* InActor, UMaterialInterface* InMaterial, FVector2D InSize);
	//绘制Character点的纹理贴图
	bool DrawCharacterPoint(AActor* EntityActor, AServerCharacter* PlayerActor);
	//绘制NPC点的纹理贴图
	bool DrawNPCPoint(AActor* EntityActor, AServerCharacter* PlayerActor);
	//绘制队友点的纹理贴图
	void DrawTeamMembersPoint();
	//绘制怪物点的纹理贴图
	bool DrawMonsterPoint(AActor* EntityActor, AServerCharacter* PlayerActor);
	//绘制SpellBox的纹理图片
	bool DrawSpellBoxPoint(AActor* EntityActor, AServerCharacter* PlayerActor);
	//绘制摄像机的朝向(暂时不需要显示预留方法)
	void DrawCameraPoint();
	//绘制DropBox的纹理图片
	bool DrawDropBoxPoint(AActor* EntityActor, AServerCharacter* PlayerActor);
	//entity脚本ID是否在任务可见性配置表中
	bool IsInQuestEntityVisibleCfg(const FString& scriptID);
	//entity脚本ID是否在BUFF可见性配置表中
	bool IsInBuffEntityVisibleCfg(const FString& scriptID);
	//entity脚本ID是否在英雄王座Entity标记图标配置表
	UTexture2D* IsYXWZSignCfg(const FString& scriptID, bool& OutIsFind);
	//获取NPC点的可见性
	bool GetNPCPointVisible(ANPCCharacter* InNPC);
	bool GetNPCVisible(ANPCCharacter* InNPC);
	//获取怪物点的可见性
	bool GetMonsterPointVisible(AMonsterCharacter* InMonster, AServerCharacter* PlayerActor);
	bool GetMonsterVisible(AMonsterCharacter* InMonster, AServerCharacter* PlayerActor);
	//获取SpellBox点的可见性
	bool GetSpellBoxPointVisible(ASpellBoxCharacter *InSpellBox);
	bool GetSpellBoxVisible(ASpellBoxCharacter *InSpellBox);
	//获取DropBox点的可见性
	bool GetDropBoxPointVisible(ADropBoxCharacter* InDropBox);
	//获取Actor点绘制的屏幕位置
	bool GetActorPointXYHW(AActor* InActor, FVector2D TextureSize, float& ScreenX, float& ScreenY, float& ScreenW, float& ScreenH);
	bool GetPointXYHW(FVector InPosition, FVector2D TextureSize, float& ScreenX, float& ScreenY, float& ScreenW, float& ScreenH);
	//获取小地图图片绘制的屏幕位置
	bool GetMinimapXYHW( float& ScreenX, float& ScreenY, float& ScreenW, float& ScreenH, float& TextureU, float& TextureV, float& TextureUWidth, float& TextureVHeight);
	void UpdateMiniMapTexture(const FString& InFileName);
	void DrawOneLine(FVector2D StartPoint, FVector2D EndPoint);

protected:
	virtual void BeginPlay() override;
	virtual void BeginDestroy() override;
private:
	//初始化设置数据
	void InitHUDDatas();
	//加载Root界面到视口中
	void AddRootUMG();
	//初始化相关配置表
	void InitConfigData();
	void ClearConfigDatas();

public:
	//贴图纹理(小地图切割后拼合的贴图（变量为指针，更新的时候不需重新设置变量，变量值会自动更新）)
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "CS3GameHUD|MiniMap", DisplayName = "MiniMapTexture")
		UTexture2D* MiniMapTexture;
	//关卡名
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "CS3GameHUD|MiniMap", DisplayName = "LevelName")
		FString LevelName;
	//地图实际关卡尺寸（单位：厘米）
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "CS3GameHUD|MiniMap", DisplayName = "LevelSize")
		FVector2D LevelSize;
	//关卡的原点坐标（单位：厘米）
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "CS3GameHUD|MiniMap", DisplayName = "LevelOrign")
		FVector2D LevelOrign;
	//地图实际图片的纹理尺寸（单位：像素）
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "CS3GameHUD|MiniMap", DisplayName = "MiniMapUISize")
		FVector2D MiniMapUISize;
	//是否显示小地图
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "CS3GameHUD|MiniMap", DisplayName = "IsShowMiniMap")
		bool IsShowMiniMap;
	//地图实际尺寸除以地图纹理尺寸的比例（Rate=LevelSize/MiniMapUISize）
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "CS3GameHUD|MiniMap", DisplayName = "Rate")
		float Rate = 1.0;
	//小地图可视尺寸（像素）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CS3GameHUD|MiniMap|ReadWrite", DisplayName = "MiniMapViewSize")
		FVector2D MiniMapViewSize = FVector2D(230.0, 215.0);
	//缩放比例
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CS3GameHUD|MiniMap", DisplayName = "ZoomRate")
		float ZoomRate = 1.0;
	//屏幕X尺寸（像素）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CS3GameHUD|MiniMap", DisplayName = "ResX")
		float ResX;
	//屏幕Y尺寸（像素）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CS3GameHUD|MiniMap", DisplayName = "ResY")
		float ResY;
	//小地图生成的位置与屏幕左上角的间距
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CS3GameHUD|MiniMap|ReadWrite", DisplayName = "MiniMapUIPadding")
		FVector2D MiniMapUIPadding = FVector2D(3.0, 45.0);
	//玩家点的纹理图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CS3GameHUD|MiniMap|ReadWrite", DisplayName = "PlayerPoint")
		TSoftObjectPtr<UTexture2D> PlayerPoint;
	//怪物、NPC 非敌对点的纹理图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CS3GameHUD|MiniMap|ReadWrite", DisplayName = "GreenPoint")
		TSoftObjectPtr<UTexture2D> GreenPoint;
	//怪物、NPC 敌对点的纹理图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CS3GameHUD|MiniMap|ReadWrite", DisplayName = "RedPoint")
		TSoftObjectPtr<UTexture2D> RedPoint;
	//怪物、NPC 非敌对点的动态图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CS3GameHUD|MiniMap|ReadWrite", DisplayName = "GreenMatPoint")
		TSoftObjectPtr<UMaterialInterface> GreenMatPoint;
	//怪物、NPC 敌对点的动态图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CS3GameHUD|MiniMap|ReadWrite", DisplayName = "RedMatPoint")
		TSoftObjectPtr<UMaterialInterface> RedMatPoint;
	//队友点的纹理图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CS3GameHUD|MiniMap|ReadWrite", DisplayName = "TeamMemberPoint")
		TSoftObjectPtr<UTexture2D> TeamMemberPoint;
	//摄像机角度的纹理图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CS3GameHUD|MiniMap|ReadWrite", DisplayName = "CameraRotationImg")
		TSoftObjectPtr<UTexture2D> CameraRotationImg;
	//掉落宝箱的纹理图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CS3GameHUD|MiniMap|ReadWrite", DisplayName = "DropBoxPoint")
		TSoftObjectPtr<UTexture2D> DropBoxPoint;

private:
	//小地图可视目标尺寸（像素）：用来做小地图放大缩小
	FVector2D MiniMapViewSizeTarget = FVector2D(230.0, 215.0);
	//地图图片上玩家的点的像素坐标
	FVector2D MiniMapPlayerPos;
	//地图图片上小地图可视范围的原点的像素坐标
	FVector2D MiniMapViewOrigin;
	//小地图可视范围的原点在MiniMapTexture上的UV坐标（0~1）
	FVector2D MiniMapViewOriginUV;
	//地图可视范围的默认缩放倍数
	float ViewDefaultScale = 1.0f;
	//最大放大倍数
	float MaxZoomScale = 2.0f;
	//最小缩小倍数
	float MinZoomScale = 0.5f;
	//每次缩放的增量
	float PerZoomRate = 0.1f;
	float DpiScale = 1.0;

	UPROPERTY()
		UTexture2D* PlayerPointIcon;
	UPROPERTY()
		UTexture2D* GreenPointIcon;
	UPROPERTY()
		UTexture2D* RedPointIcon;
	UPROPERTY()
		UMaterialInterface* GreenPointMat;
	UPROPERTY()
		UMaterialInterface* RedPointMat;
	UPROPERTY()
		UTexture2D* TeamMemberPointIcon;
	UPROPERTY()
		UTexture2D* CameraRotationIcon;
	UPROPERTY()
		UTexture2D* DropBoxPointIcon;
	UPROPERTY()
		UTexture2D* SpellBoxPointIcon;

	//使Entity可见性任务配置表数据
	TMap<FName, FQEV_CFG_ROW_DATA*> QuestEntityVisibleMap;
	//使Entity可见性BUFF配置表数据
	TMap<FName, FBEV_CFG_ROW_DATA*> BuffEntityVisibleMap;
	//英雄王座图标数据
	TMap<FName, FSIGN_ICON_DATA*> YXWZSignIconMap;

// 伤害浮动文字效果 ---------------------------------------------------------------------------------
private:
	static const uint32 MaxDamageEffectCount = 100;
	TArray<DamageEffectInfo, TInlineAllocator<MaxDamageEffectCount>> DamageEffectInfos_CircularArray;
	int32 NowAddIndex_DamageEffect = 0; //当前插入位置

	TArray<FCanvasIcon, TInlineAllocator<10>> DamageNumIcons_Common;
	TArray<FCanvasIcon, TInlineAllocator<10>> DamageNumIcons_Critical;
	TArray<FCanvasIcon, TInlineAllocator<10>> DamageNumIcons_LocalPlayerAreAttacked;
public:
	// 伤害效果图片字体表 普通
	UPROPERTY(EditDefaultsOnly, Category = "CS3GameHUD|DamageEffect")
	UDataTable* DamageNumIconsTable_Common;

	// 伤害效果图片字体表 暴击
	UPROPERTY(EditDefaultsOnly, Category = "CS3GameHUD|DamageEffect")
	UDataTable* DamageNumIconsTable_Critical;

	// 伤害效果图片字体表 本地玩家受到伤害
	UPROPERTY(EditDefaultsOnly, Category = "CS3GameHUD|DamageEffect")
	UDataTable* DamageNumIconsTable_LocalPlayerAreAttacked;

	// 闪避图片
	UPROPERTY(EditDefaultsOnly, Category = "CS3GameHUD|DamageEffect")
	UTexture2D* DodgeIcon;

	// 招架图片
	UPROPERTY(EditDefaultsOnly, Category = "CS3GameHUD|DamageEffect")
	UTexture2D* ParryIcon;

	UFUNCTION(BlueprintCallable, Category = "CS3GameHUD|DamageEffect")
		void AddDamageEffect(FVector WorldLocation, int32 DamageValue, bool IsCritical, bool IsParry, bool IsDodge, bool IsPlayer);

	UFUNCTION(BlueprintCallable, Category = "CS3GameHUD|DamageEffect")
		void DrawDamageEffect();
// --------------------------------------------------------------------------------------------------

// 技能名称文字效果 ---------------------------------------------------------------------------------
private:
	static const uint32 MaxSkillNameEffectCount = 50;
	TArray<SkillNameEffectInfo, TInlineAllocator<MaxSkillNameEffectCount>> SkillNameEffectInfos_CircularArray;
	int32 NowAddIndex_SkillNameEffect = 0; //当前插入位置
public:
	// 技能名称效果字体
	UPROPERTY(EditDefaultsOnly, Category = "CS3GameHUD|DamageEffect")
	UFont* SkillNameEffect_Font;

	UFUNCTION(BlueprintCallable, Category = "CS3GameHUD|DamageEffect")
	void AddSkillNameEffect(FVector WorldLocation, const FString& SkillName, bool IsLocalPlayer);

	UFUNCTION(BlueprintCallable, Category = "CS3GameHUD|DamageEffect")
	void DrawSkillNameEffect();
// --------------------------------------------------------------------------------------------------

// 战斗状态变化效果 ---------------------------------------------------------------------------------
private:
	FightStateChangeEffectInfo NowFightStateChangeEffectInfo;
public:
	// 战斗状态效果字体
	UPROPERTY(EditDefaultsOnly, Category = "CS3GameHUD|DamageEffect")
		UFont* FightStateChangeEffect_Font;

	UFUNCTION(BlueprintCallable, Category = "CS3GameHUD|DamageEffect")
		void AddFightStateChangeEffect(FVector WorldLocation, bool IsEnterFight);

	UFUNCTION(BlueprintCallable, Category = "CS3GameHUD|DamageEffect")
		void DrawFightStateChangeEffect();
// --------------------------------------------------------------------------------------------------

private:
	// GetMonsterPointVisible方法结果缓存
	GetMonsterPointVisible_ResultCache MonsterPointVisible_ResultCache{*this};
};
