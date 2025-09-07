func (c *SpaceController) List(ctx *app.ListSpaceContext) error {
	_, err := login.ContextIdentity(ctx)
	if err != nil {
		return jsonapi.JSONErrorResponse(ctx, goa.ErrUnauthorized(err.Error()))
	}
	offset, limit := computePagingLimits(ctx.PageOffset, ctx.PageLimit)

	var response app.SpaceList
	txnErr := application.Transactional(c.db, func(appl application.Application) error {
		spaces, cnt, err := appl.Spaces().List(ctx.Context, &offset, &limit)
		if err != nil {
			return err
		}
		entityErr := ctx.ConditionalEntities(spaces, c.config.GetCacheControlSpaces, func() error {
			count := int(cnt)
			spaceData, err := ConvertSpacesFromModel(ctx.Request, spaces, IncludeBacklogTotalCount(ctx.Context, c.db))
			if err != nil {
				return err
			}
			response = app.SpaceList{
				Links: &app.PagingLinks{},
				Meta:  &app.SpaceListMeta{TotalCount: count},
				Data:  spaceData,
			}
			setPagingLinks(response.Links, buildAbsoluteURL(ctx.Request), len(spaces), offset, limit, count)
			return nil
		})
		if entityErr != nil {
			return entityErr
		}

		return nil
	})
	if txnErr != nil {
		return jsonapi.JSONErrorResponse(ctx, txnErr)
	}
	return ctx.OK(&response)
}