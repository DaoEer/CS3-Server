// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "MonsterAIEnum.h"

typedef void(*monster_ai_event_cb)( void *arg );
/**
 * 
 */

struct MONSTER_AI_EVENT_STRUCT {
	int entity_id;
	enum TimerOptions mevent;
	monster_ai_event_cb callback;
	void* arg;
};
class CHUANGSHI_API MonsterAIEvent
{
public:
	MonsterAIEvent();
	~MonsterAIEvent();

	void bindEventCB(int32 ai_event, monster_ai_event_cb callback );
	void triggerEvent(MONSTER_AI_EVENT ai_event );
private:
	TArray < TMap< MONSTER_AI_EVENT, monster_ai_event_cb > > triggerEvents;
};
