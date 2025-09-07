private void addPreflightOptionsRequestSupport(RestExpress server, CorsOptionsController corsOptionsController)
    {
	    RouteBuilder rb;

	    for (String pattern : methodsByPattern.keySet())
	    {
	    	rb = server.uri(pattern, corsOptionsController)
		    	.action("options", HttpMethod.OPTIONS)
		    	.noSerialization()
		    	// Disable both authentication and authorization which are usually use header such as X-Authorization.
		    	// When browser does CORS preflight with OPTIONS request, such headers are not included.
		    	.flag(Flags.Auth.PUBLIC_ROUTE)
		    	.flag(Flags.Auth.NO_AUTHORIZATION);

	    	for (String flag : flags)
	    	{
	    		rb.flag(flag);
	    	}

	    	for (Entry<String, Object> entry : parameters.entrySet())
	    	{
	    		rb.parameter(entry.getKey(), entry.getValue());
	    	}

	    	routeBuilders.add(rb);
	    }
    }