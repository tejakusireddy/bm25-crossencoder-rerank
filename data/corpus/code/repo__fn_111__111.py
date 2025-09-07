func (in *GitBuildSource) DeepCopy() *GitBuildSource {
	if in == nil {
		return nil
	}
	out := new(GitBuildSource)
	in.DeepCopyInto(out)
	return out
}