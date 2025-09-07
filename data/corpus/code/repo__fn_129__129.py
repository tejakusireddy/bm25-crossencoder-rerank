private Observable<DocumentFragment<Lookup>> getCountIn(final String id, final LookupSpec spec,
        final long timeout, final TimeUnit timeUnit) {
        return Observable.defer(new Func0<Observable<DocumentFragment<Lookup>>>() {
            @Override
            public Observable<DocumentFragment<Lookup>> call() {
                final SubGetCountRequest request = new SubGetCountRequest(id, spec.path(), bucketName);
                request.xattr(spec.xattr());
                request.accessDeleted(accessDeleted);
                addRequestSpan(environment, request, "subdoc_count");
                return applyTimeout(deferAndWatch(new Func1<Subscriber, Observable<SimpleSubdocResponse>>() {
                    @Override
                    public Observable<SimpleSubdocResponse> call(Subscriber s) {
                        request.subscriber(s);
                        return core.send(request);
                    }
                }).map(new Func1<SimpleSubdocResponse, DocumentFragment<Lookup>>() {
                    @Override
                    public DocumentFragment<Lookup> call(SimpleSubdocResponse response) {
                        try {
                            if (response.status().isSuccess()) {
                                try {
                                    long count = subdocumentTranscoder.decode(response.content(), Long.class);
                                    SubdocOperationResult<Lookup> single = SubdocOperationResult
                                        .createResult(spec.path(), Lookup.GET_COUNT, response.status(), count);
                                    return new DocumentFragment<Lookup>(id, response.cas(), response.mutationToken(),
                                        Collections.singletonList(single));
                                } finally {
                                    if (response.content() != null) {
                                        response.content().release();
                                    }
                                }
                            } else {
                                if (response.content() != null && response.content().refCnt() > 0) {
                                    response.content().release();
                                }

                                if (response.status() == ResponseStatus.SUBDOC_PATH_NOT_FOUND) {
                                    SubdocOperationResult<Lookup> single = SubdocOperationResult
                                        .createResult(spec.path(), Lookup.GET_COUNT, response.status(), null);
                                    return new DocumentFragment<Lookup>(id, response.cas(), response.mutationToken(), Collections.singletonList(single));
                                } else {
                                    throw SubdocHelper.commonSubdocErrors(response.status(), id, spec.path());
                                }
                            }
                        } finally {
                            if (environment.operationTracingEnabled()) {
                                environment.tracer().scopeManager()
                                    .activate(response.request().span(), true)
                                    .close();
                            }
                        }
                    }
                }), request, environment, timeout, timeUnit);
            }
        });
    }