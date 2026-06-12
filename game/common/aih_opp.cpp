/* game/common/aih_opp.cpp -- RECONSTRUCTED (AI state-machine hierarchy; C++ TU)
 *   52 fns across 11 classes (AIState_Base + Normal/NonActive/Idle/Chase/Offroad/Purgatory/
 *   RovingTraffic/Donuts/GotoSlice/Cruise) + 3 free AIState_StartUp/Restart/CleanUp.
 *   Composition-modeled inheritance (_base_ members); manual _vf vtable dispatch (8-byte
 *   __vtbl_ptr_type entries); deleting dtors. Each ctor/dtor installs AIState_<C>_vtable.
 *   Faithful C++ (option A). NOT original source; SYM-faithful, recompilable. vs disasm-v2.
 */
#include <new>
#include "../../nfs4_types.h"
#include "aih_opp_externs.h"


/* ---- CheckForWipeOut__15AIHigh_Opponent  AIHigh_Opponent::CheckForWipeOut  [AIH_OPP.CPP:38-94] SLD-VERIFIED ---- */

void AIHigh_Opponent::CheckForWipeOut()



{
  int perTickProb;
  int randVal;
  int oppLevel;
  int oppFines;
  int hLoop;
  Car_tObj*thisPlayerObj;
  AIHigh_Player*thisPlayer;
  int playFines;

  bool bVar1;

  int iVar2;

  

  if ((Cars_gNumCopCars != 0) &&

     (((this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_)->wipeOutEndTick <=

      simGlobal.gameTicks)) {

    bVar1 = false;

    if (((this->_base_AIHigh_Player)._base_AIHigh_BasicPerp.basicPerpInfo_.crime_ == 0) ||

       ((this->_base_AIHigh_Player)._base_AIHigh_BasicPerp.basicPerpInfo_.copsAssigned_[0] +

        (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp.basicPerpInfo_.copsAssigned_[1] == 0)) {

      bVar1 = true;

    }

    if ((!bVar1) &&

       (0x27f < simGlobal.gameTicks -

                ((this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_)->wipeOutEndTick)) {

      randtemp = fastRandom * randSeed;

      fastRandom = randtemp & 0xffff;

      iVar2 = 0;

      if ((this->_base_AIHigh_Player).perpChaseInfo_.bestChaseLevelIndex_ !=

          ((this->_base_AIHigh_Player).perpChaseInfo_.copGameInfo_)->numLevels + -1) {

        for (; iVar2 < Cars_gNumHumanRaceCars; iVar2 = iVar2 + 1) {

        }

      }

    }

  }

  return;

}








/* ---- DoRearEnder__15AIHigh_Opponent  AIHigh_Opponent::DoRearEnder  [AIH_OPP.CPP:97-146] SLD-VERIFIED ---- */

int AIHigh_Opponent::DoRearEnder()



{
  int attackIndex;
  Car_tObj*otherCarObj;
  int longDistance;
  int latDistance;
  int racerLoop;

  int iVar1;

  int iVar2;

  u_int uVar3;

  Car_tObj *pCVar4;

  int iVar5;

  Car_tObj *pCVar6;

  Car_tObj **ppCVar7;

  

  iVar1 = AIScript_DoReAction(&((this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_)->script,0x100);

  if (iVar1 != -1) {

    pCVar6 = Cars_gList[iVar1];

    iVar2 = AIWorld_SplineDistance(pCVar6,(this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_);

    pCVar4 = (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_;

    iVar2 = iVar2 * pCVar4->direction;

    iVar5 = pCVar4->roadPosition - pCVar6->roadPosition;

    if (iVar5 < 0) {

      iVar5 = -iVar5;

    }

    if ((iVar2 - 0x10001U < 0x26ffff) && (iVar5 < iVar2 * 2)) {

      iVar2 = pCVar6->currentSpeed;

      if (iVar2 < 0) {

        iVar2 = -iVar2;

      }

      if (0xb1c71 < iVar2) {

        return iVar1;

      }

    }

  }

  pCVar4 = (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_;

  if ((pCVar4->N).simOptz == '\0') {

    iVar1 = pCVar4->currentSpeed;

    if (iVar1 < 0) {

      iVar1 = -iVar1;

    }

    iVar2 = 0;

    if (0x140000 < iVar1) {

      ppCVar7 = Cars_gHumanRaceCarList;

      for (; iVar2 < Cars_gNumHumanRaceCars; iVar2 = iVar2 + 1) {

        pCVar4 = *ppCVar7;

        iVar1 = (pCVar4->N).simRoadInfo.slice * 0x20 + BWorldSm_slices;

        if (((int)-((u_int)*(u_char *)(iVar1 + 0x1e) * 0x8000 * (u_int)(*(u_char *)(iVar1 + 0x1d) >> 4))

             <= pCVar4->roadPosition) &&

           (pCVar4->roadPosition <=

            (int)((u_int)*(u_char *)(iVar1 + 0x1f) * 0x8000 * (*(u_char *)(iVar1 + 0x1d) & 0xf)))) {

          iVar1 = AIWorld_SplineDistance(pCVar4,(this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_);

          pCVar6 = (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_;

          iVar1 = iVar1 * pCVar6->direction;

          iVar5 = pCVar6->roadPosition - pCVar4->roadPosition;

          if (iVar5 < 0) {

            iVar5 = -iVar5;

          }

          if ((((iVar1 - 0x10001U < 0x26ffff) && (iVar5 < iVar1 * 2)) &&

              (uVar3 = *(u_int *)(pCVar6->personality + 0x48),

              (simGlobal.gameTicks + pCVar6->carIndex * 0x7b & uVar3) == uVar3)) ||

             ((iVar1 + 0x3ffffU < 0x7ffff &&

              (pCVar6 = (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_,

              uVar3 = *(u_int *)(pCVar6->personality + 0x4c),

              (simGlobal.gameTicks + pCVar6->carIndex * 0x7b & uVar3) == uVar3)))) {

            return pCVar4->carIndex;

          }

        }

        ppCVar7 = ppCVar7 + 1;

      }

    }

  }

  return -1;

}








/* ---- HighExecute__15AIHigh_Opponent  AIHigh_Opponent::HighExecute  [AIH_OPP.CPP:150-247] SLD-VERIFIED ---- */

void AIHigh_Opponent::HighExecute()



{
  AIState_Base*newState;
  int attackIndex;
  coorddef pos;
  int aggression;
  AIState_Chase*attackState;

  AIState_Normal *pAVar1;

  AIState_Base *pAVar2;

  int aggressionLevel;

  AIHigh_tAttackMode AVar3;

  AIState_Base *pAVar4;

  int iVar5;

  int iVar6;

  AIState_Chase *pAVar7;

  coorddef cStack_28;

  

  switch((this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.stateType_) {

  case 0:

    pAVar1 = operator new(8);

    pAVar2 = &(new(pAVar1) AIState_Normal((this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_))->_base_AIState_Base;

    pAVar4 = (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.state_;

    if (pAVar4 != (AIState_Base *)0x0) {

      (*(int (*)(...))pAVar4->_vf[5])((int)&pAVar4->carObj_ + (int)*(short *)pAVar4->_vf[4],3);

    }

    (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.state_ = pAVar2;

    (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.stateType_ = 2;

    return;

  case 2:

    this->_base_AIHigh_Player.HandleCops();

    this->CheckForWipeOut();

    iVar5 = AIScript_DoReAction(&((this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_)->script,0x40);

    if (iVar5 == -1) {

      iVar5 = this->DoRearEnder();

      if (iVar5 != -1) {

        AVar3 = 1;

        goto LAB_800638c0;

      }

      iVar5 = this->DoProvokedAttack();

      AVar3 = 3;

      if (iVar5 != -1) goto LAB_800638c0;

    }

    else {

      AVar3 = 2;

LAB_800638c0:

      this->attackMode_ = AVar3;

    }

    if (this->attackMode_ != 0) {

      memset((u_char *)&cStack_28,'\0',0xc);

      iVar6 = this->attackMode_ - 1;

      aggressionLevel = 2;

      if (1 < iVar6) {

        aggressionLevel = iVar6;

      }

      pAVar7 = operator new(0x94);

      pAVar7 = (new(pAVar7) AIState_Chase((this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_,

                          Cars_gList[iVar5],&cStack_28,0x20,0x960000,0x960000,aggressionLevel,

                          0x10000));

      pAVar2 = (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.state_;

      if (pAVar2 != (AIState_Base *)0x0) {

        (*(int (*)(...))pAVar2->_vf[5])((int)&pAVar2->carObj_ + (int)*(short *)pAVar2->_vf[4],3);

      }

      (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.state_ = &pAVar7->_base_AIState_Base;

      (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.stateType_ = 4;

    }

    break;

  case 4:

    pAVar7 = (AIState_Chase *)(this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.state_;

    this->_base_AIHigh_Player.HandleCops();

    this->CheckForWipeOut();

    (pAVar7)->SetMurderMode(1,0xf);

    AVar3 = this->attackMode_;

    if (AVar3 == 2) {

      iVar5 = AIScript_DoReAction(&((this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_)->script,0x40)

      ;

      if (iVar5 == -1) {

        this->attackMode_ = 0;

      }

    }

    else if ((int)AVar3 < 3) {

      if ((AVar3 == 1) && (iVar5 = this->DoRearEnder(), iVar5 == -1)) {

        this->attackMode_ = 0;

      }

    }

    else if ((AVar3 == 3) &&

            (iVar5 = this->attackTicksLeft_, this->attackTicksLeft_ = iVar5, iVar5 < 1)) {

      this->attackMode_ = 0;

    }

    if (this->attackMode_ == 0) {

      iVar5 = -1;

      if (GameSetup_gData.reverseTrack == 0) {

        iVar5 = 1;

      }

      ((this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_)->desiredDirection = iVar5;

      pAVar1 = operator new(8);

      pAVar2 = &(new(pAVar1) AIState_Normal((this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_))->_base_AIState_Base;

      pAVar4 = (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.state_;

      if (pAVar4 != (AIState_Base *)0x0) {

        (*(int (*)(...))pAVar4->_vf[5])((int)&pAVar4->carObj_ + (int)*(short *)pAVar4->_vf[4],3);

      }

      (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.state_ = pAVar2;

      (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.stateType_ = 2;

      this->attackMode_ = 0;

    }

  }

  ((this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.state_)->StateExecute();

  return;

}








/* ---- __15AIHigh_OpponentP8Car_tObj  AIHigh_Opponent::ctor  [AIH_OPP.CPP:250-255] SLD-VERIFIED ---- */
AIHigh_Opponent::AIHigh_Opponent(Car_tObj *carObj)



{

  (new(&this->_base_AIHigh_Player) AIHigh_Player(carObj));

  (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base._vf =

       (__vtbl_ptr_type (*) [3])AIHigh_Opponent_vtable;

  this->attackMode_ = 0;

  this->lastHumanHitter_ = (Car_tObj *)0x0;

  this->hitCount_ = 0;

  this->attackTicksLeft_ = 0;

  return;

}








/* ---- DoProvokedAttack__15AIHigh_Opponent  AIHigh_Opponent::DoProvokedAttack  [AIH_OPP.CPP:260-280] SLD-VERIFIED ---- */

int AIHigh_Opponent::DoProvokedAttack()



{

  int iVar1;

  Car_tObj *pCVar2;

  Car_tObj *pCVar3;

  int iVar4;

  

  pCVar3 = (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_;

  if (((simGlobal.gameTicks - (pCVar3->N).collision.lastTime < 0xf) &&

      (pCVar3 = (Car_tObj *)(pCVar3->N).collision.lastOtherObj, pCVar3 != (Car_tObj *)0x0)) &&

     ((pCVar3->carFlags & 4U) != 0)) {

    if (this->lastHumanHitter_ != pCVar3) {

      this->lastHumanHitter_ = pCVar3;

      this->hitCount_ = 0;

    }

    pCVar2 = (this->_base_AIHigh_Player)._base_AIHigh_BasicPerp._base_AIHigh_Base.carObj_;

    iVar1 = this->hitCount_ + 1;

    this->hitCount_ = iVar1;

    iVar4 = pCVar2->personality;

    if (*(int *)(iVar4 + 0x24) < iVar1) {

      iVar1 = *(int *)(iVar4 + 0x28);

      this->hitCount_ = 0;

      this->attackTicksLeft_ = iVar1;

      return pCVar3->carIndex;

    }

  }

  return -1;

}







/* end of aih_opp.cpp */
