// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Components/SceneComponent.h"
#include "Engine/DataTable.h"
#include "ML_ProjectCharacter.h"
#include "SC_DialogueM.generated.h"

USTRUCT(BlueprintType)
struct FPlayerDialogue : public FTableRowBase
{
	GENERATED_BODY()

	///** Camera boom positioning the camera behind the character */
	//UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = Camera, meta = (AllowPrivateAccess = "true"))
	//class UDataTable* Datas;

public:



	/** montage **/
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString LabelString;

	/** montage **/
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 Attitude;

	/** montage **/
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString Type;

	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		TArray<float> LabelCorrs;

};

UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class ML_PROJECT_API USC_DialogueM : public USceneComponent
{
	GENERATED_BODY()

public:	
	// Sets default values for this component's properties
	USC_DialogueM();

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Dialogue, meta = (AllowPrivateAccess = "true"))
	class UDataTable* PlayerDialogueData;

	UFUNCTION(BlueprintCallable)
	void InitiateDialogue(bool ShouldSpeak, bool ReferenceBool);

	UFUNCTION(BlueprintCallable)
	void EnableCheck(bool CheckTalk);

	UFUNCTION(BlueprintCallable)
	void Reset();

	void StartDialogue();

protected:
	// Called when the game starts
	virtual void BeginPlay() override;

public:	
	// Called every frame
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString OutputDialogue = "This is empty";

private:

	// Enable the movement of the component
	UPROPERTY(EditAnywhere)
	bool SpeakEnable = false;

	// Does an initial check for confirmation
	UPROPERTY(EditAnywhere)
	bool CheckSpeakEnable = false;

	// Does an initial check for confirmation
	UPROPERTY(EditAnywhere)
	bool RefBool = false;

	UPROPERTY(EditAnywhere)
	int ChatToken = 0;

	UPROPERTY(EditAnywhere)
	int32 PlayerDialogueNum = 1;

	UPROPERTY(EditAnywhere)
	TArray<int32> RelevantRow;

	UPROPERTY(EditAnywhere)
	TArray<int32> UsedRow;




	// COmputed Locations
	FVector StartRelativeLocation;
	FVector MoveOffsetNorm;
	float MaxDistance = 0.0f;
	float CurDistance = 0.0f;
	int MoveDirection = 1;
		
};
