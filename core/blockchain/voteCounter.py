from pyteal import *
import os



def approval_program():
    # program = Return(Int(1))
    # creation of model submission, waiting for votes
    handle_vote_creation = Seq(
        App.globalPut(Bytes("Vote"), Int(0)),
        Return(Int(1))
    )
    program = Cond(
        [Txn.application_id() == Int(0), handle_vote_creation],
        # [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        # [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        # [Txn.on_completion() == OnComplete.UpdateApplication, handle_updateapp],
        # [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp],
        # [Txn.on_completion() == OnComplete.NoOp, handle_noop]
		)

    return compileTeal(program, Mode.Application)

def clear_state_program():
    program = Return(Int(1))
    return compileTeal(program, Mode.Application)

print(approval_program());