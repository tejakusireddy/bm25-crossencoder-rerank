func (bot TgBot) SendAudioWithKeyboardHide(cid int, audio string, duration *int, performer *string, title *string, rmi *int, rm ReplyKeyboardHide) ResultWithMessage {
	var rkm ReplyMarkupInt = rm
	return bot.SendAudio(cid, audio, duration, performer, title, rmi, &rkm)
}