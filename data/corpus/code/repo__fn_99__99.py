func CreateNonce() ([]byte, error) {
	nonce, err := crypto.GetRandomNonce()
	return nonce, errors.WithMessage(err, "error generating random nonce")
}