// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "GameData/GameDeFine.h"
#include "Util/CS3Debug.h"
#include "SkillTableData.generated.h"

/**
* 文件名称：SkillTableData.h
* 功能说明：
* 文件作者：ranxuanwen
* 目前维护：xuyongqi
* 创建时间：2017-08-21
*/

///主动技能脚本类型
UENUM(BlueprintType)
enum class ENUM_SKILL_CLASS_TYPE : uint8
{
	///CombatSkill（主动引导技能）
	///	Param1~4：无
	///	Param5：标记列表（|竖号分隔，留空代表“没有标记”，具体功能与参数格式由标记定义）
	///		示例：“IsReTPRandom:随机半径”，代表“执行目标位置随机偏移”
	///设计原意：
	///	可自定义的灵活的“既定打击流程”（@CST-1356）
	///支持：
	///	继承：InstantSkill
	///	引导流程、中断（@CST-1356）
	///	情景免疫：引导占位，避免施法者同时施展多个技能（@CST-1356）
	///		引导技能受“引导占位”制约，若引导数量已满，则新的引导技能将施展失败
	///		暂定“同时引导技能数量上限”＝1（@CST-1771）
	///注意：
	CombatSkill = 0 UMETA(DisplayName = "CombatSkill"),
	///InstantSkill（主动瞬发技能）
	///	Param1~4：无
	///	Param5：标记列表（|竖号分隔，留空代表“没有标记”，具体功能与参数格式由标记定义）
	///		示例：“IsReTPRandom:随机半径”，代表“执行目标位置随机偏移”
	///设计原意：
	///	不受引导占位制约的，随时使用的瞬发的主动技能
	///支持：
	///	开关条件、自定义条件、冷却、消耗、施法表现、瞬发流程（@CST-987）
	///	打击作用范围、受术者条件、受术者排序、命中判定、添加技能效果（@CST-987）
	///	技能事件：技能施法开始/结束时（@CST-1206）
	///注意：
	///	打击列表中的“HitTime”参数配置无效（修正为0秒），表现为“立即触发”（@CST-2555）
	///	瞬发技能不受“引导中占位”制约，可以在引导中施展，不影响引导进行（@CST-1771）
	InstantSkill = 1 UMETA(DisplayName = "InstantSkill"),
	///SkillJump（跳劈技能）
	///	Param1：延迟跳劈时间，配合动作表现用（秒）
	///	Param2：跳劈持续时间，配合动作表现用（秒）
	///		不论距离远近，表现都是固定时间，如“距离＝0”表现为“原地跳劈”
	///	Param3~5：无
	///设计原意：
	///	野蛮人的跳劈（配合固定时长的动作）
	///支持：
	///	继承：CombatSkill
	///	跳劈表现：延迟X秒后，位移X秒，直到引导结束（@CST-888）
	///注意：
	///	施法者单位类型：非PC限定
	SkillJump = 2 UMETA(DisplayName = "SkillJump"),
	///SkillItemSpar（炼化晶核技能）
	///	Param1：炼化音效ID（@DT_AudioCfg，留空代表“非仙化技能”）
	///	Param2：炼化开始动作ID（留空代表“没有表现”）
	///	Param3：炼化持续动作ID（同上）
	///	Param4：炼化结束动作ID（同上）
	///	Param5：无
	///支持：
	///	继承：SkillItemBase
	///	吸收晶核表现、功能待定（@CST-2033）
	///注意：
	///	使用方法：“通过道具ItemSpar使用”限定
	///	施法者单位类型：PC限定（@\CS3_Server\res\scripts\data\Skill\SkillCasterDefine.py）
	SkillItemSpar = 3 UMETA(DisplayName = "SkillItemSpar"),
	///SkillItemPetEgg（孵化幻兽蛋技能）
	///	Param1~5：无
	///支持：
	///	继承：SkillItemBase
	///	孵化幻兽表现：孵化“幻兽蛋”、解除“封印幻兽蛋”（@CST-1867）
	///		相关配置已转移到道具配置中，需要配合道具使用（@CST-8757）
	///		技能配置的重点转向了“表现”：动作表现、读条文字、条件判断、引导中断……等（@CST-8757）
	///注意：
	///	施法者单位类型：PC限定（@\CS3_Server\res\scripts\data\Skill\SkillCasterDefine.py）
	///	使用方法：“通过道具ItemPetEgg使用”限定
	///		通过【/spell】，直接使用技能无效，因为缺少道具相关的目标幻兽信息
	///		通过【/addItem】，直接添加的“封印幻兽蛋”无效，因为跳过了“封印”操作，缺少相关幻兽信息
	SkillItemPetEgg = 4 UMETA(DisplayName = "SkillItemPetEgg"),
	///SkillCharge（冲锋技能）
	///	Param1：冲锋速度（＜0修正为“0米/秒”，＝0代表“没有冲锋”）
	///		服务器位移速度有≤50米/秒的限制，实际上为了同步表现正确，建议速度表现≤25米/秒
	///	Param2：冲锋距离（＜0修正为“0米”，＝0代表“没有冲锋”）
	///	Param3~5：无
	///设计原意：
	///	农药里项羽的冲锋（无锁定的）
	///支持：
	///	继承：CombatSkill
	///	冲锋表现：冲锋前转向目标，过程中一直引导（@CST-629/@CST-1813/@CST-3295）
	///		“冲锋移动”即使被中断，技能引导也不会中断（以表达“怼在墙上继续顶”），可按需配置“移动停止时中断”
	///	支持PC使用（@CST-6806）
	///		PC的“主动移动”会中断“冲锋移动”，请按需配置“持有定身”或“移动开始时中断”
	///		PC的“真位移动作”会中断“冲锋移动”，请避免配置“真位移”的施法动作
	///注意：
	///	已废弃：“蓄力表现”支持，请使用“吟唱表现”替代（@CST-4907、@CST-8282）
	///	已知风险：由于位置同步与延迟问题（详见事务说明），冲锋技能可能会遗漏路上的目标（@CST-6806）
	///		对表现要求不高的场合，可以适当放宽打击范围，利用重叠和CD来提供冗余，以避免遗漏
	///		对表现要求精确的场合，建议使用“子弹方案”加以补充，详见DT_SkillCfg中相关配置示例，以避免遗漏
	///	已知风险：技能持续时间和冲锋持续时间接近时，冲锋位移可能播放不完整（@CST-6806）
	///		建议预留0.3秒以上的无位移后摇时间，以保障位移完整
	SkillCharge = 5 UMETA(DisplayName = "SkillCharge"),
	///SkillSpellBox（场景物件交互技能）
	///	Param1~5：无
	///支持：
	///	继承：CombatSkill
	///	交互表现：技能吟唱结束后，通知技能施展目标SpellBox单位，完成交互（@CST-8744）
	///		已经不再需要配合EffectSpellBox使用（@CST-8744）
	///注意：
	///	施展目标类型：TargetLock限定（@CST-2761）
	///	受术者单位类型：SpellBox限定（依赖SpellBox单位限制交互，如“避免多人同时交互”）
	///	一般地，“F键交互”应视为“交互行为”，相关开关条件应默认配置“禁止交互（ForbidTalk）”（@CST-4581）
	SkillSpellBox = 6 UMETA(DisplayName = "SkillSpellBox"),
	///SkillChase（追击技能）
	///	Param1：追击速度（＜0修正为“0米/秒”，＝0代表“没有追击，不会触发追击抵达”）
	///		服务器位移速度有≤50米/秒的限制，实际上为了同步表现正确，建议速度表现≤25米/秒
	///	Param2：追击截止距离（＜0修正为“0米”，如0.5表现为“追至距离目标0.5米时停下”）
	///		若“初始距离≤截止距离”，则修正为“立即抵达，不位移”
	///	Param3：追击抵达时触发的技能ID（@DT_SkillCfg，留空代表“靠近后啥都不干”）
	///		追击子技能的“施法距离”，应当＞追击技能的“追击截止距离”，以避免子技能施展失败
	///		尤其是PC使用时，子技能的施法距离应该至少增加2米的设计冗余（详见@CST-6806）
	///	Param4~5：无
	///设计原意：
	///	农药里亚瑟的追击（锁定目标的跟随表现）
	///支持：
	///	继承：CombatSkill
	///	追击表现：尾行目标，距离足够接近时停止移动，并怼目标一下（@CST-2601）
	///		若“追击移动”被中断，则技能引导中断（以表达“追击被阻挠”），无需配置
	///		若“追击移动”直到技能引导结束仍未追上，则停止移动，不会触发追击抵达
	///	支持PC使用（@CST-6806）
	///		PC的“主动移动”会中断“冲锋移动”，请按需配置“持有定身”或“移动开始时中断”
	///		PC的“真位移动作”会中断“冲锋移动”，请避免配置“真位移”的施法动作
	///	技能施展目标类型自适应（@CST-6339）
	///注意：
	///	已废弃：“蓄力表现”支持，请使用“吟唱表现”替代（@CST-4907、@CST-8282）
	///	已知风险：支持“追击触发追击”，可能循环触发致使服务器崩溃，请谨慎使用（@CST-8282）
	///	已知风险：“追击截止距离”的具体表现误差，与技能配置相关（详见@CST-3026）
	///		建议“追击速度”小些，“截止距离”大些，“抵达技能的前摇”短些，以保障将误差控制在容易接受的范围
	SkillChase = 7 UMETA(DisplayName = "SkillChase"),
	///SkillMountOnPet（坐骑骑乘技能）
	///	Param1：延迟开车时间，配合吹口哨上马等动作表现用（秒）
	///	Param2~5：无
	///支持：
	///	继承：CombatSkill
	///	功能待定（@CST-2909）
	///注意：
	///	施法者单位类型：PC限定
	SkillMountOnPet = 8 UMETA(DisplayName = "SkillMountOnPet"),
	///SkillSpellBoxExtTeleportStone（传送石技能）
	///	Param1~5：无
	///支持：
	///	继承：SkillSpellBox
	///	交互表现：技能吟唱结束后，通知技能施展目标SpellBox单位，完成交互（@CST-8744）
	///		已经不再需要配合EffectSpellBox使用（@CST-8744）
	///	传送石相关专用功能待定（@CST-2452）
	///注意：
	///	施展目标类型：TargetLock限定（@CST-2761）
	///	施法者单位类型：PC限定（@\CS3_Server\res\scripts\data\Skill\SkillCasterDefine.py）
	///	受术者单位类型：SpellBox限定（依赖SpellBox单位限制交互，如“避免多人同时交互”）
	///	一般地，“F键交互”应视为“交互行为”，相关开关条件应默认配置“禁止交互（ForbidTalk）”（@CST-4581）
	SkillSpellBoxExtTeleportStone = 9 UMETA(DisplayName = "SkillSpellBoxExtTeleportStone"),
	///SkillCanyonCharge（穿越峡谷冲刺技能）
	///	Param2：冲刺速度（厘米/秒）
	///	Param2：冲刺持续时间（秒）
	///	Param3：用于摧毁巨石的BuffID（@DT_BuffCfg，功能待定）
	///	Param4：Temp临时值（字符串，需要配合陷阱行为TrapNormalSetTemp使用，功能待定）
	///	Param5：无
	///支持：
	///	继承：CombatSkill
	///	穿越峡谷专用，冲刺表现：功能待定（@CST-2146）
	///	速度叠加：支持与SkillCanyonCharge、多个EffectAddSpeed同时作用，速度表现为“矢量和”
	///注意：
	///	施法者单位类型：PC限定
	///	使用方法：“需要配合BuffHoldThroughCanyon使用”限定
	SkillCanyonCharge = 10 UMETA(DisplayName = "SkillCanyonCharge"),
	///SkillSing（“吟唱”技能）
	///	Param1：引导结束后触发的技能ID（@DT_SkillCfg，不得缺省）
	///	Param2~5：无
	///设计原意：
	///	用一个完整的技能来描述“吟唱表现”，在这一个技能引导结束之后，触发下一个技能（@CST-6164）
	///支持：
	///	继承：CombatSkill
	///	传递技能申请：存储“技能申请”相关信息，在引导结束后，发送“技能申请”（@CST-6164）
	///		触发时机在“原技能结束”之后，可实现“引导接续引导”
	///	技能施展目标类型自适应（@CST-6339）
	///		技能施展时，将依据技能施展目标类型的要求，对技能申请目标进行适当的修正
	///	　申请TargetNothing
	///		施展TargetNothing，	施展目标【单位】＝申请者【单位】（原配）
	///		施展TargetLock，		   施展目标【单位】＝申请者【单位】
	///		施展TargetPosition，	施展目标【位置】＝申请者【单位】的【位置】（修正）
	///	　申请TargetLock
	///		施展TargetNothing，	施展目标【单位】＝申请者【单位】
	///		施展TargetLock，		   施展目标【单位】＝申请目标【单位】（原配）
	///		施展TargetPosition，	施展目标【位置】＝申请目标【单位】的【位置】（修正）
	///	　申请TargetPosition
	///		施展TargetNothing，	施展目标【单位】＝申请者【单位】
	///		施展TargetLock，		   施展目标【单位】＝无【单位】，申请失败（不作修正）
	///		施展TargetPosition，	施展目标【位置】＝申请目标【位置】（原配）
	///注意：
	///	已知风险：支持“吟唱触发吟唱”，可能循环触发致使服务器崩溃，请谨慎使用（@CST-6164）
	///反思：
	///	其实“申请TargetPosition，施展TargetLock”的情况，也有修正的空间
	///		曾考虑修正为，“在目标位置，创建一个受术者傀儡，作为技能施展目标”
	///	此处选择不修正，主要考虑是，若支持修正，则可能导致“策划与玩家都不易理解”
	///		策划在配置过程中，并不会考虑“若锁定技能的目标变成了傀儡，要如何容错”
	///		玩家也不会考虑“这些技能如果对着空气放会怎样”
	///		一般来说，即使修正使技能可以施展成功，其表达的意义也已经改变，不再可控（因为一般不会去补充这些情况的定义）
	SkillSing = 11 UMETA(DisplayName = "SkillSing"),
	///SkillFillFloor（仙岛归墟填充格子用技能）
	///	Param1~5：无
	///支持：
	///	继承：CombatSkill
	///	环任务“仙岛归墟”，填充格子用技能（@CST-6096）
	///注意：
	///	施展目标类型：TargetPosition限定（@CST-6096）
	///	施法者单位类型：PC限定
	SkillFillFloor = 12 UMETA(DisplayName = "SkillFillFloor"),
	///CombatSkillClient（客户端主动引导技能）
	///	Param1~5：无
	///支持：
	///	客户端版本的CombatSkill（@CST-9038）
	CombatSkillClient = 14 UMETA(DisplayName = "CombatSkillClient"),
	///InstantSkillClient（客户端瞬发引导技能）
	///	Param1~5：无
	///支持：
	///	客户端版本的InstantSkill（@CST-9038）
	InstantSkillClient = 15 UMETA(DisplayName = "InstantSkillClient"),
	///SkillClientJump（客户端跳劈技能）
	///	Param1：延迟跳劈时间，配合动作表现用（秒）
	///	Param2：跳劈持续时间，配合动作表现用（秒）
	///		不论距离远近，表现都是固定时间，如“距离＝0”表现为“原地跳劈”
	///	Param3~5：无
	///支持：
	///	客户端版本的SkillJump（@CST-9038）
	SkillClientJump = 16 UMETA(DisplayName = "SkillClientJump"),
	///SkillClientCharge（客户端冲锋技能）
	///	Param1：冲锋速度（＜0修正为“0米/秒”，＝0代表“不冲锋”）
	///	Param2：冲锋距离（＜0修正为“0米”）
	///	Param3~5：无
	///支持：
	///	客户端版本的SkillCharge（@CST-9038）
	SkillClientCharge = 17 UMETA(DisplayName = "SkillClientCharge"),
	///SkillClientSing（客户端“吟唱”技能）
	///	Param1：引导结束后触发的技能ID（@DT_SkillCfg，不得缺省）
	///	Param2~5：无
	SkillClientSing = 18 UMETA(DisplayName = "SkillClientSing"),
	///SkillSoldierCmdUseSkillToEntity（玩家指挥士兵技能 对目标施法）
	///	Param1：指挥士兵使用的技能ID（@DT_SkillCfg，不得缺省）
	///	Param2~5：无
	///支持：
	///	功能待定（@CST-8891）
	///注意：
	///	施法者单位类型：PC限定
	SkillSoldierCmdUseSkillToEntity = 19 UMETA(DisplayName = "SkillSoldierCmdUseSkillToEntity"),
	///SkillSoldierCmdUseSkillToPosition（玩家指挥士兵技能 对位置施法）
	///	Param1：指挥士兵使用的技能ID（@DT_SkillCfg，不得缺省）
	///	Param2~5：无
	///支持：
	///	功能待定（@CST-8891）
	///注意：
	///	施法者单位类型：PC限定
	SkillSoldierCmdUseSkillToPosition = 20 UMETA(DisplayName = "SkillSoldierCmdUseSkillToPosition"),
	///SkillSoldierCmdUseSkillToSelf（玩家指挥士兵技能 对自身施法）
	///	Param1：指挥士兵使用的技能ID（@DT_SkillCfg，不得缺省）
	///	Param2~5：无
	///支持：
	///	功能待定（@CST-8891）
	///注意：
	///	施法者单位类型：PC限定
	SkillSoldierCmdUseSkillToSelf = 21 UMETA(DisplayName = "SkillSoldierCmdUseSkillToSelf"),
};

///主动技能，目标类型
UENUM(BlueprintType)
enum class ENUM_CAST_TARGET_TYPE : uint8
{
	///TargetNothing（对自己施法）
	///设计原意：
	///	“无需选定目标”的施法形式
	///支持：
	///	技能施展目标类型自适应（@CST-6339）
	///	　发送申请时，初始化“技能申请目标信息”（以“客户端PC主动施法”为例）
	///		技能申请者　【单位】＝客户端PC【单位】
	///		技能申请目标【单位】＝客户端PC【单位】
	///	　技能施展时，初始化“技能施展目标信息”（收到的申请有可能类型不符）
	///		技能施法者　【单位】＝技能申请者【单位】
	///		技能施展目标【单位】＝技能申请者【单位】
	///反思：
	///	实现上，变成了“不管选中谁，都是向自己施法”，其实叫“TargetSelf”更合适
	TargetNothing = 0 UMETA(DisplayName = "TargetNothing"),
	///TargetLock（对锁定单位施法）
	///设计原意：
	///	“对已选定目标施法”的施法形式
	///		若客户端锁定目标为“空”，则修正为“PC单位对自身施法”
	///支持：
	///	技能施展目标类型自适应（@CST-6339）
	///	　发送申请时，初始化“技能申请目标信息”（以“客户端PC主动施法”为例）
	///		技能申请者　【单位】＝客户端PC【单位】
	///		技能申请目标【单位】＝客户端UI锁定的【单位】
	///	　技能施展时，初始化“技能施展目标信息”（收到的申请有可能类型不符）
	///		技能施法者　【单位】＝技能申请者【单位】
	///		技能施展目标【单位】＝技能申请目标【单位】（若技能申请目标类型＝【位置】，则不修正，返回申请失败）
	///		，则，不修正，返回申请失败
	///	施法辅助支持（@CST-3198）
	///		辅助目标选择、辅助追击、辅助转向
	TargetLock = 1 UMETA(DisplayName = "TargetLock"),
	///TargetPosition（对指定位置施法）
	///设计原意：
	///	“对鼠标指定位置施法”的施法形式
	///支持：
	///	技能施展目标类型自适应（@CST-6339）
	///	　发送申请时，初始化“技能申请目标信息”（以“客户端PC主动施法”为例）
	///		技能申请者　【单位】＝客户端PC【单位】
	///		技能申请目标【位置】＝客户端UI辅助指定的【位置】
	///	　技能施展时，初始化“技能施展目标信息”（收到的申请有可能类型不符）
	///		技能施法者　【单位】＝技能申请者【单位】
	///		技能施展目标【位置】＝技能申请目标【位置】（或修正为，技能申请目标【单位】的【位置】）
	///	施法辅助支持（@CST-3198）
	///		辅助目标选择、辅助范围指示器、辅助追击、辅助转向
	///反思：
	///	目前“目标位置”信息只有“坐标”，不包含其他信息（如，地图名称）
	TargetPosition = 2 UMETA(DisplayName = "TargetPosition"),
};

///技能施法碰撞类型（@GameDefine.COLLISION_TYPE）
UENUM(BlueprintType)
enum class ENUM_CAST_COLLISION_TYPE : uint8
{
	///COLLISION_DEFAULT（默认碰撞）
	///支持：
	///	技能引导过程中，维持默认碰撞表现，不作改变（@CST-2386）
	COLLISION_DEFAULT = 0 UMETA(DisplayName = "COLLISION_DEFAULT"),
	///COLLISION_ENEMY（碰撞敌对单位）
	///支持：
	///	技能引导过程中，施法位移将会受到敌对单位的阻挡
	///注意：
	///	施法者单位类型：PC限定（@CST-2386）
	///	已知风险：怪物尚未支持施法位移表现，请谨慎使用（@CST-883）
	COLLISION_ENEMY = 1 UMETA(DisplayName = "COLLISION_ENEMY"),
};

///辅助显示“施法范围指示器”
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_ASSIST_EFFECT
{
	GENERATED_BODY()
	///范围指示器表现用光效ID（@DT_EffectCfg）
	///	需要配合符合规范的贴花粒子资源使用（@CST-3538）
	///支持：
	///	对位置施法时，提供施法范围指示表现
	///	支持水面贴花表现（@CST-3538）
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
	FString DecalEffectID;
	///范围指示器大小
	///	X：“施法者单位视角的”左右方向长度（厘米，左右各半）
	///	Y：“施法者单位视角的”前后方向长度（厘米，前后各半）
	///	Z：“铅直方向”长度（厘米，上下各半）
	///支持：
	///	描述范围的大小（@CST-3538）
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FVector DecalSize;
};

///技能冷却数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_COOL_DOWN
{
	GENERATED_BODY()
	///冷却ID（整型，需要配合具体冷却配置使用）
	///注意：
	///	冷却ID，暂无占位表，请谨慎使用，注意避让
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 CooldownId = 0;
	///冷却持续时间（秒，＝0代表“受其制约，但不产生此CD”）
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		float CoolDownTime;
};

///技能消耗类型
UENUM(BlueprintType)
enum class ENUM_SKILL_REQUIRE_TYPE : uint8
{
	///RequireMP（消耗MP）
	///	Param1：MP消耗固定值（点）
	///	Param2：MP消耗百分比（如0.5代表“50%MP上限”）
	///支持：
	///	消耗结算：消耗＝上限×消耗百分比＋消耗固定值
	///		有效范围：消耗量≥0
	///注意：
	///	允许扣完
	RequireMp = 1 UMETA(DisplayName = "RequireMp"),
	///RequireHP（消耗HP）
	///	Param1：HP消耗固定值（点）
	///	Param2：HP消耗百分比（如0.5代表“50%HP上限”）
	///支持：
	///	消耗结算：消耗＝上限×消耗百分比＋消耗固定值
	///		有效范围：消耗量≥0
	///注意：
	///	不允许扣完，要求至少剩余1点HP，以避免导致死亡（@CST-1356）
	RequireHp = 2 UMETA(DisplayName = "RequireHp"),
	///RequireGangQi（消耗罡气）
	///	Param1：罡气消耗固定值（点）
	///	Param2：罡气消耗百分比（如0.5代表“50%罡气上限”）
	///		查询：可以通过【/queryAttr gangQiValue】，查询【当前罡气值】属性
	///		查询：可以通过【/queryAttr gangQiState】，查询【罡气状态】属性（1气盈|2气短|3气竭|4气绝，@csdefine.GANG_QI_STATE_QI_YING）
	///支持：
	///	消耗结算：消耗＝上限×消耗百分比＋消耗固定值
	///		有效范围：消耗量≥0
	///注意：
	///	不允许扣完，要求至少剩余1点罡气，以避免导致气竭（@CST-1356）
	RequireGangQi = 3 UMETA(DisplayName = "RequireGangQi"),
	///RequireCostItem（消耗道具）
	///	Param1：消耗道具ID（@DT_ItemDataCfg）
	///	Param2：消耗道具数量（个，≤0代表“不消耗，但要求拥有”）
	///支持：
	///	要求，当前道具数量≥消耗道具数量（@CST-4141）
	///注意：
	///	允许扣完
	///	相同ID的道具，依据“获得顺序”，后入先出，表现为先消耗后获得的道具
	///	金钱被视为“资源”（依赖PC的属性存储），而不是“道具”（依赖背包的道具信息存储）
	RequireCostItem = 4 UMETA(DisplayName = "RequireCostItem"),
};

///技能使用消耗
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_REQUIRE
{
	GENERATED_BODY()
	///消耗资源类型
	///	不同类型，决定着不同的参数定义
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		ENUM_SKILL_REQUIRE_TYPE Type = ENUM_SKILL_REQUIRE_TYPE::RequireMp;
	///参数1（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString Param1;
	///参数2（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString Param2;
};

///技能使用条件类型
UENUM(BlueprintType)
enum class ENUM_USE_CONDITION_TYPE : uint8
{
	///ConditionTypeRelation（单位类型与敌对关系条件）
	///	Param1：技能目标单位类型列表（|竖号分隔，留空代表“无要求”）
	///		Role：PC/玩家角色（@csconst.ENTITY_TYPE_DICT）
	///		Monster：怪物
	///		Pet：幻兽
	///		SpellBox：施法盒子
	///		Trap：陷阱
	///		查询：可以通过【/queryAttr entityFlag】，查询【单位类型】属性
	///		示例：“Role|Monster|Pet”，代表“玩家、怪物、幻兽”
	///	Param2：敌对关系列表（|竖号分隔，留空代表“无要求”）
	///		1：友好的（@csdefine.COMBAT_RELATION_NORMAL）
	///		2：敌对的
	///		3：中立的
	///		4：无关的
	///		查询：可以通过【/queryRelation】，查询【施受双方的敌对关系】判定结果
	///	Param3：无
	///注意：
	///	目前只支持填写“宏观分类”，使用时需要注意单位类型的具体分类（@CS3_Server\res\scripts\cell\ObjectScript\*\*.py）
	///		如Monster包括：MonsterExtTiShen（替身）、MonsterExtXinMo（心魔）、MonsterExtCall（召唤物）…等
	ConditionTypeRelation = 0 UMETA(DisplayName = "ConditionTypeRelation"),
	///ConditionRate（成功率条件）
	///	Param1：成功率值（如0.5代表“50%成功”，不得缺省）
	///	Param2~3：无
	///反思：
	///	目前成功率判定与施受双方都无关，以后可以考虑引入相关影响，如幸运值
	ConditionRate = 1 UMETA(DisplayName = "ConditionRate"),
	///ConditionState（单位基础状态条件）
	///	Param1：单位基础状态列表（|竖号分隔，不得缺省）
	///		0：未决（@csdefine.ENTITY_STATE_PEAD）
	///		1：自由
	///		2：警戒
	///		3：战斗
	///		4：死亡
	///		5：重置（怪物限定）
	///		6：表演（怪物限定）
	///		7：摆摊
	///		8：稳定（怪物限定）
	///		查询：可以通过【/queryAttr state】，查询【单位基础状态】属性
	///	Param2：要求类型（缺省0）
	///		0：非“处于上述状态”
	///		1：是“处于上述状态”
	///	Param3：无
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“无法通过条件检测”
	ConditionState = 2 UMETA(DisplayName = "ConditionState"),
	///ConditionPropertyCount（属性值条件）
	///	Param1：通用单位属性类型（留空表现为“肯定找不到对应属性，必然无法通过条件检测”）
	///		查询：通过【/queryAttr 指定属性名】可以查询的【数值类型】属性，都可以使用
	///		示例：“level”，代表“以目标单位的等级属性为判断依据”
	///	Param2：要求类型（不得缺省）
	///		0：＝等于
	///		1：＞大于
	///		2：＜小于
	///		3：≥大于等于
	///		4：≤小于等于
	///		5：≠不等于
	///	Param3：数量指标（浮点型，不得缺省）
	///支持：
	///	补充通用的属性支持（@CST-3053）
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“无法通过条件检测”
	ConditionPropertyCount = 3 UMETA(DisplayName = "ConditionPropertyCount"),
	///ConditionPropertyPercent（资源存量条件）
	///	Param1：“存量”辅助属性类型（留空表现为“肯定找不到对应属性，必然无法通过条件检测”）
	///		HP：当前生命值/生命值上限
	///		MP：当前法力值/法力值上限
	///		gangQiValue：当前罡气值/罡气值上限
	///		查询：此类“辅助属性”不存在，只在需要时临时产生，可以理解为“技术指标”，暂无法查询
	///			可以通过如【/queryAttr HP_Max】，查询【具体指定属性】，再进行推算
	///	Param2：要求类型（不得缺省）
	///		0：＝等于
	///		1：＞大于
	///		2：＜小于
	///		3：≥大于等于
	///		4：≤小于等于
	///		5：≠不等于
	///	Param3：数量指标（浮点型，不得缺省）
	///支持：
	///	补充一批辅助属性支持（@CST-3053）
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“无法通过条件检测”
	///示例：
	///	①要求满血时不准喝药（应该描述为，血量比例＜100%）
	///		Param1：HP（生命值比率）
	///		Param2：2（＜小于）
	///		Param3：1（100%）
	ConditionPropertyPercent = 4 UMETA(DisplayName = "ConditionPropertyPercent"),
	///ConditionDistance（相对距离条件）
	///	Param1：“距离”辅助属性类型（留空表现为“肯定找不到对应属性，必然无法通过条件检测”）
	///		3D：三维距离
	///		2D：水平距离
	///		Z：垂直距离
	///		查询：此类“辅助属性”不存在，只在需要时临时产生，可以理解为“技术指标”，暂无法查询
	///			可以通过【/queryAttr position】，查询【位置】属性，再进行推算
	///	Param2：要求类型（不得缺省）
	///		0：＝等于
	///		1：＞大于
	///		2：＜小于
	///		3：≥大于等于
	///		4：≤小于等于
	///		5：≠不等于
	///	Param3：数量指标（浮点型，不得缺省）
	///支持：
	///	补充一批辅助属性支持（@CST-3053）
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“无法通过条件检测”
	ConditionDistance = 5 UMETA(DisplayName = "ConditionDistance"),
	///ConditionPropertySubtract（属性值差距条件）
	///	Param1：通用“差值”辅助属性类型（不得缺省）
	///		查询：通过【/queryAttr 指定属性名】可以查询的【数值类型】属性，都可以使用
	///		示例：“level”，代表“以目标单位的等级属性为判断依据”
	///	Param2：要求类型（不得缺省）
	///		0：＝等于
	///		1：＞大于
	///		2：＜小于
	///		3：≥大于等于
	///		4：≤小于等于
	///		5：≠不等于
	///	Param3：数量指标（浮点型，不得缺省）
	///支持：
	///	通用的属性对比支持：都是指“施法者－受术者”的该属性差值（@CST-3053）
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“无法通过条件检测”
	///示例：
	///	①等级比我低的单位伤害翻倍（应当描述为，等级差＞0）
	///		Param1：level（等级）
	///		Param2：1（＞大于）
	///		Param3：0（0级）
	ConditionPropertySubtract = 6 UMETA(DisplayName = "ConditionPropertySubtract"),
	///ConditionBuffCount（指定ID的Buff个数条件）
	///	Param1：BuffID列表（@DT_BuffCfg，|竖号分隔，不得缺省）
	///		查询：可以通过【/queryBuff】，查询【Buff列表】属性，再进行推算
	///		示例：“99900103|99900104”，代表“其中任一Buff达到数量要求即可”而不是“数量加起来达到要求”
	///	Param2：要求类型（不得缺省）
	///		0：＝等于
	///		1：＞大于
	///		2：＜小于
	///		3：≥大于等于
	///		4：≤小于等于
	///		5：≠不等于
	///	Param3：数量指标（浮点型，不得缺省）
	///支持：
	///	确认“指定Buff的个数”是否满足要求（@CST-3053）
	///		无指定Buff，视为0个；N层的指定Buff，视为1个
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“无法通过条件检测”
	///示例：
	///	①要求拥有紧急回避Buff（应当描述为，指定ID的Buff个数≥1）
	///		Param1：90000101（紧急回避霸体的BuffID）
	///		Param2：3（≥大于等于）
	///		Param3：1（1个）
	ConditionBuffCount = 7 UMETA(DisplayName = "ConditionBuffCount"),
	///ConditionBuffLayer（指定ID的Buff层数条件）
	///	Param1：BuffID（@DT_BuffCfg，不得缺省）
	///		查询：可以通过【/queryBuff】，查询【Buff列表】属性，再进行推算
	///	Param2：要求类型（不得缺省）
	///		0：＝等于
	///		1：＞大于
	///		2：＜小于
	///		3：≥大于等于
	///		4：≤小于等于
	///		5：≠不等于
	///	Param3：数量指标（浮点型，不得缺省）
	///支持：
	///	确认“指定Buff的层数”是否满足要求（@CST-3053）
	///		无指定Buff，视为0层；多个非叠加的指定Buff，视为1层
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“无法通过条件检测”
	ConditionBuffLayer = 8 UMETA(DisplayName = "ConditionBuffLayer"),
	///ConditionPropertyAssemble（属性值是否属于指定集合条件）
	///	Param1：通用单位属性类型（不得缺省）
	///		profession：职业（1战士|2剑客|3刺客|4法师|5强防，@csdefine.CLASS_FIGHTER）
	///		gangQiState：罡气状态（1气盈|2气短|3气竭|4气绝，@csdefine.GANG_QI_STATE_QI_YING）
	///		camp：阵营（1仙道|2魔道|3中立敌对|4中立友好，@csdefine.CAMP_TAOSIM）
	///		faction：势力（@\CS3_Server\res\scripts\data\FactionRelationConfig.json）
	///		tempCamp：临时阵营（同“阵营”）
	///		tempFaction：临时势力（同“势力”）
	///		查询：通过【/queryAttr 指定属性名】可以查询的【枚举类型】属性，都可以使用
	///	Param2：要求类型（不得缺省）
	///		1：是“以下选项之一”
	///		0：非“以下选项之一”
	///	Param3：目标集合，即目标属性取值列表（|竖号分隔，不得缺省）
	///支持：
	///	描述指定属性值，是否“属于”指定的目标集合之中（@CST-3053）
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“无法通过条件检测”
	ConditionPropertyAssemble = 9 UMETA(DisplayName = "ConditionPropertyAssemble"),
	///ConditionEnemy（敌对关系条件）
	///	Param1：敌对关系列表（|竖号分隔，不得缺省）
	///		1：友好的（@csdefine.COMBAT_RELATION_NORMAL）
	///		2：敌对的
	///		3：中立的
	///		4：无关的
	///		查询：可以通过【/queryRelation】，查询【施受双方的敌对关系】判定结果
	///	Param2：要求类型（不得缺省）
	///		1：是“以下选项之一”
	///		0：非“以下选项之一”
	///	Param3：无
	///支持：
	///	判断“施法者→受术者”的敌对关系（@CST-3053）
	///		敌对关系未必是对称的，使用时需要注意方向
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“无法通过条件检测”
	ConditionEnemy = 10 UMETA(DisplayName = "ConditionEnemy"),
	///ConditionRelationAssemble（社交关系条件）
	///	Param1：“社交关系”辅助属性类型（留空表现为“肯定找不到对应属性，必然无法通过条件检测”）
	///		Self：自己
	///		Pet：我的幻兽（PC限定）
	///		Enemy：敌人（敌人列表）
	///		Team：队友（PC限定，队友列表）
	///		CallMonster：随从（PC限定，随从列表）
	///		Owner：我的主人（幻兽、随从、替身限定）
	///		查询：可以通过如【/queryAttr enemyList】，查询【敌人列表】属性，再进行推算
	///	Param2：要求类型（不得缺省）
	///		1：是“属于对应列表之中”
	///		0：非“属于对应列表之中”
	///	Param3：无
	///支持：
	///	补充，我的敌人列表、我的幻兽…等判断（@CST-3053）
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“无法通过条件检测”
	ConditionRelationAssemble = 11 UMETA(DisplayName = "ConditionRelationAssemble"),
	///ConditionType（单位类型条件）
	///	Param1：技能目标单位类型列表（|竖号分隔，留空代表“无要求”）
	///		Role：PC/玩家角色（@csconst.ENTITY_TYPE_DICT）
	///		Monster：怪物
	///		Pet：幻兽
	///		SpellBox：施法盒子
	///		Trap：陷阱
	///		查询：可以通过【/queryAttr entityFlag】，查询【单位类型】属性
	///		示例：“Role|Monster|Pet”，代表“玩家、怪物、幻兽”
	///	Param2：要求类型（不得缺省）
	///		1：是“以下选项之一”
	///		0：非“以下选项之一”
	///	Param3：无
	///支持：
	///	单纯的判断单位类型的条件（@CST-3053）
	///注意：
	///	目前只支持填写“宏观分类”，使用时需要注意单位类型的具体分类（@CS3_Server\res\scripts\cell\ObjectScript\*\*.py）
	///		如Monster包括：MonsterExtTiShen（替身）、MonsterExtXinMo（心魔）、MonsterExtCall（召唤物）等
	///反思：
	///	为了提供可读性，单位类型没有采用序号，而是使用了文字。这同时也引入了一些新的问题
	///		类型间失去了易于识别的“顺序”，配置易乱
	///		拼写检查变得困难
	///		后续考虑通过正则表达式进行相关排查
	ConditionType = 12 UMETA(DisplayName = "ConditionType"),
	///ConditionScriptID（单位脚本ID条件）
	///	Param1：单位ID列表（@DT_MonsterCfg，|竖号分隔，不得缺省）
	///		查询：可以通过【/queryAttr scriptID】，查询【单位脚本ID】属性
	///	Param2：要求类型（不得缺省）
	///		1：是“以下选项之一”
	///		0：非“以下选项之一”
	///	Param3：是否允许PC通过判定（缺省0）
	///		1：是“特批PC通过”
	///		0：非“特批PC通过”
	///支持：
	///	判断目标是否“指定的单位”（@CST-3793）
	///	为PC单位提供特别支持（@CST-7997）
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“无法通过条件检测”
	///		PC没有ScriptID属性，为方便使用额外补充了参数3的支持
	///反思：
	///	参数3的支持，其实很适合用“标记扩展”来描述，在将来类似扩展变多之后，可以考虑参数扩容再标记化
	ConditionScriptID = 13 UMETA(DisplayName = "ConditionScriptID"),
	///ConditionCoolDownTime（指定类型的冷却时间条件）
	///	Param1：冷却类型（整型，不得缺省）
	///		查询：可以通过【/queryAttr attrCooldowns】，查询【单位CD列表】属性，再进行推算
	///	Param2：要求类型（不得缺省）
	///		0：＝等于
	///		1：＞大于
	///		2：＜小于
	///		3：≥大于等于
	///		4：≤小于等于
	///		5：≠不等于
	///	Param3：数量指标（秒，不得缺省）
	///支持：
	///	判断指定CD时间（@CST-3776）
	///注意：
	///	若“负CD”或“无CD”，则实现上有“当前CD时间＝0”，所以判断“有某个CD”应该写“CD时间＞0”
	///示例：
	///	①要求藏空剑的CD时间＜1秒（这里只需要判断，一个条件）
	///	　ConditionCoolDownTime
	///		Param1：200001（藏空剑的冷却类型）
	///		Param2：2（＜小于）
	///		Param3：1（1秒）
	///	②要求藏空剑的CD时间存在且＜1秒（“有CD”并且“当前CD时间＜1”，需要两个条件）
	///	　ConditionCoolDownTime
	///		Param1：200001（藏空剑的冷却类型）
	///		Param2：1（＞大于）
	///		Param3：0（0秒）
	///	　ConditionCoolDownTime
	///		Param1：200001（藏空剑的冷却类型）
	///		Param2：2（＜小于）
	///		Param3：1（1秒）
	ConditionCoolDownTime = 14 UMETA(DisplayName = "ConditionCoolDownTime"),
	///ConditionSkillPosture（心法状态条件）
	///	Param1：心法状态列表（|竖号分隔，不得缺省）
	///		　0：默认心法（@csdefine.SKILL_POSTURE_NONE）
	///		101：天怒心法（战士）
	///		102：神威心法（战士）
	///		201：幻剑心法（剑客）
	///		202：天剑心法（剑客）
	///		301：九幽心法（刺客）
	///		302：雷鸣心法（刺客）
	///		401：寒霜心法（法师）
	///		402：神逸心法（法师）
	///		查询：可以通过【/queryAttr skillPosture】，查询【单位心法状态】属性
	///	Param2：要求类型（不得缺省）
	///		1：是“属于对应列表之中”
	///		0：非“属于对应列表之中”
	///	Param3：无
	///支持：
	///	心法状态相关条件支持（@CST-4778）
	///	支持列表输入（@CST-7259）
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“无法通过条件检测”
	ConditionSkillPosture = 15 UMETA(DisplayName = "ConditionSkillPosture"),
	///ConditionDirection（相对朝向条件）
	///	Param1：“方向”辅助属性类型（不得缺省）
	///		1：目标的绝对水平方向（如“角度＝90”，代表“目标单位朝向西方”）
	///		2：受者在施者哪个水平方向（如“角度＝90”，代表“目标在我左边”）
	///		3：施者在受者哪个水平方向（如“角度＝90”，代表“我在目标左边”）
	///		查询：可以通过【/queryAttr direction】，查询【朝向】属性
	///			可以通过【/queryAttr position】，查询【位置】属性，再进行推算
	///	Param2：角度指标A（角度，不得缺省）|B（缺省＝A）
	///		示例：“270|90”，代表“从右边开始，逆时针转向左边”，表现为“前方”
	///		示例：“90|270”，代表“从左边开始，逆时针转向右边”，表现为“后方”
	///		示例：“90|90”，代表“从左边开始，逆时针转向左边”，表现为“精确的正左边”（而不是“360度都可以”）
	///	Param3：无
	///支持：
	///	判断角度，角度是否在“从角度A【逆时针转向】角度B”的范围内（@CST-6245）
	///		角度方向，从上往下看，逆时针为正（即“右手螺旋定则”）
	///注意：
	///	此类“辅助属性”不存在（也无法查询），只在需要时临时产生，可以理解为“技术指标”
	///	若因位置重叠导致朝向计算失效，则修正为“朝向＝0”，表现为“自己在自己前面”
	ConditionDirection = 16 UMETA(DisplayName = "ConditionDirection"),
	///ConditionJumpShowState（PC跳跃状态条件）
	///	Param1：PC跳跃状态列表（@csdefine.JUMP_SHOW_STATE，|竖号分隔，不得缺省）
	///		0：站立（@csdefine.JUMP_SHOW_STATE_STAND）
	///		7：上升
	///		8：下降（其他“短状态”此略，不影响技能条件判断，仅供动作表现用）
	///		查询：可以通过【/queryAttr jumpShowState】，查询【跳跃状态】属性
	///	Param2：要求类型（缺省0）
	///		0：非“处于上述状态”
	///		1：是“处于上述状态”
	///	Param3：无
	///支持：
	///	判断目标玩家的跳跃状态（@CST-3448）
	///	整合跳跃状态：实际上跳跃状态类型繁多（@csdefine.JUMP_SHOW_STATE），为了策划理解与配置，此处对跳跃状态类型进行了整合
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“无法通过条件检测”
	///		目前只有PC支持该属性，若其他单位使用，则都将无法通过检测
	ConditionJumpShowState = 17 UMETA(DisplayName = "ConditionJumpShowState"),
	///ConditionEffectState（效果状态条件）
	///	Param1：效果状态列表（@csdefine.EFFECT_STATE_LIST，|竖号分隔，不得缺省）
	///		  0：眩晕
	///		  1：霸体
	///		  2：无敌
	///		  3：受击（击退类Buff默认持有）
	///		  4：定身
	///		  5：睡眠
	///		  6：根须缠绕
	///		  7：保护
	///		  8：跟随（包括组队跟随和队友跟随）
	///		  9：混乱
	///		10：不屈
	///		11：冻结
	///		12：表演
	///		13：隐身
	///		查询：可以通过【/queryAttr effectCounter】，查询【效果状态计数器】属性，再进行推算
	///	Param2：要求类型（缺省0）
	///		0：上述状态都是“假”
	///		1：上述状态都是“真”
	///	Param3：无
	///支持：
	///	判断目标的效果状态，以方便调试（@CST-8198）
	///注意：
	///	不适应于判断“单位是否拥有指定的行为能力”
	///		判断行为能力，应当直接使用开关条件参数，而不是自定义条件
	///		“开关”是“条件”、“中断”、“触发”的统一，只描述自定义条件是不完善的
	ConditionEffectState = 18 UMETA(DisplayName = "ConditionEffectState"),
	///ConditionActForbid（开关状态条件）
	///	Param1：开关状态列表（@csdefine.ACTION_FLAG_LIST，|竖号分隔，不得缺省）
	///		  0：禁止主动移动（ForbidMove，@csdefine.ACTION_FORBID_MOVE）
	///		  1：禁止施法（ForbidSpell）
	///		  2：禁止使用道具（ForbidItem）
	///		  3：禁止被攻击（ForbidBeAttack）
	///		  4：禁止攻击（ForbidAttack）
	///		  5：禁止跳跃（ForbidJump）
	///		  6：禁止穿戴装备（ForbidWield）
	///		  7：禁止聊天（ForbidChat）
	///		  8：禁止交互（ForbidTalk）
	///		  9：禁止触发被动技能（ForbidTriggerPassiveSkill）
	///		10：禁止被击退（ForbidBeHitBack）
	///		11：禁止变换模型（ForbidChangeBody）
	///		12：禁止变换姿势（ForbidChangePoseture）
	///		13：禁止召唤幻兽（ForbidConjurePet）
	///		14：禁止改变朝向（ForbidTranslateDirection）
	///		15：禁止紧急回避（ForbidEmergencyExit）
	///		16：禁止幻兽骑乘（ForbidMountPet）
	///		17：禁止被控制（ForbidBeControl）
	///		18：禁止被增益（ForbidBeImpress）
	///		19：禁止被减损（ForbidBeDepress）
	///		查询：可以通过【/queryAttr actCounter】，查询【开关状态计数器】的属性，确认指定开关的状态
	///	Param2：要求类型（缺省0）
	///		0：上述状态都是“假”
	///		1：上述状态都是“真”
	///	Param3：无
	///支持：
	///	判断目标的开关状态，以方便调试（@CST-8198）
	///注意：
	///	不适应于判断“单位是否拥有指定的行为能力”
	///		判断行为能力，应当直接使用开关条件参数，而不是视为自定义条件
	///		“开关”是“条件”、“中断”、“触发”的统一，只描述自定义条件是不完善的
	ConditionActForbid = 19 UMETA(DisplayName = "ConditionActForbid"),
	///ConditionRoleMoveState（PC移动状态条件）
	///	Param1：PC移动状态列表（|竖号分隔，不得缺省）
	///		0：不移动
	///		1：主动移动（@csdefine.ACTIVE_MOVE_LIST）
	///		2：被动移动（@csdefine.PASSIVE_MOVE_LIST）
	///		查询：可以通过【/queryAttr roleMoveType】，查询【玩家移动状态】属性，再进行推算
	///	Param2：要求类型（缺省0）
	///		0：非“处于上述状态”
	///		1：是“处于上述状态”
	///	Param3：无
	///支持：
	///	判断目标玩家的移动状态（@CST-10393）
	///	整合移动状态：实际上移动状态类型繁多（@csdefine.MOVE_TYPE_NONE），为了策划理解与配置，此处对跳跃状态类型进行了整合
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“无法通过条件检测”
	///		目前只有PC支持该属性，若其他单位使用，则都将无法通过检测
	///	特别的，【Numlk键】的“自动移动”的移动类型是2，看来像是“只是帮我按住了W”的感觉
	ConditionRoleMoveState = 20 UMETA(DisplayName = "ConditionRoleMoveState"),
	///ConditionBuffEnergy（能量值条件）
	///	Param1：BuffID（@DT_BuffCfg，不得缺省）
	///	Param2：要求类型（不得缺省）
	///		0：＝等于
	///		1：＞大于
	///		2：＜小于
	///		3：≥大于等于
	///		4：≤小于等于
	///		5：≠不等于
	///	Param3：数量指标（浮点型，不得缺省）
	///支持：
	///	说明：也应当沿用独占判定，确认施法者是否符合要求
	///	若是独占的，且施法者不符合要求，则返回0，代表“目标身上没有合适的Buff”
	ConditionBuffEnergy = 21 UMETA(DisplayName = "ConditionBuffEnergy"),
	///ConditionBelongSide（受术者是否是 攻（守）方）
	///	Param1：(0：攻方，1：守方)
	///	Param2~5：无参数
	///支持：
	///	说明：受术者是否属于 施法者挑战的洞府相关entity
	ConditionBelongSide = 22 UMETA(DisplayName = "ConditionBelongSide"),
};

///技能条件
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_USE_CONDITION
{
	GENERATED_BODY()
	///条件类型
	///	不同类型，决定着不同的参数定义
	UPROPERTY(EditAnywhere)
		ENUM_USE_CONDITION_TYPE ConditionType;
	///参数1（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param1;
	///参数2（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param2;
	///参数3（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param3;
};

///打击作用范围类型
UENUM(BlueprintType)
enum class ENUM_SKILIL_HIT_AREA_TYPE : uint8
{
	///NoRange（空集范围）
	///	Param1~3：无
	///支持：
	///	无任何受术者，受术者列表是“空集”（@CST-2187）
	///	跳过打击流程：若作用范围选择此项，则直接跳过整个打击流程，以节省消耗
	///注意：
	///	常用于“空”的打击配置（如：后摇表现、临时屏蔽配置…）
	NoRange = 0 UMETA(DisplayName = "NoRange"),
	///Single（单体范围）
	///	Param1：单位基准（缺省1）
	///		1：施法者单位
	///		2：施展目标单位（若“施展目标类型＝位置”，则修正为“空集”）
	///	Param2~3：无
	///支持：
	///	选择一个单位（@CST-2187）
	Single = 1 UMETA(DisplayName = "Single"),
	///Sphere（球形范围）
	///	Param1：位置基准（缺省1）
	///		0：地图原点（世界位置0,0,0）
	///		1：施法者当前位置
	///		2：施展目标当前位置（若“施展目标类型＝位置”，则修正为“目标位置”）
	///	Param2：半径（米）
	///	Param3：结果偏移 前|左|上（米）; 起点偏移 前|左|上; 终点偏移 前|左|上（|竖号和;分号分隔）
	///		示例：“0.7|0.7”，代表“向前0.7米，向左0.7米，向上0米”，表现为“结果偏移到左前方约1米远处”
	///		示例：“;0|1|0”，代表“起点向左偏移1米”，表现为“从【施法者左边1米】向【目标】”
	///		示例：“;;1|0|0”，代表“终点向前偏移1米”，表现为“从【施法者】向【目标前方1米】”
	///支持：
	///	以“位置基准”为圆心的，指定半径的，球体范围（@CST-2187）
	///注意：
	///	已废弃：“方向基准”的配置支持（@CST-9076）
	Sphere = 2 UMETA(DisplayName = "Sphere"),
	///Rectangle（矩形范围）
	///	Param1：位置|方向基准（|竖号分隔）
	///	　位置基准（缺省1）
	///		0：地图原点（世界位置0,0,0）
	///		1：施法者当前位置
	///		2：施展目标当前位置（若“施展目标类型＝位置”，则修正为“目标位置”）
	///	　方向基准，决定矩形长边的朝向（缺省＝位置基准）
	///		0：地图X轴方向（世界旋转0,0,0）
	///		1：施法者当前朝向
	///		2：施展目标当前朝向（若“施展目标类型＝位置”，则修正为“施法者单位的当前朝向”）
	///		3：“施法者→目标”水平方向
	///		4：“目标→施法者”水平方向
	///		5：（矩形范围不支持）“施法者→目标”三维方向
	///		6：（矩形范围不支持）“目标→施法者”三维方向
	///	Param2：长，往前（米，不得缺省）|宽，左右各半（米，不得缺省）|高，上下各有（缺省3米）
	///	Param3：结果偏移 前|左|上（米）|左转（角度，从上往下看逆时针为正）; 起点偏移 前|左|上|左转; 终点偏移 前|左|上|左转（|竖号和;分号分隔）
	///		示例：“0.7|0.7”，代表“【结果】向前0.7米，向左0.7米，向上0米”，表现为“偏移到左前方约1米远处”
	///		示例：“0|0|0|90”，代表“【结果】旋转偏移90°”，表现为“向左转”
	///		示例：“;0|1|0”，代表“【起点】向左偏移1米”，表现为“从【施法者左边1米】向【目标】”
	///		示例：“;;1|0|0”，代表“【终点】向前偏移1米”，表现为“从【施法者】向【目标前方1米】”
	///		示例：“;1|0|0;1|0|0”，代表“终点向前偏移1米”，表现为“从【施法者前方1米】向【目标前方1米】”
	///支持：
	///	以“位置基准”为宽边中点，以“方向基准”为长边方向的，矩形柱体范围（@CST-2187）
	///	扩展起点/终点偏移，方便更灵活地调整目标范围（@CST-9076）
	///		“施法者的位置/朝向信息”称为“起点”，可通过“起点偏移”修正
	///		“施展目标的位置/朝向信息”称为“终点”，可通过“终点偏移”修正
	///		以修正后的“起点”和“终点”为输入，计算得到的“输出位置/朝向信息”称为“结果”，可通过“结果偏移”修正
	Rectangle = 3 UMETA(DisplayName = "Rectangle"),
	///Circular（圆形范围）
	///	Param1：位置基准（缺省1）
	///		0：地图原点（世界位置0,0,0）
	///		1：施法者当前位置
	///		2：施展目标当前位置（若“施展目标类型＝位置”，则修正为“目标位置”）
	///	Param2：半径（米，不得缺省）|高，上下各有（缺省3米）
	///	Param3：结果偏移 前|左|上（米）; 起点偏移 前|左|上; 终点偏移 前|左|上（|竖号和;分号分隔）
	///		示例：“0.7|0.7”，代表“向前0.7米，向左0.7米，向上0米”，表现为“结果偏移到左前方约1米远处”
	///		示例：“;0|1|0”，代表“起点向左偏移1米”，表现为“从【施法者左边1米】向【目标】”
	///		示例：“;;1|0|0”，代表“终点向前偏移1米”，表现为“从【施法者】向【目标前方1米】”
	///支持：
	///	以“位置基准”为圆心的，指定半径的，圆形柱体范围（@CST-2187）
	///注意：
	///	已废弃：“方向基准”的配置支持（@CST-9076）
	Circular = 4 UMETA(DisplayName = "Circular"),
	///Sector（扇形范围）
	///	Param1：位置|方向基准（|竖号分隔）
	///	　位置基准（缺省1）
	///		0：地图原点（世界位置0,0,0）
	///		1：施法者当前位置
	///		2：施展目标当前位置（若“施展目标类型＝位置”，则修正为“目标位置”）
	///	　方向基准，决定扇形对称轴的朝向（缺省＝位置基准）
	///		0：地图X轴方向（世界旋转0,0,0）
	///		1：施法者当前朝向
	///		2：施展目标当前朝向（若“施展目标类型＝位置”，则修正为“施法者单位的当前朝向”）
	///		3：“施法者→目标”水平方向
	///		4：“目标→施法者”水平方向
	///		5：（扇形范围不支持）“施法者→目标”三维方向
	///		6：（扇形范围不支持）“目标→施法者”三维方向
	///	Param2：半径（米，不得缺省）|圆心角，左右各半（角度，不得缺省）|高，上下各有（缺省3米）
	///	Param3：结果偏移 前|左|上（米）|左转（角度，从上往下看逆时针为正）; 起点偏移 前|左|上|左转; 终点偏移 前|左|上|左转（|竖号和;分号分隔）
	///		示例：“0.7|0.7”，代表“向前0.7米，向左0.7米，向上0米”，表现为“结果偏移到左前方约1米远处”
	///		示例：“0|0|0|90”，代表“结果偏移【向左转】”
	///		示例：“;0|1|0”，代表“起点向左偏移1米”，表现为“从【施法者左边1米】向【目标】”
	///		示例：“;;1|0|0”，代表“终点向前偏移1米”，表现为“从【施法者】向【目标前方1米】”
	///支持：
	///	以“位置基准”为圆心的，指定角度、高度的，扇形柱体范围（@CST-2187）
	///	扩展起点/终点偏移，方便更灵活地调整目标范围（@CST-9076）
	///		“施法者的位置/朝向信息”称为“起点”，可通过“起点偏移”修正
	///		“施展目标的位置/朝向信息”称为“终点”，可通过“终点偏移”修正
	///		以修正后的“起点”和“终点”为输入，计算得到的“输出位置/朝向信息”称为“结果”，可通过“结果偏移”修正
	Sector = 5 UMETA(DisplayName = "Sector"),
	///Ghost（傀儡受术者范围）
	///	Param1：位置|方向基准（|竖号分隔）
	///	　位置基准，决定傀儡单位的位置（缺省1）
	///		0：地图原点（世界位置0,0,0）
	///		1：施法者当前位置
	///		2：施展目标当前位置（若“施展目标类型＝位置”，则修正为“目标位置”）
	///	　方向基准，决定傀儡单位的朝向（缺省＝位置基准）
	///		0：地图X轴方向（世界旋转0,0,0）
	///		1：施法者当前朝向
	///		2：施展目标当前朝向（若“施展目标类型＝位置”，则修正为“施法者单位的当前朝向”）
	///		3：“施法者→目标”水平方向
	///		4：“目标→施法者”水平方向
	///		5：“施法者→目标”三维方向（如“斜向射击表现”）
	///		6：“目标→施法者”三维方向
	///	Param2：存活时间（缺省1秒）
	///	Param3：结果偏移 前|左|上（米）|左转（角度，从上往下看逆时针为正）; 起点偏移 前|左|上|左转; 终点偏移 前|左|上|左转（|竖号和;分号分隔）
	///		示例：“0.7|0.7”，代表“向前0.7米，向左0.7米，向上0米”，表现为“结果偏移到左前方约1米远处”
	///		示例：“0|0|0|90”，代表“结果偏移【向左转】”
	///		示例：“;0|1|0”，代表“起点向左偏移1米”，表现为“从【施法者左边1米】向【目标】”
	///		示例：“;;1|0|0”，代表“终点向前偏移1米”，表现为“从【施法者】向【目标前方1米】”
	///设计原意：
	///	为了，既实现“对位置产生效果”的同时（如“在指定位置创建光效”），又避免“需要扩展技能效果，支持其位置生效”
	///	因此，此处尝试，直接在指定位置摆一个【临时的单位】（并利用单位既有的支持，来解决同步问题）
	///支持：
	///	傀儡：打击时，临时创建一个傀儡单位，并立即使其作为本次打击的“受术者”（@CST-2187）
	///		傀儡有完整的模型表现（模型ID＝SK_#204，表现为“空盒子”），可按需进行变身、缩放…等操作，以达成一些有趣的表现
	///	扩展起点/终点偏移，方便更灵活地调整目标范围（@CST-9076）
	///		“施法者的位置/朝向信息”称为“起点”，可通过“起点偏移”修正
	///		“施展目标的位置/朝向信息”称为“终点”，可通过“终点偏移”修正
	///		以修正后的“起点”和“终点”为输入，计算得到的“输出位置/朝向信息”称为“结果”，可通过“结果偏移”修正
	///	自适应浮空：若打击目标是“位置”或“浮空的怪物”或“跳跃中的PC”，则傀儡默认“浮空”；否则“贴地”（@CST-6621）
	///		也可以在该傀儡的打击效果列表里，手动添加/移除浮空标志位，使其强制浮空/贴地
	///	自适应平台：若打击目标是“浮台上的单位”，则傀儡默认绑定该浮台（@CST-9112）
	///注意：
	///	已知风险：若作存活时间不够长，则客户端表现（如播放光效）可能表现不完整，建议谨慎配置“存活时间”
	///	已知风险：傀儡的表现同步有延迟，请谨慎使用（@CST-2187）
	///		使用“广播机制”进行同步的效果（如EffectAction、Buff的添加光效），在“傀儡受术者”创建时立即添加无效，需要延迟添加
	Ghost = 6 UMETA(DisplayName = "Ghost"),
	///Annulus（环形范围）
	///	Param1：位置基准（缺省1）
	///		0：地图原点（世界位置0,0,0）
	///		1：施法者当前位置
	///		2：施展目标当前位置（若“施展目标类型＝位置”，则修正为“目标位置”）
	///	Param2：内径（米，不得缺省）|环宽（缺省0米）|高，上下各有（缺省3米）
	///	Param3：位置偏移 前|左|上（米）
	///		示例：“0.7|0.7”，代表“向前0.7米，向左0.7米，向上0米”，表现为“结果偏移到左前方约1米远处”
	///	Param3：结果偏移 前|左|上（米）; 起点偏移 前|左|上; 终点偏移 前|左|上（|竖号和;分号分隔）
	///		示例：“0.7|0.7”，代表“向前0.7米，向左0.7米，向上0米”，表现为“结果偏移到左前方约1米远处”
	///		示例：“;0|1|0”，代表“起点向左偏移1米”，表现为“从【施法者左边1米】向【目标】”
	///		示例：“;;1|0|0”，代表“终点向前偏移1米”，表现为“从【施法者】向【目标前方1米】”
	///支持：
	///	以“位置基准”为圆心的，指定内径、环宽的，环形柱体范围（@CST-5194）
	///注意：
	///	已废弃：“方向基准”的配置支持（@CST-9076）
	Annulus = 7 UMETA(DisplayName = "Annulus"),
	///Owner（主人范围）
	///	Param1：单位基准（缺省1）
	///		1：施法者单位
	///		2：施展目标单位（若“施展目标类型＝位置”，则修正为“空集”）
	///	Param2：幻兽与主人之间的距离上限要求（缺省修正为-1，代表"没有距离要求"）
	///	Param3：无
	///支持：
	///	指定打击目标的“主人”为受术者（@CST-11398）
	///注意：
	///	打击目标的单位脚本类型：幻兽、随从、替身限定（若其他单位类型，没有主人，则返回“受术者列表＝空集”）
	///	距离要求是指“幻兽和它的主人”之间的距离，原意是避免“找到离开幻兽太远的主人”（若需要判断施法者与主人的距离，则应该补充自定义条件）
	///	目前，主人最多只有一个
	Owner = 8 UMETA(DisplayName = "Owner"),
};

///技能打击作用范围
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_HIT_AREA
{
	GENERATED_BODY()
	///打击范围类型
	///	不同类型，决定着不同的参数定义
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ENUM_SKILIL_HIT_AREA_TYPE HitAreaType;
	///参数1（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param1;
	///参数2（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param2;
	///参数3（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param3;
};

///受术者过滤排序类型
UENUM(BlueprintType)
enum class ENUM_FLITER_CONDITION_TYPE : uint8
{
	///OrderByRandom（随机排序）
	///	Param1：受术者数量上限（个，≤0代表“数量不限”）
	///	Param2~3：无
	///设计原意：
	///	避免一些情况下“每次目标顺序都是固定的”
	///支持：
	///	对受术者列表再次进行随机排序（@CST-3053）
	OrderByRandom = 0 UMETA(DisplayName = "OrderByRandom"),
	///OrderByProperty（依据属性值排序）
	///	Param1：通用单位属性类型（留空表现为“肯定找不到对应属性，必然放到最后”）
	///		查询：通过【/queryAttr 指定属性名】可以查询的【数值类型】属性，都可以使用
	///		示例：“level”，代表“以目标单位的等级属性为判断依据”
	///	Param2：排序类型（不得缺省）
	///		0：↘降序（从大到小）
	///		1：↗升序（从小到大）
	///	Param3：受术者数量上限（个，≤0代表“数量不限”）
	///设计原意：
	///	“选中血量最低的目标”之类
	///支持：
	///	对受术者列表依据“单位属性”排序（@CST-3053）
	OrderByProperty = 1 UMETA(DisplayName = "OrderByProperty"),
	///OrderByDistanceToCaster（依据与施法者的相对距离排序）
	///	Param1：“距离”辅助属性类型（留空表现为“肯定找不到对应属性，必然无法通过条件检测”）
	///		3D：三维距离
	///		2D：水平距离
	///		Z：垂直距离
	///		查询：此类“辅助属性”不存在，只在需要时临时产生，可以理解为“技术指标”，暂无法查询
	///			可以通过【/queryAttr position】，查询【位置】属性，再进行推算
	///	Param2：排序类型（不得缺省）
	///		0：↘降序（从大到小）
	///		1：↗升序（从小到大）
	///	Param3：受术者数量上限（个，≤0代表“数量不限”）
	///设计原意：
	///	“选中离施法者最近的目标”之类的
	///支持：
	///	对受术者列表依据“与施法者的距离”排序（@CST-3053）
	///注意：
	///	此类“辅助属性”不存在（也无法查询），只在需要时临时产生，可以理解为“技术指标”
	OrderByDistanceToCaster = 2 UMETA(DisplayName = "OrderByDistanceToCaster"),
	///OrderByDistanceToTarget（依据与施展目标的相对距离排序）
	///	Param1：“距离”辅助属性类型（留空表现为“肯定找不到对应属性，必然无法通过条件检测”）
	///		3D：三维距离
	///		2D：水平距离
	///		Z：垂直距离
	///		查询：此类“辅助属性”不存在，只在需要时临时产生，可以理解为“技术指标”，暂无法查询
	///			可以通过【/queryAttr position】，查询【位置】属性，再进行推算
	///	Param2：排序类型（不得缺省）
	///		0：↘降序（从大到小）
	///		1：↗升序（从小到大）
	///	Param3：受术者数量上限（个，≤0代表“数量不限”）
	///设计原意：
	///	“选中离指定位置最近的目标”之类的
	///支持：
	///	对受术者列表依据“与施展目标的距离”排序（@CST-3053）
	///注意：
	///	此类“辅助属性”不存在（也无法查询），只在需要时临时产生，可以理解为“技术指标”
	OrderByDistanceToTarget = 3 UMETA(DisplayName = "OrderByDistanceToTarget"),
};

///受术者过滤条件类型
USTRUCT(BlueprintType)
struct CHUANGSHI_API FRECEIVER_FLITER_CONDITION
{
	GENERATED_BODY()
	///过滤条件类型
	///	不同类型，决定着不同的参数定义
	UPROPERTY(EditAnywhere)
		ENUM_FLITER_CONDITION_TYPE FliterConditionType;
	///参数1（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param1;
	///参数2（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param2;
	///参数3（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param3;
};

///命中判定类型
UENUM(BlueprintType)
enum class ENUM_HIT_TYPE : uint8
{
	///HitDirect（直接命中）
	HitDirect = 1 UMETA(DisplayName = "HitDirect"),
	///HitDodge（闪避判定）
	///支持：
	///	闪避结算：依据双方的命中率/闪避率，判定命中
	///		打击命中率＝施法者命中率－受术者命中率
	///注意：
	///	闪避，应该理解为“【没打着】”，意味着“啥影响都没有”，表现为“整个打击里的全部效果都不会添加”
	///	免疫，应该理解为“被【打中】了但是一点都【不痛】”，意味着“有些影响没有作用”，表现为“有一些效果，不会添加”
	HitDodge = 2 UMETA(DisplayName = "HitDodge"),
};

///技能打击效果脚本类型
UENUM(BlueprintType)
enum class ENUM_HIT_EFFECT_TYPE : uint8
{
	///EffectAction（表现效果）
	///	Param1：动作ID1:起始帧时间1|动作ID2:起始帧时间2（秒）…（:冒号和|竖号分隔）
	///		示例：“Attack_01|Attack_02:0.5”，代表“顺序播放：从头开始的Attack_01、从0.5秒开始的Attack_02”
	///	Param2：光效ID列表（@DT_EffectCfg，|竖号分隔）
	///	Param3：音效ID列表（@DT_AudioCfg，|竖号分隔）
	///	Param4：标记列表（|竖号分隔，留空代表“没有标记”，具体功能与参数格式由标记定义）
	///		示例：“IsLocal”，代表“只有施法者可见”（@CST-8739）
	///	Param5：无
	///支持：
	///	支持同时播放光效、音效（@CST-2648）
	///	支持动作起始帧时间设定（@CST-1192）
	///	支持连续播放动作：若任一动作中断，则中断连续动作（@CST-3036）
	///	标记扩展（@CST-8739）
	///注意：
	///	已知风险：傀儡的表现同步有延迟，请谨慎使用（@CST-2187）
	///		使用“广播机制”进行同步的效果（如EffectAction、Buff的添加光效），在“傀儡受术者”创建时立即添加无效，建议延迟添加
	EffectAction = 0 UMETA(DisplayName = "EffectAction"),
	///EffectDamage（真实伤害效果）
	///	Param1：伤害百分比（如0.5代表“50%HP上限”）|固定值（整型）
	///	Param2：标记列表（|竖号分隔，留空代表“没有标记”，具体功能与参数格式由标记定义）
	///		示例：“IsSkipEvent”，代表“跳过事件触发及其影响，如连击计数”（@CST-6388）
	///		示例：“IsDoDeadEffect”，代表“击杀目标时，额外触发其被杀特效”（需要配合怪物表的DeadEffect类型2配置，@CST-1619/@CST-1908）
	///		示例：“IsDoPrivateOnKill:99900102”，代表“击杀目标时，额外触发被动技能99900102”（忽视被动技能的响应配置，@CST-8363）
	///	Param3~5：无
	///支持：
	///	情景免疫：死亡免疫（@CST-1635）
	///	伤害结算：依据生命值上限，造成伤害，忽视暴击、护盾、护甲（@CST-1635）
	///		伤害量＝生命值上限×伤害百分比＋伤害固定值
	///	仇恨结算：自然仇恨（@CST-12837）
	///		自然仇恨＝生命值扣除量×受术者自然仇恨系数×施法者造成仇恨修正
	///		自然仇恨下限＝【受术者的】自然仇恨下限
	///		查询：可以通过【/queryAttr hatredList】，查询【怪物的仇恨列表】属性
	///	技能事件：伤害时/被伤害时/击杀时/被击杀时（@CST-1754）
	///		以下情况除外：来源是被动技能（@CST-1206）、来源非技能（@CST-5054）
	///		只有主动技能、Buff流程下的效果才触发技能事件
	///	标记扩展（@CST-8739）
	///注意：
	///	一般地，“伤害”应视为“战斗效果”，相关开关条件应默认配置“禁止受攻击”（ForbidBeAttack）
	EffectDamage = 1 UMETA(DisplayName = "EffectDamage"),
	///EffectItem（获得道具效果）
	///	Param1：获得道具ID（@DT_ItemDataCfg，不得缺省）
	///	Param2：获得道具数量（个，不得缺省）
	///	Param3~5：无
	///注意：
	///	受术者单位类型：PC限定（@\CS3_Server\res\scripts\data\Skill\SkillReceiverDefine.py）
	EffectItem = 3 UMETA(DisplayName = "EffectItem"),
	///EffectXiuWei（获得修为效果）
	///	Param1：获得修为数量（点，不得缺省）
	///	Param2~5：无
	///注意：
	///	受术者单位类型：PC限定（@\CS3_Server\res\scripts\data\Skill\SkillReceiverDefine.py）
	EffectXiuWei = 4 UMETA(DisplayName = "EffectXiuWei"),
	///EffectScene（播放剧情动画效果）
	///	Param1：剧情动画ID（@StoryConfig）
	///	Param2~5：无
	///注意：
	///	受术者单位类型：PC限定（@\CS3_Server\res\scripts\data\Skill\SkillReceiverDefine.py）
	EffectScene = 5 UMETA(DisplayName = "EffectScene"),
	///EffectTeleport（传送到指定位置效果）
	///	Param1：传送目标坐标位置（ 空格分隔，如“-25587 -587 696”，不得缺省）
	///	Param2：传送目标坐标朝向（ 空格分隔，如“0 0 0”，留空代表“不改变朝向”）
	///	Param3~5：无
	///支持：
	///	瞬移到指定坐标位置（@CST-629）
	EffectTeleport = 7 UMETA(DisplayName = "EffectTeleport"),
	///EffectFlyTeleport（飞行传送表现效果）
	///	Param1：飞行路径ID（@DT_FlyPatrolCfg，留空代表“没有效果”）
	///	Param2：载具表现配置ID（@DT_CarrierCfg，留空代表“改为使用参数3”）
	///	Param3：御剑飞行骑乘表现配置ID（@DT_FlyCarrierCfg，缺省“依据阵营选择1或2”，若已配置参数2，则参数3无效）
	///	Param4~5：无
	///支持：
	///	功能待定（@CST-2194）
	///注意：
	///	受术者单位类型：PC限定
	EffectFlyTeleport = 8 UMETA(DisplayName = "EffectFlyTeleport"),
	///EffectTeleportSpace（传送到指定地图效果）
	///	Param1：传送目标地图ID（@DT_HashMapCfg，留空代表“当前地图内传送”）
	///		查询：可以通过【/queryAttr spaceScriptID】，查询【当前地图ID】属性
	///	Param2：传送目标坐标位置（ 空格分隔，如“-25587 -587 696”，不得缺省）
	///	Param3：传送目标坐标朝向（ 空格分隔，如“0 0 0”，不得缺省）
	///	Param4~5：无
	///支持：
	///	传送至指定地图的指定坐标位置（@CST-572）
	///注意：
	///	受术者单位类型：PC限定
	EffectTeleportSpace = 9 UMETA(DisplayName = "EffectTeleportSpace"),
	///EffectAddHP（生命值治疗效果）
	///	Param1：治疗百分比（如0.5代表“50%HP上限治疗”）|固定值（整型）
	///	Param2：标记列表（|竖号分隔，留空代表“没有标记”，具体功能与参数格式由标记定义）
	///		示例：“IsSkipEvent”，代表“跳过事件触发及其影响，如连击计数”（@CST-6388）
	///	Param3~5：无
	///支持：
	///	情景免疫：死亡免疫（@CST-2228）
	///	治疗结算：依据生命值上限，获得生命值治疗（@CST-403）
	///		治疗量＝生命值上限×治疗百分比＋治疗固定值
	///	仇恨结算：自然连带仇恨（@CST-12837）
	///		自然连带仇恨＝生命值恢复量×受术者的敌人的自然连带仇恨系数×施法者造成连带仇恨修正
	///		自然连带仇恨下限＝【受术者的敌人的】自然连带仇恨下限
	///		查询：可以通过【/queryAttr hatredList】，查询【怪物的仇恨列表】属性
	///	技能事件：治疗时/被治疗时（@CST-1206）
	///		以下情况除外：来源是被动技能（@CST-1206）、来源非技能（@CST-5054）
	///		只有主动技能、Buff流程下的效果才触发技能事件
	///	标记扩展（@CST-6388）
	///注意：
	///	不支持满血免疫：满血也可以治疗，包括事件触发
	EffectAddHP = 10 UMETA(DisplayName = "EffectAddHP"),
	///EffectAddMP（法力值治疗效果）
	///	Param1：治疗百分比（如0.5代表“50%MP上限治疗”）|固定值（整型）
	///	Param2~5：无
	///支持：
	///	情景免疫：死亡免疫（@CST-2228）
	///	治疗结算：依据法力上限，获得法力值治疗（@CST-403）
	///		治疗量＝法力值上限×治疗百分比＋治疗固定值
	///注意：
	///	法力治疗尚未支持“治疗时”事件
	EffectAddMP = 11 UMETA(DisplayName = "EffectAddMP"),
	///EffectRevive（复活效果）
	///	Param1：复活重置生命值百分比（如0.5代表“50%HP上限”）|固定值（整型）
	///	Param2：复活重置法力值百分比|固定值（同上）
	///	Param3~5：无
	///支持：
	///	情景免疫：非死亡免疫（@CST-2761）
	///	复活，并恢复至指定生命值/法力值比例（@CST-8739）
	///	复活生命值、法力值结算：（@CST-8739）
	///		目标生命值＝生命值上限×复活生命百分比＋复活生命固定值
	///			有效范围：目标生命值≥1，目标法力值≥0
	///注意：
	///	不支持“治疗时”事件
	EffectRevive = 12 UMETA(DisplayName = "EffectRevive"),
	///EffectAddBuff（添加Buff效果）
	///	Param1：添加BuffID（@DT_BuffCfg，不得缺省）
	///	Param2~5：无
	///支持：
	///	给目标添加一个Buff
	///反思：
	///	不支持列表输入，是为了避免引入歧义与误导
	///	连续添加Buff不是独立的，未必都能成功，因为添加Buff之前还有额外和替代流程
	EffectAddBuff = 13 UMETA(DisplayName = "EffectAddBuff"),
	///EffectCreateEntity（创建单位效果）
	///	Param1：创建单位ID（@DT_MonsterCfg）
	///	Param2：创建位置偏移前|左（米）
	///	Param3~5：无
	///支持：
	///	支持“在目标附近创建一个单位”（@CST-4218）
	///		所创建的单位，与施法者/受术者都没有关系
	EffectCreateEntity = 14 UMETA(DisplayName = "EffectCreateEntity"),
	///EffectRemoveBuff（移除Buff效果）
	///	Param1：BuffID列表（@DT_BuffCfg，|竖号分隔，不得缺省）
	///	Param2~5：无
	///支持：
	///	移除指定ID的全部Buff（@CST-1356）
	///	支持列表输入（@CST-7259）
	EffectRemoveBuff = 15 UMETA(DisplayName = "EffectRemoveBuff"),
	///EffectAddFixIDEffect（添加效果效果）
	///	Param1：作用类型（缺省0）
	///		0：正作用（施法者→受术者，@csdefine.SKILL_EFFECT_TYPE_POSITIVE）
	///		1：反作用（受术者→施法者）
	///		2：副作用（施法者→施法者）
	///		3：催化作用（受术者→受术者）
	///	Param2：技能效果ID（@DT_SkillEffectCfg，不得缺省）
	///	Param3：连续多次添加效果（缺省1次）
	///	Param4~5：无
	///设计原意：
	///	①方便数值批量调整配置，②提供“作用类型”扩展支持
	///支持：
	///	添加指定ID的技能效果，作用类型扩展（@CST-1223）
	///	支持“先后添加数次同个效果”（@CST-3723）
	///注意：
	///	配置方式：非SkillEffectTable限定（@CST-2761）
	///	已知风险：连续添加未必一定成功，需要考虑上次效果可能影响下次效果的添加（如Buff替换条件），请谨慎使用
	EffectAddFixIDEffect = 17 UMETA(DisplayName = "EffectAddFixIDEffect"),
	///EffectTriggerCustomEvent（触发自定义技能事件效果）
	///	Param1：自定义技能事件ID（字符串，需要配合具体CustomEvent使用，留空代表“没有事件”）
	///		自定义技能事件ID，暂无占位表，请谨慎使用，注意避让
	///		示例：“999001001”，代表“只要CustomEvent也配置999001001，就可以响应触发”
	///	Param2~5：无
	///设计原意：
	///	做个可以自由定义的事件，按需要触发任何事情，只要触发和响应互相匹配即可
	///支持：
	///	技能事件：自定义事件（@CST-1314）
	///		需要配合（如“技能响应事件中断”、“被动技能响应事件触发”中的）“CustomEvent”使用
	EffectTriggerCustomEvent = 18 UMETA(DisplayName = "EffectTriggerCustomEvent"),
	///EffectAbsorbHP（抽血效果）
	///	Param1：伤害百分比（如0.5代表“50%HP上限”）|固定值（整型）
	///	Param2：吸血转换率（如0.5代表“吸收50%伤害量”）
	///	Param3~5：无
	///支持：
	///	情景免疫：死亡免疫（@CST-2228）
	///	伤害结算：依据生命值上限造成伤害，再依据伤害获得治疗（@CST-888）
	///		伤害量＝生命值上限×伤害百分比＋伤害固定值
	///		治疗量＝伤害量×吸血转换率
	///	仇恨结算：自然仇恨（@CST-12837）
	///		自然仇恨＝生命值扣除量×受术者自然仇恨系数×施法者造成仇恨修正
	///		自然仇恨下限＝【受术者的】自然仇恨下限
	///		查询：可以通过【/queryAttr hatredList】，查询【怪物的仇恨列表】属性
	///	仇恨结算：自然连带仇恨（@CST-12837）
	///		自然连带仇恨＝生命值恢复量×受术者的敌人的自然连带仇恨系数×施法者造成连带仇恨修正
	///		自然连带仇恨下限＝【受术者的敌人的】自然连带仇恨下限
	///		查询：可以通过【/queryAttr hatredList】，查询【怪物的仇恨列表】属性
	///	技能事件：治疗时/被治疗时/伤害时/被伤害时/击杀时/被击杀时（@CST-1206）
	///		以下情况除外：来源是被动技能（@CST-1206）、来源非技能（@CST-5054）
	///		只有主动技能、Buff流程下的效果才触发技能事件
	///注意：
	///	一般地，“伤害”应视为“战斗效果”，相关开关条件应默认配置“禁止受攻击”（ForbidBeAttack）
	EffectAbsorbHP = 20 UMETA(DisplayName = "EffectAbsorbHP"),
	///EffectNormalDamage（标准伤害效果）
	///	Param1：伤害性质类型（不得缺省）
	///		1：物理伤害（物攻、物防）
	///		2：法术伤害（法攻、法防）
	///	Param2：生命伤害百分比（如0.5代表“50%物理攻击”）|生命伤害固定值（整型）
	///	Param3：冰元素伤害百分比 : 冰元素伤害固定值 | 火百分比 : 固定值 | 雷百分比 : 固定值 | 玄百分比 : 固定值
	///			支持部分缺省，如"|0:100||"，代表"火元素伤害固定100点"
	///	Param4：标记列表（|竖号分隔，留空代表“没有标记”，具体功能与参数格式由标记定义）
	///		示例：“IsReAttrC:30008:50”，代表“校正施法者属性，物攻＋50”（战斗属性ID详见HoldEffectAddAttr相关说明，@CST-7698）
	///		示例：“IsReAttrR:30010:-50”，代表“校正受术者属性，物防－50”（同上）
	///		示例：“IsSkipEvent”，代表“跳过事件触发及其影响，如连击计数”（@CST-6388）
	///		示例：“IsDoPrivateOnKill:99900102”，代表“击杀目标时，额外触发指定被动技能”（无需注册直接使用，@CST-8363）
	///		示例：“IsDoDeadEffect”，代表“击杀目标时，额外触发其被杀特效”（需要配合怪物表的DeadEffect类型2配置，@CST-1619/@CST-1908）
	///	Param5：无
	///支持：
	///	情景免疫：死亡免疫（@CST-1635）
	///	伤害结算：标准生命伤害，伤害性质选择（以外功性质为例），暴击/招架（@CST-1635）
	///		生命伤害量＝施法者外功攻击×生命伤害百分比+生命伤害固定值
	///		生命伤害量＝生命伤害量×造成伤害修正
	///		暴击率＝施法者暴击÷施法者等级对应的暴击基准
	///		招架率＝受术者招架÷(受术者招架×(1－基准招架倍率)＋受术者等级对应的招架基准)
	///		护甲减免率＝受术者外功防御÷(受术者外功防御＋受术者等级对应的外功防御基准)
	///		生命伤害量＝生命伤害量×暴击修正×招架修正×(1－护甲减免率)
	///		生命扣除＝生命伤害量×承受伤害修正
	///		更多流程细节此略（详见alienbrain://NEWAB/创世3/01_设计文档/战斗系统/03_技能框架流程图.vsdx）
	///	仇恨结算：自然仇恨（@CST-12837）
	///		自然仇恨＝生命值扣除量×受术者自然仇恨系数×施法者造成仇恨修正
	///		自然仇恨下限＝【受术者的】自然仇恨下限
	///		查询：可以通过【/queryAttr hatredList】，查询【怪物的仇恨列表】属性
	///	技能事件：伤害时/被伤害时/击杀时/被击杀时（@CST-1754）
	///		以下情况除外：来源是被动技能（@CST-1206）、来源非技能（@CST-5054）
	///		只有主动技能、Buff流程下的效果才触发技能事件
	///注意：
	///	一般地，“伤害”应视为“战斗效果”，相关开关条件应默认配置“禁止受攻击”（ForbidBeAttack）
	///	罡气伤害（@CST-2420）已从标准伤害中移除（@CST-12828）
	EffectNormalDamage = 21 UMETA(DisplayName = "EffectNormalDamage"),
	///EffectCircleRound（把大家传送到身边效果）
	///	Param1：围绕半径（米）
	///	Param2~5：无
	///支持：
	///	把大家拉过来围一圈，任务播放剧情动画用（@CST-1405）
	EffectCircleRound = 22 UMETA(DisplayName = "EffectCircleRound"),
	///EffectChangeSkillCD（改变CD效果）
	///	Param1：冷却ID列表（整型，|竖号分隔，需要配合具体冷却配置使用，不得缺省）
	///		冷却ID，暂无占位表，请谨慎使用，注意避让
	///	Param2：冷却持续时间增量（秒，≥0代表“增加”，≤0代表“减少”）
	///	Param3~5：无
	///支持：
	///	延长、缩短当前冷却时间（@CST-1794）
	EffectChangeSkillCD = 23 UMETA(DisplayName = "EffectChangeSkillCD"),
	///EffectAddSkillCD（获得CD效果）
	///	Param1：冷却ID列表（整型，|竖号分隔，需要配合具体冷却配置使用，不得缺省）
	///		冷却ID，暂无占位表，请谨慎使用，注意避让
	///	Param2：冷却持续时间（秒，＜0修正为0，＝0代表“没有获得CD，只是更新下时间”）
	///	Param3~5：无
	///支持：
	///	获得冷却时间（@CST-8745）
	EffectAddSkillCD = 24 UMETA(DisplayName = "EffectAddSkillCD"),
	///EffectUseSkillByQuestID（依据任务挑选技能效果）
	///	Param1：任务ID列表（@DT_QuestInfoCfg，|竖号分隔，要求与参数2数量匹配）
	///	Param2：技能ID列表（@DT_SkillCfg，|竖号分隔，要求与参数1数量匹配）
	///	Param3~5：无
	///支持：
	///	依照任务ID，挑选出合适的技能ID（@CST-1884）
	///注意：
	///	已知风险：若任务ID与技能ID数量不比配，则【未必能有效报错】，请谨慎配置
	EffectUseSkillByQuestID = 25 UMETA(DisplayName = "EffectUseSkillByQuestID"),
	///EffectCreateEntityOnStraight（创建一排单位效果）
	///	Param1：创建单位ID1:数量1|单位ID2:数量2…（@DT_MonsterCfg，:冒号和|竖号分隔，不得留空，不得部分缺省）
	///	Param2：半径（米）|间距（米）
	///	Param3~5：无
	///支持：
	///	真龙棋阵专用，召唤指定数量的怪物在一条随机直线上（@CST-1895）
	EffectCreateEntityOnStraight = 26 UMETA(DisplayName = "EffectCreateEntityOnStraight"),
	///EffectGangQiDamage（罡气伤害效果）
	///	Param1：罡气伤害百分比（如0.5代表“50%罡气攻击”）|固定值（整型）
	///		查询：可以通过【/queryAttr gangQiValue】，查询【当前罡气值】属性
	///		查询：可以通过【/queryAttr gangQiState】，查询【罡气状态】属性（1气盈|2气短|3气竭|4气绝，@csdefine.GANG_QI_STATE_QI_YING）
	///	Param2~5：无
	///支持：
	///	情景免疫：死亡免疫（@CST-2420）
	///	伤害结算：罡气伤害（@CST-2420）
	///		罡气伤害量＝施法者罡气攻击×罡气伤害百分比＋罡气伤害固定值
	///		罡气伤害防御减免率＝受术者罡气防御÷(受术者罡气防御＋受术者等级对应的罡气防御基准)
	///		罡气伤害终值＝罡气伤害量×(1－罡气伤害防御减免率)
	///注意：
	///	一般地，“伤害”应视为“战斗效果”，相关开关条件应默认配置“禁止受攻击”（ForbidBeAttack）
	EffectGangQiDamage = 27 UMETA(DisplayName = "EffectGangQiDamage"),
	///EffectStopCycleFlyPatrol（飞行传送衔接环形路线效果）
	///	Param1：飞行路径ID（@DT_FlyPatrolCfg，留空代表“没有效果”）
	///	Param2~5：无
	///支持：
	///	飞行传送衔接环形路线（@CST-2420）
	///支持：
	///	功能待定（@CST-9731）
	///注意：
	///	受术者单位类型：PC限定
	EffectStopCycleFlyPatrol = 28 UMETA(DisplayName = "EffectStopCycleFlyPatrol"),
	///EffectDestroy（直接销毁效果）
	///	Param1~3：无
	///支持：
	///	功能待定（@CST-2936/@CST-3132）
	EffectDestroy = 29 UMETA(DisplayName = "EffectDestroy"),
	///EffectTeleportRandomPos（随机传送到附近位置效果）
	///	Param1：传送目标坐标位置（ 空格分隔，如“-25587 -587 696”，不填时为效果受术者的当前坐标）
	///	Param2：圆形随机范围的半径（不得缺省，≤0代表“全地图随机选点”）
	///	Param3~5：无
	///支持：
	///	在圆形范围内随机取点，闪现过去（@CST-2936）
	EffectTeleportRandomPos = 30 UMETA(DisplayName = "EffectTeleportRandomPos"),
	///EffectAddSpeed（穿越峡谷专用，获得冲刺速度效果）
	///	Param1：冲刺速度方向类型，相对于受术者单位（留空代表“没有改变速度”）
	///		1：向上
	///		2：向下
	///		3：向左
	///		4：向右
	///		5：向前
	///		6：向后
	///	Param2：冲刺速度大小（厘米/秒）
	///	Param3：持续时间（秒）
	///	Param4~5：无
	///支持：
	///	穿越峡谷专用，冲刺表现：根据目标朝向添加一个速度（@CST-2146）
	///	速度叠加：支持与SkillCanyonCharge、多个EffectAddSpeed同时作用，速度表现为“矢量和”
	///注意：
	///	受术者单位类型：PC限定
	///	使用方法：“需要配合BuffHoldThroughCanyon使用”限定
	EffectAddSpeed = 31 UMETA(DisplayName = "EffectAddSpeed"),
	///EffectDirectlyKill（直接击杀效果）
	///	Param1~3：无
	///设计原意：
	///	避免“无敌”、“不屈”…等基于伤害的被动扩展，制约“必须死亡”的表现设计
	///支持：
	///	不依赖伤害，使目标在还有生命值的情况下，也可以死亡（@CST-3132）
	///注意：
	///	已知风险：直接击杀可能导致“目标死亡时未有所有者”，请谨慎使用
	EffectDirectlyKill = 32 UMETA(DisplayName = "EffectDirectlyKill"),
	///EffectBeBlow（吹风效果）
	///	Param1：吹风速度大小（米/秒）
	///	Param2：吹风持续时间（秒）
	///	Param3~5：无
	///支持：
	///	功能待定（@CST-3135）
	///		速度方向在效果开始时固定为，施法者→受术者方向，表现为“远离吹风施法者”
	///		若位置重叠则修正为“施法者当前朝向”（类似击退的方向定义）
	///注意：
	///	受术者单位类型：PC限定
	EffectBeBlow = 33 UMETA(DisplayName = "EffectBeBlow"),
	///EffectUpdateScoreForLHSL（灵域狩魂专用，更新计分效果）
	///	Param1~5：无
	///支持：
	///	灵域狩魂专用，更新计分（@CST-3232）
	///注意：
	///	受术者单位类型：非PC限定
	EffectUpdateScoreForLHSL = 34 UMETA(DisplayName = "EffectUpdateScoreForLHSL"),
	///EffectCreateTiShen（召唤替身效果）
	///	Param1：替身单位ID（@DT_MonsterCfg，需要配合MonsterExtTiShen使用）
	///	Param2：召唤位置偏移前|左（米）
	///	Param3：存活时间（秒）
	///	Param4~5：无
	///支持：
	///	为目标创建替身单位：指认受术者为“主人”，与其模型、属性一致，继承敌对关系（@CST-4218）
	///	“AI指定目标”置换：创建时，主动影响附近怪物，若当前AI目标为“替身主人”，则置换为“本替身单位”（@CST-4218）
	///		（替身的具体表现取决于AI配置，需要AI配合才能发挥良好的替身表现）
	///	敌我表现差异：若敌方观看，则UI与PC相同，若友方观看，则UI比PC多一个“替身”标记（@CST-4218）
	///注意：
	///	受术者单位类型：PC限定
	///	替身单位类型：MonsterExtTiShen限定（@CST-4218）
	///	“替身表现”与“嘲讽表现”不一致，需要注意辨别
	EffectCreateTiShen = 35 UMETA(DisplayName = "EffectCreateTiShen"),
	///EffectExpelTheSoul（灵魂之誓专用，灵魂出窍表现效果）
	///	Param1：effectID（功能待定）
	///	Param2：delayDestroyTime（功能待定）
	///	Param3~5：无
	///支持：
	///	灵魂之誓专用，附身表现（@CST-4220，功能待定）
	EffectExpelTheSoul = 36 UMETA(DisplayName = "EffectExpelTheSoul"),
	///EffectTeleportAppointSpace（神行石传送效果）
	///	Param1~5：无
	///支持：
	///	神行石专用，把玩家传送到相应的地点（@CST-4305）
	///注意：
	///	受术者单位类型：PC限定
	EffectTeleportAppointSpace = 37 UMETA(DisplayName = "EffectTeleportAppointSpace"),
	///EffectPauseFlyPatrol（暂停飞行效果）
	///	Param1~5：无
	///支持：
	///	暂停飞行（@CST-4392）
	///注意：
	///	受术者单位类型：PC限定
	EffectPauseFlyPatrol = 38 UMETA(DisplayName = "EffectPauseFlyPatrol"),
	///EffectReviveFlyPatrol（恢复飞行效果）
	///	Param1~5：无
	///支持：
	///	恢复飞行（@CST-4392）
	///注意：
	///	受术者单位类型：PC限定
	EffectReviveFlyPatrol = 39 UMETA(DisplayName = "EffectReviveFlyPatrol"),
	///EffectCreateFaZhen（创建法阵效果）
	///	Param1：法阵单位ID（@DT_SpellBoxCfg，留空代表“没有召唤”）
	///	Param2~5：无
	///支持：
	///	创建法阵（@CST-4161）
	EffectCreateFaZhen = 40 UMETA(DisplayName = "EffectCreateFaZhen"),
	///EffectAbsorbTheSoul（吸魂表现效果）
	///	Param1~5：无
	///支持：
	///	灵魂之誓专用，吸魂表现（@CST-4220）
	EffectAbsorbTheSoul = 41 UMETA(DisplayName = "EffectAbsorbTheSoul"),
	///EffectUpdateSoulNumForLHZS（灵域狩魂专用，更新灵魂数量效果）
	///	Param1~5：无
	///支持：
	///	灵域狩魂专用，更新灵魂吸收数量：功能待定（@CST-4220）
	///注意：
	///	受术者单位类型：PC限定
	EffectUpdateSoulNumForLHZS = 42 UMETA(DisplayName = "EffectUpdateSoulNumForLHZS"),
	///EffectTriggerAIEvent（触发自定义AI事件效果）
	///	Param1：自定义AI事件ID（字符串，需要配合具体AI事件使用，留空代表“没有事件”）
	///		自定义AI事件ID，暂无占位表，请谨慎使用，注意避让
	///	Param2~5：无
	///支持：
	///	触发自定义AI事件（@CST-4722）
	///	　需要配合以下支持使用：
	///		AI行为：AIAction#10、#25（通过技能发送时，实际上可以提前筛选受术者，可以按需忽视“消息目标单位ID要求”配置）
	///		AI条件：AICondition#25、#73（PC发送自定义AI事件时，条件的“施法者ID要求”应该留空）
	///		副本行为：SEAction#10（以供参考）
	///注意：
	///	受术者单位类型：Monster限定
	EffectTriggerAIEvent = 44 UMETA(DisplayName = "EffectTriggerAIEvent"),
	///EffectAircraftUseSkill（触发飞行器的技能效果）
	///	Param1~5：无
	///支持：
	///	技能事件：自定义事件（@CST-4755）
	///注意：
	///	受术者单位类型：PC限定
	EffectAircraftUseSkill = 45 UMETA(DisplayName = "EffectAircraftUseSkill"),
	///EffectSkillPosture（设置心法状态效果）
	///	Param1：心法状态类型（@DT_SkillPostureUICfg，不得缺省）
	///		　0：默认心法（@csdefine.SKILL_POSTURE_NONE）
	///		101：天怒心法（战士）
	///		102：神威心法（战士）
	///		201：幻剑心法（剑客）
	///		202：天剑心法（剑客）
	///		301：九幽心法（刺客）
	///		302：雷鸣心法（刺客）
	///		401：寒霜心法（法师）
	///		402：神逸心法（法师）
	///	Param2：心法等级（整型，不得缺省）
	///	Param3~5：无
	///支持：
	///	切换当前心法、心法等级（@CST-4778）
	EffectSkillPosture = 46 UMETA(DisplayName = "EffectSkillPosture"),
	///EffectFlag（改变标志位效果）
	///	Param1：操作类型（不得缺省）
	///		1：添加标志位
	///		0：移除标志位
	///	Param2：标志位列表（|竖号分隔）
	///	　对于“玩家PC”：
	///		1：观察者（@csdefine.ROLE_FLAG_WATCHER）
	///		2：处于队伍中
	///	　对于“怪物Monster”：
	///		  1：怪物和玩家可以互相攻击（@csdefine.FLAG_RELATION_ENEMY_TO_ROLE）
	///		  2：怪物和玩家不可以互相攻击
	///		  3：怪物和怪物可以互相攻击
	///		  4：怪物和怪物不可以互相攻击
	///		  7：强制开启，AI心跳（即不需要AOI内有PC）
	///		  8：不可见
	///		  9：浮空（即不贴地）
	///		10：不能转向
	///		11：不能被选中
	///		12：啥都碰
	///		13：强制关闭，头顶名称显示
	///		14：强制关闭，头顶血条显示
	///		15：强制关闭，头顶等级显示
	///		16：强制开启，头顶名称显示
	///		17：强制开启，头顶血条显示
	///		18：强制开启，头顶等级显示
	///		19：游荡
	///		20：陷阱单向敌对玩家
	///		21：陷阱单向优好玩家
	///		22：使用服务器追击
	///		23：啥都不碰
	///		24：真实碰撞（关闭胶囊碰撞，激活组件碰撞）
	///		25：防弹（敌对子弹碰撞时，消灭子弹）
	///		26：强制开启，头顶伤害进度条显示
	///		27：开启，最小攻击距离限制
	///	Param3~5：无
	///支持：
	///	让技能也有设置标志位的能力（@CST-4791）
	///注意：
	///	已知风险：不同单位类型对应的标志位意义不同，请谨慎使用
	///		建议配合自定义条件，筛选受术者的单位类型条件，以避免表现错误
	EffectFlag = 47 UMETA(DisplayName = "EffectFlag"),
	///EffectRequestSkill（申请技能效果）
	///	Param1：触发申请的技能ID（@DT_SkillCfg，不得缺省）
	///	Param2~5：无
	///设计原意：
	///	用来方便灵活地描述“蓄力”、“吟唱”…等表现
	///		另，吟唱已独立支持，详见SkillSing
	///支持：
	///	提交一个主动技能申请，表现与玩家通过客户端主动申请一样（@CST-4908）
	///		可以理解为，技能申请目标类型＝TargetLock
	///		技能申请者　【单位】＝效果施法者【单位】
	///		技能申请目标【单位】＝效果受术者【单位】
	///		只是单纯的提交申请，不保证施放成功（与PC主动申请一样），需要按流程走一遍才知道
	///	技能施展目标类型自适应（@CST-6339）
	///		若所申请的技能，施展目标类型＝TargetPosition，则施展失败（不修正）
	///注意：
	///	已知风险：支持“申请触发申请”，可能循环触发致使服务器崩溃，请谨慎使用（@CST-4908）
	///	不会触发玩家操作申请事件（RequestActionSkillEvent）
	///反思：
	///	从追击技能脚本中得到的灵感，在申请标准化之后得到规范
	///	做完之后发现，在引导技能中申请引导技能会失败，从而有了吟唱技能的想法
	EffectRequestSkill = 48 UMETA(DisplayName = "EffectRequestSkill"),
	///EffectVideo（播放视频效果）
	///	Param1：视频ID（@DT_MediaPlayerCfg）
	///	Param2~5：无
	///支持：
	///	客户端播放视频（@CST-5247）
	EffectVideo = 50 UMETA(DisplayName = "EffectVideo"),
	///EffectResetJump（重置跳跃次数效果）
	///	Param1~5：无
	///支持：
	///	重置客户端跳跃次数（@CST-4369）
	///注意：
	///	受术者单位类型：PC限定
	EffectResetJump = 51 UMETA(DisplayName = "EffectResetJump"),
	///EffectSetViewTarget（玩家摄像机注视表现效果）
	///	Param1：摄像机前往时间 停留时间 返程时间（秒， 空格分隔，如“2 3 1”表现为“去2秒，停3秒，回1秒”）
	///	Param2：起始位置偏移X Y Z（厘米， 空格分隔，如“0 0 500”表现为“提高5米”）
	///	Param3：目标位置偏移X Y Z（同上）
	///	Param4：截止距离（厘米，如50表现为“距离目标0.5米时停下”）
	///	Param5：返程后是否恢复原视角（缺省1）
	///		0：返程后，维持摄像机当前视角
	///		1：返程后，恢复原摄像机出发前视角
	///支持：
	///	强制玩家摄像机注视指定目标单位（@CST-5026）
	///注意：
	///	受术者单位类型：PC限定（@CST-5026）
	EffectSetViewTarget = 52 UMETA(DisplayName = "EffectSetViewTarget"),
	///EffectTriggerSpaceEvent（触发自定义副本事件效果）
	///	Param1：自定义副本事件ID（字符串，需要配合具体副本事件使用，留空代表“没有事件”）
	///		自定义副本事件ID，暂无占位表，请谨慎使用，注意避让
	///	Param2~5：无
	///支持：
	///	触发自定义副本事件（@CST-4056）
	EffectTriggerSpaceEvent = 53 UMETA(DisplayName = "EffectTriggerSpaceEvent"),
	///EffectTeleportSpaceRead（玩家同地图传送并且读条效果）
	///	Param1：传送目标地图ID（@DT_HashMapCfg，留空代表“当前地图内传送”）
	///		查询：可以通过【/queryAttr spaceScriptID】，查询【当前地图ID】属性
	///	Param2：传送目标坐标位置（ 空格分隔，如“-25587 -587 696”，不得缺省）
	///	Param3：传送目标坐标朝向（ 空格分隔，如“0 0 0”，不得缺省）
	///	Param4~5：无
	///支持：
	///	传送至同地图的指定坐标位置（@CST-6555）
	///注意：
	///	受术者单位类型：PC限定
	///反思：
	///	这个其实挺适合标记扩展的
	EffectTeleportSpaceRead = 54 UMETA(DisplayName = "EffectTeleportSpaceRead"),
	///EffectRandomTeleportFloorXDGX（环任务仙岛归墟专用，随机格子传送效果）
	///	Param1~5：无
	///支持：
	///	（@CST-6096）
	EffectRandomTeleportFloorXDGX = 55 UMETA(DisplayName = "EffectRandomTeleportFloorXDGX"),
	///EffectDestroyGridXDGX（环任务仙岛归墟专用，周围格子自爆效果）
	///	Param1：范围（米，不得缺省）
	///	Param2~5：无
	///支持：
	///	（@CST-6096）
	EffectDestroyGridXDGX = 56 UMETA(DisplayName = "EffectDestroyGridXDGX"),
	///EffectStopRandomDestroyFloorXDGX（环任务仙岛归墟专用，停止随机销毁格子效果）
	///	Param1：停止随机销毁的时间（秒，不得缺省）
	///	Param2~5：无
	///支持：
	///	（@CST-6096）
	EffectStopRandomDestroyFloorXDGX = 57 UMETA(DisplayName = "EffectStopRandomDestroyFloorXDGX"),
	///EffectUpGradeYXLMSoldier（英雄王座专用，升级小兵效果）
	///	Param1~5：无
	///支持：
	///	（@CST-6511）
	EffectUpGradeYXLMSoldier = 58 UMETA(DisplayName = "EffectUpGradeYXLMSoldier"),
	///EffectDoubleHit（连击计数效果）
	///	Param1：改变连击次数（缺省1次，＞0代表“增加”，＜0代表“减少”，＝0代表“只是更新时间”）
	///		查询：可以通过【/queryAttr doubleHitTimes】，查询【连击次数】属性
	///		查询：可以通过【/queryAttr doubleHitState】，查询【连击状态】属性（@csconst.DOUBLE_HIT_STATE）
	///	Param2~5：无
	///设计原意：
	///	在连击计数的默认规则之外，补充手动调整的空间
	///		伤害与治疗可以默认触发连击计数，无需额外配置
	///		只有，当不是上述情况，而我们又希望触发连击计数时，才需要配置此效果
	///支持：
	///	手动触发【施法者】的“连击计数”，也会更新连击计时器（@CST-6388）
	///注意：
	///	施法者单位类型：PC限定（类型不正确时，会有警告信息）
	EffectDoubleHit = 59 UMETA(DisplayName = "EffectDoubleHit"),
	///EffectAddPetHPSlot（幻兽血槽回复效果）
	///	Param1：回复固定值（整型）
	///	Param2~5：无
	///支持：
	///	（@CST-6330）
	EffectAddPetHPSlot = 60 UMETA(DisplayName = "EffectAddPetHPSlot"),
	///EffectAddPetMPSlot（幻兽蓝槽回复效果）
	///	Param1：回复固定值（整型）
	///	Param2~5：无
	///支持：
	///	（@CST-6330）
	EffectAddPetMPSlot = 61 UMETA(DisplayName = "EffectAddPetMPSlot"),
	///EffectPetReviveHP（幻兽血槽往幻兽血条补充血量效果）
	///	Param1~5：无
	///支持：
	///	（@CST-6330）
	EffectPetReviveHP = 62 UMETA(DisplayName = "EffectPetReviveHP"),
	///EffectPetReviveMP（幻兽蓝槽往幻兽蓝条补充蓝量效果）
	///	Param1~5：无
	///支持：
	///	（@CST-6330）
	EffectPetReviveMP = 66 UMETA(DisplayName = "EffectPetReviveMP"),
	///EffectJSZZSearch（金树种子专用，搜索种植点效果）
	///	Param1：怪物ID（@DT_MonsterCfg，功能待定）
	///	Param2：半径（米，不得缺省）
	///	Param3：总时间（秒，不得缺省）|显示时间（秒，不得缺省）
	///	Param4~5：无
	///支持：
	///	（@CST-7419）
	EffectJSZZSearch = 67 UMETA(DisplayName = "EffectJSZZSearch"),
	///EffectCompleteTask（完成任务目标效果）
	///	Param1：任务ID（@DT_QuestInfoCfg，不得缺省）
	///	Param2：任务目标ID列表（@DT_QuestInfoCfg.Task，|竖号分隔，不得缺省）
	///	Param3~5：无
	///支持：
	///	完成指定任务的一些任务目标（@CST-7419）
	///注意：
	///	已知风险：任务目标有优先级限制，需要考虑完成顺序，请谨慎使用
	EffectCompleteTask = 68 UMETA(DisplayName = "EffectCompleteTask"),
	///EffectRotateRoleCamera（玩家摄像机偏转表现效果）
	///	Param1：旋转偏移X|Y|Z（角度，不得缺省）
	///		示例：“0|90|0”，代表“右转90度”
	///	Param2：摄像机臂长（厘米，不得缺省）
	///		示例：“300”，代表“摄像机臂长3米”
	///	Param3~5：无
	///支持：
	///	（@CST-7419）
	///注意：
	///	已知风险：若参数1格式不正确，则使用时可能导致客户崩溃，请谨慎配置“旋转偏移”
	EffectRotateRoleCamera = 69 UMETA(DisplayName = "EffectRotateRoleCamera"),
	///EffectMQLeaveAim（冥气人参果专用，离开瞄准状态效果）
	///	Param1~5：无
	///支持：
	///	（@CST-6327）
	EffectMQLeaveAim = 70 UMETA(DisplayName = "EffectMQLeaveAim"),
	///EffectAddBuffByProfession（依据职业、性别获得不同Buff效果）
	///	Param1：给男战士的Buff（不得缺省，0代表“没有Buff”）|给女战士的Buff（缺省＝男）
	///		示例：“0”，代表“男女战士都没有Buff”
	///		示例：“99900101”，代表“男女战士都有Buff”
	///		示例：“99900101|0”，代表“男战士有Buff，女战士没有Buff”
	///	Param2：给男|女剑客的Buff（同上）
	///	Param3：给男|女链刃的Buff（同上）
	///	Param4：给男|女法师的Buff（同上）
	///	Param5：无
	///支持：
	///	可以依据职业，提供不同的Buff（@CST-6327）
	///		查询：可以通过【/queryAttr profession】，查询【职业】属性
	///	可以依据性别，提供不同的Buff（@CST-10442）
	///		查询：可以通过【/queryAttr gender】，查询【性别】属性
	///注意：
	///	受术者单位类型：PC限定（因为怪物没有性别，设计原意也是方便玩家单位）
	///	已知风险：若目标的职业和性别不在指定范围内，则将不会获得任何Buff（如，设置职业＝5，则不会获得任何Buff）
	EffectAddBuffByProfession = 71 UMETA(DisplayName = "EffectAddBuffByProfession"),
	///EffectAttributeWXHJ（五行画卷专用，属性判定效果）
	///	Param1：画卷五行属性类型（功能待定）
	///		jin：金属性（功能待定）
	///		mu：木属性（同上）
	///		shui：水属性（同上）
	///		huo：火属性（同上）
	///		tu：土属性（同上）
	///	Param2~5：无
	///支持：
	///	五行画卷专用，属性判断效果：需要配合MonsterExtWXHJ使用，按需发送指定的AI事件（@CST-7976）
	///注意：
	///	受术者单位类型：MonsterExtWXHJ限定
	EffectAttributeWXHJ = 72 UMETA(DisplayName = "EffectAttributeWXHJ"),
	///EffectRequestPassiveSkill（申请被动技能效果）
	///	Param1：申请被动技能ID（@DT_PassiveSkillCfg，不得缺省）
	///	Param2：标记列表（|竖号分隔，留空代表“没有标记”，具体功能与参数格式由标记定义）
	///		示例：“IsReDict:takeDamage:100”，代表“校正技能申请信息，伤害量＝100”（@CST-7696）
	///	Param3~5：无
	///支持：
	///	不需要效果施法者持有该被动技能，可以跳过事件机制，直接申请一个被动技能（@CST-7696）
	///		技能申请者　＝原技能施法者
	///		技能申请目标＝原技能受术者
	///	技能施展目标类型自适应（@CST-6339）
	///注意：
	///	一般的，被动技能触发表现不需要额外补充申请信息，相关事件将自行传达相关信息
	///	具体信息需求，视具体情况而定，详情可联系相关策划、程序同仁了解
	EffectRequestPassiveSkill = 73 UMETA(DisplayName = "EffectRequestPassiveSkill"),
	///EffectLearnSkill（技能学习效果）
	///	Param1：技能ID（@DT_SkillCfg，不得缺省）
	///	Param2~5：无
	///支持：
	///	（@CST-8131）
	///注意：
	///	受术者单位类型：PC限定
	EffectLearnSkill = 74 UMETA(DisplayName = "EffectLearnSkill"),
	///EffectDiedDissolve（废弃：死亡消融表现效果）
	///	Param1：消融的边缘颜色  “R|G|B”(范围0-1)
	///	Param2：消融的方向（可自行尝试直至效果满意）
	///		示例：“0|0|0”，表现为“整体消融”
	///		示例：“0|0|1”，表现为“从上到下”
	///		示例：“0|1|0”，表现为“从右到左”
	///	Param3：初始消融程度（0表现为“不消融”，1表现为“完全消融”）|目标消融程度|消融时间（秒）|延时（秒）
	///	Param4~5：无
	///支持：
	///	模型消融效果（@CST-7926，未启用）
	EffectDiedDissolve = 75 UMETA(DisplayName = "EffectDiedDissolve"),
	///EffectRemoveYCJMDBossItemData（勇闯夺命岛专用，扣除Boss物品效果）
	///	Param1：扣除道具ID（@DT_ItemDataCfg）
	///	Param2：扣除道具数量（缺省1个）
	///	Param3~5：无
	///支持：
	///	扣除勇闯夺命岛Boss物品数据（@CST-8727）
	EffectRemoveYCJMDBossItemData = 76 UMETA(DisplayName = "EffectRemoveYCJMDBossItemData"),
	///EffectCameraLookAtTarget（摄像机注视效果）
	///	Param1：飞行时间 摄像机停留时间 摄像机飞回时间（秒，|竖号分隔，如“2|3|1”表现为“去2秒，停3秒，回1秒”）
	///	Param2：摄像机目标位置偏移量X Y Z（厘米，|竖号分隔，如“0|0|500”表现为“提高5米”）
	///	Param3：摄像机目标旋转偏移量X Y Z（同上）
	///	Param4~5：无
	///支持：
	///	从施法者当前视角飞到目标视角（@CST-8770）
	EffectCameraLookAtTarget = 77 UMETA(DisplayName = "EffectCameraLookAtTarget"),
	///EffectForcedJump（PC受迫跳跃效果）
	///	Param1：跳跃高度（米，＝0表现为“下落速度重置为0”，＜0表现为“无效”）
	///	Param2~5：无
	///支持：
	///	受迫跳跃表现：使用“被动跳跃”动作，忽视禁止跳跃，不计主动跳跃计数（@CST-8284）
	///	跳跃表现受当前环境影响（@CST-8284）
	///		向上速度与当前环境的重力无关，表现为“在低重力环境跳得更高”，反之亦然
	///		向上速度与移动平台的Z轴速度无关，平台的移动不影响跳跃表现
	///	跳跃速度结算：
	///		向上速度＝(＋默认重力加速度×2×跳跃高度)^0.5
	///		默认重力加速度＝9.8米/秒²
	///注意：
	///	受术者单位类型：PC限定
	///	已知风险：若目标向上速度＜当前向上速度，则影响无效（即无法用小上跳中止大上跳），请谨慎配置“目标跳跃高度”
	EffectForcedJump = 78 UMETA(DisplayName = "EffectForcedJump"),
	///EffectFlashToTarget（瞬移到目标附近效果）
	///	Param1：瞬移位置偏移前|左（米，以瞬移目标为基准）
	///	Param2：瞬移后朝向类型（缺省2）
	///		0：同“施法者当前朝向”（表现为“施法者朝向不变”）
	///		1：逆“施法者当前朝向”（表现为“施法者向后转”）
	///		2：施法者→受术者方向（表现为“面向受术者”，若位置重叠则修正为“施法者当前朝向”）
	///		3：受术者→施法者方向（表现为“背向受术者”，若位置重叠则修正为“受术者当前朝向”）
	///		4：同“受术者当前朝向”（表现为“与瞬移目标同向”）
	///		5：逆“受术者当前朝向”（表现为“与瞬移目标反向”）
	///	Param3：是否交换目标（缺省0）
	///		0：不交换目标（“效果施法者”瞬移到“效果受术者”附近，表现为“逆转通灵”）
	///		1：是交换目标（“效果受术者”瞬移到“效果施法者”附近，表现为“通灵术”）
	///	Param4~5：无
	///支持：
	///	瞬移到目标附近：瞬移施法者，瞬移到瞬移目标的附近，并更新朝向（@CST-9020）
	///		先瞬移到目标单位当前位置（假设其当前位置是有效的），再依据导航向目标方向移动（确保后续位置也有效，类似击退的位移表现）
	///		到达目标位置后，更新瞬移者的朝向为所需朝向
	///	情景免疫：
	///		同地图免疫：瞬移者与瞬移目标不在同一个地图内时，失败（原意是瞬移，而不是地图间传送）
	///		未决免疫：瞬移者或瞬移目标处于未决状态时（不适宜作瞬移相关表现）
	EffectFlashToTarget = 79 UMETA(DisplayName = "EffectFlashToTarget"),
	///EffectDodgeRotation（紧急回避专用，朝向修正效果）
	///	Param1~5：无
	///支持：
	///	配合紧急回避技能使用，以修正PC的单位朝向（@CST-9056）
	///		配合客户端紧急回避的相关操作作用，仅供紧急回避使用
	///注意：
	///	受术者单位类型：PC限定
	EffectDodgeRotation = 80 UMETA(DisplayName = "EffectDodgeRotation"),
	///EffectStopFlyPatrol（停止飞行传送效果）
	///	Param1~5：无
	///支持：
	///	功能待定（@CST-9731）
	///注意：
	///	受术者单位类型：PC限定
	EffectStopFlyPatrol = 81 UMETA(DisplayName = "EffectStopFlyPatrol"),
	///EffectNormalCure（标准治疗）
	///	Param1：治疗百分比（如0.5代表“50%治疗成效”）|固定值（整型）
	///		查询：可以通过【/queryAttr cure】，查询【治疗成效】属性
	///	Param2：标记列表（|竖号分隔，留空代表“没有标记”，具体功能与参数格式由标记定义）
	///		示例：“IsSkipEvent”，代表“跳过事件触发及其影响，如连击计数”（@CST-10638）
	///		示例：“IsReAttrC:30024:50”，代表“校正施法者属性，治疗成效＋50”（战斗属性ID详见HoldEffectAddAttr相关说明，@CST-10638）
	///	Param3~5：无
	///支持：
	///	情景免疫：死亡免疫（@CST-10638）
	///	治疗结算：标准生命治疗（@CST-10638）
	///		生命治疗量＝施法者治疗成效×生命治疗百分比+生命治疗固定值
	///		生命补充＝生命伤害量×受术者承受治疗修正
	///		更多流程细节此略（详见alienbrain://NEWAB/创世3/01_设计文档/战斗系统/03_技能框架流程图.vsdx）
	///	仇恨结算：自然连带仇恨（@CST-12837）
	///		自然连带仇恨＝生命值恢复量×受术者的敌人的自然连带仇恨系数×施法者造成连带仇恨修正
	///		自然连带仇恨下限＝【受术者的敌人的】自然连带仇恨下限
	///		查询：可以通过【/queryAttr hatredList】，查询【怪物的仇恨列表】属性
	///	技能事件：治疗时/被治疗时（@CST-10638）
	///注意：
	///	不支持满血免疫：满血也可以治疗，包括事件触发
	EffectNormalCure = 82 UMETA(DisplayName = "EffectNormalCure"),
	///EffectPoJieFu（轮回秘境 破解符）
	///	Param1~5：无
	EffectPoJieFu = 83 UMETA(DisplayName = "EffectPoJieFu"),
	///EffectEnergyChange（充能效果）
	///	Param1：伤BuffID（能级Buff限定）
	///	Param2：能量改变百分比（基于当前能量值）|固定值（负值代表减少）
	///	Param3：标记列表（|竖号分隔，留空代表“没有标记”，具体功能与参数格式由标记定义）
	///		示例：“IsBuffAgainTime”，代表像重新添加Buff一样，额外刷新持续时间
	///	Param4~5：无
	EffectEnergyChange = 84 UMETA(DisplayName = "EffectEnergyChange"),
	///EffectLearnPassiveSkill（被动技能学习效果）
	///	Param1：技能ID（@DT_PassiveSkillCfg，不得缺省）
	///	Param2：1:学习, 0：遗忘
	///	Param3~5：无
	///支持：
	///	（@CST-11040）
	///注意：
	///	受术者单位类型：PC限定
	EffectLearnPassiveSkill = 85 UMETA(DisplayName = "EffectLearnPassiveSkill"),
	///EffectLearnShenTongSkill（神通技能学习）
	///	Param1：技能ID（@DT_PassiveSkillCfg，不得缺省）
	///	Param2：可使用次数(不得缺省)
	///	Param3~5：无
	///支持：
	///	（@CST-11251）
	///注意：
	///	受术者单位类型：PC限定
	EffectLearnShenTongSkill = 86 UMETA(DisplayName = "EffectLearnShenTongSkill"),
	///EffectClientNormalDamage1（标准伤害效果）
	///	Param1：伤害性质类型（不得缺省）
	///		1：物理伤害（物攻、物防）
	///		2：法术伤害（法攻、法防）
	///	Param2：生命伤害百分比（如0.5代表“50%物理攻击”）|生命伤害固定值（整型）
	///	Param3：标记列表（|竖号分隔，留空代表“没有标记”，具体功能与参数格式由标记定义）
	///		示例：“IsReAttrC:30008:50”，代表“校正施法者属性，物攻＋50”（战斗属性ID详见HoldEffectAddAttr相关说明，@CST-7698）
	///		示例：“IsReAttrR:30010:-50”，代表“校正受术者属性，物防－50”（同上）
	///		示例：“IsSkipEvent”，代表“跳过事件触发及其影响，如连击计数”（@CST-6388）
	///		示例：“IsDoPrivateOnKill:99900102”，代表“击杀目标时，额外触发指定被动技能”（无需注册直接使用，@CST-8363）
	///		示例：“IsDoDeadEffect”，代表“击杀目标时，额外触发其被杀特效”（需要配合怪物表的DeadEffect类型2配置，@CST-1619/@CST-1908）
	///	Param4~5：无
	///支持：
	///	情景免疫：死亡免疫
	///	伤害结算：标准生命伤害，伤害性质选择（以外功性质为例），暴击/招架（@CST-1635）
	///		生命伤害量＝施法者外功攻击×生命伤害百分比+生命伤害固定值
	///		生命伤害量＝生命伤害量×造成伤害修正
	///		暴击率＝施法者暴击÷施法者等级对应的暴击基准
	///		招架率＝受术者招架÷(受术者招架×(1－基准招架倍率)＋受术者等级对应的招架基准)
	///		护甲减免率＝受术者外功防御÷(受术者外功防御＋受术者等级对应的外功防御基准)
	///		生命伤害量＝生命伤害量×暴击修正×招架修正×(1－护甲减免率)
	///		生命扣除＝生命伤害量×承受伤害修正
	///		更多流程细节此略（详见alienbrain://NEWAB/创世3/01_设计文档/战斗系统/03_技能框架流程图.vsdx）
	///	技能事件：伤害时/被伤害时/击杀时/被击杀时（@CST-1754）
	///		以下情况除外：来源是被动技能（@CST-1206）、来源非技能（@CST-5054）
	///		只有主动技能、Buff流程下的效果才触发技能事件
	///注意：
	///	一般地，“伤害”应视为“战斗效果”，相关开关条件应默认配置“禁止受攻击”（ForbidBeAttack）
	EffectClientNormalDamage1 = 87 UMETA(DisplayName = "EffectClientNormalDamage1"),
	///EffectCreateFenShen（召唤分身效果）
	///	Param1：分身单位ID（@DT_MonsterCfg，需要配合MonsterExtFenShen使用）
	///	Param2：召唤位置偏移前|左（米）
	/// Param3: 不可进入的space
	///	Param4：存活时间（秒）
	///	Param5：无
	///支持：
	///	为目标创建分身单位：指认受术者为“主人”，与其模型、属性一致，继承敌人列表，技能（@CST-11495）
	///注意：
	///	受术者单位类型：PC限定
	///	分身单位类型：MonsterExtFenShen限定（@CST-11495）
	EffectCreateFenShen = 88 UMETA(DisplayName = "EffectCreateFenShen"),
	///EffectCreateDisposable（召唤"一次性的随从单位"效果）
	///	Param1：随从单位ID（@DT_MonsterCfg，需要配合MonsterExtDisposable使用）
	///	Param2：召唤位置偏移前|左（米）
	/// Param3: 存活时间（秒）
	///	Param4~5：无
	///支持：
	///	（@CST-12452）
	///注意：
	///	受术者单位类型：PC限定
	///	分身单位类型：MonsterExtDisposable限定（@CST-12452）
	EffectCreateDisposable = 89 UMETA(DisplayName = "EffectCreateDisposable"),
	///EffectElementalDamage（元素伤害效果）
	///	Param1：冰元素伤害百分比 : 冰元素伤害固定值 | 火百分比 : 固定值 | 雷百分比 : 固定值 | 玄百分比 : 固定值
	///			支持部分缺省，如"|0:100||"，代表"火元素伤害固定100点"
	///	Param2：标记列表（|竖号分隔，留空代表“没有标记”，具体功能与参数格式由标记定义）
	///		示例：“IsSkipEvent”，代表“跳过事件触发及其影响，如连击计数”（@CST-6388）
	///		示例：“IsDoDeadEffect”，代表“击杀目标时，额外触发其被杀特效”（需要配合怪物表的DeadEffect类型2配置，@CST-1619/@CST-1908）
	///		示例：“IsDoPrivateOnKill:99900102”，代表“击杀目标时，额外触发被动技能99900102”（忽视被动技能的响应配置，@CST-8363）
	///	Param3~5：无
	///支持：
	///	（@CST-12828）
	///	仇恨结算：自然仇恨（@CST-12837）
	///		自然仇恨＝生命值扣除量×受术者自然仇恨系数×施法者造成仇恨修正
	///		自然仇恨下限＝【受术者的】自然仇恨下限
	///		查询：可以通过【/queryAttr hatredList】，查询【怪物的仇恨列表】属性
	///注意：
	EffectElementalDamage = 90 UMETA(DisplayName = "EffectElementalDamage"),
	///EffectHatred（人为仇恨改变效果）
	///	Param1：仇恨基准
	///		1＝效果施法者
	///		2＝效果受术者
	///	Param2：基准仇恨百分比（如0.5代表“50%基准仇恨”）|固定值（整型）
	///		正值，代表“增加受术者对自身的仇恨”（如“嘲讽”）
	///		负值，代表“降低受术者对自己的仇恨”（如“遁入虚空”）
	///	Param3~5：无
	///支持：
	///	人为产生仇恨，以描述如“对敌人使用眩晕”等限制行为的仇恨影响（@CST-12837）
	///		直接通知受术者，改变仇恨
	///	情景免疫：非敌对免疫（@CST-12837）
	///		只有对敌对单位使用时有效
	///	仇恨结算：人为仇恨（@CST-12837）
	///		仇恨改变量＝（施法者或受术者的）基准仇恨值×百分比＋固定值
	///		正值代表“增加目标对自身的仇恨”，负值代表“降低目标对自己的仇恨”
	///		查询：可以通过【/queryAttr hatredList】，查询【怪物的仇恨列表】属性
	///注意：
	///	基准仇恨，相当于标准角色当前等级所造成的“1秒”的伤害量
	///	仇恨基准的选择，取决于此项效果“如何生效”，举例如：
	///		若效果是“眩晕2秒”，其强度由“施法者这段时间可以产生多少伤害”决定，应以施法者为基准
	///		若效果是“攻击－10%”，其强度由受术者的强度决定，应以受术者的敌人为基准
	EffectHatred = 91 UMETA(DisplayName = "EffectHatred"),
	///EffectRelatedHatred（人为连带仇恨改变效果）
	///	Param1：仇恨基准
	///		1＝效果施法者
	///		2＝效果受术者
	///		3＝效果受术者的敌人
	///	Param2：基准仇恨百分比 | 固定值
	///		正值，代表“增加受术者的敌人对自身的仇恨”（如“给怪物的敌人添加护盾”）
	///		负值，代表“降低受术者的敌人对自己的仇恨”（暂时没有想到例子）
	///	Param3~5：无
	///支持：
	///	人为产生连带仇恨，以描述如“对队友使用增益效果”等辅助行为的仇恨影响（@CST-12837）
	///		通知受术者的敌人列表，改变仇恨
	///	情景免疫：非友好免疫（@CST-12837）
	///		只有对友好单位使用时有效
	///	仇恨结算：人为连带仇恨（@CST-12837）
	///		仇恨改变量＝（施法者或受术者或其敌人的）基准仇恨值×百分比＋固定值
	///		查询：可以通过【/queryAttr hatredList】，查询【怪物的仇恨列表】属性
	///注意：
	///	基准仇恨，相当于标准角色当前等级所造成的“1秒”的伤害量
	///	仇恨基准的选择，取决于此项效果“如何生效”，举例如：
	///		若效果是“攻击＋10%”，其强度由受术者的强度决定，应以受术者为基准
	///		若效果是“防御＋10%”，其强度由受术者的敌人的强度决定，应以受术者的敌人为基准
	EffectRelatedHatred = 92 UMETA(DisplayName = "EffectRelatedHatred"),
	///EffectEnterDF（回洞府）
	///	Param1：低级洞府的scriptID
	///	Param2：高级洞府的scriptID
	///	Param3~5：无
	///支持：
	///	（@CST-13475）
	///注意：
	EffectEnterDF = 93 UMETA(DisplayName = "EffectEnterDF"),
	///EffectQuickBarEnable（设置快捷栏是否有效）
	///	Param1：1为激活，0为无效
	///	Param2~5：无
	///支持：
	///	（@CST-13475）
	///注意：
	EffectQuickBarEnable = 94 UMETA(DisplayName = "EffectQuickBarEnable"),
	///EffectReward（“给予奖励”效果）
	///	Param1：奖励ID
	///	Param2：指定数值信息标签（信息属性名:属性值）
	///   level(通用等级), tongLevel(帮会等级), spaceLevel(副本等级), ratio(道具奖励系数)
	///	Param3~5：无
	///支持：
	///	（@CST-12829）
	EffectReward = 95 UMETA(DisplayName = "EffectReward"),
};

///技能打击效果
USTRUCT(BlueprintType)
struct CHUANGSHI_API FHIT_EFFECT
{
	GENERATED_BODY()
	///主动技能打击效果脚本类型
	///	不同类型，决定着不同的参数定义
	UPROPERTY(EditAnywhere)
		ENUM_HIT_EFFECT_TYPE HitEffectType;
	///施法者开关条件
	///支持：
	///	效果条件（@CST-7617）
	///注意：
	///	暂未支持事件触发的判断依据（@CST-7617）
	UPROPERTY(EditAnywhere, DisplayName = "CasterActForbid")
		ACTION_FLAG CasterActForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	///受术者开关条件
	///支持：
	///	效果条件（@CST-1209）
	///	事件触发（@CST-1314）
	UPROPERTY(EditAnywhere, DisplayName = "ReceiverActForbid")
		ACTION_FLAG ReceiverActForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	///参数1（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param1;
	///参数2（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param2;
	///参数3（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param3;
	///参数4（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param4;
	///参数5（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param5;
};

///持有效果脚本类型
UENUM(BlueprintType)
enum class ENUM_HOLD_EFFECT_TYPE : uint8
{
	///HoldEffectDizzy（眩晕效果）
	///	Param1~5：无
	///设计原意：
	///	无法行动
	///支持：
	///	效果状态持有（/queryAttr effectCounter，#0，第1个）
	///	开关限制（@csconst.EFFECT_STATE_TO_ACTION_FLAGS）
	///		禁止玩家改变朝向、禁止主动移动、禁止跳跃、禁止施法（@CST-1209）、禁止使用道具、禁止交互（@CST-4581）
	///注意：
	///	自带光效表现（@DT_EffectStatePerformanceCfg，@CST-3076）
	///	一般地，“能力异常表现”应视为“控制行为”，相关开关条件应默认配置“禁止受控制”
	HoldEffectDizzy = 0 UMETA(DisplayName = "HoldEffectDizzy"),
	///HoldEffectUncontrollable（霸体效果）
	///	Param1~5：无
	///设计原意：
	///	坚韧不拔，不被约束
	///支持：
	///	效果状态持有（/queryAttr effectCounter，#1，第2个）
	///	开关限制（@csconst.EFFECT_STATE_TO_ACTION_FLAGS）
	///		禁止被击退（@CST-1356）、禁止被控制（@CST-3582）
	///注意：
	///	自带光效表现（@DT_EffectStatePerformanceCfg，@CST-3076）
	HoldEffectUncontrollable = 1 UMETA(DisplayName = "HoldEffectUncontrollable"),
	///HoldEffectInvincible（无敌效果）
	///	Param1~5：无
	///设计原意：
	///	各种各样的免疫表现、免战表现
	///支持：
	///	效果状态持有（/queryAttr effectCounter，#2，第3个）
	///	开关限制（@csconst.EFFECT_STATE_TO_ACTION_FLAGS）
	///		禁止被攻击、禁止被击退、禁止被控制（@CST-3582）、禁止被减损（@CST-11494）
	///注意：
	///	自带光效表现（@DT_EffectStatePerformanceCfg，@CST-3076）
	///	已知风险：目前从开关影响上看，表演与无敌完全一致，只有光效表现上的差异，请谨慎使用
	HoldEffectInvincible = 2 UMETA(DisplayName = "HoldEffectInvincible"),
	///HoldEffectFix（定身效果）
	///	Param1~5：无
	///设计原意：
	///	身体不能动，但是可以转向，供带位移的技能施放过程使用
	///支持：
	///	效果状态持有（/queryAttr effectCounter，#4，第5个）
	///	开关限制（@csconst.EFFECT_STATE_TO_ACTION_FLAGS）
	///		禁止主动移动、禁止跳跃
	///注意：
	///	自带光效表现（@DT_EffectStatePerformanceCfg，@CST-3076）
	///	一般地，“能力异常表现”应视为“控制行为”，相关开关条件应默认配置“禁止受控制”
	HoldEffectFix = 3 UMETA(DisplayName = "HoldEffectFix"),
	///HoldEffectActionSpeed（定帧表现测试专用，设置动作播放速率效果）
	///	Param1：动作播放速率（如0.1代表“10%速率播放”，不得缺省）
	///	Param2~5：无
	///支持：
	///	定帧表现测试专用（@CST-1616）
	///注意：
	///	临时方案，仅供测试表现用
	HoldEffectActionSpeed = 4 UMETA(DisplayName = "HoldEffectActionSpeed"),
	///HoldEffectCallMonster（召唤随从效果）
	///	Param1：召唤物单位ID（@DT_MonsterCfg，需要配合monsterExtCall使用）
	///	Param2：允许召唤物进入的地图ID列表（@DT_HashMapCfg，留空代表“地图不限，啥地图都允许去”）
	///		在“不允许进入的地图”中，召唤将失败，而效果不会移除，再次进入“允许进入的地图”时，将重新创建召唤物
	///		查询：可以通过【/queryAttr spaceScriptID】，查询【当前地图ID】属性
	///	Param3~5：无
	///支持：
	///	召唤随从单位：指认受术者为“主人”，继承敌对关系，跟随移动/传送、协助攻击（@CST-1455）
	///注意：
	///	受术者单位类型：PC限定（@CST-1455）
	///	召唤物单位类型：monsterExtCall限定（@CST-1455）
	///	已知风险：未存储召唤物的相关信息，切换地图时将销毁原召唤物，再重新召唤一个全新的召唤物，请谨慎使用
	HoldEffectCallMonster = 5 UMETA(DisplayName = "HoldEffectCallMonster"),
	///HoldEffectAddFixIDEffect（持有效果效果）
	///	Param1：持有效果ID（@DT_SkillHoldEffectCfg）
	///	Param2~5：无
	///设计原意：
	///	①方便数值批量调整配置
	///	②提供装备、称号…等道具支持“持有效果”
	///支持：
	///	通过持有效果表添加持有效果（@CST-1223）
	///注意：
	///	配置方式：非SkillHoldEffectTable限定（@CST-2761）
	HoldEffectAddFixIDEffect = 6 UMETA(DisplayName = "HoldEffectAddFixIDEffect"),
	///HoldEffectAddAttr（战斗属性增益效果）
	///	Param1：战斗属性ID列表（@ItemTypeEnum，|竖号分隔，不得缺省）
	///		30001/2/3/4/5：根骨/筋力/内力/洞察/身法（corporeity…等，此略）
	///		30006：生命上限（HP_Max）
	///		30007：法力上限（MP_Max）
	///		30008/10：物理【攻击/防御】（damage/armor）
	///		30009/11：法术【攻击/防御】（magic_damage/magic_armor）
	///		30012/13：暴击/招架（criticalstrike/parry）
	///		30014：移速（speed）
	///		30015/16：【命中/闪避】率（hitrate/dodgerate）
	///		30017：脱战自愈率（healingrate）
	///		30018：罡气值上限（gangQiValue_Max）
	///		30019/20：罡气【攻击/防御】（gangQi_damagePoint/gangQi_armorPoint）
	///		30021/22：罡气【气竭/气盈】自愈率（gangQi_qiYingRevive/gangQi_qiJieRevive）
	///		30023：临时移速（tempSpeed），非常规移动时使用，如“野外竞速”（@CST-2139）
	///		30024：治疗成效（cure）
	///		30025/26：【暴击/招架】倍率（critRatio/parryRatio）
	///		40001/2：【造成/承受】伤害修正（详见@CST-4575）
	///		40003/4：造成【物理/法术】伤害修正（同上）
	///		40005/6：承受【物理/法术】伤害修正（同上）
	///		40007/8/9：造成对【玩家/幻兽/怪物】伤害修正（同上）
	///		40010/11/12：承受被【玩家/幻兽/怪物】伤害修正（同上）
	///		40013：造成治疗修正
	///		40014：承受治疗修正
	///	Param2：增益加成值（如0.5代表“增益50%”，-0.5代表“衰减50%”）
	///	Param3：增益附加值（整型，如5代表“增益5点”，-5代表“衰减5点”）
	///		对于“百分比”形式的属性，如伤害修正、命中率，配置“附加值增益”时需要注意配合放大（@ItemTypeEnum.PRECENTRATIO）
	///		示例：“1000”，代表“【命中率附加值】＋10%”
	///	Param4~5：无
	///支持：
	///	战斗属性的增益/衰减（@CST-1634/@CST-4575）
	///	战斗属性增益结算：（详见alienbrain://NEWAB/创世3/01_设计文档/战斗系统/战斗属性/战斗属性框架.vsdx）
	///		属性终值＝(属性基础值＋属性成长值)＋(1×属性加成值)＋属性附加值
	///			有效范围：加成值∈[-1,1]（如“移动速度增益＝9999%”，表现为“有效增益＝100%”）
	///			有效范围：终值∈[0,99999999]（如“攻击力增益＝-99999999”，表现为“攻击力终值＝0”）
	///	可影响“属性跑”的怪物AI移动表现，不影响“意愿跑”的表现（@CST-4174）
	///注意：
	///	“上限”类型的属性（如，生命值最大值、法力值最大值）更新时，将“等比例影响”对应的当前值（如“现在半血，换件衣服提高了上限，还是半血”）
	///	以下属性，终值下限为1（而不是0）：生命值最大值、法力值最大值、罡气最大值、物攻、法攻（@CST-6398）
	///	已知风险：暴击倍率已被老板钦点为“最强劲的技能”的作用效果，日常使用时请慎用，避免滥用
	HoldEffectAddAttr = 7 UMETA(DisplayName = "HoldEffectAddAttr"),
	///HoldEffectPlayEffect（持有表现效果）
	///	Param1：动作ID1:起始帧时间1|动作ID2:起始帧时间2（秒）…（:冒号和|竖号分隔）
	///		示例：“Attack_01|Attack_02:0.5”，代表“顺序播放：从头开始的Attack_01、从0.5秒开始的Attack_02”
	///	Param2：光效ID列表（@DT_EffectCfg，|竖号分隔）
	///	Param3：音效ID列表（@DT_AudioCfg，|竖号分隔）
	///	Param4~5：无
	///支持：
	///	动作/光效/音效表现的播放/中止/重播（@CST-1719）
	///	支持动作起始帧时间设定（@CST-1192）
	///	支持连续播放动作：若任一动作中断，则中断连续动作（@CST-3036）
	///注意：
	///	已知风险：若表现的有效依赖施受双方都存在，则不能保证表现重播成功（@CST-2568）
	///		建议改用专用的支持，如连线Buff，详见BuffLink（@CST-2568）
	HoldEffectPlayEffect = 8 UMETA(DisplayName = "HoldEffectPlayEffect"),
	///HoldEffectWind（根须缠绕效果）
	///	Param1~5：无
	///设计原意：
	///	被根须缠绕了，走不动
	///支持：
	///	效果状态持有（/queryAttr effectCounter，#6，第7个）
	///	开关限制（@csconst.EFFECT_STATE_TO_ACTION_FLAGS）
	///		禁止玩家改变朝向、禁止主动移动、禁止跳跃（@CST-572）
	///注意：
	///	自带光效表现（@DT_EffectStatePerformanceCfg，@CST-3076）
	///	一般地，“能力异常表现”应视为“控制行为”，相关开关条件应默认配置“禁止受控制”
	HoldEffectWind = 9 UMETA(DisplayName = "HoldEffectWind"),
	///HoldEffectAddActCounter（自定义开关限制效果）
	///	Param1：开关状态列表（|竖号分隔，不得缺省）
	///		  0：禁止主动移动（ForbidMove，@csdefine.ACTION_FORBID_MOVE）
	///		  1：禁止施法（ForbidSpell）
	///		  2：禁止使用道具（ForbidItem）
	///		  3：禁止被攻击（ForbidBeAttack）
	///		  4：禁止攻击（ForbidAttack）
	///		  5：禁止跳跃（ForbidJump）
	///		  6：禁止穿戴装备（ForbidWield）
	///		  7：禁止聊天（ForbidChat）
	///		  8：禁止交互（ForbidTalk）
	///		  9：禁止触发被动技能（ForbidTriggerPassiveSkill）
	///		10：禁止被击退（ForbidBeHitBack）
	///		11：禁止变换模型（ForbidChangeBody）
	///		12：禁止变换姿势（ForbidChangePoseture）
	///		13：禁止召唤幻兽（ForbidConjurePet）
	///		14：禁止改变朝向（ForbidTranslateDirection）
	///		15：禁止紧急回避（ForbidEmergencyExit）
	///		16：禁止幻兽骑乘（ForbidMountPet）
	///		17：禁止被控制（ForbidBeControl）
	///		18：禁止被增益（ForbidBeImpress）
	///		19：禁止被减损（ForbidBeDepress）
	///		查询：可以通过【/queryAttr actCounter】，查询【开关状态计数器】的属性，确认指定开关的状态
	///		示例：“0|1|5”，代表“禁止主动移动、禁止施法、禁止跳跃，但没有眩晕状态”
	///	Param2~5：无
	///设计原意：
	///	提供一个“方便直接的不需要考虑复用的开挂方法”以降低必要的状态数量
	///支持：
	///	不通过“效果状态”，直接自定义地影响“开关状态”（@CST-1947）
	///注意：
	///	仅当“足够简单”且“未有合适的效果状态”时适用，请谨慎使用，避免滥用
	///	情况足够复杂时，应当优先考虑“是否应当定义成效果状态”，欢迎联系策划数值组同人
	HoldEffectAddActCounter = 10 UMETA(DisplayName = "HoldEffectAddActCounter"),
	///HoldEffectProtect（保护效果）
	///	Param1~5：无
	///设计原意：
	///	为客户端加载中的玩家，提供有限的保护
	///支持：
	///	效果状态持有（/queryAttr effectCounter，#7，第8个）
	///	保护表现：避免单位间交互，隐藏模型，结束时重新触发陷阱（@CST-1995）
	///	开关限制（@csconst.EFFECT_STATE_TO_ACTION_FLAGS）
	///		禁止主动移动、禁止跳跃、禁止紧急回避、禁止施法、禁止触发被动技能、禁止使用道具、禁止装备道具、禁止交互、
	///		禁止攻击、禁止被攻击、禁止被击退、禁止被控制、
	///注意：
	///	自带光效表现（@DT_EffectStatePerformanceCfg，@CST-3076）
	HoldEffectProtect = 11 UMETA(DisplayName = "HoldEffectProtect"),
	///HoldEffectRegisterPassiveSkill（注册被动技能效果）
	///	Param1：被动技能ID列表（@DT_PassiveSkillCfg，|竖号分隔）
	///	Param2~5：无
	///支持：
	///	持有期间可以触发该被动技能（@CST-2212）
	///	支持列表输入（@CST-7259）
	///注意：
	///	已知风险：若被动技能ID错误，则初始化时无报错，使用时才有报错，请谨慎配置“被动技能ID”
	HoldEffectRegisterPassiveSkill = 12 UMETA(DisplayName = "HoldEffectRegisterPassiveSkill"),
	///HoldEffectBeBlow（持有吹风效果）
	///	Param1：吹风速度方向（世界的绝对的方向，格式“X Y Z”）
	///	Param2：吹风速度大小基础值（米/秒）
	///	Param3~5：无
	///支持：
	///	PC吹风表现：在不需要移动的情况下，给玩家附加一个速度（@CST-2354）
	///	怪物吹风表现（@CST-8926）
	///	吹风速度结算：吹风速度＝吹风速度基础值×（1＋吹风速度修正）
	///注意：
	///	受术者单位类型：PC、Monster限定
	///	需要配合HoldEffectSetBlowPercentage使用
	HoldEffectBeBlow = 13 UMETA(DisplayName = "HoldEffectBeBlow"),
	///HoldEffectConfusion（混乱效果）
	///	Param1~5：无
	///设计原意：
	///	不受控制地胡乱移动
	///支持：
	///	效果状态持有（/queryAttr effectCounter，#9，第10个）
	///	混乱表现：不受控制地随机乱走（@CST-2937）
	///	开关限制（@csconst.EFFECT_STATE_TO_ACTION_FLAGS）
	///		禁止交互（@CST-4581）
	///注意：
	///	受术者单位类型：PC限定
	///	自带光效表现（@DT_EffectStatePerformanceCfg，@CST-3076）
	HoldEffectConfusion = 15 UMETA(DisplayName = "HoldEffectConfusion"),
	///HoldEffectAddKvDecayRate（杀气恢复增益效果）
	///	Param1：杀气恢复速度修正（如0.5代表“提高50%杀气恢复速度”，不得缺省）
	///	Param2~5：无
	///支持：
	///	道具“清心丹”相关表现，加速杀气值恢复的速度（@CST-2467）
	///注意：
	///	受术者单位类型：PC限定
	HoldEffectAddKvDecayRate = 16 UMETA(DisplayName = "HoldEffectAddKvDecayRate"),
	///HoldEffectSetBlowPercentage（受迫吹风增益效果）
	///	Param1：吹风速度修正（如0.5代表“加速50%”）
	///	Param2~5：无
	///支持：
	///	吹风表现修正，调整吹风表现的速度（@CST-2354）
	///	风速结算：需要配合HoldEffectBeBlow使用
	///		风速＝风速基础值×（1＋吹风速度修正）
	///注意：
	///	受术者单位类型：PC限定
	HoldEffectSetBlowPercentage = 17 UMETA(DisplayName = "HoldEffectSetBlowPercentage"),
	///HoldEffectAddOnsMesh（持有模型挂件效果）
	///	Param1：模型挂件配置ID（@DT_MeshBindCfg）
	///	Param2~5：无
	///支持：
	///	把某个模型绑定到目标单位身上的表现（@CST-2359/@CST-3326）
	HoldEffectAddOnsMesh = 18 UMETA(DisplayName = "HoldEffectAddOnsMesh"),
	///HoldEffectCallMonsterByMonster（召唤协同作战怪物效果）
	///	Param1：目标怪物ID:替换召唤物ID|目标怪物ID:替换召唤物ID（@DT_MonsterCfg，:冒号和|竖号分隔，不得留空，不得部分缺省）
	///	Param2：半径（米）
	///	Param3~5：无
	///支持：
	///	把目标怪物，替换成召唤物：继承PC的敌对关系，跟随移动/传送、协助攻击（@CST-3704）
	///注意：
	///	受术者单位类型：PC限定（@CST-1455）
	///	召唤物单位类型：monsterExtCall限定（@CST-1455）
	HoldEffectCallMonsterByMonster = 19 UMETA(DisplayName = "HoldEffectCallMonsterByMonster"),
	///HoldEffectUnyielding（不屈效果）
	///	Param1~5：无
	///设计原意：
	///	确保单位不会因为“战斗”而死亡
	///支持：
	///	效果状态持有（/queryAttr effectCounter，#10，第11个）
	///	不屈表现：怎么打都剩“1点血”（@CST-4146）
	///		与AI锁血冲突，优先级有：锁血＞不屈＞默认
	///注意：
	///	自带光效表现（@DT_EffectStatePerformanceCfg，@CST-3076）
	HoldEffectUnyielding = 20 UMETA(DisplayName = "HoldEffectUnyielding"),
	///HoldEffectFabaoPlayEffect（法宝持有表现效果）
	///	Param1：动作ID列表（|竖号分隔，多个动作融合为一个动作）
	///	Param2：光效ID列表（@DT_EffectCfg，|竖号分隔，要求与参数3数量匹配）
	///	Param3：光效播放时间列表（秒，|竖号分隔，要求与参数2数量匹配）
	///	Param4~5：无
	///支持：
	///	法宝播放动作效果（@CST-4153/@CST-4589）
	HoldEffectFabaoPlayEffect = 21 UMETA(DisplayName = "HoldEffectFabaoPlayEffect"),
	///HoldEffectAddExtraFaBaoSkillBar（法宝额外快捷栏效果）
	///	Param1：额外技能ID列表（@DT_SkillCfg，|竖号分隔，顺序显示）
	///	Param2~3：无
	///支持：
	///	法宝额外快捷栏表现（@CST-4153）
	HoldEffectAddExtraFaBaoSkillBar = 22 UMETA(DisplayName = "HoldEffectAddExtraFaBaoSkillBar"),
	///HoldEffectCreateFaBao（召唤法宝效果）
	///	Param1：法宝ID（@DT_FaBaoCfg）
	///	Param2~5：无
	///支持：
	///	功能待定（@CST-4339）
	HoldEffectCreateFaBao = 23 UMETA(DisplayName = "HoldEffectCreateFaBao"),
	///HoldEffectCreateAirCraft（召唤飞行器效果）
	///	Param1：飞行模型配置ID（@DT_FlyBindActorCfg）
	///	Param2~5：无
	///支持：
	///	实现环绕在玩家周围：功能待定（@CST-4755）
	///注意：
	///	受术者单位类型：PC限定
	HoldEffectCreateAirCraft = 24 UMETA(DisplayName = "HoldEffectCreateAirCraft"),
	///HoldEffectFreeze（冻结效果）
	///	Param1~5：无
	///支持：
	///	效果状态持有（/queryAttr effectCounter，#11，第12个）
	///	动作冻结表现：动作停住，后续恢复到待机（@CST-4747）
	///	开关限制（@csconst.EFFECT_STATE_TO_ACTION_FLAGS）
	///		禁止玩家改变朝向、禁止主动移动、禁止跳跃、禁止紧急回避、
	///		禁止施法（@CST-1209）、禁止使用道具、禁止交互（@CST-4581）
	HoldEffectFreeze = 25 UMETA(DisplayName = "HoldEffectFreeze"),
	///HoldEffectFly（飞行状态效果）
	///	Param1~5：无
	///支持：
	///	待定（@CST-4369/@CST-5288）
	HoldEffectFly = 26 UMETA(DisplayName = "HoldEffectFly"),
	///HoldEffectMonsterExtArmorLock（镇煞宫专用，金钟罩表现效果）
	///	Param1：淡出时间
	///	Param2~5：无
	///支持：
	///	（@CST-3804）
	///注意：
	///	需要配合MonsterExtArmorLock使用，怪物模型SK_GW2295
	HoldEffectMonsterExtArmorLock = 27 UMETA(DisplayName = "HoldEffectMonsterExtArmorLock"),
	///HoldEffectBindDisplayObject（模型绑定部件效果）
	///	Param1：模型挂件配置ID（@DT_MeshBindCfg）
	///	Param2~5：无
	///支持：
	///	（@CST-5453）
	HoldEffectBindDisplayObject = 28 UMETA(DisplayName = "HoldEffectBindDisplayObject"),
	///HoldEffectSubmerge（遁地效果）
	///	Param1~5：无
	///支持：
	///	（@CST-5772）
	HoldEffectSubmerge = 29 UMETA(DisplayName = "HoldEffectSubmerge"),
	///HoldEffectCrossFade（消融表现效果）
	///	Param1：消融的边缘颜色  “R|G|B”(范围0-1)
	///	Param2：消融的方向（可自行尝试直至效果满意）
	///		示例：“0|0|0|0”，表现为“整体消融”
	///		示例：“0|0|1|0”，表现为“从上到下”
	///		示例：“0|0|1|1”，表现为“从下到上”
	///		示例：“1|0|0|0”，表现为“从右到左”
	///		示例：“1|0|0|1”，表现为“从左到右”
	///	Param3：初始消融程度（0表现为“不消融”，1表现为“完全消融”）|目标消融程度|消融时间/s|延迟消融时间（缺省0秒）
	///	Param4~5：无
	///支持：
	///	类似火焰烧穿的材质特效表现，注册时消融过去，注销时恢复表现（@CST-1659）
	///注意：
	///	已知风险：尚不支持PC相关模型表现，部分怪物材质表现有遗漏，如有发现请随时吐槽（@CST-1659）
	///	已知风险：多个此持有效果同时作用时，可只独立触发渐变表现，但过程中的状态表现不正确，请谨慎使用（@CST-7926）
	HoldEffectCrossFade = 30 UMETA(DisplayName = "HoldEffectCrossFade"),
	///HoldEffectShow（表演效果）
	///	Param1~5：无
	///设计原意：
	///	保护表演时的单位，但不显示霸体光效（@CST-6473）
	///支持：
	///	效果状态持有（/queryAttr effectCounter，#12，第13个）
	///	开关限制（@csconst.EFFECT_STATE_TO_ACTION_FLAGS）
	///		禁止被攻击（@CST-7538）、禁止被击退、禁止被控制（@CST-6473）
	///注意：
	///	自带光效表现（@DT_EffectStatePerformanceCfg，@CST-3076）
	///	已知风险：目前从开关影响上看，表演与无敌完全一致，只有光效表现上的差异，请谨慎使用
	HoldEffectShow = 32 UMETA(DisplayName = "HoldEffectShow"),
	///HoldEffectGravityScale（重力系数增益效果）
	///	Param1：增益百分比（如-0.5代表“重力减少50%”）|固定值（浮点型，米/秒²）
	///	Param2~5：无
	///设计原意：
	///	支持“缓缓下落”、“漂浮”…等表现
	///支持：
	///	调整PC的重力系数（@CST-8284）
	///		重力系数的基础值由客户端按需调整（如上升1.0，下降2.0），此处调整的是“加成值和附加值修正”
	///	重力加速度结算：
	///		重力系数终值＝重力系数基础值×(1＋加成值)＋附加值
	///		有效范围：重力系数终值≥0
	///		重力加速度＝默认重力加速度×重力系数终值
	///		默认重力加速度＝9.8米/秒²
	///注意：
	///	受术者单位类型：PC限定
	///	此类“辅助属性”不存在（也无法查询），只在需要时临时产生，可以理解为“技术指标”
	///		重力系数由客户端特别支持，通过重播机制同步，而非服务器属性广播同步
	HoldEffectGravityScale = 33 UMETA(DisplayName = "HoldEffectGravityScale"),
	///HoldEffectHide（隐身效果）
	///	Param1：透明淡入时间（秒，＝0代表“立即”）
	///	Param2：透明淡出时间（同上）
	///	Param3~5：无
	///支持：
	///	隐身表现：非友好关系者，不可见，不可选定，不可碰撞；友好关系者，看到半透明表现（@CST-9111）
	///注意：
	///	已知风险：此渲染透明方案表现上有局限，请谨慎使用
	///		①同屏渲染透明表现，建议不多于3人（@CST-4650）
	///		②单位透明度，建议优先选择0.3、0.7、1.0，三个预设档次（@CST-4650）
	///		③渲染透明表现与“阴影”、“贴花”、“单位头顶UI”…等表现有冲突，建议主动规避（@CST-4841）
	///		④渲染透明表现之间互相冲突，优先级有：HoldEffectHide＞BuffTransparency（@CST-9111）
	HoldEffectHide = 34 UMETA(DisplayName = "HoldEffectHide"),
	///HoldEffectIntensifySkill（技能进阶效果）
	///	Param1：技能容器ID（@DT_QuickSkillCfg）
	///	Param2：“升级等级”改变，对应师门技能菜单中的“升级”（级）
	///	Param3：“进阶等级”改变，对应被动技能菜单中的“进阶”（级）
	///	Param4~5：无
	///支持：
	///	描述“师门技能进阶”的表现，可以灵活地更新“升级等级”和“进阶等级”（@CST-11040）
	///注意：
	///	受术者单位类型：PC限定
	HoldEffectIntensifySkill = 35 UMETA(DisplayName = "HoldEffectIntensifySkill"),
	///HoldEffectChangePetAI（幻兽AI切换效果）
	///	Param1：幻兽AI的ID（@DT_PetSTAICfg）
	///	Param2~5：无
	///支持：
	///	让幻兽可以按需切换AI行为表现，供幻兽神通技能的变身效果使用（@CST-12344）
	///注意：
	///	受术者单位类型：Pet限定
	HoldEffectChangePetAI = 36 UMETA(DisplayName = "HoldEffectChangePetAI"),
	///HoldEffectCreateTrace（生成移动轨迹【毒雾】）
	///	Param1：轨迹表现用，光效ID（@DT_EffectCfg）
	///	Param2：轨迹生成间隔距离，每段轨迹生成一个矩形碰撞盒（厘米，建议＞70）
	///	Param3：每个碰撞盒持续时间（秒，表现上应该和光效表现保持一致）
	///	Param4：矩形碰撞盒的 宽 | 高（厘米，长度由间隔距离决定无需配置，表现上应该和光效表现保持一致）
	///	Param5：对进入轨迹的单位使用技能ID（@DT_SkillCfg，只有进入时触发）
	///		技能申请者　【单位】＝效果持有者【单位】
	///		技能申请目标【单位】＝进入轨迹碰撞盒的【单位】
	///支持：
	///	支持“边走边放毒，后续进来的人会中毒”的表现（@CST-12344）
	///注意：
	///	受术者单位类型：PC、Pet、Monster限定
	///	引入裁判机制：
	///		①施法者是玩家或幻兽时，由主机玩家作为裁判，对目标进入轨迹的判定负责
	///		②受术者是玩家或幻兽时，由主机玩家作为裁判，对目标进入轨迹的判定负责
	///		③施法者、受术者都不是玩家或幻兽时，没有裁判，进入轨迹的判定触发无效
	HoldEffectCreateTrace = 37 UMETA(DisplayName = "HoldEffectCreateTrace"),
	///HoldEffectToxicosis（中毒表现的全屏动态效果@CST-11064）
	///	Param1~5：无
	///支持：
	///注意：
	HoldEffectToxicosis = 38 UMETA(DisplayName = "HoldEffectToxicosis"),
};

///持有效果
USTRUCT(BlueprintType)
struct CHUANGSHI_API FHOLD_EFFECT
{
	GENERATED_BODY()
	///持有效果脚本类型
	///	不同类型，决定着不同的参数定义
	UPROPERTY(EditAnywhere)
		ENUM_HOLD_EFFECT_TYPE HitEffectType;
	///参数1（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param1;
	///参数2（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param2;
	///参数3（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param3;
	///参数4（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param4;
	///参数5（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param5;
};

UENUM(BlueprintType)
enum class ENUM_SKILL_EVENT : uint8
{
	///OnDieEvent（死亡/击杀事件）
	///	Param1：开关状态列表（|竖号分隔，留空代表“无要求”）
	///		  0：禁止主动移动（ForbidMove，@csdefine.ACTION_FORBID_MOVE）
	///		  1：禁止施法（ForbidSpell）
	///		  2：禁止使用道具（ForbidItem）
	///		  3：禁止被攻击（ForbidBeAttack）
	///		  4：禁止攻击（ForbidAttack）
	///		  5：禁止跳跃（ForbidJump）
	///		  6：禁止穿戴装备（ForbidWield）
	///		  7：禁止聊天（ForbidChat）
	///		  8：禁止交互（ForbidTalk）
	///		  9：禁止触发被动技能（ForbidTriggerPassiveSkill）
	///		10：禁止被击退（ForbidBeHitBack）
	///		11：禁止变换模型（ForbidChangeBody）
	///		12：禁止变换姿势（ForbidChangePoseture）
	///		13：禁止召唤幻兽（ForbidConjurePet）
	///		14：禁止改变朝向（ForbidTranslateDirection）
	///		15：禁止紧急回避（ForbidEmergencyExit）
	///		16：禁止幻兽骑乘（ForbidMountPet）
	///		17：禁止被控制（ForbidBeControl）
	///		18：禁止被增益（ForbidBeImpress）
	///		19：禁止被减损（ForbidBeDepress）
	///		查询：可以通过【/queryAttr actCounter】，查询【开关状态计数器】的属性，确认指定开关的状态
	///		示例：“3”，代表“只响应被正常伤害效果所造成的击杀”
	///	Param2：流程类型（缺省1）
	///		0：（施法者）击杀事件
	///		1：（受术者）被击杀事件
	///	Param3：无
	///支持：
	///	技能事件持有（/queryAttr casterSkillEventList，#0）
	///	（伤害行为）击杀时触发：	EffectAbsorbHP、EffectDamage、EffectNormalDamage（@CST-1314、@CST-6360）
	///	（非伤害行为）死亡时表现：EffectDirectlyKill（非伤害类，@CST-6360）
	///		触发者　＝（伤害效果的）受术者
	///		触发目标＝（伤害效果的）施法者
	///	触发开关筛选：只有触发事件的效果/技能的开关符合要求时，才响应触发（@CST-6360）
	///		如：“伤害致死时”，开关要求＝“要求伤害效果的开关条件为禁止被攻击”
	OnDieEvent = 0 UMETA(DisplayName = "OnDieEvent"),
	///StateChangeEvent（单位基础状态改变事件）
	///	Param1：旧状态要求（留空代表“无要求”）
	///		0：未决（@csdefine.ENTITY_STATE_PEAD）
	///		1：自由
	///		2：警戒
	///		3：战斗
	///		4：死亡
	///		5：重置（怪物限定）
	///		6：表演（怪物限定）
	///		7：摆摊（PC限定）
	///		8：稳定（怪物限定）
	///	Param2：新状态要求（留空代表“无要求”）
	///	Param3：无
	///支持：
	///	技能事件持有（/queryAttr casterSkillEventList，#1）
	///	单位基础状态改变时触发，可以输入新旧状态进行筛选（@CST-1314）
	///		触发者＝触发目标＝单位自身
	///示例：
	///	①脱战时（应当描述为，战斗状态→自由状态）
	///		Param1：3（旧状态＝战斗状态）
	///		Param2：1（新状态＝自由状态）
	///		Param3：无
	StateChangeEvent = 1 UMETA(DisplayName = "StateChangeEvent"),
	///ActWorldChangeEvent（开关状态改变事件）
	///	Param1：开关状态（不得缺省）
	///		  0：禁止主动移动（ForbidMove，@csdefine.ACTION_FORBID_MOVE）
	///		  1：禁止施法（ForbidSpell）
	///		  2：禁止使用道具（ForbidItem）
	///		  3：禁止被攻击（ForbidBeAttack）
	///		  4：禁止攻击（ForbidAttack）
	///		  5：禁止跳跃（ForbidJump）
	///		  6：禁止穿戴装备（ForbidWield）
	///		  7：禁止聊天（ForbidChat）
	///		  8：禁止交互（ForbidTalk）
	///		  9：禁止触发被动技能（ForbidTriggerPassiveSkill）
	///		10：禁止被击退（ForbidBeHitBack）
	///		11：禁止变换模型（ForbidChangeBody）
	///		12：禁止变换姿势（ForbidChangePoseture）
	///		13：禁止召唤幻兽（ForbidConjurePet）
	///		14：禁止改变朝向（ForbidTranslateDirection）
	///		15：禁止紧急回避（ForbidEmergencyExit）
	///		16：禁止幻兽骑乘（ForbidMountPet）
	///		17：禁止被控制（ForbidBeControl）
	///		18：禁止被增益（ForbidBeImpress）
	///		19：禁止被减损（ForbidBeDepress）
	///		查询：可以通过【/queryAttr actCounter】，查询【开关状态计数器】的属性，确认指定开关的状态
	///		示例：“0”，代表“响应禁止移动开关的状态改变”
	///	Param2：流程类型（缺省1）
	///		0：“变成0时”（下降沿），响应“该开关状态从1→0时”
	///		1：“变成1时”（上升沿），响应“该开关状态从0→1时”
	///	Param3：无
	///支持：
	///	技能事件持有（/queryAttr casterSkillEventList，#2）
	///	开关状态改变时触发：各种效果状态改变、单位基础状态改变（@CST-1314）
	///		触发者＝触发目标＝单位自身
	ActWorldChangeEvent = 2 UMETA(DisplayName = "ActWorldChangeEvent"),
	///CustomEvent（自定义技能事件）
	///	Param1：自定义技能事件ID（字符串，需要配合具体EffectTriggerCustomEvent使用，留空代表“没有事件”）
	///		自定义技能事件ID，暂无占位表，请谨慎使用，注意避让
	///		示例：“999001001”，代表“只要EffectTriggerCustomEvent也配置999001001，就可以响应触发”
	///	Param2~3：无
	///支持：
	///	技能事件持有（/queryAttr casterSkillEventList，#3）
	///	自定义事件：EffectTriggerCustomEvent（@CST-1314）
	///		触发者　＝（自定义事件效果的）受术者
	///		触发目标＝（自定义事件效果的）施法者
	CustomEvent = 3 UMETA(DisplayName = "CustomEvent"),
	///MoveChangeEvent（PC移动状态改变事件）
	///	Param1：PC移动状态类型（缺省0）
	///		0：全部移动
	///		1：主动移动（寻路移动…等）
	///		2：被动移动（击退位移…等）
	///	Param2：流程类型（缺省1）
	///		0：“变成非指定类型移动时”（下降沿），表现为“指定类型移动停止时”
	///		1：“变成指定类型移动时”（上升沿），表现为“指定类型移动开始时”
	///	Param3：无
	///支持
	///	技能事件持有（/queryAttr casterSkillEventList，#7）
	///	PC移动状态改变时触发：移动、击退…等（@CST-1754）
	///		触发者＝触发目标＝客户端PC单位
	///	整合移动状态：实际上移动状态类型繁多（@csdefine.MOVE_TYPE_STOP），为了策划理解与配置，此处对移动状态类型进行了整合
	///注意：
	///	触发者单位类型：PC限定（因为PC在客户端和怪物在服务器的移动状态类型定义不一致）
	///	“跳跃”不视为“移动”（因为“可以跳起来在空中移动”，所以跳跃与移动是互相独立的）
	MoveChangeEvent = 5 UMETA(DisplayName = "MoveChangeEvent"),
	///CureEvent（治疗事件）
	///	Param1：开关状态列表（|竖号分隔，留空代表“无要求”）
	///		  0：禁止主动移动（ForbidMove，@csdefine.ACTION_FORBID_MOVE）
	///		  1：禁止施法（ForbidSpell）
	///		  2：禁止使用道具（ForbidItem）
	///		  3：禁止被攻击（ForbidBeAttack）
	///		  4：禁止攻击（ForbidAttack）
	///		  5：禁止跳跃（ForbidJump）
	///		  6：禁止穿戴装备（ForbidWield）
	///		  7：禁止聊天（ForbidChat）
	///		  8：禁止交互（ForbidTalk）
	///		  9：禁止触发被动技能（ForbidTriggerPassiveSkill）
	///		10：禁止被击退（ForbidBeHitBack）
	///		11：禁止变换模型（ForbidChangeBody）
	///		12：禁止变换姿势（ForbidChangePoseture）
	///		13：禁止召唤幻兽（ForbidConjurePet）
	///		14：禁止改变朝向（ForbidTranslateDirection）
	///		15：禁止紧急回避（ForbidEmergencyExit）
	///		16：禁止幻兽骑乘（ForbidMountPet）
	///		17：禁止被控制（ForbidBeControl）
	///		18：禁止被增益（ForbidBeImpress）
	///		19：禁止被减损（ForbidBeDepress）
	///		查询：可以通过【/queryAttr actCounter】，查询【开关状态计数器】的属性，确认指定开关的状态
	///	Param2：流程类型（缺省1）
	///		0：（施法者）治疗事件
	///		1：（受术者）被治疗事件
	///	Param3：无
	///支持：
	///	技能事件持有（/queryAttr casterSkillEventList，#9）
	///	治疗时触发：EffectAddHP（@CST-1314）、EffectNormalCure（@CST-10638）
	///		不同“流程类型”将在不同目标（施法者或受术者）身上触发
	///	触发开关筛选：要求触发事件的效果/技能的开关，与要求一致，才响应触发（@CST-1314）
	///注意：
	///	吸血、自愈、复活…等不视为治疗（不是“主动的治疗”，而是“被动的恢复”）
	///	尚未支持“携带治疗值信息触发被动”（如治疗、反弹）
	CureEvent = 6 UMETA(DisplayName = "CureEvent"),
	///HurtEvent（伤害事件）
	///	Param1：开关状态列表（|竖号分隔，留空代表“无要求”）
	///		  0：禁止主动移动（ForbidMove，@csdefine.ACTION_FORBID_MOVE）
	///		  1：禁止施法（ForbidSpell）
	///		  2：禁止使用道具（ForbidItem）
	///		  3：禁止被攻击（ForbidBeAttack）
	///		  4：禁止攻击（ForbidAttack）
	///		  5：禁止跳跃（ForbidJump）
	///		  6：禁止穿戴装备（ForbidWield）
	///		  7：禁止聊天（ForbidChat）
	///		  8：禁止交互（ForbidTalk）
	///		  9：禁止触发被动技能（ForbidTriggerPassiveSkill）
	///		10：禁止被击退（ForbidBeHitBack）
	///		11：禁止变换模型（ForbidChangeBody）
	///		12：禁止变换姿势（ForbidChangePoseture）
	///		13：禁止召唤幻兽（ForbidConjurePet）
	///		14：禁止改变朝向（ForbidTranslateDirection）
	///		15：禁止紧急回避（ForbidEmergencyExit）
	///		16：禁止幻兽骑乘（ForbidMountPet）
	///		17：禁止被控制（ForbidBeControl）
	///		18：禁止被增益（ForbidBeImpress）
	///		19：禁止被减损（ForbidBeDepress）
	///		查询：可以通过【/queryAttr actCounter】，查询【开关状态计数器】的属性，确认指定开关的状态
	///		示例：“3”，代表“只响应被正常伤害效果所造成的伤害”
	///	Param2：流程类型（缺省1）
	///		0：（施法者）伤害事件
	///		1：（受术者）被伤害事件
	///	Param3：标记列表（|竖号分隔，留空代表“没有标记”，具体功能与参数格式由标记定义）
	///		示例：“IsCritical”，代表“要求本次伤害流程的过程，有暴击成功”（@CST-7346）
	///		示例：“IsParry”，代表“要求本次伤害流程的过程，有招架成功”（@CST-7346）
	///支持：
	///	技能事件持有（/queryAttr casterSkillEventList，#12）
	///	伤害时触发：EffectAbsorbHP、EffectDamage、EffectNormalDamage（@CST-1635）
	///		不同“流程类型”将在不同目标（施法者或受术者）身上触发
	///	触发开关筛选：要求触发事件的效果/技能的开关，与要求一致，才响应触发（@CST-1635）
	///	触发标记筛选：以“本次伤害流程是否暴击/招架”为依据，判断是否响应触发（@CST-7320）
	///	携带伤害值信息：可以依据伤害值触发被动，如反弹、吸血（@CST-4169）
	HurtEvent = 9 UMETA(DisplayName = "HurtEvent"),
	///SkillProcessEvent（技能流程事件）
	///	Param1：开关状态（留空代表“无要求”）
	///		  0：禁止主动移动（ForbidMove，@csdefine.ACTION_FORBID_MOVE）
	///		  1：禁止施法（ForbidSpell）
	///		  2：禁止使用道具（ForbidItem）
	///		  3：禁止被攻击（ForbidBeAttack）
	///		  4：禁止攻击（ForbidAttack）
	///		  5：禁止跳跃（ForbidJump）
	///		  6：禁止穿戴装备（ForbidWield）
	///		  7：禁止聊天（ForbidChat）
	///		  8：禁止交互（ForbidTalk）
	///		  9：禁止触发被动技能（ForbidTriggerPassiveSkill）
	///		10：禁止被击退（ForbidBeHitBack）
	///		11：禁止变换模型（ForbidChangeBody）
	///		12：禁止变换姿势（ForbidChangePoseture）
	///		13：禁止召唤幻兽（ForbidConjurePet）
	///		14：禁止改变朝向（ForbidTranslateDirection）
	///		15：禁止紧急回避（ForbidEmergencyExit）
	///		16：禁止幻兽骑乘（ForbidMountPet）
	///		17：禁止被控制（ForbidBeControl）
	///		18：禁止被增益（ForbidBeImpress）
	///		19：禁止被减损（ForbidBeDepress）
	///		查询：可以通过【/queryAttr actCounter】，查询【开关状态计数器】的属性，确认指定开关的状态
	///		示例：“1”，代表“只响应一般的技能流程事件”
	///	Param2：流程类型（缺省1）
	///		0：施法 结束时（打击结束后，持有注销前）
	///		1：施法 开始时（持有注册后，打击开始前）
	///		2：施法 中断时（中断了，就不会触发施法结束时）
	///	Param3：技能ID要求（@DT_SkillCfg，留空代表“无要求”）
	///支持：
	///	技能事件持有（/queryAttr casterSkillEventList，#13）
	///	技能施展/结束时触发：InstantSkill、CombatSkill（@CST-2761）
	///		触发者＝触发目标＝（主动技能的）施法者
	///	触发开关筛选：要求“技能/效果开关”符合要求才响应触发（@CST-2761）
	///	技能ID筛选：要求“技能ID”符合要求才响应触发（@CST-4317）
	///注意：
	///	不同流程类型，都在施法者身上触发
	///示例：
	///	①紧急回避开始时（可描述为，开关是禁止紧急回避的技能，施展开始时）
	///		Param1：15（禁止紧急回避）
	///		Param2：1（施法开始）
	///		Param3：无
	SkillProcessEvent = 10 UMETA(DisplayName = "SkillProcessEvent"),
	///SpaceChangeEvent（地图间传送事件）
	///	Param1：旧地图要求（格式“1|地图ID1:地图ID2…”，留空代表“无要求”）
	///	　条件类型：
	///		0：不是其中任一地图
	///		1：是其中任一地图
	///	　地图ID列表（@DT_HashMapCfg，:冒号分隔）：
	///		查询：可以通过【/queryAttr spaceScriptID】，查询【当前地图ID】属性
	///	Param2：新地图要求（同上）
	///	Param3：流程类型（缺省1）
	///		0：（触发者）离开地图前，还在旧地图中
	///		1：（触发者）离开地图后，已在新地图中
	///支持：
	///	技能事件持有（/queryAttr casterSkillEventList，#14）
	///	当前所在地图改变时触发，PC上线创建时不触发（@CST-2761）
	///		触发者＝触发目标＝单位自身
	///	区分“传送前”和“传送后”（@CST-5033）
	///注意：
	///	触发者单位类型：PC、MonsterExtCall、Pet限定
	///示例：
	///	①传送到测试地图bigmap_1之后
	///		Param1：0|bigmap_1（旧地图不是bigmap_1）
	///		Param2：1|bigmap_1（新地图是bigmap_1）
	///		Param3：无（缺省1，到了新地图之后）
	SpaceChangeEvent = 11 UMETA(DisplayName = "SpaceChangeEvent"),
	///InitiaiveStopSkillEvent（玩家主动中止技能事件）
	///	Param1~3：无
	///支持：
	///	技能事件持有（/queryAttr casterSkillEventList，#20）
	///	按下ESC键时，申请中断当前引导技能（@CST-3817）
	///		触发者＝触发目标＝（操作的）客户端PC单位
	///注意：
	///	触发目标单位类型：PC限定（依赖客户端支持）
	///	使用方法：“技能的CasterInterruptSkillEvent配置使用”限定
	///	热更新方法：由于需要客户端协助发送申请，因此配置热更新后，还需要重新施展一次该技能后，才能生效
	InitiaiveStopSkillEvent = 12 UMETA(DisplayName = "InitiaiveStopSkillEvent"),
	///InitiaiveStopBuffEvent（玩家主动中止Buff事件）
	///	Param1~3：无
	///支持：
	///	技能事件持有（/queryAttr casterSkillEventList，#21）
	///	鼠标右键点Buff图标时，申请中断指定的Buff（@CST-3817）
	///		触发者＝触发目标＝（操作的）客户端PC单位
	///注意：
	///	触发目标单位类型：PC限定（依赖客户端支持）
	///	使用方法：“Buff的TargetInterruptBuffEvent配置使用”限定
	///	热更新方法：由于需要客户端协助发送申请，因此配置热更新后，还需要重新添加一次该Buff后，才能生效
	InitiaiveStopBuffEvent = 13 UMETA(DisplayName = "InitiaiveStopBuffEvent"),
	///BuffProcessEvent（Buff流程事件）
	///	Param1：开关状态（留空代表“无要求”）
	///		  0：禁止主动移动（ForbidMove，@csdefine.ACTION_FORBID_MOVE）
	///		  1：禁止施法（ForbidSpell）
	///		  2：禁止使用道具（ForbidItem）
	///		  3：禁止被攻击（ForbidBeAttack）
	///		  4：禁止攻击（ForbidAttack）
	///		  5：禁止跳跃（ForbidJump）
	///		  6：禁止穿戴装备（ForbidWield）
	///		  7：禁止聊天（ForbidChat）
	///		  8：禁止交互（ForbidTalk）
	///		  9：禁止触发被动技能（ForbidTriggerPassiveSkill）
	///		10：禁止被击退（ForbidBeHitBack）
	///		11：禁止变换模型（ForbidChangeBody）
	///		12：禁止变换姿势（ForbidChangePoseture）
	///		13：禁止召唤幻兽（ForbidConjurePet）
	///		14：禁止改变朝向（ForbidTranslateDirection）
	///		15：禁止紧急回避（ForbidEmergencyExit）
	///		16：禁止幻兽骑乘（ForbidMountPet）
	///		17：禁止被控制（ForbidBeControl）
	///		18：禁止被增益（ForbidBeImpress）
	///		19：禁止被减损（ForbidBeDepress）
	///		查询：可以通过【/queryAttr actCounter】，查询【开关状态计数器】的属性，确认指定开关的状态
	///		示例：“10”，代表“只响应击退行为的Buff流程事件”
	///	Param2：流程类型（缺省1）
	///		0：Buff注销时（持有注销后）
	///		1：Buff注册时（持有注册前）
	///		2：Buff开始时（持有注册后，打击开始前）
	///		3：Buff中断时（中断发生后，持有注销前）
	///		4：Buff结束时（打击结束后，持有注销前）
	///	Param3：BuffID要求（@DT_BuffCfg，留空代表“无要求”）
	///支持：
	///	技能事件持有（/queryAttr casterSkillEventList，#24）
	///	Buff添加/移除/开始/结束/中断时时触发（@CST-4317、CST-10374）
	///		触发者＝触发目标＝（Buff的）持有者
	///	触发开关筛选：要求触发事件的效果/技能的开关，与要求一致，才响应触发（如“伤害致死时”，开关要求＝“要求伤害效果的开关条件为禁止被攻击”）
	///注意：
	///	不同流程类型，都在Buff受术者身上触发
	///	Buff中断行为，将触发中断时、注销时；结束行为，触发结束时、注销时；结束和中断不会一起触发
	BuffProcessEvent = 14 UMETA(DisplayName = "BuffProcessEvent"),
	///SkillPostureChangeEvent（心法状态改变事件）
	///	Param1：旧心法状态要求（留空代表“无要求”）
	///		　0：默认心法（@csdefine.SKILL_POSTURE_NONE）
	///		101：天怒心法（战士）
	///		102：神威心法（战士）
	///		201：幻剑心法（剑客）
	///		202：天剑心法（剑客）
	///		301：九幽心法（刺客）
	///		302：雷鸣心法（刺客）
	///		401：寒霜心法（法师）
	///		402：神逸心法（法师）
	///	Param2：新心法状态要求（同上）
	///	Param3：无
	///支持：
	///	技能事件持有（/queryAttr casterSkillEventList，#25）
	///	心法状态改变时触发（@CST-4778）
	///		触发者＝触发目标＝单位自身
	///注意：
	///	触发者单位类型：PC限定
	SkillPostureChangeEvent = 15 UMETA(DisplayName = "SkillPostureChangeEvent"),
	///EffectStateChangeEvent（效果状态改变事件）
	///	Param1：效果状态（@csdefine.EFFECT_STATE_LIST，不得缺省）
	///		  0：眩晕
	///		  1：霸体
	///		  2：无敌
	///		  3：受击（击退类Buff默认持有）
	///		  4：定身
	///		  5：睡眠
	///		  6：根须缠绕
	///		  7：保护
	///		  8：跟随（包括组队跟随和队友跟随）
	///		  9：混乱
	///		10：不屈
	///		11：冻结
	///		12：表演
	///		13：隐身
	///	Param2：流程类型（缺省1）
	///		0：“变成0时”（下降沿），响应“该效果状态从1→0时”
	///		1：“变成1时”（上升沿），响应“该效果状态从0→1时”
	///	Param3：无
	///支持：
	///	技能事件持有（/queryAttr casterSkillEventList，#27）
	///	效果状态改变时触发（@CST-4934）
	///		触发者＝触发目标＝单位自身
	EffectStateChangeEvent = 16 UMETA(DisplayName = "EffectStateChangeEvent"),
	///RequestActionSkillEvent（玩家操作申请事件）
	///	Param1：操作申请类型（留空代表“无要求，全部类型可以”）
	///		1：（已废弃，@CST-9527）主动移动
	///		2：使用技能
	///		3：使用物品
	///		4：交互（NPC、spellBox…等）
	///		5：幻兽相关操作（召唤、收回…等）
	///	Param2：具体ID要求（对应指定的操作申请类型，留空代表“无要求”）
	///		对应操作申请类型“2：使用技能”：技能ID列表（@DT_SkillCfg，|竖号分隔）
	///		对应操作申请类型“3：使用物品”：道具ID列表（@DT_ItemDataCfg，|竖号分隔）
	///	Param3：开关状态要求（对应指定的操作申请类型，留空代表“无要求”）
	///		  0：禁止主动移动（ForbidMove，@csdefine.ACTION_FORBID_MOVE）
	///		  1：禁止施法（ForbidSpell）
	///		  2：禁止使用道具（ForbidItem）
	///		  3：禁止被攻击（ForbidBeAttack）
	///		  4：禁止攻击（ForbidAttack）
	///		  5：禁止跳跃（ForbidJump）
	///		  6：禁止穿戴装备（ForbidWield）
	///		  7：禁止聊天（ForbidChat）
	///		  8：禁止交互（ForbidTalk）
	///		  9：禁止触发被动技能（ForbidTriggerPassiveSkill）
	///		10：禁止被击退（ForbidBeHitBack）
	///		11：禁止变换模型（ForbidChangeBody）
	///		12：禁止变换姿势（ForbidChangePoseture）
	///		13：禁止召唤幻兽（ForbidConjurePet）
	///		14：禁止改变朝向（ForbidTranslateDirection）
	///		15：禁止紧急回避（ForbidEmergencyExit）
	///		16：禁止幻兽骑乘（ForbidMountPet）
	///		17：禁止被控制（ForbidBeControl）
	///		18：禁止被增益（ForbidBeImpress）
	///		19：禁止被减损（ForbidBeDepress）
	///		查询：可以通过【/queryAttr actCounter】，查询【开关状态计数器】的属性，确认指定开关的状态
	///		示例：“1”，代表“只响应一般的技能操作申请事件”
	///设计原意：
	///	中断“保护状态”的时机，应该比“行为执行时”更早，因此定义了一个新的技能事件，在“收到操作申请时”进行触发（@CST-3009）
	///支持：
	///	技能事件持有（/queryAttr casterSkillEventList，#28）
	///	玩家提交申请时触发，包括：使用技能、使用物品、交互、幻兽相关操作（@CST-3009）
	///		触发者＝触发目标＝客户端PC单位
	///	收到“玩家操作申请”就会触发，与申请是否成功通过无关
	///		（如“又保护又眩晕时，按下技能键，保护将会中断，而技能将会施展失败”）
	///	可以筛选操作申请类型（@CST-5448）
	///	可以筛选具体ID、开关（@CST-7320）
	///注意：
	///	已知风险：为了避免过于频繁的通讯，客户端会在某些情况下屏蔽操作申请（也就不会触发本事件），请谨慎使用
	///		①快捷栏冷却时，不会发送技能申请
	///		②技能引导时，不会发送引导技能的申请，可以发送瞬发技能的申请（如“F交互过程中按下藏空剑”、“藏空剑引导过程中按下藏空剑”）
	RequestActionSkillEvent = 17 UMETA(DisplayName = "RequestActionSkillEvent"),
	///PropertyPercentChangeEvent（资源存量改变事件）
	///	Param1：“存量”辅助属性类型（留空表现为“肯定找不到对应属性，必然无法通过”）
	///		HP：当前生命值/生命值上限
	///		MP：当前法力值/法力值上限
	///		gangQiValue：当前罡气值/罡气值上限
	///		查询：此类“辅助属性”不存在，只在需要时临时产生，可以理解为“技术指标”，暂无法查询
	///			可以通过如【/queryAttr HP_Max】，查询【具体指定属性】，再进行推算
	///	Param2：触发类型（不得缺省）
	///		0：↘下降沿（从大变小，从“≥目标值”变成“＜目标值”，即“变得不足目标值时”）
	///		1：↗上升沿（从小变大，从“≤目标值”变成“＞目标值”，即“变得超过目标值时”）
	///	Param3：数量指标（浮点型，不得缺省）
	///支持：
	///	技能事件持有（/queryAttr casterSkillEventList，#32）
	///	资源类属性值改变时触发（@CST-6292）
	///		触发者＝触发目标＝单位自身
	///注意：
	///	角色初始化时，不触发（如上线时）
	PropertyPercentChangeEvent = 18 UMETA(DisplayName = "PropertyPercentChangeEvent"),
	///JumpStateChangeEvent（PC跳跃状态改变事件）
	///	Param1：PC跳跃状态类型（缺省1）
	///		1：跳跃全程（非站立）
	///		2：上升
	///		3：下降
	///	Param2：流程类型（缺省1）
	///		0：“变成非指定类型跳跃时”（下降沿），表现为“指定类型跳跃停止时”
	///		1：“变成指定类型跳跃时”（上升沿），表现为“指定类型跳跃开始时”
	///	Param3：无
	///支持：
	///	技能事件持有（/queryAttr casterSkillEventList，#34）
	///	PC跳跃状态改变事件（@CST-3448）
	///		触发者＝触发目标＝客户端PC单位
	///	整合跳跃状态：实际上跳跃状态类型繁多（@csdefine.JUMP_SHOW_STATE），为了策划理解与配置，此处对跳跃状态类型进行了整合
	///		“跳跃全程”，总结起来，就是补充筛选条件，“其他↔0站立”
	///		“上升”，总结起来，就是补充筛选条件，“其他↔7上升”
	///		“下降”，总结起来，就是补充筛选条件，“其他↔8下降”（所以原则上，同一个状态改变事件，可以被多种类型同时响应）
	///注意：
	///	触发者单位类型：PC限定
	///	角色初始化时，不触发（如上线时）
	///	“跳跃”与“移动”互相独立，可同时触发（因为“可以跳起来在空中移动”）
	///反思：
	///	跳跃状态，由客户端驱动，通过服务器属性广播同步，已经可以视为正规的服务器属性了
	JumpStateChangeEvent = 19 UMETA(DisplayName = "JumpStateChangeEvent"),

	///OnDestoryEvent（销毁事件）
	///	Param1~3：无
	///支持：
	///（@CST-13819）
	OnDestoryEvent = 20 UMETA(DisplayName = "OnDestoryEvent"),
};

///技能事件
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_EVENT
{
	GENERATED_BODY()
	///技能事件类型
	///	不同类型，决定着不同的参数定义
	UPROPERTY(EditAnywhere)
		ENUM_SKILL_EVENT EventType;
	///参数1（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param1;
	///参数2（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param2;
	///参数3（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param3;
};

///主动技能打击
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_HIT
{
	GENERATED_BODY()
	///打击时间（精确到0.001秒）
	///支持：
	///	从技能施法开始，多久后触发此打击
	///		应当依据打击时间，升序排列打击，以保障打击顺序正确（@CST-2754）
	///注意：
	///	脚本类型：CombatSkill限定（InstantSkill的打击时间，修正为0秒）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float HitTime;
	///打击作用范围
	///支持：
	///	选择受术者的初始方法
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FSKILL_HIT_AREA HitArea;
	///受术者条件列表
	///支持：
	///	判断“施法者→受术者”的条件是否满足，把不满足条件的受术者排除（如“对HP≤10%的目标造成斩杀”）
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“无法通过条件检测”（@CST-2113）
	UPROPERTY(EditAnywhere)
		TArray<FSKILL_USE_CONDITION> ReceiverCondition;
	///受术者排序列表
	///支持：
	///	使受术者按需排序，并选择前几个受术者（如“攻击血量最少的3个目标”）
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“丢至队末”（@CST-2113）
	UPROPERTY(EditAnywhere)
		TArray<FRECEIVER_FLITER_CONDITION> FilterCondition;
	///打击命中类型
	///支持：
	///	对受术者列表依据“命中判定”进行筛选，让一部分“合格的”受术者“免受打击”的方法
	///		流程上在“条件筛选”、“排序筛选”之后
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“无法通过命中检测”（@CST-2113）
	///反思：
	///	这里其实叫“打击闪避类型”更合理，其原意是“已经被选为合格目标之后，还有可以免受打击”的方法
	///		默认类型，应该是“无闪避”，单纯的无条件通过，代表“没有闪避这回事”
	///		然后，逐步引入不同的闪避方法
	///			①按随机概率判定，表现为“运气不好好”
	///			②按闪避、命中属性结算，表现为“单位的身手好不好”
	///			③按异常抗性结算，表现为“单位的免疫力好不好”
	///		区别是，当目标没有闪避属性时，是应该默认“闪避失败”还是“命中失败”，我觉得“闪避失败”更合适
	UPROPERTY(EditAnywhere)
		ENUM_HIT_TYPE HitType = ENUM_HIT_TYPE::HitDodge;
	///打击效果列表
	///支持：
	///	“施法者→受术者”添加技能效果（如“伤害”、“表现”…等）
	///注意：
	///	若获取流程所需的双方属性时错误，则直接视为异常，表现为“效果添加失败”（@CST-2113）
	UPROPERTY(EditAnywhere)
		TArray<FHIT_EFFECT> EffectList;
};

//技能效果表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_EFFECT_TABLE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///效果脚本类型
	///	不同类型，决定着不同的参数定义
	UPROPERTY(EditAnywhere)
		ENUM_HIT_EFFECT_TYPE HitEffectType;
	///施法者开关条件
	///支持：
	///	效果条件判定（@CST-7617）
	UPROPERTY(EditAnywhere, DisplayName = "CasterActForbid")
		ACTION_FLAG CasterActForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	///受术者开关条件
	///支持：
	///	效果条件判定（@CST-1209）
	///	事件触发的判断依据（@CST-1314）
	UPROPERTY(EditAnywhere, DisplayName = "ReceiverActForbid")
		ACTION_FLAG ReceiverActForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	///参数1（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param1;
	///参数2（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param2;
	///参数3（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param3;
	///参数4（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param4;
	///参数5（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param5;
	///备注
	///	没有任何功能，仅供策划记录及查看
	UPROPERTY(EditAnywhere, DisplayName = "备注")
		FString Remarks;
	
	public:
		void CheckEffectActionData(RowCheckResultInfo& ResultInfo)
		{
			if (Param1 != "")
			{
				TArray<FString> Param1Data = SplitString(Param1, false, TEXT("|"));
				for (auto Data : Param1Data)
				{
					TArray<FString> ActionInfo = SplitString(Data, false, TEXT(":"));
					if (ActionInfo.Num() > 1)
					{
						if (!CheckParamFloatData(ResultInfo, ActionInfo[1], "Param1", false))
						{
							break;
						}
					}
				}
			}
		}
	
		void CheckEffectDamageData(RowCheckResultInfo& ResultInfo)
		{
			if (Param1 != "")
			{
				TArray<FString> Param1Split = SplitString(Param1, false, TEXT("|"));
				if (!CheckParamFloatData(ResultInfo, Param1Split[0], "Param1", false))
				{
					return;
				}
				else if (Param1Split.Num() > 1)
				{
					CheckParamIntData(ResultInfo, Param1Split[1], "Param1", false);
				}
			}
		}
	
		void CheckEffectAddHPOrMPData(RowCheckResultInfo& ResultInfo)
		{
			if (Param1 != "")
			{
				TArray<FString> Param1Split = SplitString(Param1);
				if (!CheckParamFloatData(ResultInfo, Param1Split[0], "Param1", false))
				{
					return;
				}
				if (Param1Split.Num() > 1)
				{
					CheckParamIntData(ResultInfo, Param1Split[1], "Param1", false);
				}
			}
		}
	
		void CheckEffectCreateEntityData(RowCheckResultInfo& ResultInfo)
		{
			if (Param2 != "")
			{
				CheckParamFloatData(ResultInfo, Param2, "Param2", true, "|");
			}
		}
	
		void CheckEffectNormalDamageData(RowCheckResultInfo& ResultInfo)
		{
			TArray<FString> Params;
	
			if (Param1 != "")
			{
				CheckParamIntData(ResultInfo, Param1, "Param1", false);
			}
	
			if(Param2 != "")
			{
				TArray<FString> Param2Split = SplitString(Param2);
				if (!CheckParamFloatData(ResultInfo, Param2Split[0], "Param2", false))
				{
					return;
				}
				if (Param2Split.Num() > 1)
				{
					CheckParamIntData(ResultInfo, Param2Split[1], "Param2", false);
				}
			}
			if (Param3 != "")
			{
				TArray<FString> Param3Split = SplitString(Param3);
				if (!CheckParamFloatData(ResultInfo, Param3Split[0], "Param3", false))
				{
					return;
				}
				if (Param3Split.Num() > 1)
				{
					CheckParamIntData(ResultInfo, Param3Split[1], "Param3", false);
				}
			}
		}
	
		///不会加载其他资源得浅检查
		virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
		{
			ResultInfo.Result = Ok;
			bool bHasError = false;
			if (HitEffectType == ENUM_HIT_EFFECT_TYPE::EffectAction)
			{
				CheckEffectActionData(ResultInfo);
			}
			else if (HitEffectType == ENUM_HIT_EFFECT_TYPE::EffectDamage)
			{
				CheckEffectDamageData(ResultInfo);
			}
			else if (HitEffectType == ENUM_HIT_EFFECT_TYPE::EffectAddHP || HitEffectType == ENUM_HIT_EFFECT_TYPE::EffectAddMP)
			{
				CheckEffectAddHPOrMPData(ResultInfo);
			}
			else if (HitEffectType == ENUM_HIT_EFFECT_TYPE::EffectCreateEntity)
			{
				CheckEffectCreateEntityData(ResultInfo);
			}
			else if (HitEffectType == ENUM_HIT_EFFECT_TYPE::EffectNormalDamage)
			{
				CheckEffectNormalDamageData(ResultInfo);
			}

			if (ResultInfo.Result == Error)
			{
				ResultInfo.CheckLog = "Error: " + ResultInfo.CheckLog.Right(ResultInfo.CheckLog.Len() - 2);
			}

		}
	
		///会加载其他资源得深检查(深检查中要先调用浅检查)
		virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
		{
			CheckShallow(ResultInfo);
		}
};

//持有效果表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_HOLD_EFFECT_TABLE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///持有效果脚本类型
	///	不同类型，决定着不同的参数定义
	UPROPERTY(EditAnywhere)
		ENUM_HOLD_EFFECT_TYPE HitEffectType;
	///参数1（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param1;
	///参数2（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param2;
	///参数3（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param3;
	///参数4（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param4;
	///参数5（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere)
		FString Param5;
	///备注
	///	没有任何功能，仅供策划记录及查看
	UPROPERTY(EditAnywhere, DisplayName = "备注")
		FString Remarks;

public:
	void CheckHoldEffectAddActCounterData(RowCheckResultInfo& ResultInfo)
	{
		if (Param1 != "")
		{
			CheckParamIntData(ResultInfo, Param1, "Param1", true, "|");

			///TArray<FString> Param1Split = SplitString(Param1, false, TEXT("|"));
			///for (auto SplitStr : Param1Split)
			///{
			///	if (SplitStr.TrimStartAndEnd() != "0" && FSTRING_TO_INT(SplitStr) == 0)
			///	{
			///		ResultInfo.Result = Error;
			///		ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"Param1\" config error"));
			///
			///	}
			///}
		}
	}
	
	void CheckHoldEffectAddAttrData(RowCheckResultInfo& ResultInfo)
	{
		if (Param1 != "")
		{
			CheckParamIntData(ResultInfo, Param1, "Param1", true, "|");
		}
		if (Param2 != "")
		{
			CheckParamFloatData(ResultInfo, Param2, "Param2", false);
		}

		if (Param3 != "")
		{
			CheckParamIntData(ResultInfo, Param3, "Param3", false);
		}
	}

	void CheckHoldEffectPlayEffectData(RowCheckResultInfo& ResultInfo)
	{
		if (Param1 != "")
		{
			TArray<FString> Param1Split = SplitString(Param1, false, TEXT("|"));
			for (auto SplitStr: Param1Split)
			{
				TArray<FString> SplitInfos = SplitString(SplitStr, false, TEXT(":"));
				if (SplitInfos.Num() > 1)
				{
					if (SplitInfos[1].TrimStart() != "0" &&SplitInfos[1].TrimStart() != "0.0" && FCString::Atof(*SplitInfos[1]) == 0)
					{
						ResultInfo.Result = Error;
						ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"Param1\" config error"));
					}
				}
			}
		}
	}

	///不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		if (HitEffectType == ENUM_HOLD_EFFECT_TYPE::HoldEffectAddActCounter)
		{
			CheckHoldEffectAddActCounterData(ResultInfo);
		}
		else if (HitEffectType == ENUM_HOLD_EFFECT_TYPE::HoldEffectAddAttr)
		{
			CheckHoldEffectAddAttrData(ResultInfo);
		}
		else if (HitEffectType == ENUM_HOLD_EFFECT_TYPE::HoldEffectPlayEffect)
		{ 
			CheckHoldEffectPlayEffectData(ResultInfo);
		}

		if (ResultInfo.Result == Error)
		{
			ResultInfo.CheckLog = "Error: " + ResultInfo.CheckLog.Right(ResultInfo.CheckLog.Len() - 2);
		}

		/*	bool bHasError = false;
			TArray<FString> StackAmountData = SplitString(StackAmount, false, TEXT("|"));
			if (StackAmountData.Num() > 0)
			{
				int IntTemp0 = FCString::Atoi(*StackAmountData[0]);
				if (StackAmountData[0].TrimStartAndEnd() != "0" && IntTemp0 == 0)
				{
					bHasError = true;
					ResultInfo.Result = Error;
					ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"StackAmount\" config error"));
				}
				else if (IntTemp0 != 0)
				{
					if (StackAmountData.Num() >= 2)
					{
						int IntTemp1 = FCString::Atoi(*StackAmountData[1]);
						if (StackAmountData[1].TrimStartAndEnd() != "0" && IntTemp1 == 0)
						{
							bHasError = true;
							ResultInfo.Result = Error;
							ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"StackAmount\" config error"));
						}

					}
					else
					{
						bHasError = true;
						ResultInfo.Result = Error;
						ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"StackAmount\" config error"));
					}
				}
			}
			TArray<FString> ClassesData = SplitString(ReqClasses, false, TEXT("|"));
			if (ClassesData.Num() > 0)
			{
				for (auto Data : ClassesData)
				{
					if (Data.TrimStartAndEnd() != TEXT("") && FCString::Atoi(*Data) == 0)
					{
						ResultInfo.Result = Error;
						if (bHasError)
						{
							ResultInfo.CheckLog += FString::Printf(TEXT("; \"ReqClasses\" config error"));
						}
						else
						{
							ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"ReqClasses\" config error"));
						}
					}
				}
			}*/
	}

	///会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};
//辅助选择目标
UENUM(BlueprintType)
enum class ENUM_SKILL_ASSIST_TARGET_TYPE : uint8
{
	///NoAssistTarget（默认的，无辅助目标指定）
	///	需要与操作模式配合使用
	///	技能无要求（沿用操作模式的默认目标指定设定）
	NoAssistTarget = 0 UMETA(DisplayName = "NoAssistTarget"),
	///AssistTargetEnemy（辅助指定敌对目标）
	///	需要与操作模式配合使用
	///	辅助指定“与施法者距离最近”的敌对单位（Role、Monster、Pet限定）
	AssistTargetEnemy = 1 UMETA(DisplayName = "AssistTargetEnemy"),
	///AssistTargetNormal（辅助指定友好目标）
	///	需要与操作模式配合使用
	///	辅助指定“与施法者距离最近”的友好单位（Role、Monster、Pet限定）
	AssistTargetNormal = 2 UMETA(DisplayName = "AssistTargetNormal"),
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_TABLE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///技能名称
	///支持：
	///	界面显示、技能反馈显示、技能冒字（@CST-1356）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "SkillName")
		FString SkillName;
	///技能图标
	///支持：
	///	界面显示（@CST-1356）
	///	技能测试菜单显示（临时的）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "SkillIcon")
		TSoftObjectPtr<UTexture2D> SkillIcon;
	///技能品质
	///	0：没有自定义品质，没有外框显示
	///	1：白色（白色边框）
	///	2：蓝色（蓝色边框）
	///	3：金色（金色边框）
	///	4：粉色（粉色边框）
	///	5：地阶（绿色边框）
	///	6：天阶（绿色边框）
	///	7：圣阶（绿色边框＋流光）
	///	8：神阶（绿色边框＋闪电）
	///支持：
	///	界面显示（@CST-11464）
	///注意：
	///	只做界面显示用，不影响具体功能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "Quality")
		int32 Quality = 0;
	///技能等级（级）
	///支持：
	///	界面显示（@CST-12843）
	///注意：
	///	只做界面显示用，不影响具体功能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "SkillLevel")
		int32 SkillLevel = 0;
	///自定义“冷却时间”显示（文本）
	///	格式：“自定义文本 秒”
	///		示例：“10”，代表“10秒”，表现为“冷却时间：10 秒”
	///		示例：“10.0”，代表“10秒”，表现为“冷却时间：10.0 秒”
	///支持：
	///	界面显示：自定义技能信息界面上的“冷却时间”，以支持灵活多变的技能表现需要（@CST-12843）
	///		当自定义信息有值时，优先显示自定义值；当自定义信息留空时，再按默认规则显示状态信息
	///		默认规则为：依据“施法者技能冷却列表”的第一项配置，显示“冷却时间”信息
	///注意：
	///	只做界面显示用，不影响具体功能
	///	已知风险：可以配出比较奇怪的表现，请谨慎使用
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "CasterCoolDownDescribe")
		FString CasterCoolDownDescribe;
	///自定义“技能消耗”显示（文本）
	///	格式：“消耗类型|消耗数量（整数）|道具ID（@DT_ItemDataCfg）”
	///		示例：“1|100”，代表“消耗内息”，表现为“技能消耗：100 内息”
	///		示例：“2|100”，代表“消耗气血”，表现为“技能消耗：100 气血”
	///		示例：“3|100”，代表“消耗罡气”，表现为“技能消耗：100 罡气”
	///		示例：“4|1|203010004”，代表“消耗道具”，表现为“技能消耗：1 龙珠”
	///支持：
	///	界面显示：自定义技能信息界面上的“技能消耗”，以支持灵活多变的技能表现需要（@CST-12843）
	///		当自定义信息有值时，优先显示自定义值；当自定义信息留空时，再按默认规则显示状态信息
	///		默认规则为：依据“施法者技能消耗列表”的第一项内容，显示“技能消耗”信息
	///注意：
	///	只做界面显示用，不影响具体功能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "CasterRequireDescribe")
		FString CasterRequireDescribe;
	///技能描述
	///支持：
	///	界面显示（@CST-1356）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "Description")
		FString Description;
	///是否显示“施法冒字”
	///支持：
	///	技能施法冒字（@CST-1550）
	///	若技能施展目标是PC，则其客户端界面上也可以显示施法冒字（@CST-2601）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "IsPromptSkillName")
		bool IsPromptSkillName;
	///是否显示“引导进度条”
	///支持：
	///	技能施展表现（@CST-1754）
	///	怪物对PC施法时，可以看到怪物的引导条表现（@CST-5316）
	///注意：
	///	脚本类型：CombatSkill限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "ShowIntonate")
		bool ShowIntonate = false;
	///引导进度条文字显示
	///支持：
	///	技能施展表现（@CST-1754）
	///	怪物对PC施法时，可以看到怪物的引导条表现（@CST-5316）
	///注意：
	///	脚本类型：CombatSkill限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "IntonateName")
		FString IntonateName;
	///技能脚本类型
	///支持：
	///	明确技能行为、决定具体参数定义（@CST-1356）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "SkillType")
		ENUM_SKILL_CLASS_TYPE SkillType;
	///施法者开关条件
	///支持：
	///	技能条件：如，藏空剑施展时，若正被“禁止施法”，则施展失败（@CST-1209）
	///	事件触发：如，技能施展事件响应时，可以依据开关条件，判断是否需要响应（@CST-1314）
	///	技能中断：如，藏空剑引导中，若获得“禁止施法”，则引导中断（@CST-1209）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "CasterActForbid")
		ACTION_FLAG CasterActForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	///施展目标开关条件
	///支持：
	///	施展条件判定（@CST-7617）
	///注意：
	///	施展目标类型：TargetNothing/TargetLock限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "TargetActForbid")
		ACTION_FLAG TargetActForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	///参数1（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "Param1")
		FString Param1;
	///参数2（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "Param2")
		FString Param2;
	///参数3（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "Param3")
		FString Param3;
	///参数4（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "Param4")
		FString Param4;
	///参数5（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "Param5")
		FString Param5;
	///施展目标类型
	///原意：
	///	描述技能的目标是啥，和玩家如何指定目标
	///支持：
	///	玩家使用主动技能时，客户端将依此
	///		提供施法辅助：辅助范围指示、辅助目标选择、辅助追击、辅助转向…等（@CST-1590）
	///		指定技能申请目标（@CST-6339）
	///	技能施展时，服务器将依此
	///		指定技能施展目标（@CST-1356）
	///		若技能施展目标与技能申请目标类型不一致，则进行适当的修正（@CST-6339）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "TargetType")
		ENUM_CAST_TARGET_TYPE TargetType;
	///施法距离要求（米）
	///支持：
	///	技能条件判断（@CST-1356）
	///		指“三维距离”
	///	辅助追击表现（@CST-2323）
	///		若距离不够，则追击到施法距离上限 2/3 处再施法
	///注意：
	///	0代表“默认施法距离上限”（@CST-2180），表现为99999999米（与战斗属性上限保持一致，@csdefine.SKILL_CAST_RANGE_MAX）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "CastRangeMax")
		float CastRangeMax;
	///辅助范围指示
	///	若对位置施法，则辅助玩家对具体目标位置进行指定（@CST-1293）
	///注意：
	///	施展目标类型：TargetPosition限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "AssistEffect")
		FSKILL_ASSIST_EFFECT AssistEffect;
	///辅助目标选定
	///支持：
	///	提供给“PC施法辅助”判断，让客户端决定是否需要“辅助选择目标”（@CST-3199）
	///	提供给“AI”判断，让AI决定是否需要“辅助选择目标”（@CST-3199）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "AssistTargetType")
		ENUM_SKILL_ASSIST_TARGET_TYPE AssistTargetType;
	///是否“辅助施法者转向施展目标”
	///支持：
	///	提供给“PC施法辅助”判断，让客户端决定是否需要“辅助转向”（@CST-1590）
	///	提供给“AI”判断，让AI决定是否需要“辅助转向”（@CST-1590）
	///注意：
	///	怪物的辅助转向行为，忽视“禁止转向”开关的制约，解释详见（@CST-7630）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "IsTurnToTarget")
		bool IsTurnToTarget = true;
	///辅助施法碰撞
	///支持：
	///	技能施法过程中，可以改变施法者的碰撞表现（@CST-2386）
	///		如引导中调整“客户端PC”的碰撞类型，可以选择“是否碰撞敌人”
	///注意：
	///	脚本类型：CombatSkill限定（瞬发技能省略了一些表现支持）
	///	施法者单位类型：PC限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "CollisionType")
		ENUM_CAST_COLLISION_TYPE CollisionType;
	///施法者条件列表
	///支持：
	///	判断“施法者→施法者”的条件是否满足（@CST-1356）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "CasterCondition")
		TArray<FSKILL_USE_CONDITION> CasterCondition;
	///施展目标条件列表
	///支持：
	///	判断“施法者→施展目标”的条件是否满足（@CST-1356）
	///注意：
	///	施展目标类型：TargetNothing/TargetLock限定
	///	若施展目标类型＝TargetNothing，则“施法者表现”和“受术者表现”表现相同，建议选用“施法者表现”，以方便理解
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "TargetCondition")
		TArray<FSKILL_USE_CONDITION> TargetCondition;
	///施法者技能冷却列表
	///支持：
	///	技能施展受制于此CD、施法成功时产生此CD（@CST-1356）
	///		“CD持续时间＝0”，代表“受制于某CD，而不产生某CD”
	///	界面显示：默认的技能信息界面上的“冷却时间”（@CST-12843）
	///		当自定义信息有值时，优先显示自定义值；当自定义信息留空时，再按默认规则显示状态信息
	///		默认规则为：依据“施法者技能冷却列表”的第一项配置，显示“冷却时间”信息
	///反思：
	///	刻意避免了“不受制于某CD，而生产某CD”的表现，建议将其视为技能的效果，通过EffectChangeSkillCD实现
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "CasterCoolDown")
		TArray<FSKILL_COOL_DOWN> CasterCoolDown;
	///施展目标技能冷却列表
	///支持：
	///	技能施展受制于此CD、施法成功时产生此CD（@CST-7617）
	///		“CD持续时间＝0”，代表“受制于某CD，而不产生某CD”
	///注意：
	///	施展目标类型：TargetNothing/TargetLock限定（@CST-7617）
	///	若施展目标类型＝TargetNothing，则“施法者表现”和“受术者表现”表现相同，建议选用“施法者表现”，以方便理解
	///反思：
	///	刻意避免了“不受制于某CD，而生产某CD”的表现，建议将其视为技能的效果，通过EffectChangeSkillCD实现
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "TargetCoolDown")
		TArray<FSKILL_COOL_DOWN> TargetCoolDown;
	///施法者技能消耗列表
	///支持：
	///	技能施展受制于此消耗，施法成功时产生此消耗（@CST-1356）
	///	界面显示：自定义技能信息界面上的“技能消耗”，以支持灵活多变的技能表现需要（@CST-12843）
	///		当自定义信息有值时，优先显示自定义值；当自定义信息留空时，再按默认规则显示状态信息
	///		默认规则为：依据“施法者技能消耗列表”的第一项内容，显示“技能消耗”信息
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "CasterRequireDefine")
		TArray<FSKILL_REQUIRE> CasterRequireDefine;
	///施展目标技能消耗列表
	///支持：
	///	技能施展受制于此消耗，施法成功时产生此消耗（@CST-7617）
	///注意：
	///	施展目标类型：TargetNothing/TargetLock限定（@CST-7617）
	///	若施展目标类型＝TargetNothing，则“施法者表现”和“受术者表现”表现相同，建议选用“施法者表现”，以方便理解
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "TargetRequireDefine")
		TArray<FSKILL_REQUIRE> TargetRequireDefine;
	///技能施法动作列表
	///	配置格式：动作ID1:起始帧时间1|动作ID2:起始帧时间2（秒）…（:冒号和|竖号分隔）
	///		示例：“Attack_01|Attack_02:0.5”，代表“顺序播放：从头开始的Attack_01、从0.5秒开始的Attack_02”
	///支持：
	///	技能施法表现：开始时播放，中断时中止，结束时不中止（@CST-1192/@CST-3036）
	///	支持动作起始帧时间设定（@CST-1192）
	///	支持连续播放动作：若任一动作中断，则中断连续动作（@CST-3036）
	///注意：
	///	不支持表现重播
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "CasterCastActionId")
		FString CasterCastActionId;
	///技能施法光效列表
	///	配置格式：光效ID1|光效ID2…（@DT_EffectCfg，|竖号分隔）
	///		示例：“10003|10004”，代表“同时播放两个光效”
	///支持：
	///	技能施法表现：开始时播放，中断时中止，结束时不中止（@CST-265）
	///		“施法者”对“施法者”添加光效
	///注意：
	///	不支持表现重播
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "CasterCastEffectId")
		FString CasterCastEffectId;
	///技能施法音效列表
	///	配置格式：音效ID1|音效ID2…（@DT_AudioCfg，|竖号分隔）
	///		示例：“A010001|A0100012”，代表“同时播放两个音效”
	///支持：
	///	技能施法表现：开始时播放，中断时中止，结束时不中止（@CST-888）
	///注意：
	///	不支持表现重播
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "CasterCastSoundId")
		FString CasterCastSoundId;
	///施展目标施法动作列表
	///	配置格式：动作ID1:起始帧时间1|动作ID2:起始帧时间2（秒）…（:冒号和|竖号分隔）
	///		示例：“Attack_01|Attack_02:0.5”，代表“顺序播放：从头开始的Attack_01、从0.5秒开始的Attack_02”
	///支持：
	///	技能施法表现：开始时播放，结束时不中止（@CST-1192/@CST-3036）
	///	支持动作起始帧时间设定（@CST-1192）
	///	支持连续播放动作：若任一动作中断，则中断连续动作（@CST-3036）
	///注意：
	///	施展目标类型：TargetNothing/TargetLock限定（@CST-7617）
	///	若施展目标类型＝TargetNothing，则“施法者表现”和“受术者表现”表现相同，建议选用“施法者表现”，以方便理解
	///	不支持表现重播
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "TargetCastActionId")
		FString TargetCastActionId;
	///施展目标施法光效列表
	///	配置格式：光效ID1|光效ID2…（@DT_EffectCfg，|竖号分隔）
	///		示例：“10003|10004”，代表“同时播放两个光效”
	///支持：
	///	技能施法表现：开始时播放，中断时中止，结束时不中止（@CST-888
	///		光效表现施法者＝（技能的）施法者
	///		光效表现目标　＝（技能的）施展目标
	///注意：
	///	若施展目标类型＝TargetPosition，则在目标位置创建表现
	///	若施展目标类型＝TargetNothing，则“施法者表现”和“受术者表现”表现相同，建议选用“施法者表现”，以方便理解
	///	不支持表现重播
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "TargetCastEffectId")
		FString TargetCastEffectId;
	///施展目标音效列表
	///	配置格式：音效ID1|音效ID2…（@DT_AudioCfg，|竖号分隔）
	///		示例：“A010001|A0100012”，代表“同时播放两个音效”
	///支持：
	///	技能施法表现：开始时播放，中断时中止，结束时不中止（@CST-888）
	///		音效表现施法者＝（技能的）施法者
	///		音效表现目标　＝（技能的）施展目标
	///注意：
	///	施展目标类型：TargetNothing/TargetLock限定（@CST-7617）
	///	若施展目标类型＝TargetNothing，则“施法者表现”和“受术者表现”表现相同，建议选用“施法者表现”，以方便理解
	///	不支持表现重播
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "TargetCastSoundId")
		FString TargetCastSoundId;
	///施法者持有效果列表
	///支持：
	///	持有表现（@CST-1356）
	///		技能引导过程中，施法者拥有某种效果
	///注意：
	///	已知风险：可以导致当前技能引导中断（如，持有眩晕），请谨慎使用
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "CasterHoldEffectList")
		TArray<FHOLD_EFFECT> CasterHoldEffectList;
	///响应事件中断列表
	///支持：
	///	响应“施法者”的技能事件，而中断当前技能引导（@CST-1356）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "CasterInterruptSkillEvent")
		TArray<FSKILL_EVENT> CasterInterruptSkillEvent;
	///受术者响应事件中断列表
	///支持：
	///	响应“受术者”的技能事件，而中断当前技能引导
	///注意：
	///	脚本类型：CombatSkill限定
	///	施展目标类型：TargetNothing/TargetLock限定（@CST-7617）
	///	若施展目标类型＝TargetNothing，则“施法者表现”和“受术者表现”表现相同，建议选用“施法者表现”，以方便理解
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "TargetInterruptSkillEvent")
		TArray<FSKILL_EVENT> TargetInterruptSkillEvent;
	///技能打击列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "HitList")
		TArray<FSKILL_HIT> HitList;
	///备注信息
	///	没有任何功能，仅供策划记录及查看
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SkillData", DisplayName = "备注")
		FString Remarks;
public:
	///不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		if (SkillIcon.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(SkillIcon.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: SkillIcon字段配置的资源不存在"));
			}
		}
	}
	
	///会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};
