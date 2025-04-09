#pragma once

#include "Actor/GameCharacter.h"
#include "GameData/StoryData.h"
#include "GameData/ModelPartData.h"
#include "Manager/CfgManager.h"
#include "StoryCharacter.generated.h"


/*
* 文件名称：StoryCharacter.h
* 功能说明：剧情编辑使用模型父类
* 文件作者：LiuShuang
* 目前维护：wuxiaoou
* 创建时间：2016-12-01
*/

class UAnimSequenceBase;
class APoseableBlur;
DECLARE_STATS_GROUP(TEXT("AStoryCharacter"), STATGROUP_AStoryCharacter, STATCAT_Advanced);

UCLASS(BlueprintType)
class CHUANGSHI_API AStoryCharacter : public AGameCharacter
{
	GENERATED_BODY()
public:
	AStoryCharacter();
	~AStoryCharacter();
	virtual void BeginPlay()override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	virtual void Tick(float DeltaSeconds)override;

	UFUNCTION(BlueprintCallable, Category = "StoryCharacter")
		void PlayStroyAction(FName ActionId, bool IsBreakAction = true);

	UFUNCTION(BlueprintCallable, Category = "StoryCharacter")
		void StopStroyAction();

	UFUNCTION(BlueprintCallable, Category = "StoryCharacter")
		void PlayAnimByName(FString AnimName, float PlayRate = 1.0f, bool bLoop = false);

	UFUNCTION(Category = "StoryCharacter")
		void PlayAnim(UAnimSequenceBase *AnimSequenceBase, float PlayRate, bool bLoop);

	UFUNCTION(Category = "StoryCharacter")
		void StopAnim();

	//播放头部动画（仅用于角色模型，因为角色模型的头是独立骨架、头有自己的动画蓝图） 
	UFUNCTION(BlueprintCallable, Category = "StoryCharacter")
		void PlayHeadAction(UAnimSequenceBase *AnimSequenceBase, float PlayRate = 1.0f, 
			float StartPosition = 0.0f, bool bLoop = true);
	//停止头部动画（仅用于角色模型）
	UFUNCTION(BlueprintCallable, Category = "StoryCharacter")
		void StopHeadAction();

	///<CST-10263 剑客右手到左手武器绑定
	UFUNCTION(BlueprintCallable, Category = "StoryCharacter")
		void UpdateWeaponRightToLeft(bool IsRightToLeft, int32 InProfession);

	UFUNCTION(BlueprintCallable, Category = "StoryCharacter")
		void MeshForceClothNextUpdateTeleport();
	void SetDissolveValue(float DissolveDegreeValue);
	void SetDissolveDirectionValue(float DissolveDirectionValue);

	virtual void ReSetOpenScen3DUI() { OpenScene3DUI = true; };
protected:
	/** If true, actor is ticked even if TickType==LEVELTICK_ViewportsOnly */
	virtual bool ShouldTickIfViewportsOnly() const override;
	virtual FName GetWeaponSockName(bool IsLeft);///获取武器的插槽位置

	void UpdateMeshPorperty();
	virtual void InitBaseComponent() override;
	UFUNCTION(BlueprintCallable)
		void RegisterComponent(bool bIsRegister = true);
	UFUNCTION(BlueprintCallable)
		void SetUpdateAnimationInEditor();
	UFUNCTION(BlueprintCallable)
		void InitSpawnModel();///<初始化模型
	UFUNCTION(BlueprintCallable)
		void SetModelAlpha();
	UFUNCTION(BlueprintNativeEvent)
		bool SetHeadAlphaInfo();
	UFUNCTION(BlueprintCallable)
		void BindAnimationEvent();
	UFUNCTION(BlueprintCallable)
		void InitProfessionID();///<初始化职业ID
	UFUNCTION(BlueprintCallable, Category = "StoryCharacter")
		void SetPlayerState(bool IsShowWeapon, ENTITY_STATE State, int32 Profession);
	UFUNCTION(BlueprintCallable, Category = "StoryCharacter")
		void SetForceMipStreaming();///<CST-6336
	UFUNCTION(BlueprintCallable, Category = "StoryCharacter")
		void RefreshTrackData();///<刷新轨道数据
	UFUNCTION(BlueprintCallable, Category = "StoryCharacter")
		void SetMaterialsParam(FName ParamName, float Value,int32 type = 0, bool OpenStaticMaterial = true);///type:0:默认类型 1：CloakOpacity（该功能对Hair材质做特殊处理）
	UFUNCTION(BlueprintNativeEvent, Category = "StoryCharacter")
		void SetHeadInfo();
	UFUNCTION()
		void OnWorldPostActorTick();

private:
	void SetModelonLandInEditor();
	void ClearWorldPostActorTickHandle();
	void PostInitProperties();
	void PostEditChangeProperty(FPropertyChangedEvent& PropertyChangedEvent);
	void InitPlayer();
	void InitPlayerTeamMemb();
	void InitModelByModelID();
	void ClearModelData();
	void SetModelByParts(TMap<MODEL_PART_TYPE, FString> PartMap, FString ModelNumber);
	void GetModelTable();
	void InitSpawnModelByEditor(TMap<MODEL_PART_TYPE, FString>& InNewPartMap);
	void SetModleByPartMap(AGameCharacter* GameCharacter);
	void SetActorPart(MODEL_PART_TYPE PartPos, FMODEL_PART_DATA PartData);
	void SetStoneOpacity();
	void SetEmissiveColor();
	void SetDissolveColor();
	void ChangeModelAlpha();
	void PlayBornEffect();
	void ClearAnimData();
	void ForceClothNextUpdateTeleport();
	void ResetSkeletalMeshPosition();
	void SetMaterialsParam(FName ParamName, FLinearColor Value,bool OpenStaticMaterial = true);
	void SetStaticMaterialsParam(FName ParamName, FLinearColor Value);
	const FSTORY_ANIM_EVENT* GetStoryAnimEventData(const FString& AnimName);
	//替换材质功能 因父材质替换问题暂不启用
	void LoadNewMaterial(float model);

	void SkipAnimNotifies();///<跳过动画通知
	void AfterimageEffectEvent();//残影效果CST-10500
	void CreateMontionVlurEvent();//残影效果CST-10500
public:
	UPROPERTY(/*EditAnywhere, */BlueprintReadOnly)
		UAnimSequenceBase* OldAnim;
protected:
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		bool bStopNativeData = true; ///<是否禁止原生数据修改
	UPROPERTY(/*EditAnywhere, */BlueprintReadOnly)
		bool bRetainCamera;
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		bool IsPlayer;
	///<是否女性玩家角色
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		bool IsFemalePlayer = false;
	////<CST-9160多玩家组队镜头角色
	UPROPERTY(EditAnywhere, BlueprintReadOnly, meta = (EditCondition = "!IsPlayer"))
		bool IsPlayerTeamMemb =false;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, meta = (EditCondition = "IsPlayerTeamMemb"))
		int32 PlayerTeamMembIndex = -1;

	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		bool bUseModelId;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, meta = (EditCondition = "!bStopNativeData"))
		FName ModelId;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, meta = (EditCondition = "bStopNativeData"))
		FString ModelIdTrack;
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		float ModelScale = 1.0f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp)
		bool IsShowName;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, meta = (EditCondition = "!bStopNativeData"))
		FName UName;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, meta = (EditCondition = "bStopNativeData"))
		FString UNameTrack;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, meta = (EditCondition = "IsShowName"))
		FSlateColor NameColor;
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		bool IsBeginOnLand;
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 ProfessionIDByCinematics = 1;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp)
		ENTITY_STATE CurState = ENTITY_STATE::EntityStateFree;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp)
		bool StartNewOpacity = false;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp)
		float Opacity = 1.0f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp)
		float StoneOpacity = 0.0f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp)
		bool IsShowWeapon = true;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp)
		bool IsWeaponRightToLeft = false;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp)
		bool IsMoveOnLand = false;

	/*--------------自发光表现效果-----------------------*/
	////<材质是否计算内发光
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, Category = "StoryCharacter|Edge")
		float EnableEdge = 0.0f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, Category = "StoryCharacter|Edge")
		float EdgeGlowWidth = -1.0f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, Category = "StoryCharacter|Edge")
		FLinearColor EdgeGlowColor =FLinearColor(0,1,1,0);
	/*--------------消融表现效果-----------------------*/
	///是否开启消融效果
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, Category = "StoryCharacter|Dissolve")
		bool bIsDissolve = false;
	///消融渐变值
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, Category = "StoryCharacter|Dissolve")
		float DissolveDegree = 0.0f;
	///消融宽度
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, Category = "StoryCharacter|Dissolve")
		float FringeAmount = 1.0f;
	///消融方向（0:整体；1:上；2:下；3:左；4:右）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, Category = "StoryCharacter|Dissolve")
		float DissolveDirection = 0.0f;
	///消融颜色
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, meta = (EditCondition = "bIsDissolve"), Category = "StoryCharacter|Dissolve")
		FLinearColor DissolveColor = FLinearColor(10, 1, 0, 1);
	///开启包围盒
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, Category = "StoryCharacter|Dissolve|LocalBound")
		bool DissolveBoundsSet = false;
	///包围盒大小
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, meta = (EditCondition = "DissolveBoundsSet"), Category = "StoryCharacter|Dissolve|LocalBound")
		FLinearColor LocalBoundsSize = FLinearColor(200.0f,100.0f,200.0f,0);
	///包围盒偏移
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, meta = (EditCondition = "DissolveBoundsSet"), Category = "StoryCharacter|Dissolve|LocalBound")
		FLinearColor LocalBoundsMin = FLinearColor(0, 0, 0, 0);
	///开启武器包围盒
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, meta = (EditCondition = "DissolveBoundsSet"), Category = "StoryCharacter|Dissolve|LocalBound")
		bool DissolveBounds_W = false;
	///武器包围盒大小
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, meta = (EditCondition = "DissolveBoundsSet"), Category = "StoryCharacter|Dissolve|LocalBound")
		FLinearColor LocalBoundsSize_W = FLinearColor(0, 0, 0, 0);
	///武器包围盒偏移
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, meta = (EditCondition = "DissolveBoundsSet"), Category = "StoryCharacter|Dissolve|LocalBound")
		FLinearColor LocalBoundsMin_W = FLinearColor(0, 0, 0, 0);


	/*--------------残影表现效果-----------------------*/
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, Category = "StoryCharacter|Afterimage")
		bool bIsAfterimage = false;
	///代表每隔CreateInterval秒创建个残影单位
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, Category = "StoryCharacter|Afterimage")
		float CreateInterval = 1.0f;
	///残影生存时间
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, Category = "StoryCharacter|Afterimage")
		float AfterimageLifeTime = 1.0f;
	///残影是否使用原材质
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, Category = "StoryCharacter|Afterimage")
		bool bIsAfterimageMaterial = false;
	///残影颜色
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, Category = "StoryCharacter|Afterimage", meta = (EditCondition = "!bIsAfterimageMaterial"))
		FLinearColor AfterimageColor = FLinearColor(0, 0, 0, 1);
	///残影透明度
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, Category = "StoryCharacter|Afterimage")
		float AfterimageAphla = 1.0f;
	///残影偏移值
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, Category = "StoryCharacter|Afterimage")
		FVector AfterimageDeviation = FVector::ZeroVector;
	///残影是否与目标同步动作
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Interp, Category = "StoryCharacter|Afterimage")
		bool bIsAfterimageSync = false;


	/*--------------CST-6336-镜头中模型加载不完全-----------------------*/
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		bool IsForceMipStreaming;

	UPROPERTY()
		const UConfigTable* ModelTable;
	UPROPERTY()
		const UConfigTable* PartTable;
	UPROPERTY()
	TArray<APoseableBlur*> BlurMeshs;
private:
	TArray<FSTORY_CHARACTER_ANIM> CharacterAnims;
	bool IsFightState = false;
	TArray<FString> EffectIds;
	TArray<int32> EffectUIds;
	float CurrOpacity = 1.0f;
	float CurrStoneOpacity = 0.0f;
	FTransform LastTranform;
	bool bIsConstantTranform = false;
	FDelegateHandle WorldPostActorTickHandle;
	bool bIsVisibilityPlayerTeamMemb = true;
	bool bIsVisibilityPlayer = true;///<男女角色
	bool bIsChangeMaterial = false;//当前材质只切换一次
	float CurModel = 1 ;//1：Mask模式 2：Tran模式
	float AfterimageTime = 0.0f;
	float AfterimageTimer = 100000.0f;//残影定时器
	float OldEnableEdge = 0.0f;
	bool bIsEnableEdgeChanged = false;
	bool AfterimageClear;
	bool bIsMontionBlurChange = true;//残影只调用一次
	FTimerHandle MontionBlurEventHandle;///<残影生成定时器
	float CurDissolveDirection = 10.0f;
	bool M_DissableSwitch = false;
};
