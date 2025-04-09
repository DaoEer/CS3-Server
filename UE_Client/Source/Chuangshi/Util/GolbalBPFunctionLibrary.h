// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Kismet/BlueprintFunctionLibrary.h"
#include "Engine/Texture2D.h"
#include "Color.h"

#include "HorizonDialogueMsgTextBlock.h"
#include "KBEngine.h"

#include "GameData/KitbagTypeEnum.h"
#include "GameData/Item/CS3ItemData.h"
#include "GameData/Item/ItemBase.h"
#include "GameData/InputData.h"
#include "GameData/ConstData.h"
#include "GameData/ProfessionData.h"
#include "GameData/LevelHashMap.h"
#include "GameData/CharacterData.h"
#include "Manager/HeadManager.h"
#include "GameData/ChatData.h"
#include "Entity/Role/CS3PlayRole.h"
#include "Manager/QuickBarManager.h"
#include "GameData/UIConfigData.h"
#include "GolbalBPFunctionLibrary.generated.h"


/*
* 文件名称：GolbalBPFunctionLibrary.h
* 功能说明：全局公共方法类
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2016-09-08
*/

DECLARE_STATS_GROUP(TEXT("UGolbalBPFunctionLibrary"), STATGROUP_UGolbalBPFunctionLibrary, STATCAT_Advanced);

UCLASS(BlueprintType)
class CHUANGSHI_API UGolbalBPFunctionLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	static  int32 ModelTextNumber;

#pragma region	/** 获取游戏全局实例节点(Manager相关) */
	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UUECS3GameInstance* GameInstance();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UCfgManager* CfgManager();
	
	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UResourceManager* ResourceManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class ULoginManager* LoginManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class ULevelManager* LevelManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UActionManager* ActionManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UParticleManager* ParticleManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class AAudioManager* AudioManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class ULocalDataSaveManager* LocalDataSaveManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UCustomCursorManager* CustomCursorManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UMediaPlayerManager* MediaPlayerManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UGStoryManager* GStoryManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UMessageManager* MessageManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UMapManager* MapManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UQuestManager* QuestManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UGLoaderManager* GLoaderManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UVisibleManager* VisibleManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UGUIManager* GUIManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UUIFixerManager* UIFixerManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UUIDockManager* UIDockManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UGEventManager* GEventManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UGameplayEventManager* GameplayEventManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UTipsManager* TipsManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UEmoteManager* EmoteManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UDecalManager* DecalManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class USkillManager* SkillManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UForceManager* ForceManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UTutorialManager* TutorialManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UAutoFightMar* AutoFightMar();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UControllerModeMgr* ControllerModeMgr();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UOperationModeMgr* OperationModeMgr();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UTimeManager* TimeManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UCustomTimerManager* CustomTimerManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UModifyFaceManager* ModifyFaceManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class AHeadManager* HeadManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UQuickBarManager* QuickBarManager();

	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UImageLoader* ImageLoader();

  	UFUNCTION(BlueprintPure, Category = "Golbal")
	static class UMotionBlurManager* MotionBlurManager();

	///<获取相应interface(id默认为0 即返回玩家的interface)
	UFUNCTION(BlueprintPure, Category = "cs3")
		static class UCS3EntityInterface* GetInterfaceByName(const FString& name, int32 id = 0);

#pragma endregion

#pragma region	/** 角色相关 */
	///<获取玩家ID
	UFUNCTION(BlueprintPure, Category = "cs3player")
		static int GetPlayerID();
	UFUNCTION(BlueprintPure, Category = "cs3player")
		static int GetPlayerPropertyInt(const FString& pName );
	UFUNCTION(BlueprintPure, Category = "cs3player")
		static float GetPlayerPropertyFloat(const FString& pName);
	//UFUNCTION(BlueprintPure, Category = "cs3player")
	static double GetPlayerPropertyDouble(const FString& pName);
	UFUNCTION(BlueprintPure, Category = "cs3player")
		static FString GetPlayerPropertyString(const FString& pName);

	UFUNCTION(BlueprintPure, Category = "cs3player")
		static int32 GetPlayerCamp();
	UFUNCTION(BlueprintPure, Category = "cs3player")
		static int32 GetPlayerGender();
	UFUNCTION(BlueprintPure, Category = "cs3player")
		static int64 GetPlayerMoney();
	UFUNCTION(BlueprintPure, Category = "cs3player")
		static int32 GetPlayerPotential();
	UFUNCTION(BlueprintPure, Category = "cs3player")
		static FString GetPlayerName();
	UFUNCTION(BlueprintPure, Category = "cs3player")
		static int32 GetPlayerProfession();
	UFUNCTION(BlueprintPure, Category = "cs3player")
		static int32 GetPlayerState();
	UFUNCTION(BlueprintPure, Category = "cs3player")
		static int32 GetPlayerLevel();

	static uint64 GetPlayerPlayerDBID();

	///<获取选中的目标对象EntityID
	UFUNCTION(BlueprintPure, Category = "cs3")
		static int GetTargetEntityID();

	UFUNCTION(BlueprintCallable, Category = "cs3")
		static void SetTargetEntity(const AActor* targetActor);
	
	///<单独对所需要的模型数据进行加载，与外观组件无关,该方法为只需要加载单个动作所处理，可以节省许多无关资源的加载导致的卡顿
	UFUNCTION(BlueprintCallable, Category = "Golbal|Model")
		static void CS3SetModelPart(class AGameCharacter* Actor, FString ModelID);

	///<播放对应的动作
	UFUNCTION(BlueprintCallable, Category = "Golbal|Model")
		static void CS3PlayModelAction(class AGameCharacter* Target, FString ModelID, FString ActionID);

	UFUNCTION(BlueprintCallable, Category = "Golbal|Model")
		static void SetModelonLand(const UObject* Object, UCapsuleComponent* CapsuleComp, float ModelScale, float CheckHeight);

	///<恢复Entity朝向为服务器朝向
	UFUNCTION(BlueprintCallable, Category = "Golbal")
		static void RecoverEntityRotator(const int32& EntityID);

	UFUNCTION(BlueprintCallable, Category = "Golbal | StrToUClass")
		static UClass* GetUClassByStr(const FString& Str);

	///<得到人物控制器
	UFUNCTION(BlueprintPure, Category = "Golbal")
		static class ACS3PlayerController* GetCS3PlayerController();

	///<得到人物
	UFUNCTION(BlueprintPure, Category = "Golbal")
		static class AServerCharacter* GetCS3PlayerCharacter();

	///<得到玩家Entity
		static class GameObject* GetCS3PlayerEntity();

	UFUNCTION(BlueprintPure, Category = "Actor")
		static 	AActor* GetActorByID(const int32& EntityID);

	///<获取与EntityID关系类型
	UFUNCTION(BlueprintPure, Category = "Golbal")
		static COMBAT_RELATION QueryRelationByEntityID(const int32& EntityID, const int32& TargetID);

	UFUNCTION(BlueprintCallable, Category = "CS3")
		static void SetModelTextNumber(int32 modenumber);

	UFUNCTION(BlueprintPure, Category = "CS3")
		static int32 GetModelTextNumber();

	UFUNCTION(BlueprintPure, Category = "Entity")
		static FString GetEntityPropertyValue(const int32& entityid, const FString& propname);

	UFUNCTION(BlueprintPure, Category = "Entity")
		static int32 GetIntPropertyValue(const int32& entityid, const FString& propname);

	UFUNCTION(BlueprintPure, Category = "Entity")
		static float GetFloatPropertyValue(const int32& entityid, const FString& propname);

	///<蓝图不支持double类型，此文件不提供蓝图版
	//UFUNCTION(BlueprintPure, Category = "Entity")
	static double GetDoublePropertyValue(const int32& entityid, const FString& propname);

	UFUNCTION(BlueprintPure, Category = "Entity")
		static FString GetFStringPropertyValue(const int32& entityid, const FString& propname);

	static KBEngine::Entity* FindEntity(const int32& entityid);

	UFUNCTION(BlueprintCallable, Category = "cs3")
		static void GetAllActorsOfClassExt(TSubclassOf<AActor> ActorClass, TArray<AActor*>& outActor);

	/**
	*BlueprintPure,修改摄像机臂长
	*
	*@param SpringArm 摄像机臂长组件
	*@param LengthValue 摄像机臂长
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3 | CameraControl")
		static void SetCameraTargetArmLength(class USpringArmComponent* SpringArm, float LengthValue,bool bForce=false);

	/**	
	*BlueprintCallable,修改摄像机偏移量
	*
	*@param	SpringArm 摄像机臂长组件
	*@param	OffsetValue 摄像机偏移量
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3 | CameraControl")
		static void SetCameraSocketOffset(class USpringArmComponent* SpringArm, FVector OffsetValue);

	/**
	*BlueprintCallable,修改摄像机FOV
	*
	*@param	CameraComponent 摄像机组件
	*@param	Fov FOV值
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3 | CameraControl")
		static void SetCameraFOV(UCameraComponent* CameraComponent, float Fov);
	//将Actor从摄像机剔除不渲染
	UFUNCTION(BlueprintCallable, Category = "HeadProxyCharacter")
		static void AddCameraHiddenActor(AActor* InActor);

	/**
	*BlueprintPure,根据阵营和职业获取门派信息数据
	*
	*@param CampType 阵营
	*@param ProfessionType 品质
	*
	*@return UTexture2D
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal|UTexture2D")
		static FProfessionData GetPlayerSchoolData(int32 CampType, int32 ProfessionType);

	/**
	*BlueprintPure,获取怪物周围玩家
	*
	*@param Class 类型(UClass*)
	*@param Range 距离(float)
	*@param Pos 位置(FVector)
	*
	*@return TArray<AActor*>
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal")
		static TArray<AActor*> GetPlayersInRange(UClass* Class = nullptr, float Range = 200.0f, FVector Pos = FVector::ZeroVector);

	/**
	*BlueprintPure，创建纯客户端角色(创建幻莲天池的鱼)
	*
	*@param ModelID 模型ID
	*@param BPName 
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal | HorizonPlugin")
		static AClientGameCharacter* CreateClientGameCharacter(FString ModelID, FString BPName);

	UFUNCTION(BlueprintCallable, Category = "Global")
		static class AActor* BeginDeferredActorSpawnFromClass(TSubclassOf<AActor> ActorClass, const FTransform& SpawnTransform, ESpawnActorCollisionHandlingMethod CollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn, AActor* Owner = nullptr);

	UFUNCTION(BlueprintCallable, Category = "Global")
		static class AActor* FinishSpawningActor(AActor* Actor, const FTransform& SpawnTransform);

	UFUNCTION(BlueprintCallable, meta = (WorldContext = "WorldContextObject"), Category = "Golbal")
		static AActor* SpawnActorByConfig(UObject* WorldContextObject, const FString& ActorStr);

	/**
	*BlueprintCallable,设置Actor及其SceneComp组件显示或隐藏
	*
	*@param	Actor 对象,默认绑定的子对象状态一样
	*@param	CompClass 组件类(例:UWidgetComponent::StaticClass())
	*@param	bShowActor 对象状态(True:显示,False:隐藏)
	*@param	bShowComp 组件状态(True:显示,False:隐藏)
	*
	*return void
	*/
	UFUNCTION(BlueprintCallable, Category = "Actor|Rendering")
		static void SetActorAndCompVisibility(AActor* Actor, TSubclassOf<USceneComponent> CompClass, bool bShowActor = false, bool bShowComp = false);

	UFUNCTION(BlueprintCallable, Category = "Actor|Rendering")
		static void SetComponentsVisiable(AActor* Actor, TSubclassOf<USceneComponent> CompClass, const bool& Visiable);

	//创建Actor
	template< class T >
	static T* SpawnActor(UClass* InClass, const FVector Location = FVector(0, 0, 0), const FRotator Ratation = FRotator(0, 0, 0))
	{
		UUECS3GameInstance* CurInstance = UUECS3GameInstance::Instance;
		if (IsValid(CurInstance) && IsValid(CurInstance->GetWorld()))
		{
			FActorSpawnParameters SpawnParameters;
			SpawnParameters.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			return CurInstance->GetWorld()->SpawnActor<T>(InClass, Location, Ratation, SpawnParameters);
		}

		return nullptr;
	}
	//创建Actor
	template< class T >
	static T* SpawnActor(UClass* InClass, const FTransform Transform)
	{
		UUECS3GameInstance* CurInstance = UUECS3GameInstance::Instance;
		if (IsValid(CurInstance) && IsValid(CurInstance->GetWorld()))
		{
			FActorSpawnParameters SpawnParameters;
			SpawnParameters.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			return CurInstance->GetWorld()->SpawnActor<T>(InClass, Transform, SpawnParameters);
		}

		return nullptr;
	}

	template< class T >
	static T* SpawnActor()
	{
		UUECS3GameInstance* CurInstance = UUECS3GameInstance::Instance;
		if (IsValid(CurInstance) && IsValid(CurInstance->GetWorld()))
		{
			FActorSpawnParameters SpawnParameters;
			SpawnParameters.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			return CurInstance->GetWorld()->SpawnActor<T>(SpawnParameters);
		}

		return nullptr;
	}

#pragma endregion

#pragma region	/** 技能相关 */
	/**
	*BlueprintPure，玩家是否有施法辅助
	*
	* @return bool
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal | player")
		static bool GetSkillAssistUI();

	/**
	*BlueprintPure，通过技能ID获取技能图标
	*
	*@param SkillId 技能ID
	*
	*@return UTexture2D* 技能图标
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal")
		static UTexture2D* GetIconBySkillID(int32 SkillId);

	/**
	*BlueprintPure,过技能ID获取技能描述
	*
	* @param SkillId 技能ID
	*
	* @return FString 技能描述
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal")
		static FString GetDescriptionBySkillID(int32 SkillId);

	/**
	*BlueprintPure,通过技能ID获取技能中文名称
	*
	* @param SkillId 技能ID
	*
	* @return FString 技能名称
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal")
		static FString GetNameBySkillID(int32 SkillId);

	/**
	*GetNPCPositionFromTable,根据目标地图和NPC的ScriptID获取NPC位置
	*
	* @param FString DstSpaceName	目标地图
	* @param FString NPCScriptID	NPC的ScriptID
	* @param FVector & NPCPosition	最终得到的NPC位置
	*
	* @return bool
	*/
	UFUNCTION(BlueprintPure, Category = "Player")
		static bool GetNPCPositionFromTable(FString DstSpaceName, FString NPCScriptID, FVector& NPCPosition);

	/**
	*BlueprintPure,根据NPC的ScriptID获取NPC位置
	*
	* @param FString DstSpaceName	目标地图
	* @param FString NPCScriptID	NPC的ScriptID
	* @param FVector & NPCPosition	最终得到的NPC位置
	*
	* @return bool
	*/
	UFUNCTION(BlueprintPure, Category = "Player")
		static bool GetNPCPositionFromTableWithNPCScriptID(FString NPCScriptID, FString& spaceScriptID, FVector& NPCPosition);

#pragma endregion

#pragma region	/** 范围判断 */
	/**  
	*BlueprintCallable,扇形范围判断
	*
	*/

	UFUNCTION(BlueprintCallable, Category = "Role")
		static bool IsPositionInSectorRange(FVector InPos, FVector InSectorPos, FVector InSectorForwadDir, float InSectorAngle, float InSectorDistance, float InSectorHeight);

	/**	
	*BlueprintPure,获取两点之间的面向朝向
	*
	*@param	StartLocation 起始位置
	*@param	TargetLocation 目标位置
	*
	*@return FRotator 面向朝向
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal")
		static FRotator GetLookAtRotator(const FVector& StartLocation, const FVector& TargetLocation);

	/**  
	*BlueprintCallable,Actor排序方法
	*
	*@param	Array 需要排序的Actor数组
	*@param	Actor 使用此方法的Actor自身
	*
	*return void
	*/
	UFUNCTION(BlueprintCallable, Category = "Role")
	static void SortActorByDistance(const TArray<AActor*> &  Array, AActor* Actor);

	///<字典排序升序方法，按照Int；
	UFUNCTION(BlueprintCallable, Category = "Golbal | Int32")
		static TMap<int32, AActor*> LessTmap(TMap<int32, AActor*> Listmap);

	UFUNCTION(BlueprintPure, Category = "Golbal | Actor")
		static float GetActorDistance(AActor* SrcActor, AActor* DstActor);

	///<跳跃中获取距离(忽略Z轴)
	UFUNCTION(BlueprintPure, Category = "Golbal | Actor")
		static float GetActorDistanceByJump(AActor* SrcActor, AActor* DstActor);

	UFUNCTION(BlueprintPure, Category = "Golbal")
		static FVector Unreal2KBEnginePosition(const FVector& unrealPoint) { return KBEngine::KBEMath::Unreal2KBEnginePosition(unrealPoint); }

	UFUNCTION(BlueprintPure, Category = "Golbal")
		static FVector KBEngine2UnrealPosition(const FVector& kbenginePoint) { return KBEngine::KBEMath::KBEngine2UnrealPosition(kbenginePoint); }

	/**
	*BlueprintPure, 获取玩家周围Actors
	*
	*@param Class 类型(UClass*)
	*@param Range 距离(float)
	*@param Pos 位置(FVector)
	*
	*@return TArray<AActor*>
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal")
		static TArray<AActor*> GetActorsInRange(UClass* Class = nullptr, float Range = 200.0f, FVector Pos = FVector::ZeroVector, bool IsSort = false);

	/**
	*BlueprintPure, 获取玩家周围Entity,不限高度
	*
	*@param ClassName 类名
	*@param Range 距离(float)
	*@param Pos 位置(FVector)
	*
	*@return TArray<AActor*>
	*/
	static TArray<CS3Entity*> GetCS3EntitysInRange(FString ClassName = "", float Range = 200.0f, FVector Pos = FVector::ZeroVector);

	/**
	*BlueprintPure, 判断是否在矩形内
	*
	*@param dstPos 目标位置(FVector)
	*@param srcPos 自己位置(FVector)
	*@param yaw 偏航角(float)
	*@param length 长(float)
	*@param width 宽(float)
	*
	*@return TArray<AActor*>
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal")
		static bool IsInRectangle(FVector dstPos, FVector srcPos, float yaw, float width, float length);

	/**
	*BlueprintPure, 判断是否在扇形内
	*
	*@param dstPos 目标位置(FVector)
	*@param srcPos 自己位置(FVector)
	*@param yaw 偏航角(float)
	*@param radius 半径(float)
	*@param angle 角度(float)
	*
	*@return TArray<AActor*>
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal")
		static bool IsInSector(FVector dstPos, FVector srcPos, float yaw, float radius, float angle);

	///<获取spaceData
	UFUNCTION(BlueprintPure, Category = "Role")
		static const FString& GetSpaceData(const FString& key);

#pragma endregion

#pragma region	/** 字符串功能相关 */
	/** 
	*BlueprintCallable,FString字符串拆分
	*
	*@param	InString 需要拆分字符串
	*@param	IsElemUnique 是否保持分割出来数组元素唯一
	*@param	SplitChar 分隔符号
	*
	*@return TArray<FString> 引擎提供类似方法ParseIntoArray
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal | FString | Split")
		static TArray<FString> SplitString(const FString& InString, bool IsElemUnique = false, FString SplitChar = TEXT("|"));

	///<类型
	static FString TypeValidation(const FString InString);

	UFUNCTION(BlueprintPure, Category = "Chinese")
		static FString GetChinese(const FString& rowname);

	///<解析位面光墙传入的坐标字符串
	UFUNCTION(BlueprintCallable, Category = "FSrting|ResolveVector")
		static TArray<FVector> ConvertStringToVectors(const FString& VectorString);

	///<判断字符数组是否包含字符串,包含返回True
	UFUNCTION(BlueprintPure, Category = "Golbal | FString | Compare")
		static bool IsContainStr(const FString Str, const TArray<FString> Array);

	///<比较字符串的大小（大于）
	UFUNCTION(BlueprintPure, meta = (DisplayName = "String > String", CompactNodeTitle = ">", Keywords = "Compare String Greater"), Category = Game)
		static bool SGreaterThan(FString StringA, FString StringB);

	///<比较字符串的大小（小于）
	UFUNCTION(BlueprintPure, meta = (DisplayName = "String < String", CompactNodeTitle = "<", Keywords = "Compare String Less"), Category = Game)
		static bool SLessThan(FString StringA, FString StringB);

	UFUNCTION(BlueprintPure, Category = "cs3")
		static TArray<FString> IntListToStringList(const TArray<int32>& intlist);

	UFUNCTION(BlueprintPure, Category = "cs3")
		static TArray<int32> StringListToIntList(const TArray<FString>& strlist);

	UFUNCTION(BlueprintPure, Category = "cs3")
		static TArray<FString> FloatListToStringList(const TArray<float>& floatlist);

	/**
	*BlueprintPure,字符串长度大于某个数值时后面用省略号代替
	*
	*@param SourceString 原字符串
	*@param Length	显示长度
	*
	*@return FString 返回替换后的字符串
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal | FString")
		static FString GetEllipsisString(const FString& SourceString, int32 Length);

	/**
	*BlueprintPure,获取有效的文本
	*
	*@param InputText	输入的文本
	*@param LimitedLen	字符数量限制
	*@param IsBlankInputValid
	*
	*@return FString
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal | FString |Input")
		static FString GetValidInputTxt(FString InputText, int32 LimitedLen, bool IsBlankInputValid);

	/**
	*BlueprintPure,文本输入是否有效输入（内部已弹出提示）
	*
	*@param InputText	输入的文本
	*@param InputTextName	输入的文本名称（用于消息提示显示）
	*@param MinLen	字符最少数量限制， =0表示不限制字数
	*@param MaxLen	字符最多数量限制， =0表示不限制字数
	*@param IsAllChinese	是否限制全汉字
	*@param IsShield	是否限制屏蔽字
	*
	*@return FString
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal | FString |Input")
		static bool IsValidInputText(FString InputText, FString InputTextName, int32 MinLen = 0, int32 MaxLen = 0, bool IsAllChinese = false, bool IsShield = true);

	/**
	*BlueprintPure,文本输入是否超过字数限制
	*
	*@param InputText	输入的文本
	*@param LimitedLen	字符数量限制
	*
	*@return FString
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal | FString |Input")
		static bool IsOverLimitInputText(FString InputText, int32 LimitedLen);

	/**
	*BlueprintPure,文本输入是否少于字数限制
	*
	*@param InputText	输入的文本
	*@param LimitedLen	字符数量限制
	*
	*@return FString
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal | FString |Input")
		static bool IsLessLimitInputText(FString InputText, int32 LimitedLen);

	/**
	*BlueprintPure,替换换行符（输入文本不允许换行）
	*
	*@param InStr	输入的字符串
	*
	*@return FString
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal | FString |Input")
		static FString ReplaceLineBreak(const FString& InStr);


	/**
	*BlueprintPure,判断一个字符串是否包含另一个字符串中的所有元素
	* 
	*@param FString& source 源字符串
	*@param FString& target 目标字符串
	*
	*@return bool
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal | FString")
		static bool StringContains(const FString& source, const FString& target);

	/**
	*BlueprintPure,根据新旧String对比刷新当前的字符串
	* 
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal | FString")
		static void RefreshHLString(const FString& CurStr,FString OldStr, const TArray<FString> RichTextStrs, const TArray<int32> RichTextIndex, const TArray<FString> InputBoxTextStrs, FChatHyperlinkData& ChatHyperlinkData);
		
	/**
	*BlueprintPure,制作超链接字符串
	*
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal | FString")
		static void MakeHLString(const FString& CurStr, FString& ResultStr, const TArray<FString> RichTextStrs, const TArray<int32> RichTextIndex, const TArray<FString> InputBoxTextStrs);

	/**
	*BlueprintPure，将FString转换成FVector.
	*  
	*@param FString PosStr
	*
	*@return FVector
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal | FString ")
		static FVector FStringToFVector(FString PosStr);

	/**
	*BlueprintPure,获得有效的数字输入字符串
	*
	*@param	SourceString 原字符串
	*@param	InMinValue 最小输入值
	*@param	InMaxValue 最大输入值
	*
	* @return 有效的输入字符串
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal | FString |Input")
		static FString GetValidNumericInput(const FString& SourceString, int32 InMinValue = 0, int32 InMaxValue = 100);

	/**
	*BlueprintCallable,字符串替换
	*
	*@param	replaceString 原字符串
	*@param	args			替换参数
	*@param	SplitChar		可选分隔符，默认“|”
	*
	*@return FString 替换后的字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal | FString")
		static FString GetReplaceString(const FString& replaceString, const FString args = TEXT(""), FString SplitChar = TEXT("|"));


	/**
	*BlueprintCallable,int64类型转String类型
	*
	*@param	moneyValue int64类型的值
	*
	*@return FString 转换后的字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal | FString")
		static FString Int64ToString(int64 moneyValue);


	/**
	*BlueprintCallable,String类型转int64类型
	*
	*@param	moneyValue 字符串
	*
	*@return FString int64类型的值
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal | FString")
		static int64 StringToInt64(const FString& moneyValue);

	/**
	*BlueprintCallable,获取字符串字节数
	*
	*@param	replaceString 原字符串
	*
	*@return int32
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal | FString")
		static int32 GetStringBytes(const FString& SourceString);

	/**
	*BlueprintCallable,判断字符串是否只包含ASCII码,只含有ASCII码返回True，含有中文返回False
	*
	*@param	replaceString 原字符串
	*
	*@return bool
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal|String")
		static bool IsPureAnsi(const FString& SourceString);

	/**
	*BlueprintCallable,按插件格式化字符串
	*
	*@param inputstr 要格式化的字符串
	*@param colorstr 字体颜色
	*
	*@return FString 按插件格式化后的字符串
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal | FString")
		static FString StrToColorStr(const FString& inputstr, const FString& colorstr = TEXT("FFFFFFFF"));

	UFUNCTION(BlueprintPure, Category = "Global")
		static bool IsAllChineseChar(FString MsgText);

	/**
	*BlueprintCallable,判断字符串是否是纯数字（用于输入金钱等，IsNumeric()方法包含了.-符号）
	*
	*@param	SourceString 原字符串
	*
	*@return bool
	*/
	UFUNCTION(BlueprintPure, Category = "Global")
		static bool IsDigit(FString SourceString);

	/**
	*FLinearColor值转为十六进制字符串
	*
	*@return 十六进制字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "Global")
		static FString ConvertLinearColorToHex(FLinearColor InLinearColor);

#pragma endregion

#pragma region	/** 富文本功能相关 */
	/**
	*BlueprintCallable,设置富文本（商城）内容，可配置转义文本
	*
	*@return void
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal | HorizonPlugin")
		static void SetText(const FText& newText, UHorizonDialogueMsgTextBlock* pDialogueWidget);

	///<金钱转化为带图标字符串，格式：@F{fc=(230, 227, 185, 255)}99999@I{p=A5}@F{fc=(230, 227, 185, 255)}99@I{p=A4}@F{fc=(230, 227, 185, 255)}99@I{p=A3}
	UFUNCTION(BlueprintCallable, Category = "CS3 | Money")
		static FString GetRichTextMoney(int64 moneyValue, const FString& colorstr = TEXT("FFFFFFFF"), bool IsBindMoney = false);

	/**
	*BlueprintPure,处理FString的换行
	*
	*@param Line 
	*
	*@return 
	*/
	static FString& HandleLineFeeds(FString& Line);

	/**
	*BlueprintPure,设置字体样式
	*
	*@return FString
	*
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal")
		static FString SetFontStyle(const FString& FontPath, const FString& FontType, const FString& FontSize, const FString& Color, const FString& ShadowColor, const FString& ShadowOffset);

	/**
	*BlueprintCallable,单独提取静态图片格式，形如 <img filePath="Texture2D'/Game/Item/I_C_Strawberry.I_C_Strawberry'" size="[100, 100]" />
	*
	*@param	replaceString 原字符串
	*@param	ColorStr RGBA值
	*
	*@return FString 替换后的字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal | FString")
		static FString GetFormatImgStr(const FString& ImgMessage, const FString& ColorStr);

	/**
	*BlueprintCallable,格式化聊天窗口信息
	*
	*@param	replaceString 原字符串
	*@param	ColorStr RGBA值
	*
	*@return FString 替换后的字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal | FString")
		static FString GetChatMsgColorString(const FString& MsgStr, const FString& ColorStr);

	/**
	*BlueprintCallable,获得一个字典结构的Value值，Value是整型 比如：SrcString="{"money":99,"tongContribute":100}"  Key="money",则返回值是99，没找到则返回-1
	*
	*@param	SrcString	字典结构字符串
	*@param	Key			字典Key值
	*
	*@return int32 返回字典的Value值，整型，没有找到则返回-1
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal | FString")
		static int32 GetIntegerFieldByKey(const FString& SrcString, const FString& Key);

	/**
	*BlueprintCallable,消息字符串替换为富文本，比如：参数1{0}参数2{1}  变成 <text color="#FFFFFFFF">参数1</text >{0}<text color="#FFFFFFFF">参数2</text >{1}
	*
	*@param	replaceString 原字符串
	*
	*@return FString 替换后的字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal | FString")
		static FString GetFormatColorString(const FString& replaceString);

	///<将转义符格式富文本字符串替换为普通字符串
	UFUNCTION(BlueprintCallable, Category = "Golbal | FString")
		static FString ConvertRichTextToCommonText(FString InRichText);

#pragma endregion

	/**
	*BlueprintCallable,获取百分比文本
	*
	*@param InCurValue 当前值
	*@param InMaxValue 最大值
	*
	*@return FText
	*/
	UFUNCTION(BlueprintPure, meta = (DisplayName = "GetPercent", AdvancedDisplay = "2"), Category = "Golbal | Math")
	static FText GetPercent(int32 InCurValue, int32 InMaxValue );

	/**
	*BlueprintPure,获取血条当前阶段及当前阶段进度条的百分比
	*
	*@param	InCurHP 当前血量
	*@param	InMaxHP 最大血量
	*@param DefaultBloodNum 默认的配置阶段数量
	*@param OnProgressPercent 当前阶段下进度条的百分比(返回值)
	*
	*@return int32 当前血条阶段
	*
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal | Math | HP")
	static int32 GetBloodStage(float& OnProgressPercent, int32 InCurHP, int32 InMaxHP, int32 DefaultBloodNum = 1);

	/**
	*BlueprintCallable,将Vector2D数组转换为Vector3D数组
	*
	*@param Target
	*
	*@return TArray<FVector>
	*/
	UFUNCTION(BlueprintCallable, Category = "Vector2D|ConvertFVector2DToFVector")
		static TArray<FVector> ConvertFVector2DToFVector(const TArray<FVector2D>& Target);

	
#pragma region	/** 通信相关 */
	UFUNCTION(BlueprintCallable, Category = "cs3")
	static void CellCall(int EntityID, const FString &methodname, const TArray<FString> &arguments);

	UFUNCTION(BlueprintCallable, Category = "cs3")
	static void CellCallWithIntList(int EntityID, const FString &methodname, const TArray<int32> &arguments);

	UFUNCTION(BlueprintCallable, Category = "cs3")
	static void CellCallWithFStringList(int EntityID, const FString &methodname, const TArray<FString> &arguments);


	UFUNCTION(BlueprintCallable, Category = "cs3")
	static void BaseCall(int EntityID, const FString &methodname, const TArray<FString> &arguments);

	UFUNCTION(BlueprintCallable, Category = "cs3")
	static void BaseCallWithIntList(int EntityID, const FString &methodname, const TArray<int32> &arguments);

	UFUNCTION(BlueprintCallable, Category = "cs3")
	static void BaseCallWithFStringList(int EntityID, const FString &methodname, const TArray<FString> &arguments);


	static FVariant ListToFVariant(const TArray<int32>& intlist);
	static FVariant ListToFVariant(const TArray<FString>& stringlist);

	UFUNCTION(BlueprintCallable, Category = "cs3")
	static void StatusMessage(const int32& statusID, const FString& args);

	///<判断World类型为Game类型
	UFUNCTION(BlueprintPure, Category = "CS3|World")
	static bool CheckWorldTypeIsGame();
	
	/**
	*BlueprintCallable,Set a timer to execute delegate. Setting an existing timer will reset that timer with updated parameters.
	*
	* @param Object		Object that implements the delegate function. Defaults to self (this blueprint)
	* @param Event			Event. Can be a K2 function or a Custom Event.
	* @param Time			How long to wait before executing the delegate, in seconds. Setting a timer to <= 0 seconds will clear it if it is set.
	* @param bLooping		True to keep executing the delegate every Time seconds, false to execute delegate only once.
	*
	* @return				The timer handle to pass to other timer functions to manipulate this timer.
	*/
	UFUNCTION(BlueprintCallable, meta = (DisplayName = "CS3 Set Timer by Event", DefaultToSelf = "Object"), Category = "Utilities|Time")
		static FTimerHandle SetTimerbyEvent(UPARAM(DisplayName = "Event")UObject* Object, FTimerDynamicDelegate Delegate, float Time, bool bLooping, bool bReset = true);
	/**
	* Set a timer to execute delegate. Setting an existing timer will reset that timer with updated parameters.
	*
	* @param Object		Object that implements the delegate function. Defaults to self (this blueprint)
	* @param FunctionName	Delegate function name. Can be a K2 function or a Custom Event.
	* @param Time			How long to wait before executing the delegate, in seconds. Setting a timer to <= 0 seconds will clear it if it is set.
	* @param bLooping		true to keep executing the delegate every Time seconds, false to execute delegate only once.
	*
	* @return				The timer handle to pass to other timer functions to manipulate this timer.
	*/
	UFUNCTION(BlueprintCallable, meta = (DisplayName = "CS3 Set Timer by Function Name", DefaultToSelf = "Object"), Category = "Utilities|Time")
		static FTimerHandle SetTimerbyFunctionName(UObject* Object, FString FunctionName, float Time, bool bLooping);

#pragma endregion

#pragma region	/** 鼠标、键盘输入设备相关 */
	/**
	*BlueprintPure, 获取鼠标点地位置(忽视AServerCharacter)
	*
	*@return FVector
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal")
		static FVector GetMouseWorldPos();

	///<根据FInputKeyEvent类型转换成 KeyString 给UI显示
	UFUNCTION(BlueprintPure, Category = "Input")
		static FString ConvertKeysToKeyString(FInputKeyEvent keys);

	///<根据Keys转换成 FGROUPKEY_DATA类型
	UFUNCTION(BlueprintPure, Category = "Input")
		static FGROUPKEY_DATA ConvertKeysToGroupKey(TArray<FKey>Keys);

	///<获得系统鼠标移动速度
	UFUNCTION(BlueprintPure, Category = "Global")
		static float GetMouseMoveSpeed();

#pragma endregion

	///<获取服务器IP配置
	UFUNCTION(BlueprintPure, Category = "KitBag")
		static FString GetServerIP();

#pragma region	/** 地图、导航相关 */
	/**
	*BlueprintPure,目标位置是否可寻路
	*
	*@param	GoalPos 目标位置(FVector)
	*
	*@return bool
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal")
		static bool FindPathToLocation(const FVector& GoalPos);
	
	/**
	* Gets current MainLevel LevelScriptActor
	*
	* @return LevelScriptActor
	*/
	static ALevelScriptActor* GetMainLevelActor();
	
	/**
	*BlueprintPure,获得自动寻路导航路径列表
	*
	*@param GuideDistance 每个路点相隔的距离
	*
	* @return 导航路径列表
	*/
	UFUNCTION(BlueprintPure, Category = "Player")
		static TArray<FVector> GetNavigateGuidPath(float GuideDistance = 300.0);

	/**
	*BlueprintPure,创建等间距像素点
	*
	*@param InPixelList 输入的像素点列表
	*@param PixelDistance 像素点间距
	*
	*@return 等间距像素点列表
	*/
	UFUNCTION(BlueprintPure, Category = "Map")
		static TArray<FVector2D> CreateSameIntervalPixels(const TArray<FVector2D>& InPixelList, float PixelDistance = 8.0);

	/**
	*BlueprintPure,获得屏幕的缩放比例
	*
	*@return float
	*/
	UFUNCTION(BlueprintPure, Category = "Screen")
		static float GetViewportScale();

	/**
	*BlueprintPure,获得屏幕的Size
	*
	*@return float
	*/
	UFUNCTION(BlueprintPure, Category = "Screen")
		static FVector2D GetViewportSize();

#pragma endregion

#pragma region	/** 资源相关 */
	/**
	*BlueprintPure,从资源路径获取对象(同步)
	*
	*@return 资源对象
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal|LoadObject")
		static UObject* LoadObjectByAssetPath(TSoftObjectPtr<UObject> AssetPath);

	/**
	*BlueprintCallable,根据路径获取资源
	*
	*@return 资源
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal")
		static FAssetData CS3GetAssetDataByFilePath(const FString& PackagePath);

	UFUNCTION(BlueprintCallable, Category = "Global")
		static UMaterialInterface* GetFootMaterial();

	/**
	*BlueprintCallable,创建动态材质实例
	*
	*@return 动态材质实例
	*/
	UFUNCTION(BlueprintCallable, Category = "Utilities|Material")
	static UMaterialInstanceDynamic* CreateDMI(UPrimitiveComponent* Comp, int32 ElementIndex, class UMaterialInterface* SourceMaterial);

	/**
	*BlueprintCallable,在材质中修改多个同名参数的float值
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Utilities|Material")
	static void CS3SetScalarParameterOnMaterials(UMeshComponent* Comp, FName ParameterName, float ParameterValue);

	UFUNCTION(BlueprintCallable, Category = "Test")
		static int32 GetObjReferenceCount(UObject* Obj, TArray<UObject*>& OutReferredToObjects);

	/**
	*BlueprintCallable,在材质中修改多个同名参数的vector值
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Utilities|Material")
	static void CS3SetVectorParameterOnMaterials(UMeshComponent* Comp, FName ParameterName, FVector ParameterValue);

	UFUNCTION(BlueprintCallable, Category = "Utilities|Material")
	static void CS3SetLinearParameterOnMaterials(UMeshComponent* Comp, FName ParameterName, FLinearColor ParameterValue);

	static class UPathFollowingComponent* InitNavigationControl(AController& Controller);

	///<查找文件中拥有特定名字的资源并保存
	static void CheckFileInPathByPrefix(const FString& DirectoryPath, TArray<FString>& NameFix, const FString Prefix, TArray<FString>& NameAssets);

	///<查找资源文件是否存在
	static bool CheckResourceFileIsExist(const FString& ResourceFile);

#pragma endregion

#pragma region	/** 背包物品信息相关 */
	/**
	*BlueprintPure,获取物品名字的颜色
	*
	*@param Quality	品质（1白色2蓝色3金色4粉色5地阶绿色6天阶绿色7圣阶绿色8神阶绿，对应QUALITY）
	*
	*@return FLinearColor
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal")
		static FLinearColor GetItemNameColorByQuality(int32 Quality);

	/**
	*BlueprintPure,获取物品工厂
	*
	*@return UItemFactory
	*
	*/
	UFUNCTION(BlueprintPure, Category = "Manager")
		static UItemFactory* ItemFactory();

	/**
	*BlueprintCallable,根据品质获得带颜色的物品名称
	*
	*@param ItemName 需要换颜色的名字
	*@param Quality	品质（1白色2蓝色3金色4粉色5地阶绿色6天阶绿色7圣阶绿色8神阶绿，对应QUALITY）
	*
	*@return FString
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal")
		static FString GetItemNameByQuality(const FString& ItemName, int32 Quality);

	/**
	*BlueprintCallable，获取品质配置
	*
	*@param Quality	品质（1白色2蓝色3金色4粉色5地阶绿色6天阶绿色7圣阶绿色8神阶绿，对应QUALITY）
	*
	*@return FString
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal")
		static FCS3ItemQualityData GetItemQualityConfig(int32 Quality, bool& IsSuccess);


	/**
	*BlueprintCallable,获取装备部件的名字通过装备类型
	*
	*@param	PartType
	*
	*@return FString 返回转换后的字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal")
		static FString GetEquipPartNameByPartType(MODEL_PART_TYPE PartType);

	/**
	*BlueprintPure,获取按钮tips
	*
	*@param StringValue 按钮字符串
	*
	*@return FString 返回tips
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal")
		static FString GetHoverTips(const FString& StringValue);

	/**
	*BlueprintPure,根据品质获取纹理
	*
	*@param Quality 品质
	*
	*@return UTexture2D
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal|UTexture2D")
		static UTexture2D* GetTextrue2DByItemQuality(int32 Quality);

	///<根据背包类型和相对位置，获取绝对位置
	UFUNCTION(BlueprintPure, Category = "KitBag")
		static int32 GetAbsItemOrder(int32 relorder, EKITBAGTYPE bagtype);

	///<根据绝对位置获取背包类型
	UFUNCTION(BlueprintPure, Category = "KitBag")
		static EKITBAGTYPE GetBagTypeByAbsOrder(int32 absorder);

	///<根据绝对位置获取相对位置
	UFUNCTION(BlueprintPure, Category = "KitBag")
		static int32 GetRelOrderByAbsOrder(int32 absorder);

	///<根据绝对位置获取背包类型和相对位置
	UFUNCTION(BlueprintPure, Category = "KitBag")
		static void GetBagTypeAndRelOrderByAbsOrder(const int32& absorder, int32& relorder, EKITBAGTYPE& bagtype);

	///<物品的职业过滤器
	UFUNCTION(BlueprintCallable, Category = "Item | Filter")
		static void FilterProfessions(const TArray<int32> professions, const TArray<UItemBase*> &itemarray, TArray<UItemBase*>& result);

	///<物品的装备部位过滤器
	UFUNCTION(BlueprintCallable, Category = "Item | Filter")
		static void FilterEquipParts(const TArray<int32> equipparts, const TArray<UItemBase*> &itemarray, TArray<UItemBase*>& result);

	///<物品的等级过滤器
	UFUNCTION(BlueprintCallable, Category = "Item | Filter")
		static void FilterLevels(const TArray<int32> levels, const TArray<UItemBase*> &itemarray, TArray<UItemBase*>& result);

	///<物品的品质过滤器
	UFUNCTION(BlueprintCallable, Category = "Item | Filter")
		static void FilterQualities(const TArray<int32> qualities, const TArray<UItemBase*> &itemarray, TArray<UItemBase*>& result);

#pragma endregion

#pragma region	/** 小地图相关 */
	/**
	*BlueprintPure,将世界坐标转换为地图镜面中的像素坐标（不算缩放）
	*
	*@param ActorLocation Actor的世界坐标
	*@param LevelOrignLocation 关卡的世界原点坐标
	*@param LevelOrignLocation 关卡的世界尺寸/地图MapTexture的像素尺寸
	*
	*@return FVector2D
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal|UTexture2D")
		static FVector2D ConvertWorldLocationToMapPosition(FVector2D ActorLocation, FVector2D LevelOrignLocation, float Rate);

	/**
	*BlueprintPure,将点的世界位置转换成在父插槽上的位置（小地图相关）
	*
	*@param PointLocation：点的世界坐标
	*@param MiniMapViewOrigin：地图图片上小地图可视范围的原点的像素坐标
	*@param LevelOrignLocation：关卡世界原点坐标
	*@param Rate：关卡的世界尺寸/地图MapTexture的像素尺寸
	*@param ZoomRate：地图缩放倍率
	*@param MiniMapViewSize：小地图可视尺寸（像素）
	*@param PointTextureSize：点图标的尺寸
	*@param ResultVector2D：重新获取得到的新点
	*
	*@return bool 是否转换成功
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal|UTexture2D")
		static bool ConvertWorldLocToSlotPos(FVector2D PointLocation, FVector2D MiniMapViewOrigin,
			FVector2D LevelOrignLocation, float Rate, float ZoomRate, FVector2D MiniMapViewSize,
			FVector2D PointTextureSize, FVector2D& ResultVector2D);

	/**
	*BlueprintPure,获取地图数据
	*
	*@return FRESULT_MAP_DATA
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal|UTexture2D")
		static FRESULT_MAP_DATA GetMapData();

#pragma endregion

#pragma region	/** 时间转换相关 */
	/**
	* Gets time delta in seconds.
	*
	* @return Time delta in seconds.
	*/
	UFUNCTION(BlueprintPure, Category = "Input")
		static float GetDeltaTime();

	///<由日期得到星期，返回整型（0-星期一；1-星期二；2-星期三；3-星期四；4-星期五；5-星期六；6-星期日）
	UFUNCTION(BlueprintPure, Category = "Math|Week")
		static int32 GetWeekDayByDate(const FDateTime Date);

	///<返回当前时间(单位：秒)，作为自Unix纪元（1970年1月1日）以来的秒数。
	UFUNCTION(BlueprintCallable, Category = "Golbal | Time")
		static int64 GetFromUnixTimestamp(bool IsUTC = false);

	///<python time.time() 转换成 FDataTime
	UFUNCTION(BlueprintCallable, Category = "Golbal | Time")
		static FDateTime FromServerTimeToClientTime(int32 time);

	///<python Functions.getTime() 转换成 FDataTime
	UFUNCTION(BlueprintCallable, Category = "Golbal | Time")
		static FDateTime FromServerStrTimeToClientTime(FString strTime);

	///<FDataTime 转换成 python time.time()
	UFUNCTION(BlueprintCallable, Category = "Golbal | Time")
		static float FromClientTimeToServerTime(FDateTime time);

	///<FDataTime 转换成 python int( time.time() * 10000000 )
	UFUNCTION(BlueprintCallable, Category = "Golbal | Time")
		static int64 FromClientTimeToServerStrTime(FDateTime time);

	/**
	*BlueprintCallable, 将服务器时间差（扩大了10000000倍）转化为int64（解除扩大倍数）
	*
	*@param	time 服务器时间差，服务器发过来的时间扩大了10000000倍
	*@return int64 秒
	*
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal | FString")
		static int64 FromServerStrTimeToSecond(int64 time);

	/**
	*BlueprintPure, 将FDateTime类型时间值转化时间字符串，格式为2018/07/28 14:45
	*
	*@param	time 时间结构体
	*@param	IsShowToday 如果时间为今天，是否显示今天的日期，比如今天是2018/07/28 14:45，如果设为False则输出14:45，True输出2018/07/28 14:45
	*@param	type 为0表示精确到秒，为1表示精确到分，为2表示精确到时，为3表示精确到天，默认为0
	*
	*@return FString
	*/
	UFUNCTION(BlueprintPure, Category = "Golbal | FString")
		static FString ConvertDateTimeToNumberModelByType(FDateTime time, bool IsShowToday = false, int32 type = 0);

	/**
	*BlueprintCallable, 将秒转化为文字，强制格式，格式，如:xx时、xx时xx分、xx时xx分xx秒、xx分xx秒、xx秒、xx分
	*
	*@param	SecondValue 时间（单位:秒）
	*@param	type 为0表示(xx时),type为1(xx时xx分),type为2(xx时xx分xx秒),type为3(xx分xx秒),type为4(xx秒),type为5(xx分)
	*
	*@return FString
	*
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal")
		static FString ConvertSecondsToHourChineseModelByType(int64 SecondValue, int32 Type);

	/**
	*BlueprintCallable, 将秒转化为以"小时"开头的"冒号"格式，如:00:00:00
	*
	*@param	TimeValue 时间（单位:秒）
	*
	*@return FString
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal")
		static FString ConvertSecondsToHourColonModle(int32 TimeValue);

	/**
	*BlueprintCallable, 将秒转化为以"分钟"开头的"冒号"格式，如:00:00
	*
	*@param	TimeValue 时间（单位:秒）
	*
	*@return FString
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal")
		static FString ConvertSecondsToMinuteColonModle(int32 TimeValue);

	/**
	*BlueprintCallable, 将秒转化为以"天"开头的"文字"格式（某一段为0时，此段将不显示出来），如:xx天xx时xx分xx秒、xx天xx秒等等
	*
	*@param	time 时间（单位:秒）
	*
	*@return FString
	*
	*/
	UFUNCTION(BlueprintCallable, Category = "Golbal")
		static FString ConvertSecondsToDayChineseModel(float SecondValue);

#pragma endregion

	// 打开文件选择窗口选择文件,并返回选中文件路径
	UFUNCTION(BlueprintCallable, Category = "Golbal")
		static bool GetPathByFileDialog(FString& OutPath, const FString& FileTypes);

	//强制垃圾回收
	UFUNCTION(BlueprintCallable, Category = "Global")
		static void ForceGC();

	//获得游戏帧数
	UFUNCTION(BlueprintPure, Category = "Global")
		static FString GetGameFrame();

	//保存UTextureRenderTarget2D到本地文件
	UFUNCTION(BlueprintCallable, meta = (DisplayName = "SaveRenderTargetToFile", Keywords = "SaveRenderTargetToFile"), Category = "SaveToFile")
		static bool SaveRenderTargetToFile(UTextureRenderTarget2D* rt, const FString& fileDestination);

	UFUNCTION(BlueprintCallable, Category = "SaveToFile")
		static class UTexture2D* GetTexture2DFromDiskFile(const FString& FilePath);

	//获取贴图中的某个MipMap贴图大小
	UFUNCTION(BlueprintCallable, Category = "GetBigMapSizeInMips")
		static FVector2D GetMapTextureSizeByMip(UTexture2D* MapTexture, int32 MipIndex);

#pragma region	/** 排序相关 */
	//对TMap<int32, int32>类型以Key值由小到大进行排序
	UFUNCTION(BlueprintPure, Category = "Sort")
		static TMap<int32, int32> SortTMapByKey(TMap<int32, int32> MapData);

#pragma endregion
};