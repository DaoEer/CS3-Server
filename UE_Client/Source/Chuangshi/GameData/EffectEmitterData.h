#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "Engine/EngineTypes.h"
#include "Actor/ServerCharacter.h"
#include "EffectEmitterData.generated.h"

/**
* 文件名称：EffectEmitterData.h
* 功能说明：
* 文件作者：luocheng
* 目前维护：zhangfudong
* 创建时间：2016-11-09
*/



// 粒子从属类型
UENUM(BlueprintType)
enum class PARTICLE_TYPE : uint8
{
	///当前客户端玩家（包括宠物）携带的粒子光效类型
	TYPE_PARTICLE_PLAYER = 1			UMETA(DisplayName = "TYPE_PARTICLE_PLAYER"),
	///当前客户端其他玩家（包括宠物）携带的粒子光效类型
	TYPE_PARTICLE_OTHERPLAYER = 2		UMETA(DisplayName = "TYPE_PARTICLE_OTHERPLAYER"),
	///当前客户端玩家正在交互的Entity光效类型（比如和当前玩家正在战斗的Monster所产生的光效）
	TYPE_PARTICLE_PIN = 3				UMETA(DisplayName = "TYPE_PARTICLE_PIN"),
	///当前客户端其他玩家正在交互的Entity光效类型
	TYPE_PARTICLE_PIOP = 4				UMETA(DisplayName = "TYPE_PARTICLE_PIOP"),
	///除玩家外的Entity光效类型
	TYPE_PARTICLE_NPC = 5				UMETA(DisplayName = "TYPE_PARTICLE_NPC"),
	///场景光效类型
	TYPE_PARTICLE_SCENE = 6				UMETA(DisplayName = "TYPE_PARTICLE_SCENE"),
};

// 粒子显示距离等级
UENUM(BlueprintType)
enum class LOD_TYPE : uint8
{
	///近距离
	NEAR_DIS = 1		UMETA(DisplayName = "NEAR_DIS"),
	///中距离
	MIDDEL_DIS = 2		UMETA(DisplayName = "MIDDEL_DIS"),
	///远距离
	FAR_DIS = 3			UMETA(DisplayName = "FAR_DIS"),
};

UENUM(BlueprintType)
enum class BIND_COMPOENT_TYPE : uint8
{
	///（主MESH）
	DEFAULT_Mesh		UMETA(DisplayName = "DEFAULT_Mesh"),
	///（腰饰）
	WAISTADORN_Mesh		UMETA(DisplayName = "WAISTADORN_Mesh"),
	///（发饰）
	HAIRADORN_Mesh		UMETA(DisplayName = "HAIRADORN_Mesh"),
	///（头饰）
	HEADADORN_Mesh		UMETA(DisplayName = "HEADADORN_Mesh"),
	///（背饰）
	BACKADORN_Mesh		UMETA(DisplayName = "BACKADORN_Mesh"),
	///（双手静态武器）
	BWEAPON_Mesh		UMETA(DisplayName = "BWEAPON_Mesh"),
	///（左手静态武器）
	LWEAPON_Mesh		UMETA(DisplayName = "LWEAPON_Mesh"),
	///（右手静态武器）
	RWEAPON_Mesh		UMETA(DisplayName = "RWEAPON_Mesh"),
	///（左手骨架武器）
	S_LWEAPON_Mesh		UMETA(DisplayName = "S_LWEAPON_Mesh"),
	///（右手骨架武器）
	S_RWEAPON_Mesh		UMETA(DisplayName = "S_RWEAPON_Mesh")
};
USTRUCT(BlueprintType)
struct CHUANGSHI_API FEFFECT_TRANSFORM_DATA
{
	GENERATED_USTRUCT_BODY()
public:

	///特效绑定的组件
	///此功能主要为了支持主MESH之外的其他部件 当前仅支持腰饰
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	BIND_COMPOENT_TYPE BindCompoent = BIND_COMPOENT_TYPE::DEFAULT_Mesh;
	///光效目标点：绑定点
	///	指定绑定点/插槽名称（见具体模型骨骼）
	///支持：
	///	配合“是否绑定”等参数，描述“光效目标点”的具体表现
	///注意：
	///	留空、找不到插槽名时，代表“默认绑定Mesh基准点”（大概是脚的位置）
	///	项目标准插槽：Socket_Root、Socket_Body、Socket_Head（共3个）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString BindSocket;

	///光效目标点：是否“绑定”
	///支持：
	///	配合“是否世界的”等参数，描述“光效目标点”的具体表现（后详）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsBind;

	///光效目标点：位置，是否“世界的”
	///	是，代表“光效目标点”的位置是“世界的”
	///	否，代表“光效目标点”的位置是“相对的”
	///支持：
	///	配合“是否绑定”等参数，描述“光效目标点”的具体表现
	///		①绑定的＋相对的：典型的绑定表现（“光效”成为“光效目标”的子Actor）
	///		②绑定的＋世界的：不完全的绑定表现（如，位置是世界的，与光效目标不联动）
	///		③不绑定＋相对的：初始位置，与光效目标有关
	///		④不绑定＋世界的：初始位置，与光效目标无关
	///注意：
	///	①②③的初始位置表现是一致的
	///	②和③的差异是“光效Actor是否光效目标的子Actor，是否受制于其AOI、可见性等表现”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint32 bIsLocationOnWorld : 1;

	///光效目标点：旋转，是否“世界的”
	///	是，代表“光效目标点”的旋转是“世界的”
	///	否，代表“光效目标点”的旋转是“相对的”
	///支持：
	///	配合“是否绑定”等参数，描述“光效目标点”的具体表现
	///		①绑定的＋相对的：典型的绑定表现（“光效”成为“光效目标”的子Actor）
	///		②绑定的＋世界的：不完全的绑定表现（如，旋转是世界的，与光效目标不联动）
	///		③不绑定＋相对的：初始位置，与光效目标有关
	///		④不绑定＋世界的：初始位置，与光效目标无关
	///注意：
	///	①②③的初始位置表现是一致的
	///	②和③的差异是“光效Actor是否光效目标的子Actor，是否受制于其AOI、可见性等表现”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint32 bIsRotationOnWorld : 1;

	///光效目标点：缩放，是否“世界的”
	///	是，代表“光效目标点”的缩放是“世界的”
	///	否，代表“光效目标点”的缩放是“相对的”
	///支持：
	///	配合“是否绑定”等参数，描述“光效目标点”的具体表现
	///		①绑定的＋相对的：典型的绑定表现（“光效”成为“光效目标”的子Actor）
	///		②绑定的＋世界的：不完全的绑定表现（如，旋转是世界的，与光效目标不联动）
	///		③不绑定＋相对的：初始位置，与光效目标有关
	///		④不绑定＋世界的：初始位置，与光效目标无关
	///注意：
	///	①②③的初始位置表现是一致的
	///	②和③的差异是“光效Actor是否光效目标的子Actor，是否受制于其AOI、可见性等表现”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint32 bIsScaleOnWorld : 1;

	///光效目标点：形变
	///支持：
	///	描述“光效目标点”的形变修正：位置、旋转、缩放
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FTransform Transform;

	bool operator==(const FEFFECT_TRANSFORM_DATA& OtherData)
	{
		if (Transform.GetLocation() == OtherData.Transform.GetLocation() &&
			Transform.GetRotation() == OtherData.Transform.GetRotation() &&
			Transform.GetScale3D() == OtherData.Transform.GetScale3D() &&
			bIsLocationOnWorld == OtherData.bIsLocationOnWorld &&
			bIsRotationOnWorld == OtherData.bIsRotationOnWorld &&
			bIsScaleOnWorld == OtherData.bIsScaleOnWorld &&
			bIsBind == OtherData.bIsBind &&
			BindSocket == OtherData.BindSocket)
		{
			return true;
		}

		return false;
	}
};


///光效粒子数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPARTICLE_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///粒子：资源
	///支持：
	///	播放粒子系统资源表现（@/Game/Effects/Particles/）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UParticleSystem> ParticleSystemAsset;

	///粒子：形变
	///支持：
	///	描述“粒子系统”的形变修正：位置、旋转、缩放（@CST-3262）
	///		默认X/Y/Z＝左/前/上
	///注意：
	///	已知风险：表现组件层级不自然（@CST-3262）
	///		目前“粒子系统组件”为“静态模型组件”、“骨骼模型组件”的上级，因此粒子形变将影响它们的形变，请谨慎使用
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FTransform ParticleSystemTransform;

	///粒子：是否“一直渲染”
	///支持：
	///	粒子在摄像机外也可以更新模块数据（@CST-8016）
	///注意：
	///	当“粒子在摄像机外生成，跟随绑定移动到摄像机内，不显示”时，才需要使用
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint32 bAlwaysRender : 1;

	///粒子：是否“自定义光效渲染排序”
	///支持：
	///	自定义光效透明渲染排序（@CST-6166）
	///注意：
	///	当光效之间的顺序不满意时，才需要使用（如“法阵光效希望一直表现在其他光效后面”）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint32 bSortEffect : 1;

	///粒子：自定义渲染优先级
	///		优先级越小，越先渲染，越容易被其他内容覆盖，表现为“越小越在后面”
	///		优先级越大，越后渲染，越容易把其他内容覆盖，表现为“越大越在前面”
	///支持：
	///	可以调整光效的透明渲染排序的优先级（@CST-6166）
	///注意：
	///	“自定义光效渲染排序”时，此参数才生效
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 SortIndex = 0;

	///粒子：目标自定义渲染优先级
	///		优先级越小，越先渲染，越容易被其他内容覆盖，表现为“越小越在后面”
	///		优先级越大，越后渲染，越容易把其他内容覆盖，表现为“越大越在前面”
	///支持：
	///	可以调整“光效的目标2”的透明渲染排序的优先级（@CST-10243）
	///		用以修复“模型透明时，光效和模型的表现顺序不明确，导致表现不自然”的表现问题
	///注意：
	///	无需额外配置激活，缺省0代表“不激活”，非0代表“激活”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 TargetSortIndex = 0;

	///粒子：1倍缩放下粒子包围盒大小
	///	根据粒子包围盒和摄像机的位置，确定一个锥体，用于判断粒子是否在排序范围内
	///注意：
	///	这个值越精确越好
	///UPROPERTY(EditAnywhere, BlueprintReadWrite)
	///	FVector EffectBounds;

	///粒子：是否“固定透明”
	///支持：
	///	可以设定粒子的透明表现，整个持续时间过程中都保持稳定的透明度（@CST-5352）
	///注意：
	///	“固定透明”和“渐变透明”互相冲突，不可同时启用
	///	本地调试时请注意，更改此配置时会立刻更新已经创建的光效表现，请注意辨识避免误解
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint32 bUseConstAlpha : 1;

	///粒子：固定透明度目标值
	///	≤0，代表“完全透明，一点都看不到”
	///	＝1，代表“与不启用透明表现一样”
	///	＞1，代表“原来透明的光效表现，变得不那么透明了”
	///支持：
	///	可以调整固定透明度的表现（@CST-5352）
	///注意：
	///	“固定透明”时，此参数才生效
	///	本地调试时请注意，更改此配置时会立刻更新已经创建的光效表现，请注意辨识避免误解
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (EditCondition = "bUseConstAlpha"))
		float InitAlpha = 1.0f;

	///粒子：是否“渐变透明”
	///支持：
	///	可以光效在持续时间内，做出类似“淡入淡出”的表现（@CST-4390）
	///注意：
	///	“固定透明”和“渐变透明”互相冲突，不可同时启用
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bGraduallyHidden;

	///粒子：淡入时间（≤0秒代表“立刻”）
	///支持：
	///	可以调整光效渐变透明的淡入淡出表现（@CST-4390）
	///		在淡入时间内，粒子透明度从0渐变到1
	///注意：
	///	“渐变透明”时，此参数才生效
	///	淡入时间≥持续时间时，淡入时间＝持续时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (EditCondition = "bGraduallyHidden"))
		float FadeInTime = -1.f;

	///粒子：淡出时间（≤秒0代表“立刻”）
	///支持：
	///	可以调整光效渐变透明的淡入淡出表现（@CST-4390）
	///		在淡出时间内，粒子透明度从0渐变到1
	///注意：
	///	“渐变透明”时，此参数才生效
	///	淡出时间≥（持续时间－淡入时间）时，淡出时间＝（持续时间－淡入时间）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (EditCondition = "bGraduallyHidden"))
		float FadeOutTime = -1.f;


	virtual ~FPARTICLE_DATA() {}

	///只比对基础属性
	bool operator==(FPARTICLE_DATA& OtherData)
	{
		if (ParticleSystemAsset == OtherData.ParticleSystemAsset &&
			FTransform::AreTranslationsEqual(ParticleSystemTransform, OtherData.ParticleSystemTransform) &&
			bAlwaysRender == OtherData.bAlwaysRender &&
			bGraduallyHidden == OtherData.bGraduallyHidden)
		{
			return true;
		}
		return false;
	}
};

///通用光效表现脚本数据（@CST-3262）
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBASEEFFECT_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///延迟激活时间（≤0秒代表“立刻激活”）
	///支持：
	///	先创建光效Actor，延迟激活表现（创建→激活）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float DelayPlayTime = 0.0f;

	///持续时间（＜0秒代表“不会死亡，一直存在”，＝0秒代表“立刻死亡”）
	///支持：
	///	描述光效表现的持续时间（激活→死亡）
	///		各种表现原则上都从激活时开始
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float LifeTime = 0.0f;

	///延迟销毁时间（0秒代表“立刻销毁”）
	///支持：
	///	常规表现结束后，延迟销毁（死亡→销毁）
	///	弥留表现：光效死亡时，表现停止，但各组件可以延续其自定义的弥留表现
	///		粒子/连线：缓慢消散（发射器停止，粒子继续运行至结束）
	///		贴花/模型：停止动作
	///		飞行/路径：停止移动
	///吐槽：
	///	不同组件的弥留表现均需要自行定义，后续仍需继续完善
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float DelayDestroyTime = 0.0f;

	///是否“延时销毁光效可见性”
	///支持：
	///	
	///注意：
	///	
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsDelayDestroyVisibility = true;

	///是否“交换光效目标单位”
	///支持：
	///	为了简化光效配置，此处提供了交换目标的选项
	///		如“从A的手向B的脚发射一支弓箭”，交换目标后变成“从B的手向A的脚发射一支弓箭”，而不是“从B的脚向A的手倒着飞回来一支弓箭”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint32 bIsSwap : 1;

	///光效目标点1
	///	描述“光效目标点”的表现
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FEFFECT_TRANSFORM_DATA FirstTransform;

	///光效目标点2
	///	描述“光效目标点”的表现
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FEFFECT_TRANSFORM_DATA SecondTransform;

	///是否“强制绑定光效可见性”
	///支持：
	///	对于非绑定的光效，可以选择强制跟随其释放者的可见性
	///注意：
	///	只对“非绑定”的光效生效
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint32 bIsBindingVisibility : 1;

	///子光效列表
	///支持：
	///	光效激活时，触发播放一批子光效
	///		触发光效的申请者是原光效的申请者，触发光效的申请目标是原光效的申请目标
	///注意：
	///	可能导致循环触发，请自行规避循环风险
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> ChildrenEffectList;

	///是否“连带销毁子光效”
	///支持：
	///	光效销毁时，是否连带销毁子光效（@CST-2026）
	///		是：连带销毁全部子光效
	///		否：不销毁子光效，子光效继续自行播放
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsDestroyChildren;

	///死亡光效列表
	///支持：
	///	光效死亡时，触发播放一批子光效
	///		触发光效的申请者、申请目标，都是原光效Actor本身（如陨石爆炸，不是陨石撞到的人爆炸，而是陨石自己爆炸）
	///注意：
	///	可能导致循环触发，请自行规避循环风险
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> DeathEffectList;

	virtual ~FBASEEFFECT_DATA() {}

	///只比对基础属性
	bool operator==(FBASEEFFECT_DATA& OtherData)
	{
		if (FMath::Abs(DelayPlayTime - OtherData.DelayPlayTime) < 0.01f &&
			FMath::Abs(DelayDestroyTime - OtherData.DelayDestroyTime) < 0.01f &&
			SecondTransform == OtherData.SecondTransform &&
			FirstTransform == OtherData.FirstTransform &&
			FMath::Abs(LifeTime - OtherData.LifeTime) < 0.01f &&
			bIsSwap == OtherData.bIsSwap)
		{
			return true;
		}
		return false;
	}
};

///真空地带特效数据（@CST-4787）
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSHELTER_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///真空地带：是否“使用绝对位置坐标”
	///	是：配合“缺口绝对位置”参数，使用绝对坐标描述缺口的位置
	///	否：配合“缺口位置检测用光效ID”参数，使用指定光效来指定缺口的位置
	///吐槽：
	///	和前面的绑定有什么区别？
	///	放过一次之后，位置就不变了
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsBind;

	///真空地带：缺口位置检测用光效ID
	//	缺口对应的圆形光效ID（@DT_EffectCfg）
	///支持：
	///	寻找附近的指定ID的光效，获取其位置，然后制作指定大小的缺口表现
	///注意：
	///	寻找的是光效缺口的位置
	///	是否使用绝对位置坐标＝否时，此参数才生效
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ShelterEffectID;

	///真空地带：缺口绝对位置
	///吐槽：
	///	？？？
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector ShelterPosition;

	///真空地带：圆形缺口的半径（10厘米）
	///吐槽：
	///	建议后续优化，改成以毫米为单位
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float ShelterRadius;

	virtual ~FSHELTER_DATA() {}

	///只比对基础属性
	bool operator==(FSHELTER_DATA& OtherData)
	{
		if (IsBind == OtherData.IsBind &&
			!ShelterEffectID.Compare(OtherData.ShelterEffectID) &&
			FMath::Abs(ShelterRadius - OtherData.ShelterRadius) < 0.01f&&
			ShelterPosition == OtherData.ShelterPosition)
		{
			return true;
		}
		return false;
	}
};

///飞行光效
USTRUCT(BlueprintType)
struct CHUANGSHI_API FFLY_DATA
{
	GENERATED_USTRUCT_BODY()
public:

	///飞行光效：是否“指定时间抵达”
	///	是，代表“按指定时间抵达，不会提前抵达”
	///	否，代表“按指定速度飞行，但可能追不上”
	///注意：
	///	脚本类型：BP_FlyEffect、ParabolaEffectEmitter限定
	///	（包括：BP_SpiralEffectEmitter、BP_SpecialEffectEmitter等）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FlyEffect")
		bool bIsFlyByTime = false;

	///飞行光效：指定飞行时间（秒）
	///支持：
	///	在“按指定速度飞行”飞行速度表现类型时，描述飞行所需的时间
	///注意：
	///	脚本类型：BP_FlyEffect、ParabolaEffectEmitter限定
	///	（包括：BP_SpiralEffectEmitter、BP_SpecialEffectEmitter等）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FlyEffect", meta = (EditCondition = "bIsFlyByTime"))
		float FlyTime = 0.0f;

	///飞行光效：指定飞行速度（厘米/秒）
	///支持：
	///	在“按指定时间抵达”飞行速度表现类型时，描述飞行的速度
	///注意：
	///	脚本类型：BP_FlyEffect、ParabolaEffectEmitter限定
	///	（包括：BP_SpiralEffectEmitter、BP_SpecialEffectEmitter等）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FlyEffect", meta = (EditCondition = "!bIsFlyByTime"))
		float FlySpeed = 0.f;

	///飞行光效：飞行重力加速度（默认-980）
	///注意：
	///	脚本类型：BP_ParabolaEffectEmitter、BP_ParabolaRanHighEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FlyGravityZ")
		FString FlyGravityZ;

	///飞行光效：飞行最大高度随机值（最小最大值之间，用分割符“|”）
	///注意：
	///	脚本类型：BP_ParabolaRanHighEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FlyMaxHighRan")
		FString FlyMaxHighRan;

	///飞行光效：抵达光效列表（@DT_EffectCfg）
	///支持：
	///	飞行光效抵达时，触发一个光效表现（一般都是简单光效）
	///		对于“按指定时间抵达”，是“时间到的时候”触发
	///		对于“按指定速度飞行”，是“追上”的时候触发
	///		触发光效的申请者是原光效的申请者，触发光效的申请目标是原光效的申请目标
	///注意：
	///	脚本类型：BP_FlyEffect、ParabolaEffectEmitter限定
	///	（包括：BP_SpiralEffectEmitter、BP_SpecialEffectEmitter等）
	///	可能导致循环触发，请自行规避循环风险
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FlyEffect")
		TArray<FString> FlyArriveEffectList;

	///残留模型表现：静态模型资源
	///支持：
	///	撞墙时，残留一个模型表现（@CST-10306）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UStaticMesh> MotionBlurMeshAsset;

	///残留模型表现：残留时间（秒）
	///支持：
	///	渐变时间 单位秒（s）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float bIsMotionBlurTime = 0.0f;

	///残留模型表现：静态模型资源变形
	///支持：
	///	描述“残留模型”的形变修正：位置、旋转、缩放
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FTransform  MotionBlurMeshTransform;
};

///分段飞行光效
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSPECIAL_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///分段飞行光效：是否开启曲线运动
	///	冰凰符飞行表现：是否“做第二阶段的曲线运动”（@CST-5361）
	///注意：
	///	脚本类型：BP_IceBirdEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SpecialEffect")
		bool bCanSpecialMove = false;
	
	///分段飞行光效：开启距离（米）
	///	冰凰符飞行表现：距离目标多远开始第二阶段曲线运动（@CST-5361）
	///注意：
	///	脚本类型：BP_IceBirdEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SpecialEffect", meta = (EditCondition = "bCanSpecialMove"))
		float TransformationDistance = 0.0f;
	
	///分段飞行光效：上升距离（≤0米代表“不做曲线运动”）
	///	冰凰符飞行表现：第二阶段曲线运动的上升高度（@CST-5361）
	///注意：
	///	脚本类型：BP_IceBirdEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SpecialEffect", meta = (EditCondition = "bCanSpecialMove"))
		float RisingDistance = 0.0f;

	///分段飞行光效：起点高度偏移（米）
	///	获得宝物表现：起飞头顶的距离（@CST-7372）
	///注意：
	///	脚本类型：BP_SpecialEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SpecialEffect")
		float SourceHeight = 0.f;

	///分段飞行光效：终点高度偏移（米）
	///	获得宝物表现：降落头顶的距离（@CST-7372）
	///注意：
	///	脚本类型：BP_SpecialEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SpecialEffect")
		float TargetHeight = 0.f;
};

///螺旋线光效
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSPIRAL_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///螺旋线光效：偏角增量（角度）
	///	大概就是“水平方向”的初始偏航角
	///注意：
	///	脚本类型：BP_SpiralEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SpiralEffect")
		float DeltaAngleZ = 0.0f;

	///螺旋线光效：仰角增量（角度）
	///	大概就是“竖直方向”的初始俯仰角
	///注意：
	///	脚本类型：BP_SpiralEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SpiralEffect")
		float DeltaAngleXY = 0.0f;
};

///连线光效
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBEAM_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///连线光效：是否“随目标弯曲”
	///注意：
	///	脚本类型：BP_BeamEffect限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "BeamEffect")
		bool IsBendFromTarget;

	///连线光效：“随目标弯曲”的强度
	///注意：
	///	脚本类型：BP_BeamEffect限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "BeamEffect", meta = (EditCondition = "IsBendFromTarget"))
		float BendStrength = 0.0f;

	///连线光效：扰动强度
	///注意：
	///	脚本类型：BP_BeamEffect限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "BeamEffect")
		float ParticleRange = 1.0f;

	///连线光效：粒子强度（＝0代表“弱到看不到”）
	///	粒子强度越大，看起来连线越粗
	///注意：
	///	脚本类型：BP_BeamEffect限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "BeamEffect")
		float ParticleSize = 1.0f;	
};

///拖尾光效
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTRAIL_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///拖尾光效：拖尾模式类型
	///注意：
	///	脚本类型：BP_TrailEffect限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "TrailEffect")
		TEnumAsByte<enum ETrailWidthMode> Trail_WidthScaleMode = ETrailWidthMode::ETrailWidthMode_FromCentre;
};

///环形光效
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCIRCLE_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///环形光效：粒子是否在缩放
	///注意：
	///	脚本类型：CircleEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CircleEffect")
		bool IsMove;

	///环形光效：粒子发射器初始发射的数量（注意，如果发射的粒子太多可能会出现显示不出来，配置的时候需注意）
	///注意：
	///	脚本类型：CircleEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CircleEffect")
		float StartSpawnNum;

	///环形光效：粒子发射器圆柱发射初始半径
	///注意：
	///	脚本类型：CircleEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CircleEffect")
		float StartRadius;

	///环形光效：粒子缩放总时间
	///注意：
	///	脚本类型：CircleEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CircleEffect", meta = (EditCondition = "IsMove"))
		float TotalTime;

	///环形光效：粒子移动间隔时间（即每隔多久移动一下）
	///注意：
	///	脚本类型：CircleEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CircleEffect", meta = (EditCondition = "IsMove"))
		float IntervalTime;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FEFFECT_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///通用
	///	描述一般的光效行为（@CST-1661）
	///注意：
	///	所有脚本都适用
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "BaseEffect")
		FBASEEFFECT_DATA BaseEffectData;
	///飞行脚本用
	///	描述飞行表现的参数（@CST-1661）
	///注意：
	///	脚本类型：BP_FlyEffect限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "FlyEffect")
		FFLY_DATA FlyData;
	///（分段扩展）飞行脚本用
	///	描述分段飞行表现的参数（@CST-3850）
	///注意：
	///	脚本类型：BP_SpecialEffectEmitter、BP_IceBirdEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SpecialEffect")
		FSPECIAL_DATA SpecialData;
	///（螺线扩展）飞行脚本用
	///	描述螺线飞行表现的参数（@CST-4053）
	///注意：
	///	脚本类型：BP_SpiralEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "SpiralEffect")
		FSPIRAL_DATA SpiralData;
	///连线光效脚本用
	///	描述连线光效表现的参数（@CST-2074）
	///注意：
	///	脚本类型：BP_BeamEffect限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "BeamEffect")
		FBEAM_DATA BeamData;
	///拖尾光效脚本用
	///	描述拖尾光效表现的参数（@CST-2026）
	///注意：
	///	脚本类型：BP_TrailEffect限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "TrailEffect")
		FTRAIL_DATA TrailData;
	///真空地带特效脚本用
	//	描述一个光效罩子中间被打出一个洞的表现（@CST-4787）
	///注意：
	///	脚本类型：ShelterEffectEmitter限定
	///吐槽：
	///	这个脚本名称没有遵守规范啊喂
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ShelterEffect")
		FSHELTER_DATA ShelterData;
	///环形发射光效脚本用
	///	描述环形发射光效表现的参数（@CST-10407）
	///注意：
	///	脚本类型：CircleEffectEmitter限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CircleEffect")
		FCIRCLE_DATA CircleEffectData;

	virtual ~FEFFECT_DATA() {}

	///只比对基础属性
	bool operator==(FEFFECT_DATA& OtherData)
	{
		if (BaseEffectData == OtherData.BaseEffectData)
		{
			return true;
		}
		return false;
	}
};

UENUM(BlueprintType)
enum class RESPONSE_TYPE : uint8
{
	///碰撞开始事件
	BEGIN_COLLISION		UMETA(DisplayName = "BEGIN_COLLISION"),
	///碰撞结束事件
	END_COLLISION		UMETA(DisplayName = "END_COLLISION"),
};

UENUM(BlueprintType)
enum class PARAMS_TYPE : uint8
{
	BULLETBUFF		UMETA(DisplayName = "BULLETBUFF"),
	OtherEntityID	UMETA(DisplayName = "OtherEntityID"),
	SKILLID			UMETA(DisplayName = "SKILLID"),
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FMETHOD_NAME
{
	GENERATED_USTRUCT_BODY()
public:
	///碰撞效果：碰撞效果名
	///支持：
	///	不同类型，决定着不同的参数定义
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString MethodName;

	///碰撞效果：参数列表
	///支持：
	///	功能由具体碰撞效果类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<PARAMS_TYPE> ParamsList;

	FMETHOD_NAME()
	{
		MethodName = "onBulletCollisionBegin";
		ParamsList.Add(PARAMS_TYPE::BULLETBUFF);
	}
};

//碰撞响应数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FEFFECT_COLLISION_RESPONSE
{
	GENERATED_USTRUCT_BODY()
public:
	///碰撞检测：触发时机
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		RESPONSE_TYPE TriggerType;

	///重叠检测：是否激活“碰撞重叠事件检测”
	///设计原意：
	///	为了避免“一直站在风扇中间不动”或“一直跟着光效跑”导致“只能碰到进入的一次”，增加了“重叠时”的触发
	///		可以理解为，“碰撞开始时”的一个【补丁】
	///支持：
	///	在目标与光效互相重叠时，周期性地触发光效碰撞事件
	///注意：
	///	目前在子弹表现中，“重叠事件”的表现与“碰撞开始时”一致
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsLoopResponse = true;

	///重叠检测：检测周期时间（默认1秒）
	///注意：
	///	激活“重叠时触发”时，此参数才生效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (EditCondition = "bIsLoopResponse"))
		float LoopTime = 1.0f;

	///撞墙检测：是否激活“撞墙事件检测”
	///设计原意：
	///	为了让子弹可以被墙壁挡住，而设（@CST-9523）
	///支持：
	///	创建针对性的范围检测，在碰到墙壁时触发撞墙事件（@CST-9523）
	///		子弹撞墙触发（需要配合BuffBullet的Param5使用）
	///		撞墙后，移除光效
	///注意：
	///	此处的“墙壁”指的是，“与地板碰撞通道相同”的物件，如“水面”、“浮台”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsObstructible = false;

	///撞墙检测：是否激活“撞墙检测范围显示”
	///支持：
	///	可以显示具体的判定区域，方便配置与调试（@CST-9523）
	///注意：
	///	激活“撞墙事件”时，此参数才生效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (EditCondition = "bIsObstructible"))
		bool bIsDebug = false;

	///撞墙检测：Box检测范围大小（厘米）
	///支持：
	///	可以自定义判断区域的形状，以匹配不同的子弹形状与飞行速度（@CST-9523）
	///注意：
	///	激活“撞墙事件”时，此参数才生效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (EditCondition = "bIsObstructible"))
		FVector HalfSize = FVector::OneVector;

	///撞墙检测：Box检测范围旋转
	///支持：
	///	可以自定义判断区域的形状，以匹配不同飞行轨迹的形状（@CST-9523）
	///注意：
	///	激活“撞墙事件”时，此参数才生效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (EditCondition = "bIsObstructible"))
		FVector HalfRotator = FVector::ZeroVector;

	///撞墙检测：忽略类型对象
	///注意：
	///	不影响“碰撞检测”的判断
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<TSubclassOf<AActor>> ActorsToIgnore;

	///碰撞检测：客户端Actor类型要求
	///	客户端Actor类型：举例
	///		None：没有
	///		Actor：全部单位
	///		ServerCharacter：服务器单位（默认值，@CST-12420）
	///		BP_Character：PC/玩家角色
	///		BP_Monster：怪物
	///		BP_VehiclePet：幻兽
	///		BP_SpellBox：施法盒子
	///		BP_Trap：陷阱
	///注意：
	///	不影响“撞墙检测”的判断
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSubclassOf<AActor> ActorType;

	///碰撞检测：服务器单位类型要求（留空代表“没有要求”）
	///	服务器单位类型：（@csconst.ENTITY_TYPE_DICT）
	///		Role：PC/玩家角色（@csdefine.ENTITY_FLAG_ROLE）
	///		Monster：怪物
	///		Pet：幻兽
	///		SpellBox：施法盒子
	///		Trap：陷阱
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString EntityType;

	///碰撞检测：碰撞响应调用的技能ID，需要配合RESPONSE_TYPE::SKILLID使用
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ResponseSkillID = 1;

	///碰撞检测：碰撞响应效果列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FMETHOD_NAME> MethodList;

	FEFFECT_COLLISION_RESPONSE()
	{
		TriggerType = RESPONSE_TYPE::BEGIN_COLLISION;
		ActorType = AServerCharacter::StaticClass();
		MethodList.Add(FMETHOD_NAME());
	}
};

//声音效果
USTRUCT(BlueprintType)
struct CHUANGSHI_API FAUDIO_EFFECT
{
	GENERATED_USTRUCT_BODY()
public:
	///音频：资源
	///支持：
	///	播放SoundWave资源（@/Game/Medias/Sounds/）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<class USoundBase> AudioAsset;

	///音频：是否“循环播放”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsLoop;

	///音频：备注
	///	无任何功能，仅供策划记录及查看
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "说明")
		FString Description;
};

///路径资源
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSPLINE_ASSET
{
	GENERATED_USTRUCT_BODY()
public:
	///路径：资源
	///支持：
	///	依据曲线路径资源，更新粒子形变的表现（如@BP_Spline_Circle_Stand）
	///	可以触发光效抵达事件
	///注意：
	///	移动结束，表现为停在路径的终点
	///	已知风险：粒子形变覆盖（@CST-10942）
	///		目前“路径表现”的实现依赖“粒子组件”的形变，运行中将覆盖“粒子组件”的形变配置，请谨慎使用
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftClassPtr<class ABaseSplineAsset> SplineAsset;
	
	///路径：位置，是否“世界的”
	///	是，代表“路径”的位置是“世界的”
	///	否，代表“路径”的位置是“相对的”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint32 IsLocationOnWorld : 1;

	///路径：旋转，是否“世界的”
	///	是，代表“路径”的旋转是“世界的”
	///	否，代表“路径”的旋转是“相对的”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint32 IsRotationOnWorld : 1;

	///路径：缩放，是否“世界的”
	///	是，代表“路径”的缩放是“世界的”
	///	否，代表“路径”的缩放是“相对的”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint32 IsScaleOnWorld : 1;

	///路径：形变
	///支持：
	///	描述“路径”的形变修正：位置、旋转、缩放
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FTransform SplineTransform;

	///路径：移动速度（厘米/秒）
	///支持：
	///	描述沿着路径前景的绝对速度
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float MoveSpeed = 0.0f;

	///路径：循环次数（0次代表“一直循环，永不停止”）
	///支持：
	///	指定让光效在路径上的循环次数
	///注意：
	///	循环意味着“到了终点后，立刻回到起点重新开始”，路径不闭合也没关系
	///	达到指定次数后，移动结束，表现为停在路径的终点
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 LoopNumber = 0;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FMODEL_ASSET
{
	GENERATED_USTRUCT_BODY()
public:
	///骨骼模型：资源
	///支持：
	///	显示骨骼模型及使其播放动作表现（@/Game/Meshs/SkeletonMeshs/UnShare/）
	///注意：
	///	骨骼模型表现不支持碰撞响应，目前只有静态模型支持碰撞响应
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<class USkeletalMesh> SkeletalMeshAsset;

	///骨骼模型：形变
	///支持：
	///	描述“骨骼模型”的形变修正：位置、旋转、缩放
	///注意：
	///	已知风险：表现组件层级不自然（@CST-3262）
	///		目前“骨骼模型组件”为“粒子系统组件”的下级，因此模型的形变会受到粒子形变的影响，请谨慎使用
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FTransform SkeletalMeshTransform;

	///骨骼模型：动画资源列表（留空代表“T-Pose”）
	///支持：
	///	光效激活时，模型循环播放列表第一个资源（@/Game/Meshs/SkeletonMeshs/UnShare/）
	///注意：
	///	需要配合“骨骼匹配”的骨骼模型资源使用
	///	光效死亡时，动作表现暂停，表现为“动作卡住了”
	///吐槽：
	///	既然只有第一个动作有用，那为什么要做成一个列表呢？
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<TSoftObjectPtr<class UAnimationAsset>> AnimAssetList;

	///骨骼模型：动画播放速率（倍）
	///注意：
	///	与动画资源本身的速度，是乘法的表现
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float PlayRate = 1.0f;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTATICMESH_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	///静态模型：资源
	///支持：
	///	显示静态模型表现（@/Game/Effects/Meshs/）
	///	在静态模型发生碰撞时，可以触发碰撞事件（详见“碰撞响应”组件配置）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UStaticMesh> StaticMeshAsset;

	///静态模型：形变
	///支持：
	///	描述“静态模型”的形变修正：位置、旋转、缩放
	///注意：
	///	已知风险：表现组件层级不自然（@CST-3262）
	///		目前“静态模型组件”为“粒子系统组件”的下级，因此模型的形变会受到粒子形变的影响，请谨慎使用
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FTransform StaticMeshTransform;

	///静态模型：可见性设置
	///支持：
	///	设置静态模型的可见性（如：子弹光效的碰撞盒子只需要碰撞，不需要显示）
	///注意：
	///	此设定与EffectData里的“是否强制绑定光效可见性”相关，在光效Actor、静态模型同时可见时，静态模型才表现为可见
	///	静态模型不可见时，碰撞触发也依然有效
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool StaticMeshVisibility;

	///静态模型：碰撞设置
	///支持：
	///	设置静态模型的碰撞设置（@CST-10571）
	///注意：
	///	未归入碰撞通道管理，使用时请主动确认碰撞表现（@CST-9491）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TEnumAsByte< enum ECollisionResponse >CollisionResponse = ECollisionResponse::ECR_Overlap;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FEFFECT_EMITTER_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///光效表现脚本类型说明
	///支持：
	///	①None（无脚本）
	///		默认选项，没有表现
	///
	///	②BP_BeamEffect（连线表现光效脚本）
	///		连线表现：“在目标点1和目标点2之间形成连线”的表现（@CST-1661、@CST-2074）
	///		连线动态弯曲表现（@CST-3993）
	///
	///	③BP_FlyEffect（直线飞行表现脚本）
	///		直线飞行表现：“光效从目标1飞向目标2”的表现（@CST-1661）
	///
	///	④BP_IceBirdEffectEmitter（冰凰符飞行表现脚本）
	///		扩展飞行表现，冰凰符：先飞行一段，快到达目标2时，先上升再俯冲（@CST-5361）
	///
	///	⑤BP_NavigationEmitter（寻路指引专用表现脚本）
	///		寻路指引表现：一个光效带领玩家移动（@CST-5305）
	///
	///	⑥BP_ShelterEffectEmitter（真空地带专用表现脚本）
	///		光效残缺表现：两个圆形的光效相碰，其中一个出现缺口（@CST-4787）
	///
	///	⑦BP_SimpleEffect（普通光效表现脚本）
	///		普通光效表现：在目标点2上播放一个光效表现（@CST-1661）
	///
	///	⑧BP_SpecialEffectEmitter（宝物获取表现脚本）
	///		扩展飞行表现，宝物获取：从A身上飞出一个光效，非过去，接一个光效到B身上（@CST-3850）
	///
	///	⑨BP_SpiralEffectEmitter（曲线飞行表现脚本）
	///		曲线飞行表现：螺旋线形式的飞行表现（@CST-4053）
	///
	///	⑩BP_TrailEffect（拖尾表现脚本）
	///		拖尾表现：怪物跳跃出场后面拖个尾巴（@CST-2026）
	///
	///	⑫DecalEffectNewEmitter（贴花光效表现脚本）
	///		贴花表现：把材质贴在不透明的表面上的表现（@CST-2063）
	///		支持程序在光效材质里调控参数，实现虚化扭曲和消散表现（@CST-3790）
	///
	///	⑪DecalEffectEmitter（贴花光效表现脚本）
	///	【已废弃，请改用DecalEffectNewEmitter】贴花表现（@CST-2063）
	///	⑬ShelterEffectEmitter（真空地带专用表现脚本）
	///	【已废弃，请改用BP_ShelterEffectEmitter】请勿使用（@CST-4787）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "EffectInstance")
		TSoftClassPtr<class AEffectEmitter> EffectInstance;	

	///光效表现数据
	///支持：
	///	描述不同光效脚本表现的细节
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "EffectData")
		FEFFECT_DATA EffectData;

	///粒子系统组件
	///支持：
	///	描述粒子系统组件表现的细节
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ParticleSystem")
		FPARTICLE_DATA ParticleData;

	///静态模型组件
	///支持：
	///	描述静态模型组件表现的细节（@CST-3262）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "StaticMesh")
		FSTATICMESH_DATA StaticMesh;

	///骨骼模型组件
	///支持：
	///	描述骨骼模型组件表现的细节（@CST-1922）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "SkeletalMesh")
		FMODEL_ASSET SkeletalMesh;

	///音频组件
	///支持：
	///	描述音效组件表现的细节（@CST-4355）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Audio")
		FAUDIO_EFFECT Audio;

	///路径组件
	///支持：
	///	描述路径组件表现的细节，让策划可以自定义光效的位置移动（@CST-2368）
	///注意：
	///	需要配合Spline资源使用（如@BP_Spline_Circle_Stand）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Spline")
		FSPLINE_ASSET Spline;

	///碰撞响应组件
	///支持：
	///	描述静态组件碰撞响应事件触发表现的细节（@CST-4238）
	///注意：
	///	一般保留默认配置即可支持子弹使用，更复杂的配置建议联系程序同仁处理
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "CollisionResponse")
		TArray<FEFFECT_COLLISION_RESPONSE> CollisionResponse;

	FEFFECT_EMITTER_DATA()
	{
		CollisionResponse.Add(FEFFECT_COLLISION_RESPONSE());
	}

	///备注
	///	无任何功能，仅供策划记录及查看
	///	策划同人应当备注明确光效配置的语境、维护人员，以方便后续维护跟进
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "备注")
		FString Remarks;

	bool operator==(FEFFECT_EMITTER_DATA& OtherData)
	{
		if (EffectInstance == OtherData.EffectInstance &&
			EffectData == OtherData.EffectData &&
			ParticleData == OtherData.ParticleData)
		{
			return true;
		}

		return false;
	}

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		if (ParticleData.ParticleSystemAsset.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(ParticleData.ParticleSystemAsset.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"ParticleSystem.ParticleSystemAsset\" resource does not exist"));
			}
		}
		if (StaticMesh.StaticMeshAsset.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(StaticMesh.StaticMeshAsset.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"StaticMesh.StaticMeshAsset\" resource does not exist"));
			}
		}
		if (SkeletalMesh.SkeletalMeshAsset.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(SkeletalMesh.SkeletalMeshAsset.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"SkeletalMesh.SkeletalMeshAsset\" resource does not exist"));
			}
		}
		if (Audio.AudioAsset.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(Audio.AudioAsset.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"Audio.AudioAsset\" resource does not exist"));
			}
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

USTRUCT()
struct CHUANGSHI_API FStateParticles
{
	GENERATED_BODY()

	UPROPERTY()
		TArray<int32> EffectUIDList;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FEFFECT_PRELOAD_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///粒子预加载列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> PreLoadList;

	///预加载地图的名称为逻辑关卡的名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "备注")
		FString Description;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FPARTICLE_DIAPLAY
{
	GENERATED_BODY()

	///最大数量（个）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MaxCount;

	///粒子数量限制：距离 ≤10米
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap<PARTICLE_TYPE, int32> NEARCount;

	///粒子数量限制：距离 10~40米
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap<PARTICLE_TYPE, int32> MIDDELCount;

	///粒子数量限制：距离 ≥40米
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap<PARTICLE_TYPE, int32> FARCount;

	FPARTICLE_DIAPLAY()
	{
		MaxCount = 0;
		//粒子距离表
		NEARCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_PLAYER, 0);
		NEARCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_OTHERPLAYER, 0);
		NEARCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_PIN, 0);
		NEARCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_PIOP, 0);
		NEARCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_NPC, 0);
		NEARCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_SCENE, 0);

		MIDDELCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_PLAYER, 0);
		MIDDELCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_OTHERPLAYER, 0);
		MIDDELCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_PIN, 0);
		MIDDELCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_PIOP, 0);
		MIDDELCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_NPC, 0);
		MIDDELCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_SCENE, 0);

		FARCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_PLAYER, 0);
		FARCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_OTHERPLAYER, 0);
		FARCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_PIN, 0);
		FARCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_PIOP, 0);
		FARCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_NPC, 0);
		FARCount.Add(PARTICLE_TYPE::TYPE_PARTICLE_SCENE, 0);
	}
};