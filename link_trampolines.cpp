/* link_trampolines.cpp -- AUTO-GENERATED flat->member bridges (LINK phase). */
#include "nfs4_types.h"

void Display(tDialogBase* a0) {
  a0->Display();
}
void Hide(tDialogBase* a0) {
  a0->Hide();
}
void Redraw(tFEApplication* a0) {
  a0->Redraw();
}
void UpdateMusic(tFEApplication* a0) {
  a0->UpdateMusic();
}
void SaveTournament(tTournamentManager* a0, tSaveTournament* a1) {
  a0->SaveTournament(a1);
}
void LoadTournament(tTournamentManager* a0, tSaveTournament* a1) {
  a0->LoadTournament(a1);
}
int GetHelpText(tScreenControllerConfig* a0) {
  return (int)(a0->GetHelpText());
}
void DisplayHelp(tFEApplication * a0, int a1) {
  a0->DisplayHelp(a1);
}
void * GetCarFromID(tCarManager* a0, int a1) {
  return (void *)(a0->GetCarFromID(a1));
}
void * TransitionIsFinished(tOptionsMenu * a0) {
  return (void *)(a0->TransitionIsFinished());
}
int Percentage(tMenuItemLeftRightAudioSlider * a0) {
  return (int)(a0->Percentage());
}
void SetAvailable(tVideoWall* a0, unsigned a1) {
  a0->SetAvailable(a1);
}
tCarInfo * GetCarFromID(tCarManager * a0, short a1) {
  return (tCarInfo *)(a0->GetCarFromID(a1));
}
void GetAwardInformation(tTournamentManager * a0, tAwardInformation * a1) {
  a0->GetAwardInformation(a1);
}
short PlayerRanking(tTournamentManager * a0, short a1) {
  return (short)(a0->PlayerRanking(a1));
}
void Init(tCreditManager* a0, u_long a1) {
  a0->Init(a1);
}
void DeInit(tCreditManager* a0) {
  a0->DeInit();
}
short TextValue(tListIteratorTournament * a0, tPlayer a1) {
  return (short)(a0->TextValue(a1));
}
short * GetTrackList(tTournamentManager * a0, short a1, short a2) {
  return (short *)(a0->GetTrackList(a1, a2));
}
short TextValue(tListIteratorTrack * a0, tPlayer a1) {
  return (short)(a0->TextValue(a1));
}
void Decrement(tListIteratorTrack * a0, tPlayer a1) {
  a0->Decrement(a1);
}
void Increment(tListIteratorTrack * a0, tPlayer a1) {
  a0->Increment(a1);
}
void SetAvailableIcon(tVideoWall * a0, short a1, short a2, short a3, short a4, tTexture_ShapeInfo * a5) {
  a0->SetAvailableIcon(a1, a2, a3, a4, a5);
}
void SetAvailable(tVideoWall * a0, u_short a1) {
  a0->SetAvailable(a1);
}
void ProcessInput(tScreen * a0, tPlayer a1, tInputKeyType & a2, tMenuCommand & a3) {
  a0->ProcessInput(a1, a2, a3);
}
tCarInfo * GetCarFromSimID(tCarManager * a0, short a1) {
  return (tCarInfo *)(a0->GetCarFromSimID(a1));
}
