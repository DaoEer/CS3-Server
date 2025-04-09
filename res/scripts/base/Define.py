""""""
import csdefine
import csstatus
import ItemTypeEnum

#队伍修改拾取模式消息
TEAM_PICK_UP_ALLOCATION_MSG = {
	csdefine.TEAM_PICKUP_TYPE_AUCTION: csstatus.TEAM_AUCTION_PICK,
	csdefine.TEAM_PICKUP_TYPE_TEAM: csstatus.TEAM_ORDER_PICK,
	csdefine.TEAM_PICKUP_TYPE_CAPTAIN: csstatus.TEAM_LEADER_PICK
}
#队伍修改分配品质消息
TEAM_PICK_UP_QUALITY_MSG = {
	ItemTypeEnum.QUALITY_BLUE: csstatus.TEAM_PICK_QUALITY_BLUE,
	ItemTypeEnum.QUALITY_GOLD: csstatus.TEAM_PICK_QUALITY_GOLD,
	ItemTypeEnum.QUALITY_PINK: csstatus.TEAM_PICK_QUALITY_PINK,
	ItemTypeEnum.QUALITY_GREEN: csstatus.TEAM_PICK_QUALITY_GREEN
}