// Fill out your copyright notice in the Description page of Project Settings.

#include "CS3HttpRequest.h"
#include "HttpModule.h"
#include "JsonReader.h"
#include "JsonObject.h"
#include "JsonSerializer.h"
#include "Interfaces/IHttpResponse.h"


UCS3HttpRequest::UCS3HttpRequest(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
	if (HasAnyFlags(RF_ClassDefaultObject) == false)
	{
		AddToRoot();
	}
}

UCS3HttpRequest* UCS3HttpRequest::PostHttpRequest(const FString& URL, const FString& ContentString)
{
	UCS3HttpRequest* CS3HttpRequest = NewObject<UCS3HttpRequest>();
	// Create the Http request and add to pending request list
	TSharedRef<IHttpRequest> HttpRequest = FHttpModule::Get().CreateRequest();
	HttpRequest->SetURL(URL);
	HttpRequest->SetContentAsString(ContentString);
	HttpRequest->SetVerb(TEXT("POST"));
	HttpRequest->OnProcessRequestComplete().BindUObject(CS3HttpRequest, &UCS3HttpRequest::HandleRequest);
	HttpRequest->ProcessRequest();

	return CS3HttpRequest;
}

UCS3HttpRequest* UCS3HttpRequest::GetHttpRequest(const FString& URL)
{
	UCS3HttpRequest* CS3HttpRequest = NewObject<UCS3HttpRequest>();
	// Create the Http request and add to pending request list
	TSharedRef<IHttpRequest> HttpRequest = FHttpModule::Get().CreateRequest();
	HttpRequest->SetURL(URL);
	HttpRequest->SetVerb(TEXT("GET"));
	HttpRequest->OnProcessRequestComplete().BindUObject(CS3HttpRequest, &UCS3HttpRequest::HandleRequest);
	HttpRequest->ProcessRequest();

	return CS3HttpRequest;
}

FString UCS3HttpRequest::GetJsonStringField(const FString& JsonString, const FString& Key)
{
	FString outString = "";

	TSharedRef<TJsonReader<TCHAR>> JsonReader = TJsonReaderFactory<TCHAR>::Create(JsonString);
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject());
	if (FJsonSerializer::Deserialize(JsonReader, JsonObject) && JsonObject.IsValid())
	{
		if (JsonObject->TryGetStringField(*Key, outString))
		{
			return outString;
		}
	}

	return outString;
}

void UCS3HttpRequest::HandleRequest(FHttpRequestPtr HttpRequest, FHttpResponsePtr HttpResponse, bool bSucceeded)
{
	RemoveFromRoot();
	if (bSucceeded && HttpResponse.IsValid() && HttpResponse->GetContentLength() > 0)
	{
		OnSuccess.Broadcast(HttpResponse->GetContentAsString());
		return;
	}
	OnFail.Broadcast("");
}
