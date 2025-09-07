public function schemaAction(Request $request)
    {
        $api = $this->decideApiAndEndpoint($request->getUri());
        $this->registerProxySources($api['apiName']);
        $this->apiLoader->addOptions($api);

        $schema = $this->apiLoader->getEndpointSchema(urldecode($api['endpoint']));
        $schema = $this->transformationHandler->transformSchema(
            $api['apiName'],
            $api['endpoint'],
            $schema,
            clone $schema
        );
        $response = new Response(json_encode($schema), 200);
        $response->headers->set('Content-Type', 'application/json');

        return $this->templating->renderResponse(
            'GravitonCoreBundle:Main:index.json.twig',
            array ('response' => $response->getContent()),
            $response
        );
    }