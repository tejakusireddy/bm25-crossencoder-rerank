func (s *Ec2Config) SetSecurityGroupArns(v []*string) *Ec2Config {
	s.SecurityGroupArns = v
	return s
}