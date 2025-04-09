// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "SkillTableData.h"
#include "GameData/CsvTableRowBase.h"
#include "PassiveSkillTableData.generated.h"

/**
* 文件名称：PassiveSkillTableData.h
* 功能说明：
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2017-05-16
*/

///被动技能脚本类型
UENUM(BlueprintType)
enum class ENUM_PASSIVE_SKILL_CLASS_TYPE : uint8
{
	///PassiveSkill（被动瞬发技能）
	///	Param1~5：无
	///设计原意：
	///	不受引导占位制约的，随时使用的瞬发的被动技能
	///支持：
	///	开关条件、自定义条件、冷却、消耗、施法表现、瞬发打击（@CST-1206）
	///	打击作用范围、受术者条件、受术者排序、命中判定、添加技能效果（@CST-1206）
	PassiveSkill = 0 UMETA(DisplayName = "PassiveSkill")
};

///被动技能，目标类型
UENUM(BlueprintType)
enum class ENUM_PASSIVE_CAST_TARGET_TYPE : uint8
{
	///TargetNothing（对自己施法）
	///设计原意：
	///	“无需选定目标”的施法形式
	///反思：
	///	实现上，变成了“不管选中谁，都是向自己施法”，其实叫“TargetSelf”更合适
	TargetNothing = 0 UMETA(DisplayName = "TargetNothing"),
	///TargetLock（对锁定单位施法）
	///设计原意：
	///	就是“对单体目标”的施法形式
	///		与主动技能不同，所依赖的不是“基于客户端的锁定操作”，而是“基于触发机制定义的对象双方”
	///注意：
	///	与主动技能不同，未支持“施法距离上限”要求，不支持施法辅助
	TargetLock = 1 UMETA(DisplayName = "TargetLock"),
};

///被动技能效果脚本类型
UENUM(BlueprintType)
enum class ENUM_PASSIVE_HIT_EFFECT_TYPE : uint8
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
	EffectRemoveBuff = 16 UMETA(DisplayName = "EffectRemoveBuff"),
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
	EffectAbsorbHP = 21 UMETA(DisplayName = "EffectAbsorbHP"),
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
	EffectNormalDamage = 22 UMETA(DisplayName = "EffectNormalDamage"),
	///EffectChangeSkillCD（改变CD效果）
	///	Param1：冷却ID列表（整型，|竖号分隔，需要配合具体冷却配置使用，不得缺省）
	///		冷却ID，暂无占位表，请谨慎使用，注意避让
	///	Param2：冷却持续时间增量（秒，≥0代表“增加”，≤0代表“减少”）
	///	Param3~5：无
	///支持：
	///	延长、缩短当前冷却时间（@CST-1794）
	EffectChangeSkillCD = 23 UMETA(DisplayName = "EffectChangeSkillCD"),
	///EffectReboundDamage（伤害反弹效果）
	///	Param1：击杀目标时是否触发“怪物死亡特效”（需要配合怪物表的DeadEffect的类型2配置，缺省0）
	///		0：不触发
	///		1：触发
	///	Param2：反弹百分比（如0.5代表“50%伤害”）|固定值（整型）
	///	Param3~5：无
	///支持：
	///	死亡免疫（@CST-1635）
	///	情景免疫（@CST-4169）
	///		当技能信息中缺少“触发伤害量”时，此效果失败
	///		应当配合“伤害时/被伤害时”、“校正技能申请信息”使用
	///	伤害结算：依据伤害信息，造成反弹伤害，忽视暴击、护盾、护甲（@CST-4169）
	///		反弹伤害量＝信息伤害量×反弹百分比＋反弹固定值
	///	仇恨结算：自然仇恨（@CST-12837）
	///		自然仇恨＝生命值扣除量×受术者自然仇恨系数×施法者造成仇恨修正
	///		自然仇恨下限＝【受术者的】自然仇恨下限
	///		查询：可以通过【/queryAttr hatredList】，查询【怪物的仇恨列表】属性
	///注意：
	///	一般地，“伤害表现”应视为“战斗效果”，相关开关条件应默认配置“禁止受攻击”（ForbidBeAttack）
	EffectReboundDamage = 25 UMETA(DisplayName = "EffectReboundDamage"),
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
	///EffectDirectlyKill（直接击杀效果）
	///	Param1~3：无
	///设计原意：
	///	避免“无敌”、“不屈”…等基于伤害的被动扩展，制约“必须死亡”的表现设计
	///支持：
	///	不依赖伤害，使目标在还有生命值的情况下，也可以死亡（@CST-3132）
	///注意：
	///	已知风险：直接击杀可能导致“目标死亡时未有所有者”，请谨慎使用
	EffectDirectlyKill = 32 UMETA(DisplayName = "EffectDirectlyKill"),
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
	///EffectPassiveAbsorbHP（伤害吸血效果）
	///	Param1：吸血百分比（如0.5代表“50%伤害”）|固定值（整型）
	///	Param2~3：无
	///支持：
	///	死亡免疫（@CST-1635）
	///	情景免疫（@CST-4169）
	///		当技能信息中缺少“触发伤害量”时，此效果失败
	///		应当配合“伤害时/被伤害时”、“校正技能申请信息”使用
	///	伤害结算：依据伤害信息，造成生命治疗（@CST-6362）
	///		治疗量＝信息伤害量×吸血百分比+吸血固定值
	EffectPassiveAbsorbHP = 50 UMETA(DisplayName = "EffectPassiveAbsorbHP"),
	///EffectTriggerSpaceEvent（触发自定义副本事件效果）
	///	Param1：自定义副本事件ID（字符串，需要配合具体副本事件使用，留空代表“没有事件”）
	///		自定义副本事件ID，暂无占位表，请谨慎使用，注意避让
	///	Param2~5：无
	///支持：
	///	触发自定义副本事件（@CST-4056）
	EffectTriggerSpaceEvent = 53 UMETA(DisplayName = "EffectTriggerSpaceEvent"),
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
	///EffectEnergyChange（充能效果）
	///	Param1：伤BuffID（能级Buff限定）
	///	Param2：能量改变百分比（基于当前能量值）|固定值（负值代表减少）
	///	Param3：标记列表（|竖号分隔，留空代表“没有标记”，具体功能与参数格式由标记定义）
	///		示例：“IsBuffAgainTime”，代表像重新添加Buff一样，额外刷新持续时间
	///	Param4~5：无
	EffectEnergyChange = 84 UMETA(DisplayName = "EffectEnergyChange"),

};

UENUM(BlueprintType)
enum class ENUM_PASSIVE_SKILL_EVENT : uint8
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
	OnDieEvent = 1 UMETA(DisplayName = "OnDieEvent"),
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
	CustomEvent = 2 UMETA(DisplayName = "CustomEvent"),
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
	MoveChangeEvent = 3 UMETA(DisplayName = "MoveChangeEvent"),
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
	CureEvent = 4 UMETA(DisplayName = "CureEvent"),
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
	HurtEvent = 7 UMETA(DisplayName = "HurtEvent"),
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
	SkillProcessEvent = 8 UMETA(DisplayName = "SkillProcessEvent"),
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
	SpaceChangeEvent = 9 UMETA(DisplayName = "SpaceChangeEvent"),
	///PerSecondTriggerEvent（每秒触发事件）
	///	Param1~3：无
	///支持：
	///	技能事件类型：#17
	///	每秒事件：某单位的所有“每秒触发响应”，统一计时同时触发，需要注意与“周期计时”的表现区别（@CST-3267）
	///		事件注册后启动计时，事件清空后停止计时，以降低消耗（@CST-3267）
	///注意：
	///	触发者＝触发目标＝目标单位
	///示例：
	///	①辉耀装备（可以描述为，每秒触发技能攻击周围）
	///	②光环称号（可以描述为，每秒触发技能治疗周围）
	PerSecondTriggerEvent = 10 UMETA(DisplayName = "PerSecondTriggerEvent"),
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
};

///被动技能打击效果
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPASSIVE_HIT_EFFECT
{
	GENERATED_BODY()
	///被动技能打击效果脚本类型
	///	不同类型，决定着不同的参数定义
	UPROPERTY(EditAnywhere)
		ENUM_PASSIVE_HIT_EFFECT_TYPE HitEffectType = ENUM_PASSIVE_HIT_EFFECT_TYPE::EffectDamage;
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
};

///技能事件
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPASSIVE_SKILL_EVENT
{
	GENERATED_BODY()
	///技能事件类型
	///	不同类型，决定着不同的参数定义
	UPROPERTY(EditAnywhere)
		ENUM_PASSIVE_SKILL_EVENT EventType = ENUM_PASSIVE_SKILL_EVENT::OnDieEvent;
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

///被动技能打击
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPASSIVE_SKILL_HIT
{
	GENERATED_BODY()
	///打击时间（精确到0.001秒）
	///支持：
	///	从技能施法开始，多久后触发此打击
	///		应当依据打击时间，升序排列打击，以保障打击顺序正确（@CST-2754）
	///注意：
	///	未启用，被动技能目前还只有瞬发技能（@CST-7617）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float HitTime;
	///打击作用范围
	///支持：
	///	选择受术者的初始方法
	UPROPERTY(EditAnywhere)
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
		TArray<FPASSIVE_HIT_EFFECT> EffectList;
};

USTRUCT(BlueprintType)
struct  CHUANGSHI_API FPASSIVE_SKILL_TABLE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///技能名称
	///支持：
	///	界面显示、技能反馈显示、技能冒字（@CST-1356）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "SkillName")
		FString SkillName;
	///技能图标
	///支持：
	///	界面显示（@CST-1356）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "SkillIcon")
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
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "Quality")
		int32 Quality = 0;
	///技能等级（级）
	///支持：
	///	界面显示（@CST-12843）
	///注意：
	///	只做界面显示用，不影响具体功能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "SkillLevel")
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
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "CasterCoolDownDescribe")
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
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "CasterRequireDescribe")
		FString CasterRequireDescribe;
	///技能描述
	///支持：
	///	界面显示（@CST-1356）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "Description")
		FString Description;
	///技能脚本类型
	///支持：
	///	明确技能行为、决定具体参数定义（@CST-1206）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "SkillType")
		ENUM_PASSIVE_SKILL_CLASS_TYPE SkillType;
	///施法者开关条件
	///支持：
	///	技能条件：如，藏空剑施展时，若正被“禁止施法”，则施展失败（@CST-1206）
	///	事件触发：如，技能施展事件响应时，可以依据开关条件，判断是否需要响应（@CST-1314）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "CasterActForbid")
		ACTION_FLAG CasterActForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	///施展目标开关条件
	///支持：
	///	施展条件判定（@CST-7617）
	///反思：
	///	目前被动技能的施法者和施展目标都是单位，所以没有类型限定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "TargetActForbid")
		ACTION_FLAG TargetActForbid = ACTION_FLAG::ACTION_FORBID_NONE;
	///参数1（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "Param1")
		FString Param1;
	///参数2（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "Param2")
		FString Param2;
	///参数3（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "Param3")
		FString Param3;
	///参数4（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "Param4")
		FString Param4;
	///参数5（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "Param5")
		FString Param5;
	///施展目标类型
	///原意：
	///	描述技能的目标是啥，被动技能的目标指定形式比较简单
	///支持：
	///	技能施展时，服务器将依此
	///		指定技能施展目标（@CST-1356）
	///		若技能施展目标与技能申请目标类型不一致，则进行适当的修正（@CST-6339）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "TargetType")
		ENUM_PASSIVE_CAST_TARGET_TYPE TargetType;
	///响应事件触发列表
	///支持：
	///	响应“施法者”的技能事件，而触发被动技能申请
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "TriggerSkillEvent")
		TArray<FPASSIVE_SKILL_EVENT> TriggerSkillEvent;
	///施法者条件列表
	///支持：
	///	判断“施法者→施法者”的条件是否满足（@CST-1356）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "CasterCondition")
		TArray<FSKILL_USE_CONDITION> CasterCondition;
	///施展目标条件列表
	///支持：
	///	判断“施法者→施展目标”的条件是否满足（@CST-1356）
	///注意：
	///	施展目标类型：TargetNothing/TargetLock限定
	///	若施展目标类型＝TargetNothing，则“施法者表现”和“受术者表现”表现相同，建议选用“施法者表现”，以方便理解
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "TargetCondition")
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
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "CasterCoolDown")
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
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "TargetCoolDown")
		TArray<FSKILL_COOL_DOWN> TargetCoolDown;
	///施法者技能消耗列表
	///支持：
	///	技能施展受制于此消耗，施法成功时产生此消耗（@CST-1356）
	///	界面显示：自定义技能信息界面上的“技能消耗”，以支持灵活多变的技能表现需要（@CST-12843）
	///		当自定义信息有值时，优先显示自定义值；当自定义信息留空时，再按默认规则显示状态信息
	///		默认规则为：依据“施法者技能消耗列表”的第一项内容，显示“技能消耗”信息
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "CasterRequireDefine")
		TArray<FSKILL_REQUIRE> CasterRequireDefine;
	///施展目标技能消耗列表
	///支持：
	///	技能施展受制于此消耗，施法成功时产生此消耗（@CST-7617）
	///注意：
	///	施展目标类型：TargetNothing/TargetLock限定（@CST-7617）
	///	若施展目标类型＝TargetNothing，则“施法者表现”和“受术者表现”表现相同，建议选用“施法者表现”，以方便理解
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "TargetRequireDefine")
		TArray<FSKILL_REQUIRE> TargetRequireDefine;
	///技能打击列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "HitList")
		TArray<FPASSIVE_SKILL_HIT> HitList;
	///备注信息
	///	没有任何功能，仅供策划记录及查看
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PassiveSkillData", DisplayName = "备注")
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
				ResultInfo.CheckLog = FString::Printf(TEXT("; \"SkillIcon\" resource does not exist"));
			}
		}
	}
	
	///会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};
