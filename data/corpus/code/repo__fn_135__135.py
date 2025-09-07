func (cs *ConsensusState) createProposalBlock() (block *types.Block, blockParts *types.PartSet) {
	var commit *types.Commit
	if cs.Height == 1 {
		// We're creating a proposal for the first block.
		// The commit is empty, but not nil.
		commit = types.NewCommit(types.BlockID{}, nil)
	} else if cs.LastCommit.HasTwoThirdsMajority() {
		// Make the commit from LastCommit
		commit = cs.LastCommit.MakeCommit()
	} else {
		// This shouldn't happen.
		cs.Logger.Error("enterPropose: Cannot propose anything: No commit for the previous block.")
		return
	}

	proposerAddr := cs.privValidator.GetPubKey().Address()
	return cs.blockExec.CreateProposalBlock(cs.Height, cs.state, commit, proposerAddr)
}